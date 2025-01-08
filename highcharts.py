from flask import Flask, jsonify, render_template_string
import pandas as pd

app = Flask(__name__)

# Ścieżka do pliku Excel
FILE_PATH = "plik.xlsx"  # Zamień na rzeczywistą ścieżkę do pliku
SHEET_NAME = "aaa"

# Endpoint do pobierania danych
@app.route('/data', methods=['GET'])
def get_data():
    # Wczytaj dane z Excela
    df = pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME)

    # Konwertuj dane na format Highcharts
    nodes = []
    links = []
    node_positions = {}  # Ręczne przypisanie pozycji węzłów

    level_map = {"entity": 0, "property": 1, "company": 2}

    for _, row in df.iterrows():
        entity = row["reporting_entity_name"]
        property_ = row["property_name"]
        company = row["company_name"]

        # Dodaj węzły
        if entity not in node_positions:
            node_positions[entity] = {"id": entity, "level": level_map["entity"]}
            nodes.append(node_positions[entity])
        if property_ not in node_positions:
            node_positions[property_] = {"id": property_, "level": level_map["property"]}
            nodes.append(node_positions[property_])
        if company not in node_positions:
            node_positions[company] = {"id": company, "level": level_map["company"]}
            nodes.append(node_positions[company])

        # Dodaj połączenia
        links.append({"from": entity, "to": property_})
        links.append({"from": property_, "to": company})

    return jsonify({"nodes": nodes, "links": links})

# Endpoint do strony głównej
@app.route('/')
def index():
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hierarchiczny Graf Struktury Firm</title>
        <script src="https://code.highcharts.com/highcharts.js"></script>
        <script src="https://code.highcharts.com/modules/networkgraph.js"></script>
        <script src="https://code.highcharts.com/modules/exporting.js"></script>
    </head>
    <body>
        <div id="container" style="width: 100%; height: 600px;"></div>
        <script>
            document.addEventListener('DOMContentLoaded', function () {
                // Pobierz dane z backendu
                fetch('/data')
                    .then(response => response.json())
                    .then(responseData => {
                        const { nodes, links } = responseData;

                        // Przypisz ręczne pozycje dla węzłów hierarchicznych
                        const positions = {};
                        nodes.forEach(node => {
                            if (node.level === 0) positions[node.id] = { x: 0, y: 0 };
                            if (node.level === 1) positions[node.id] = { x: 0, y: -200 };
                            if (node.level === 2) positions[node.id] = { x: 0, y: -400 };
                        });

                        // Konfiguracja Highcharts
                        Highcharts.chart('container', {
                            chart: {
                                type: 'networkgraph',
                                marginTop: 80
                            },
                            title: {
                                text: 'Hierarchiczny Graf Struktury Firm'
                            },
                            plotOptions: {
                                networkgraph: {
                                    layoutAlgorithm: {
                                        enableSimulation: false
                                    }
                                }
                            },
                            series: [{
                                marker: {
                                    radius: 10
                                },
                                dataLabels: {
                                    enabled: true,
                                    linkFormat: '',
                                    allowOverlap: true
                                },
                                nodes: nodes.map(node => ({
                                    id: node.id,
                                    marker: { radius: 10 },
                                    x: positions[node.id].x,
                                    y: positions[node.id].y
                                })),
                                data: links
                            }]
                        });
                    });
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True)
