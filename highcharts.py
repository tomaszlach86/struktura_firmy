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
                        // Przekształcenie danych w hierarchiczny format
                        const nodes = {};
                        const links = [];

                        data.forEach(({ from, to }) => {
                            if (!nodes[from]) nodes[from] = { id: from, level: 0 };
                            if (!nodes[to]) nodes[to] = { id: to, level: 1 };
                            links.push({ from: from, to: to });
                        });

                        // Konfiguracja Highcharts
                        Highcharts.chart('container', {
                            chart: {
                                type: 'networkgraph',
                                inverted: true, // Układ pionowy
                                marginTop: 80
                            },
                            title: {
                                text: 'Hierarchiczny Graf Struktury Firm'
                            },
                            plotOptions: {
                                networkgraph: {
                                    keys: ['from', 'to'], // Klucze danych
                                    layoutAlgorithm: {
                                        enableSimulation: false,
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
