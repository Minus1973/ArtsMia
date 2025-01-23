from database.DB_connect import DBConnect
from model.artObject import ArtObject
from model.connessione import Connessione


class DAO():

    ##METODI STATICI DELLA CLASSE DAO
    ## NON DEVO METTERE I SELF
    @staticmethod
    def getAllObjects():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * FROM objects"""
        cursor.execute(query)

        for row in cursor:
            result.append(ArtObject(**row))
        cursor.close()
        conn.close()
        return result

    #metodo per calcolare il peso degli archi. Gli passo due oggetti nodi e verifico quante volte compaiono nelle esibizioni
    @staticmethod
    def getPeso(v1:ArtObject,v2:ArtObject):  #sono due oggetti
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select  count(*) as peso 
                    from  exhibition_objects eo1, exhibition_objects eo2 
                    where eo1.exhibition_id =eo2.exhibition_id      
                    and eo1.object_id < eo2.object_id   
                    and eo1.object_id = %s
                    and eo2.object_id = %s"""
        cursor.execute(query,(v1.object_id,v2.object_id))  #essendo oggetti devo prendere gli id da mettere nella query

        for row in cursor:
            result.append(row)  #ho un solo valore
        cursor.close()
        conn.close()
        return result




    #devo creare gli archi (che chiamo sempre Connessioni) e mi serve inventare un modo per crearli e mandarli
    # al model per elaborarli e inserrli nel grafo
    @staticmethod
    def getAllConnessioni(_artefattiMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        # prendo solo le coppie con stessa exhibition_id
        # prendo solo le coppie che hanno due object_id diverso e con il > tolgo anche le coppie con elementi scambiati
        # facendo il group by con le due colonne avrò la coppia non ripetuta con di fianco il conteggio delle ripetizioni
        query = """select  eo1.object_id as o1,eo2.object_id as o2, count(*) as peso 
                    from  exhibition_objects eo1, exhibition_objects eo2 
                    where eo1.exhibition_id =eo2.exhibition_id      
                    and eo1.object_id < eo2.object_id               
                    group by eo1.object_id, eo2.object_id           
                    order by peso desc"""
        cursor.execute(query)

        for row in cursor:
            result.append(Connessione(_artefattiMap[row["o1"]],  #oggetto nodo1
                                      _artefattiMap[row["o2"]],  #oggetto nodo2
                                      row["peso"]))
        cursor.close()
        conn.close()
        return result
