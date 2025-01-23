import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        # poiche gli oggetti non cambiano nel corso del tempo faccio che mettere nel costruttore
        # della classe Model a lista con gli artefatti
        self._artObjectList = DAO.getAllObjects()
        # costruisco il grafo vuoto  secondo le indicazioni (semplice pesato) importando networkx
        self._grafo = nx.Graph()
        #creo il dizionario degli artefatti partendo dalla lista degli oggetti che collega l'id artefatto all'oggetto
        self._artefattiMap={}
        for v in self._artObjectList:
            self._artefattiMap[v.object_id] = v


    #metodo che popola il grafo
    def popolaGrafo(self):
        # definisco cosa sono i nodi per me. Sono gli artefatti. Li prendo dalla lista degli artefatti
        self._grafo.add_nodes_from(self._artObjectList)

        # Aggiungo gli archi con un metodo che devo inventarmi.
        # ATTENZIONE non è il metodo add_edges() della libreria networkx
        self.addEdges()

    def addEdges(self):
        #per creare gli archi ho due metodi:

        # Soluzione 1. ciclare su tutti i nodi con due cicli for.
        # ogni coppia possibile la passo ad un metodo che creo.
        # questo metodo restituisce l'arco con il peso (se trova l'arco)
        # Sconsigliato se ci sono molti nodi perchè le combinazioni sono n^2. Impiega decine di minuti.
        # Lancia migliaia di volte il metodo getPeso(u,v)
        # for u in self._artObjectList:
        #     for v in self._artObjectList:
        #         peso = DAO.getPeso(u,v)
        #         self._grafo.add_edge(u,v,weight=peso)


        # Soluzione 2: trovare gli archi facendo una sola query
        # L'elaborazione è più veloce
        # richiama il metodo del DAO getAllConnessioni() passandogli la mappa degli artefatti
        # che restituisce gli archi con il loro peso
        allEdges = DAO.getAllConnessioni(self._artefattiMap)
        # ciclo su tutti gli archi trovati e li metto nel grafo
        for e in allEdges:
            self._grafo.add_edge(e.v1,e.v2,weight = e.peso)




    #metodi utili da usare nel controller per sapere quanti nodi e archi ci sono nel grafo
    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)


    #controlla che il nodo esista. Restituisce True o False
    def checkExist(self,id_nodo):
        return id_nodo in self._artefattiMap


    #restituisce in un dizionario, i nodi della componente connessa al nodo sorgente
    def getConnessa(self,v0:int):
        #ho dovuto indicare il v0 come un intero perche la form mi manda un intero.
        #per usarlo nel metodo dfs_successors devo avere il nodo
        v0=self._artefattiMap[v0]

        #MODO 1: dizionario di successori di v0 in DFS. Attenzione ad usare extend e non append
        successors = nx.dfs_successors(self._grafo, v0)
        lista_tmp= []
        for v in successors.values():
            lista_tmp.extend(v)
        print (f"metodo 1 (succ): {len(lista_tmp)}")

        #MODO 2: dizionario di predecessori in v0 DFS
        #se il grafo non è orientato l'algoritmo va al contrario e ottengo lo stesso risultato
        predecessors = nx.dfs_predecessors(self._grafo, v0)
        print(f"metodo 2 (pred): {len(predecessors.values())}")

        #MODO 3: prendo l'albero di visita e ne conto i nodi
        tree= nx.dfs_tree(self._grafo,v0)
        print(f"Metodo 3 (tree): {len(tree.nodes)}")

        #MODO 4: uso il metodo della libreria
        set_tmp= nx.node_connected_component(self._grafo, v0)
        print (f"Metodo 4 (libreria nx): {len(set_tmp)}")

        return len(set_tmp)







