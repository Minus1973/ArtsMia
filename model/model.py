import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        # poiche gli oggetti non cambiano nel corso del tempo faccio che mettere nel costruttore
        # della classe Model a lista con gli artefatti
        self._artObjectList = DAO.getAllObjects()
        # costruisco il grafo vuoto  secondo le indicazioni (semplice pesato) importando networkx
        self._grafo = nx.Graph()
        #per il punto 2 inizializzo i parametri della ricorsione: percorso vuoto, costo 0
        self._soluzioneMigliore = []
        self._pesoMassimo = 0

        #creo il dizionario degli artefatti partendo dalla lista degli oggetti che collega l'id artefatto all'oggetto
        self._artefattiMap={}

        for v in self._artObjectList:
            self._artefattiMap[v.object_id] = v




    #restituisce l'oggetto passandogli l'ID usando la mappa
    # E' il metodo da fare insieme alla mappa cosi accedo all'oggetto con l'ID
    def getObj(self,id_nodo):
        return  self._artefattiMap[id_nodo]


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

    #costruisco la ricorsione
    def getPercorso(self, lunghezza,v0):
        print(f"lunghezza cammino: {lunghezza}")
        print (f"Source: {v0}")

        #resetto i valori della ricorsione
        self._soluzioneMigliore = []
        self._pesoMassimo = 0

        #creo la lista vuota della soluzione parziale
        parziale=[]
        #parto dal nodo source quindi posso già aggiungerlo
        parziale.append(v0)
        #il punto di partenza è il source e tutti i suoi vicini. Farò un ciclo for per ognuno di essi.
        # da questi cammini troverò tutti quelli di lunghezza len
        # scarterò sempre quello meno costoso rispetto a  quello che metterò in soluzioneMigliore
        for v in self._grafo.neighbors(v0):
            #controllo che i nodi siano dello stesso tipo di V0
            if v.classification == v0.classification:
                #aggiungo il primo vicino e sono certo di lanciare la ricorsione dopo un arco
                parziale.append(v)
                self.ricorsione(parziale,lunghezza)
                #tornando verso l'elemento source devo rimuovere gli elementi della lista parziale di quel ramo
                # perchè devo entrare negli altri rami
                parziale.pop()
        #ritorno la soluzione migliore e il peso massimo
        return self._soluzioneMigliore, self._pesoMassimo


    def ricorsione(self,parziale, lunghezza):
        #appena lancio la ricorsione controllo che la lista vada bene
        #se la lunghezza è uguale a quella richiesta controllo che la soluzione sia migliore di quella che ho salvato prima
        ## CASO FINALE
        if len(parziale) ==lunghezza:
            #se la soluzione e migliore, la sostituisco con quella precedente
            #faccio una copia di parziale e la sostituisco perchè altrimenti avrei il riferimento ma quando
            #torno verso il source la lista parziale si svuta
            if self.peso(parziale)>self._pesoMassimo:
                self._pesoMassimo=self.peso(parziale)
                self._soluzioneMigliore= copy.deepcopy(parziale)
            #poichè avevo raggiunto la lunghezza di una soluzione devo uscire dalla ricorsione per tornare su nell'albero
            return

        # se arrivo qui è perchè la lunghezza non è ancora stata raggiunta: len(parziale)<lunghezza  quindi devo aggiungere nodi
        #considero i vicini dell'ultimo nodo della lista parziale, ossia parziale[-1] e ciclo per prenderli tutti
        ##CASO RICORSIVO
        for v in self._grafo.neighbors(parziale[-1]):
            #v lo aggiungo se non è gia in parziale e se ha stessa classification di V[-1] che è uguale a v0
            # e poi faccio un'altra ricorsione
            if v.classification == parziale[-1].classification and v not in parziale:
                parziale.append(v)
                self.ricorsione(parziale,lunghezza)
                parziale.pop()


    #sono certo che gli oggetti nella lista hanno tutti un arco
    def peso(self,listaObj):
        #inizializzo il peso =0
        peso_tmp = 0
        #ciclo sugli archi . ATTENZIONE AL LEN(-1)
        for i in range(0,len(listaObj)-1):
            #prendo l'arco tra l'oggetto i e l'oggetto i+1.
            peso_tmp +=self._grafo[listaObj[i]][listaObj[i+1]]["weight"]
        return peso_tmp














