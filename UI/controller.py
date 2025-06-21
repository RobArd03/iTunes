import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceDD = None

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        dMinTxt = self._view._txtInDurata.value
        if dMinTxt == "":
            self._view._txtInDurata.controls.append(ft.Text("Attenzione valore minimo di durata non inserito", color="red"))
            self._view.update_page()
            return
        try:
            dMin = int(dMinTxt)
        except ValueError:
            self._view.txtInDurata.controls.append(ft.Text("Attenzione il valore inserito non è un intero", color="red"))
            self._view.update_page()
            return
        self._model.buildGraph(dMin)
        n, e = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato corretamente. "
                                                       f"Il grafo è costituito di {n} nodi e di {e} archi"))
        self._fillDD(self._model.getAllNodes())
        self._view.update_page()

    def handleAnalisiComp(self, e):
        self._view.txt_result.controls.clear()
        if self._choiceDD is None:
            self._view.txt_result.controls.append(ft.Text("Attenzione album non selezionato", color="red"))
            self._view.update_page()
            return

        size, dTotcc = self._model.getInfoConnessa(self._choiceDD)
        self._view.txt_result.controls.append(ft.Text(f"La componente connessa che contiene {self._choiceDD} ha {size} nodi e una durata di {dTotcc} minuti"))
        self._view.update_page()


    def handleGetSetAlbum(self, e):
        self._view.txt_result.controls.clear()
        sogliaTxt = self._view._txtInSoglia.value
        if sogliaTxt == "":
            self._view.txt_result.controls.append(ft.Text("Soglia massima di durata non inserita", color="red"))
            self._view.update_page()
            return
        try: soglia = int(sogliaTxt)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text("Il valore di soglia inserito non è un intero", color="red"))
            self._view.update_page()
            return
        if self._choiceDD is None:
            self._view.txt_result.controls.append(ft.Text("Attenzione selezionare una voce dal dropdown", color="red"))
            self._view.update_page()
            return

        setOfNodes, sumDurate = self._model.getsetOfNodes(self._choiceDD, soglia)

        self._view.txt_result.controls.append(ft.Text(f"Ho trovato un set di album che soddisfa le specifiche, dimensione = {len(setOfNodes)}, durata totale = {sumDurate} min "))
        self._view.txt_result.controls.append(ft.Text(f"Di seguito gli album che fanno parte della soluzione trovata"))
        for n in setOfNodes:
            self._view.txt_result.controls.append(ft.Text(n))

        self._view.update_page()


    def _fillDD(self, listOfNodes):
        listOfNodes.sort(key = lambda x: x.Title)
        self._view._ddAlbum.options = map(lambda x: ft.dropdown.Option(text = x.Title, on_click=self._readDDValue, data = x ), listOfNodes)

    def _readDDValue(self, e):
        self._choiceDD = e.control.data
        if self._choiceDD is None:
            print("error in reading dd")
