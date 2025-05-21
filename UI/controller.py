import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._choiceDDAeroportoP = None
        self._choiceDDAeroportoD = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleAnalizza(self, e): #analizza aeroporti
        #crea un grafo che rappresenta gli aeroporti su cui operano almeno x compagnie
        #grafo semplice, non orientato e pesato
        #nodi= aeroporti con almeno x compagnie
        #archi = rotte tra gli aeroporti collegati da almeno un volo
        #peso = numero totale voli tra i due aeroporti
        #considerare sia i voli di andata che di ritorno
        cMinTxt = self._view._txtInCMin.value
        if cMinTxt == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text('Inserire un valore numerico.', color='red'))
            return
        try:
            cMin = int(cMinTxt)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text('Il valore inserito non è un intero.', color='red'))
            return

        if cMin<=0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text('Il valore inserito non è >= 0.', color='red'))
            return

        self._model.buildGraph(cMin)
        allNodes = self._model.getAllNodes()
        self._fillDD(allNodes)
        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text('Grafo correttamente creato'))
        self._view.txt_result.controls.append(ft.Text(f'Numero nodi: {nNodes}'))
        self._view.txt_result.controls.append(ft.Text(f'Numero archi: {nEdges}'))

        self._view.update_page()

    def _fillDD(self, allNodes):
        for n in allNodes:
         self._view._ddAeroportoP.options.append(ft.dropdown.Option(data=n, key=n.IATA_CODE, on_click=self.pickDDPartenza))
         self._view._ddAeroportoD.options.append(
             ft.dropdown.Option(data=n, key=n.IATA_CODE, on_click=self.pickDDDestinazione))

    def pickDDPartenza(self,e): #questo metodo legge dal dropdown ciò che l'utente sceglie e lo salva nella variabile
        self._choiceDDAeroportoP = e.control.data

    def pickDDDestinazione(self,e): #questo metodo legge dal dropdown ciò che l'utente sceglie e lo salva nella variabile
        self._choiceDDAeroportoD = e.control.data

    def handleConnessi(self,e):
        if self._choiceDDAeroportoP==None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text('Attenzione selezionare una voce dal menu'))

        viciniTuple = self._model.getSortedNeighbors(self._choiceDDAeroportoP)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text('Di seguito i vicini del aeroporto di partenza:' ))
        for v in viciniTuple:
            self._view.txt_result.controls.append(ft.Text(f'{v[0]} - peso: {v[1]}'))
        self._view.update_page()

    def handlePercorso(self,e):
        if self._choiceDDAeroportoP == None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text('Attenzione selezionare una voce dal menu Aeroporto Partenza'))
        if self._choiceDDAeroportoD==None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text('Attenzione selezionare una voce dal menu Aeroporto Destinazione'))

        path = self._model.getPath(self._choiceDDAeroportoP, self._choiceDDAeroportoD)
        if len(path) == 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text('Cammino non trovato'))
        else:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text('Cammino trovato, di seguito i nodi: '))
            for p in path:
                self._view.txt_result.controls.append(
                    ft.Text(p))
        self._view.update_page()

    def handleCerca(self,e):
        v0= self._choiceDDAeroportoP
        v1= self._choiceDDAeroportoD
        t=self._view._txtInTratteMax.value
        if t is None or t=='':
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text('ATTENZIONE inserire un valore valido di tratte massime'))
            return
        try:
            intT = int(t)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text('ATTENZIONE inserire un valore valido di tratte massime'))
            return
        bestPath, peso = self._model.getCamminoOttimo(v0, v1, intT)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f'Il percorso ottimo tra {v0} e {v1} è: '))
        for i in bestPath:
            self._view.txt_result.controls.append(ft.Text(i))
        self._view.txt_result.controls.append(ft.Text(f'Numero voli:{peso} '))
        self._view.update_page()





