import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

# Wczytanie danych z pliku Excel
file_path = "ścieżka_do_pliku.xlsx"  # Zamień na ścieżkę do swojego pliku
sheet_name = "AaA_TB"

# Odczyt danych z pliku Excel
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Tworzenie grafu
G = nx.DiGraph()

# Dodawanie wierzchołków i krawędzi z danych
for _, row in df.iterrows():
    entity = row["reporting_entity_name"]
    property_ = row["property_name"]
    company = row["company_name"]
    
    G.add_node(entity, layer=0)
    G.add_node(property_, layer=1)
    G.add_node(company, layer=2)
    G.add_edge(entity, property_)
    G.add_edge(property_, company)

# Pozycje wierzchołków dla hierarchii
pos = nx.multipartite_layout(G, subset_key="layer")

# Obrót grafu o 90 stopni w lewo - zmiana układu na pionowy
rotated_pos = {node: (y, -x) for node, (x, y) in pos.items()}

# Rysowanie grafu z pionowym układem
plt.figure(figsize=(10, 8))
nx.draw_networkx_nodes(G, rotated_pos, node_size=3000, node_color='lightblue', edgecolors='black')
nx.draw_networkx_edges(G, rotated_pos, arrowstyle='->', arrowsize=20, edge_color='gray')
nx.draw_networkx_labels(G, rotated_pos, font_size=10, font_color='black', font_weight='bold')

plt.title("Hierarchiczny Graf Struktury Firm (Obrócony o 90°)", fontsize=14)
plt.axis("off")
plt.show()
