from flask import Flask, jsonify, render_template_string
import pandas as pd

app = Flask(__name__)

# Ścieżka do pliku Excel
FILE_PATH = "ścieżka_do_pliku.xlsx"  # Zamień na rzeczywistą ścieżkę do pliku
SHEET_NAME = "AaA_TB"

# Endpoint do pobierania danych
@app.route('/data', methods=['GET'])
def get_data():
    # Wczytaj dane z Excela
    df = pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME)

    # Konwertuj dane na format Highcharts
    data = []
    for _, row in df.iterrows():
        entity = row["reporting_entity_name"]
        property_ = row["property_name"]
        company = row["company_name"]

        # Dodaj połączenia
        data.append({"from": entity, "to": property_})
        data.append({"from": property_, "to": company})

    return jsonify(data)

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
                    .then(data => {
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
                                        enableSimulation: true,
                                        linkLength: 100
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
                                data: data
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
