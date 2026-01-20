import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_create_graph(self, e):
        try:
            n_alb= int(self._view.txtNumAlbumMin.value)
            if n_alb > 0:
                self._model.BuildGraf(n_alb)
                self._view.ddArtist.disabled = False
                self._view.btnArtistsConnected.disabled = False
                self.populate_dd()
                self._view.txt_result.controls.clear()
                self._view.txt_result.controls.append(ft.Text(f'Grafo creato: {self._model.num_nodi()} nodi (artisti), {self._model.num_archi()} archi'))


                self._view.update_page()



            else :
                self._view.show_alert('Il numero inserito deve essere maggiore di 0')

        except ValueError:
            self._view.show_alert('Inserisci un numero intero minimo di album')

    def populate_dd(self):

        for artista in self._model._lista_nodi:
            self._view.ddArtist.options.append(
                ft.DropdownOption(key=artista.id, text=artista.name))

        self._view.update_page()

    def handle_connected_artists(self, e):

        artista_id = self._view.ddArtist.value
        if artista_id is not None :
            lista_artisti, start = self._model.get_artisti_vicini(artista_id)
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f'Artisti direttamente collegati all artista: {artista_id}, {start.name}'))
            for art in lista_artisti:
                peso= self._model._graph[start][art]['weight']
                self._view.txt_result.controls.append(ft.Text(f'{art.id}, {art.name} - Numero generi in comune: {peso}'))

            self._view.txtMaxArtists.disabled = False
            self._view.txtMinDuration.disabled = False
            self._view.btnSearchArtists.disabled = False
            self._view.update_page()
        else:
            self._view.show_alert('Selezionare un artista')


    def handle_search_artists(self, e):
        try :
            d_min= float(self._view.txtMinDuration.value)
            n_art = int(self._view.txtMaxArtists.value)
            if d_min > 0 and n_art >1 and n_art < len(self._model._lista_nodi):
                artista_id = self._view.ddArtist.value
                path, best_weight, start= self._model.cerca_percorso(artista_id, d_min,n_art)
                self._view.txt_result.controls.clear()
                self._view.txt_result.controls.append(
                    ft.Text(f'Cammino di peso massimo dell artista: {artista_id}, {start.name}'))
                self._view.txt_result.controls.append(
                    ft.Text(f'Lunghezza {len(path)}'))
                for nodo in path:
                    self._view.txt_result.controls.append(
                        ft.Text(f'{nodo.id}, {nodo.name}'))
                self._view.txt_result.controls.append(
                    ft.Text(f'Peso massimo: {best_weight}'))
                self._view.update_page()


            else:
                self._view.show_alert(f'Inserire nella prima casella un numero decimale maggiore di zero e nella seconda un numero intero > 1 e < di {len(self._model._lista_nodi)}')
        except ValueError:
            self._view.show_alert('Inserire nella prima casella un numero decimale e nella seconda un numero intero')

