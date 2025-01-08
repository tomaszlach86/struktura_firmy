from flask import Flask, jsonify, render_template_string
import pandas as pd

app = Flask(__name__)

# Ścieżka do pliku Excel i nazwa arkusza
FILE_PATH = "plik.xlsx"  # Domyślny plik Excel
SHEET_NAME = "aaa"  # Domyślna nazwa arkusza


# Endpoint do pobierania danych
@app.route('/data', methods=['GET'])
def get_data():
    try:
        # Wczytaj dane z Excela
        df = pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME)
    except Exception as e:
        return jsonify({"error": f"Błąd wczytywania pliku: {str(e)}"}), 500

    # Konwertuj dane na format Highcharts Organization Chart
    data = []

    for _, row in df.iterrows():
        entity = row["reporting_entity_name"]
        property_ = row["property_name"]
        company = row["company_name"]

        # Dodaj relacje dla Organization Chart
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
        <title>Structure Graph</title>
        <!-- Główna biblioteka Highcharts -->
       <script src="https://code.highcharts.com/highcharts.js"></script>
<script src="https://code.highcharts.com/modules/sankey.js"></script>
<script src="https://code.highcharts.com/modules/organization.js"></script>
<script src="https://code.highcharts.com/modules/exporting.js"></script>
<script src="https://code.highcharts.com/modules/accessibility.js"></script>
    </head>
    <body>
        <div id="container" style="width: 100%; height: 600px;"></div>
        <script>
            document.addEventListener('DOMContentLoaded', function () {
                // Pobierz dane z backendu
                fetch('/data')
                    .then(response => response.json())
                    .then(data => {
                        // Sprawdzenie błędów w danych
                        if (data.error) {
                            alert('Błąd w danych: ' + data.error);
                            return;
                        }

                        // Konfiguracja Highcharts Organization Chart
                        Highcharts.chart('container', {
                            chart: {
                                type: 'organization',
                                inverted: true,
                                height: 600
                            },
                            title: {
                                text: 'Hierarchiczny Graf Struktury Firm'
                            },
                            series: [{
                                type: 'organization',
                                name: 'Organizacja',
                                keys: ['from', 'to'],
                                data: data,
                                levels: [
                                    { level: 0, color: '#007ad0', dataLabels: { color: 'white' }, height: 25 },
                                    { level: 1, color: '#434348', dataLabels: { color: 'white' }, height: 25 },
                                    { level: 2, color: '#90ee7e', dataLabels: { color: 'black' }, height: 25 }
                                ],
                                colorByPoint: false,
                                dataLabels: {
                                    color: 'white'
                                },
                                borderColor: 'white',
                                nodeWidth: 65
                            }],
                            tooltip: {
                                outside: true
                            },
                            exporting: {
                                allowHTML: true,
                                sourceWidth: 800,
                                sourceHeight: 600
                            }
                        });
                    })
                    .catch(err => {
                        alert('Błąd podczas pobierania danych: ' + err);
                    });
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template)


if __name__ == '__main__':
    app.run(debug=True)
