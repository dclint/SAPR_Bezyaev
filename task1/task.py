import json
import numpy as np

def main(json_str: str):
    # Парсим JSON-строку
    parsed_data = json.loads(json_str)
    # Собираем список вершин
    node_ids = list(parsed_data["nodes"].keys())
    # Создаем матрицу смежности
    adjacency_matrix = np.zeros((len(node_ids), len(node_ids)), dtype=int)
    
    # Заполняем матрицу смежности
    for src_node, neighbors in parsed_data["nodes"].items():
        for dst_node in neighbors:
            i = node_ids.index(src_node)
            j = node_ids.index(dst_node)
            adjacency_matrix[i][j] = 1
            adjacency_matrix[j][i] = 1

    return adjacency_matrix

if __name__ == "__main__":
    graph_definition = """
    {
        "nodes":{
            "1": ["2"],
            "2": ["3", "4"],
            "3": ["5"],
            "4": [],
            "5": []
        }
    }
    """
    result_matrix = main(graph_definition)
    print(result_matrix)
