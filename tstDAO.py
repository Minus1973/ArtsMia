from database.DAO import DAO
from model.model import Model

#testo il metodo che restituisce gli oggetti da inserire nel grafo
#res = DAO.getAllObjects()
#print(len(res))


#testo il metodo che restituisce gli archi (Connessioni) da inserire nel grafo
model=Model()
#conn =DAO.getAllConnessioni(model._artefattiMap)
#print(len(conn))

#testo il metodo che restituisce il peso
peso= DAO.getPeso(model._artefattiMap[46],model._artefattiMap[267])
print (peso)







