from database.DB_connect import DBConnect
from model.airport import Airport
from model.arco import Arco


class DAO():

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * from airports a order by a.AIRPORT asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(nMin, idMapAirports):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        #devo fare una query annidata
        query = """select t.ID, t.IATA_CODE, count(*) as N
                from (select a.ID, a.IATA_CODE, f.AIRLINE_ID, count(*)
                from airports a, flights f 
                where a.ID = f.ORIGIN_AIRPORT_ID or a.ID =f.DESTINATION_AIRPORT_ID 
                group by a.ID , a.IATA_CODE, f.AIRLINE_ID ) as t
                group by t.ID, t.IATA_CODE
                having N>=%s"""

        cursor.execute(query,(nMin,))

        for row in cursor:
            result.append(idMapAirports[row['ID']])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesV1(idMapAirports):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        # devo fare una query annidata
        query = """select f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, count(*) as N
                    from flights f
                    group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID
                    order by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID"""

        cursor.execute(query)

        for row in cursor:
            result.append(Arco(idMapAirports[row['ORIGIN_AIRPORT_ID']],idMapAirports[row['DESTINATION_AIRPORT_ID']],row['N']))

        cursor.close()
        conn.close()
        return result