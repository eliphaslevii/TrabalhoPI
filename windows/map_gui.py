import os
import sys
import webbrowser
from urllib.parse import quote_plus
import googlemaps
import polyline
import folium
import numpy as np
from sklearn.cluster import KMeans
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QApplication, QListWidget, QListWidgetItem,
    QMessageBox, QPushButton
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from database import create_connection
from PyQt5.QtCore import QUrl, Qt, QSize

# Sua chave da Google Maps Directions API
GOOGLE_API_KEY = 'AIzaSyAXPQPmxkGD7X-KL5xGEgaSIfiKNdGrMmg'

class VehicleHeaderWidget(QWidget):
    """Widget personalizado para o cabeçalho do veículo na lista."""
    def __init__(self, vehicle_info, route_points, parent=None):
        super().__init__(parent)
        self.route_points = route_points
        self.vehicle_info = vehicle_info

        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(4)
        
        # Mostrar informações reais do veículo
        placa = vehicle_info.get('placa', 'N/A')
        modelo = vehicle_info.get('modelo', 'N/A')
        motorista = vehicle_info.get('motorista_nome', 'N/A')
        
        label = QLabel(f"--- {placa} - {modelo} ---")
        label.setStyleSheet("font-weight: bold;")
        
        motorista_label = QLabel(f"Motorista: {motorista}")
        motorista_label.setStyleSheet("font-size: 10px; color: #666;")
        
        self.gmaps_button = QPushButton("Gerar Link para este Veículo")
        self.gmaps_button.clicked.connect(self.abrir_no_google_maps)

        layout.addWidget(label)
        layout.addWidget(motorista_label)
        layout.addWidget(self.gmaps_button)
        self.setLayout(layout)

    def abrir_no_google_maps(self):
        """Gera e abre um link do Google Maps com a rota específica."""
        if not self.route_points or len(self.route_points) < 2:
            return

        base_url = "https://www.google.com/maps/dir/?api=1"
        origem_str = quote_plus(self.route_points[0]['descricao'])
        destino_str = quote_plus(self.route_points[-1]['descricao'])
        
        waypoints = self.route_points[1:-1]
        waypoints_str = "|".join([quote_plus(p['descricao']) for p in waypoints]) if waypoints else ""
        
        url = f"{base_url}&origin={origem_str}&destination={destino_str}&waypoints={waypoints_str}&travelmode=driving"
        webbrowser.open(url)


class MapaRota(QWidget):
    def __init__(self, rota_id):
        super().__init__()
        self.rota_id = rota_id
        self.setWindowTitle("Mapa da Rota")
        self.setGeometry(100, 100, 1100, 600)

        layout_principal = QHBoxLayout()
        self.setLayout(layout_principal)

        self.view = QWebEngineView()
        layout_principal.addWidget(self.view, 3)

        self.painel_info = QWidget()
        self.painel_info_layout = QVBoxLayout()
        self.painel_info.setLayout(self.painel_info_layout)
        layout_principal.addWidget(self.painel_info, 1)

        self.label_entregador = QLabel("Entregador: -")
        self.label_tempo = QLabel("Tempo estimado: -")
        self.label_distancia = QLabel("Distância total: -")
        self.label_ordem = QLabel("Ordem de Entrega:")

        self.painel_info_layout.addWidget(self.label_entregador)
        self.painel_info_layout.addWidget(self.label_tempo)
        self.painel_info_layout.addWidget(self.label_distancia)
        self.painel_info_layout.addWidget(self.label_ordem)

        self.lista_ordem = QListWidget()
        self.lista_ordem.setDragDropMode(QListWidget.InternalMove)
        self.lista_ordem.model().rowsMoved.connect(self.recalcular_rota_manual)
        self.painel_info_layout.addWidget(self.lista_ordem)

        self.gmaps = googlemaps.Client(key=GOOGLE_API_KEY)

        self.origem = {'descricao': 'Universidade Tuiuti do Paraná - R. Padre Ladislau Kula, 395 - Santo Inácio, Curitiba - PR', 'latitude': -25.42504235372448, 'longitude': -49.321218430468946}
        self.destino = self.origem
        
        # Cores para ida (mais claras) e volta (mais escuras)
        self.cores_ida = ['lightblue', 'lightgreen', 'lightcoral', 'lightpink', 'lightyellow', 'lightgray', 'lightcyan', 'lightsteelblue', 'lightseagreen', 'lightsalmon']
        self.cores_volta = ['darkblue', 'darkgreen', 'darkred', 'darkmagenta', 'darkorange', 'darkgray', 'darkcyan', 'darkviolet', 'darkolivegreen', 'darkslategray']

        self.rota_info = self.obter_info_rota()
        self.veiculos_rota = self.obter_veiculos_rota()
        self.waypoints = self.obter_enderecos()

        self.gerar_rotas_para_veiculos()

    def obter_info_rota(self):
        """Obtém informações básicas da rota."""
        conn = create_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT nome, status FROM rotas WHERE id = %s", (self.rota_id,))
                return cursor.fetchone() or {'nome': 'Rota', 'status': 'pendente'}
        except Exception as e:
            print(f"Erro ao obter info da rota: {e}")
            return {'nome': 'Rota', 'status': 'pendente'}
        finally:
            if conn: conn.close()

    def obter_veiculos_rota(self):
        """Obtém os veículos associados a esta rota com informações completas."""
        conn = create_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                    SELECT v.id, v.placa, v.modelo, u.nome as motorista_nome
                    FROM rota_veiculos rv
                    JOIN veiculos v ON rv.veiculo_id = v.id
                    LEFT JOIN users u ON v.entregador_id = u.id
                    WHERE rv.rota_id = %s
                    ORDER BY v.placa
                """
                cursor.execute(sql, (self.rota_id,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao obter veículos da rota: {e}")
            return []
        finally:
            if conn: conn.close()

    def gerar_rotas_para_veiculos(self):
        num_veiculos = len(self.veiculos_rota)

        if num_veiculos > 1 and len(self.waypoints) >= num_veiculos:
            self.lista_ordem.setDragDropMode(QListWidget.NoDragDrop)
            if self.lista_ordem.model():
                try:
                    self.lista_ordem.model().rowsMoved.disconnect(self.recalcular_rota_manual)
                except TypeError:
                    pass
            self.gerar_rotas_clusterizadas(num_veiculos)
        else:
            self.lista_ordem.setDragDropMode(QListWidget.InternalMove)
            try:
                self.lista_ordem.model().rowsMoved.disconnect(self.recalcular_rota_manual)
            except TypeError:
                pass
            self.lista_ordem.model().rowsMoved.connect(self.recalcular_rota_manual)
            self.gerar_rota_unica_otimizada()

    def gerar_rota_unica_otimizada(self):
        if not self.waypoints: return
        self.gerar_rota_para_pontos([self.waypoints], optimize=True)

    def gerar_rotas_clusterizadas(self, num_veiculos):
        coordenadas = np.array([[p['latitude'], p['longitude']] for p in self.waypoints])
        kmeans = KMeans(n_clusters=num_veiculos, random_state=0, n_init=10).fit(coordenadas)

        clusters = [[] for _ in range(num_veiculos)]
        for i, ponto in enumerate(self.waypoints):
            clusters[kmeans.labels_[i]].append(ponto)
        
        clusters = [c for c in clusters if c]

        # Salvar atribuições de veículos no banco de dados
        self.salvar_atribuicoes_veiculos(clusters)

        self.gerar_rota_para_pontos(clusters, optimize=True)

    def salvar_atribuicoes_veiculos(self, clusters):
        """Salva no banco de dados qual endereço foi atribuído a qual veículo."""
        conn = create_connection()
        try:
            with conn.cursor() as cursor:
                # Limpar atribuições anteriores
                cursor.execute("UPDATE entregas SET veiculo_id = NULL WHERE rota_id = %s", (self.rota_id,))
                
                # Atribuir novos veículos
                for i, cluster in enumerate(clusters):
                    if i < len(self.veiculos_rota):
                        veiculo_id = self.veiculos_rota[i]['id']
                        for ponto in cluster:
                            cursor.execute(
                                "UPDATE entregas SET veiculo_id = %s WHERE id = %s",
                                (veiculo_id, ponto['id'])
                            )
            
            conn.commit()
        except Exception as e:
            print(f"Erro ao salvar atribuições de veículos: {e}")
            if conn: conn.rollback()
        finally:
            if conn: conn.close()

    def recalcular_rota_manual(self):
        nova_ordem_waypoints = [self.lista_ordem.item(i).data(Qt.UserRole) for i in range(self.lista_ordem.count())]
        self.gerar_rota_para_pontos([nova_ordem_waypoints], optimize=False)

    def gerar_rota_para_pontos(self, waypoints_por_veiculo, optimize=True):
        mapa = folium.Map(location=[self.origem['latitude'], self.origem['longitude']], zoom_start=12)
        self.lista_ordem.clear()
        tempo_total_frota = 0
        distancia_total_frota = 0

        folium.Marker(location=[self.origem['latitude'], self.origem['longitude']], popup="Origem/Destino",
                      icon=folium.Icon(color='red', icon='flag')).add_to(mapa)

        for i, waypoints in enumerate(waypoints_por_veiculo):
            if not waypoints: continue
            
            origem_str = f"{self.origem['latitude']},{self.origem['longitude']}"
            destino_str = f"{self.destino['latitude']},{self.destino['longitude']}"
            waypoints_str = [f"{p['latitude']},{p['longitude']}" for p in waypoints]

            try:
                directions_result = self.gmaps.directions(
                        origin=origem_str, destination=destino_str,
                        waypoints=waypoints_str, optimize_waypoints=optimize, mode="driving"
                )
            except Exception as e:
                    veiculo_info = self.veiculos_rota[i] if i < len(self.veiculos_rota) else {'placa': f'Veículo {i+1}'}
                    QMessageBox.warning(self, "Erro de API", f"{veiculo_info['placa']}: Erro na API do Google - {e}")
                    continue

            if not directions_result:
                    veiculo_info = self.veiculos_rota[i] if i < len(self.veiculos_rota) else {'placa': f'Veículo {i+1}'}
                    QMessageBox.warning(self, "Sem resultado", f"{veiculo_info['placa']}: Nenhum resultado retornado.")
                    continue

            route = directions_result[0]
            tempo_total_frota += sum(leg['duration']['value'] for leg in route['legs'])
            distancia_total_frota += sum(leg['distance']['value'] for leg in route['legs'])

            ordem_indices = route.get('waypoint_order', list(range(len(waypoints))))
            pontos_ordenados = [waypoints[j] for j in ordem_indices]
            
            pontos_para_gmaps = [self.origem] + pontos_ordenados + [self.destino]

            # Adiciona header personalizado na lista da UI com informações reais do veículo
            veiculo_info = self.veiculos_rota[i] if i < len(self.veiculos_rota) else {'placa': f'Veículo {i+1}', 'modelo': 'N/A', 'motorista_nome': 'N/A'}
            header_widget = VehicleHeaderWidget(veiculo_info, pontos_para_gmaps)
            header_item = QListWidgetItem(self.lista_ordem)
            header_item.setSizeHint(header_widget.sizeHint())
            header_item.setFlags(header_item.flags() & ~Qt.ItemIsSelectable)
            self.lista_ordem.addItem(header_item)
            self.lista_ordem.setItemWidget(header_item, header_widget)

            cor_ida = self.cores_ida[i % len(self.cores_ida)]
            cor_volta = self.cores_volta[i % len(self.cores_volta)]

            for j, ponto in enumerate(pontos_ordenados):
                item_texto = f"{j + 1}. {ponto['descricao']}"
                list_item = QListWidgetItem(item_texto)
                list_item.setData(Qt.UserRole, ponto)
                self.lista_ordem.addItem(list_item)
                
                popup_text = f"{veiculo_info['placa']} - Parada {j + 1}"
                folium.Marker(
                    location=[ponto['latitude'], ponto['longitude']],
                        popup=popup_text,
                        icon=folium.Icon(color=cor_ida, icon='info-sign')
                ).add_to(mapa)

            # Desenhar rotas com cores diferentes para ida e volta
            for leg_index, leg in enumerate(route['legs']):
                leg_points = []
                for step in leg['steps']:
                    leg_points.extend(polyline.decode(step['polyline']['points']))
                
                # Usar cor clara para ida (primeira perna) e escura para volta (última perna)
                if leg_index == 0:  # Primeira perna - ida
                    cor_rota = cor_ida
                else:  # Última perna - volta
                    cor_rota = cor_volta
                
                folium.PolyLine(locations=leg_points, color=cor_rota, weight=5).add_to(mapa)

        self.label_tempo.setText(f"Tempo total: {tempo_total_frota // 3600}h {(tempo_total_frota % 3600) // 60}min")
        self.label_distancia.setText(f"Distância total: {distancia_total_frota / 1000:.2f} km")

        mapa.save("mapa_rota.html")
        self.view.setUrl(QUrl.fromLocalFile(os.path.abspath("mapa_rota.html")))

    def obter_enderecos(self):
        conn = create_connection()
        if not conn: return []
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT en.rua, en.numero, en.bairro, en.cidade, en.estado, en.cep, en.complemento, en.latitude, en.longitude, e.id as entrega_id
                    FROM entregas e JOIN enderecos en ON e.endereco_id = en.id
                    WHERE e.rota_id = %s
                """, (self.rota_id,))
                dados = cursor.fetchall()
                return [
                    {
                        'descricao': f"{r['rua']}, {r['numero']}, {r['bairro']}, {r['cidade']}",
                        'rua': r['rua'],
                        'numero': r['numero'],
                        'bairro': r['bairro'],
                        'cidade': r['cidade'],
                        'estado': r['estado'],
                        'cep': r['cep'],
                        'complemento': r['complemento'],
                        'latitude': float(r['latitude']),
                        'longitude': float(r['longitude']),
                        'id': r['entrega_id']
                    }
                    for r in dados if r['latitude'] and r['longitude']
                ]
        except Exception as e:
            print(f"Erro ao obter endereços: {e}")
            return []
        finally:
            if conn: conn.close()

    def mostrar_detalhes_endereco(self, item):
        ponto = item.data(Qt.UserRole)
        if not ponto or not isinstance(ponto, dict) or 'rua' not in ponto:
            return

        detalhes = f"Rua: {ponto['rua']}, {ponto['numero']}\nBairro: {ponto['bairro']}\nCidade: {ponto['cidade']} - {ponto['estado']}\nCEP: {ponto['cep']}\nComplemento: {ponto['complemento'] or '-'}"
        QMessageBox.information(self, "Detalhes do Endereço", detalhes)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MapaRota(3)  # Passa o id da rota
    form.show()
    sys.exit(app.exec())
