import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

#metodo che cerca un percorso
    #gli passo un oggetto usando la funzione get Obj alla quale passo il valore della casella di testo
    # restituisce il percorso e il peso massimo che stampo
    def handleCercaPercorso(self,e):
        print (int(self._view._ddLun.value))
        print(self._view._txtIdOggetto)
        percorso, peso=  self._model.getPercorso(int(self._view._ddLun.value),self._model.getObj(int(self._view._txtIdOggetto.value)))
        #stampo
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"percorso trovato- Peso massimo: {peso}"))
        for p in percorso:
            self._view._txt_result.controls.append(ft.Text( p))
        self._view.update_page()


    #metodo che crea il grafo
    def handleAnalizzaOggetti(self, e):
        #lancio il metodo
        self._model.popolaGrafo()
        #scrivo un po' di messaggi e informazioni utili su cosa ho fatto
        self._view._txt_result.controls.append(ft.Text(f"Grafo creato"))
        self._view._txt_result.controls.append(ft.Text(f"{self._model.getNumNodes()} nodi"))
        self._view._txt_result.controls.append(ft.Text(f"{self._model.getNumEdges()} archi"))
        self._view.update_page()

    #metodo che riceve l'id di un nodo e se esiste stampa tutti i nodi collegati
    def handleCompConnessa(self,e):
        #catturo l'id oggetto
        id_nodo= self._view._txtIdOggetto.value

        #verifico se il valore inserito è convertibile in un intero e lo trasformo da stringa a intero
        try:
           id_nodo= int(id_nodo)
        except ValueError:
            #self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("il valore non è un intero"))
            self._view.update_page()
            return

        #verifico se il nodo è presente nel DB. Devo fare un metodo nel model che lo controlla
        if(self._model.checkExist(id_nodo)):
            self._view._txt_result.controls.append(ft.Text(f"l'oggetto con id {id_nodo} è presente"))
        else:
            self._view._txt_result.controls.append(ft.Text(f"l'oggetto con id {id_nodo} non è presente"))


        #aggiorno la pagina dopo tutti i controlli
        self._view.update_page()

        ################################################################################
        # SE IL NODO ESISTE CERCO LA COMPONENTE CONNESSA CHE CONTIENE IL NODO
        # E STAMPO IL NUMERO DI VERTICI CHE A COMPONGONO
        ################################################################################

        comp_connessa= self._model.getConnessa(id_nodo)
        self._view._txt_result.controls.append(ft.Text(f"la componente connessa con il nodo {id_nodo} sono {comp_connessa}"))
        self._view.update_page()


        #riempio il DD tutte le lunghezze possibili della componente connessa, ossia la soluzione (numeri da 2 a size componente connessa)
        for i in range(2,comp_connessa):
            self._view._ddLun.options.append(ft.dropdown.Option(i))

        self._view.update_page()



