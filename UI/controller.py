import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

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
            self._view._txtIdOggetto.value = ""
            self._view.update_page()
            return

        #verifico se il nodo è presente nel DB. Devo fare un metodo nel model che lo controlla
        if(self._model.checkExist(id_nodo)):
            self._view._txt_result.controls.append(ft.Text(f"l'oggetto con id {id_nodo} è presente"))
            self._view._txtIdOggetto.value=""

        else:
            self._view._txt_result.controls.append(ft.Text(f"l'oggetto con id {id_nodo} non è presente"))
            self._view._txtIdOggetto.value = ""


        #aggiorno la pagina dopo tutti i controlli
        self._view.update_page()

        ################################################################################
        # SE IL NODO ESISTE CERCO LA COMPONENTE CONNESSA CHE CONTIENE IL NODO
        # E STAMPO IL NUMERO DI VERTICI CHE A COMPONGONO
        ################################################################################

        n_comp_connesse= self._model.getConnessa(id_nodo)
        self._view._txt_result.controls.append(ft.Text(f"le componenti connesse con il nodo {id_nodo} sono {n_comp_connesse}"))
        self._view.update_page()
