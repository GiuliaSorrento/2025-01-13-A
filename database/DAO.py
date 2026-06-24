from database.DB_connect import DBConnect
from model.classification import Classification
from model.gene import Gene
from model.interaction import Interaction


class DAO():

    @staticmethod
    def get_all_genes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                        FROM genes"""
            cursor.execute(query)

            for row in cursor:
                result.append(Gene(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_interactions():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                           FROM interactions"""
            cursor.execute(query)

            for row in cursor:
                result.append(Interaction(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_classifications():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                        FROM classification"""
            cursor.execute(query)

            for row in cursor:
                result.append(Classification(**row))

            cursor.close()
            cnx.close()
        return result



    @staticmethod
    def getAllLocalizations():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct c.Localization as loc
                    from classification c 
                    order by c.Localization desc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["loc"])

            cursor.close()
            cnx.close()
        return result



    @staticmethod
    def getAllNodes(loc):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query =  """select c.*
                        from classification c 
                        where c.Localization = %s"""
            cursor.execute(query, (loc,))

            for row in cursor:
                result.append(Classification(**row))

            cursor.close()
            cnx.close()
        return result



    @staticmethod
    def getMapGeneCromo(loc, idMapC):
        cnx = DBConnect.get_connection()

        mapGene_cromosoma = {}
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query =  """select distinct c.GeneID as geneId, g.Chromosome as cromosomaAssoc
                        from genes g,  classification c
                        where g.GeneID = c.GeneID 
                        and c.Localization = %s
                        group by c.GeneID , g.Chromosome """
            cursor.execute(query, (loc,))


            for row in cursor:
                mapGene_cromosoma[idMapC[row["geneId"]]] = row["cromosomaAssoc"]  #restituisce una mappa in cui la chiave è il nodo e il valore è il cromosoma associato


            cursor.close()
            cnx.close()
        return mapGene_cromosoma