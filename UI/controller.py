import flet as ft
from UI.view import View
from model.model import Model


class Controller:

    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        loc = self._view.dd_localization.value
        if loc is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("attenzione, per procedere devi selezionare una localization"))
            self._view.update_page()
            return
        self._model.buildGraph(loc)
        n, a = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"grafo creato con {n} nodi e {a} archi"))
        edges = self._model.getArchiPesoCres()
        for e in edges:
            self._view.txt_result.controls.append(ft.Text(f"{e[0]} <--> {e[1]}-peso: {e[2]["weight"]}"))

        self._view.update_page()

    def analyze_graph(self, e):
        componenti_connesse = self._model.get_connesse()
        self._view.txt_result.controls.append(ft.Text(f"\nLe componenti connesse sono:"))
        for connessa in componenti_connesse:
            if len(connessa) > 1:
                stringa = ""
                for nodo in connessa:
                    stringa += f"{nodo.GeneID}, "
                stringa += f" | dimensione componente = {len(connessa)}"
                self._view.txt_result.controls.append(ft.Text(stringa))
        self._view.update_page()

    def handle_path(self, e):
        pass

    def fillDDLocal(self):
        localizations = self._model.getLocalizations()
        for l in localizations:
            self._view.dd_localization.options.append(ft.dropdown.Option(l))
        self._view.update_page()

