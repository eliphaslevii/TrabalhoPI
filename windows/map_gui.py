import os
import sys
import googlemaps
import polyline
import folium
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from database import create_connection
from PyQt5.QtCore import QUrl

# Sua chave da Google Maps Directions API
GOOGLE_API_KEY = 'AIzaSyAXPQPmxkGD7X-KL5xGEgaSIfiKNdGrMmg'

class MapaRota(QWidget):
    def __init__(self, rota_id):
        super().__init__()
        super().__init__()
        self.rota_id = rota_id
        self.setWindowTitle("Mapa da Rota")
        self.setGeometry(100, 100, 1100, 600)  # Largura maior para o painel ao lado

        layout_principal = QHBoxLayout()  # Layout horizontal principal
        self.setLayout(layout_principal)

        # Área do mapa
        self.view = QWebEngineView()
        layout_principal.addWidget(self.view, 3)  # 3/4 do espaço

        # Painel lateral para infos
        self.painel_info = QWidget()
        self.painel_info_layout = QVBoxLayout()
        self.painel_info.setLayout(self.painel_info_layout)
        layout_principal.addWidget(self.painel_info, 1)  # 1/4 do espaço

        # Labels que serão atualizados depois
        self.label_entregador = QLabel("Entregador: -")
        self.label_tempo = QLabel("Tempo estimado: -")
        self.label_distancia = QLabel("Distância total: -")

        self.painel_info_layout.addWidget(self.label_entregador)
        self.painel_info_layout.addWidget(self.label_tempo)
        self.painel_info_layout.addWidget(self.label_distancia)
        self.painel_info_layout.addStretch()

        # Configura seu client da Google
        self.gmaps = googlemaps.Client(key=GOOGLE_API_KEY)

        self.mostrar_mapa()

    def mostrar_mapa(self):
        enderecos = self.obter_enderecos()
        if not enderecos:
            print("Nenhum endereço encontrado para a rota.")
            return

        # Exemplo: definir o entregador fixo (ou pode buscar do banco)
        nome_entregador = "João Silva"
        self.label_entregador.setText(f"Entregador: {nome_entregador}")

        origem = {
            'descricao': 'Faculdade Tuiuti - Curitiba',
            'latitude': -25.4367,
            'longitude': -49.2768
        }
        destino = origem
        waypoints = enderecos

        origem_str = f"{origem['latitude']},{origem['longitude']}"
        destino_str = f"{destino['latitude']},{destino['longitude']}"
        waypoints_str = [f"{p['latitude']},{p['longitude']}" for p in waypoints]

        try:
            directions_result = self.gmaps.directions(
                origin=origem_str,
                destination=destino_str,
                waypoints=waypoints_str if waypoints_str else None,
                optimize_waypoints=True,
                mode="driving"
            )
        except Exception as e:
            print(f"Erro na API Google Directions: {e}")
            return

        if not directions_result:
            print("Nenhum resultado da rota retornado.")
            return

        route = directions_result[0]

        # Extrair tempo e distância total
        tempo_total = 0
        distancia_total = 0
        for leg in route['legs']:
            tempo_total += leg['duration']['value']  # segundos
            distancia_total += leg['distance']['value']  # metros

        # Converter para formato legível
        tempo_horas = tempo_total // 3600
        tempo_minutos = (tempo_total % 3600) // 60
        distancia_km = distancia_total / 1000

        self.label_tempo.setText(f"Tempo estimado: {tempo_horas}h {tempo_minutos}min")
        self.label_distancia.setText(f"Distância total: {distancia_km:.2f} km")

        # Montar polyline da rota
        polyline_points = []
        for leg in route['legs']:
            for step in leg['steps']:
                polyline_points.extend(polyline.decode(step['polyline']['points']))

        polyline_points = list(dict.fromkeys(polyline_points))

        mapa = folium.Map(location=[origem['latitude'], origem['longitude']], zoom_start=13)

        ordem = route.get('waypoint_order', list(range(len(waypoints))))
        pontos_otimizados = [origem] + [waypoints[i] for i in ordem] + [destino]

        for i, ponto in enumerate(pontos_otimizados):
            cor = 'blue' if i == 0 else 'red' if i == len(pontos_otimizados) - 1 else 'green'
            folium.Marker(
                location=[ponto['latitude'], ponto['longitude']],
                popup=f"{i + 1}. {ponto['descricao']}",
                icon=folium.Icon(color=cor)
            ).add_to(mapa)

        folium.PolyLine(locations=polyline_points, color='blue', weight=5).add_to(mapa)

        mapa.save("mapa_rota.html")
        self.view.setUrl(QUrl.fromLocalFile(os.path.abspath("mapa_rota.html")))

    def obter_enderecos(self):
        conn = create_connection()
        if not conn:
            return []

        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        e.id AS entrega_id,
                        en.rua,
                        en.numero,
                        en.bairro,
                        en.cidade,
                        en.estado,
                        en.cep,
                        en.complemento,
                        en.latitude,
                        en.longitude
                    FROM entregas e
                    JOIN enderecos en ON e.endereco_id = en.id
                    WHERE e.rota_id = %s
                    ORDER BY e.ordem;
                """, (self.rota_id,))
                dados = cursor.fetchall()
                return [
                    {
                        'descricao': f"{row['rua']}, {row['numero']} - {row['bairro']}, {row['cidade']}/{row['estado']}",
                        'latitude': float(row['latitude']),
                        'longitude': float(row['longitude'])
                    }
                    for row in dados if row['latitude'] and row['longitude']
                ]
        except Exception as e:
            print(f"Erro ao obter endereços: {e}")
            return []
        finally:
            conn.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MapaRota(3)  # Passa o id da rota
    form.show()
    sys.exit(app.exec())
