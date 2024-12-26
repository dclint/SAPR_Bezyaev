import csv
from collections import defaultdict

def main(csv_data: str) -> str:
    # Разбиваем входную CSV-строку на строки и парсим
    parsed_rows = csv.reader(csv_data.splitlines())
    pairs = [(int(a), int(b)) for a, b in parsed_rows]
    
    # Словари для хранения связей
    children_map = defaultdict(list)
    parent_map = defaultdict(list)
    
    # Заполнение children_map и parent_map
    for first, second in pairs:
        children_map[first].append(second)
        parent_map[second].append(first)
    
    # Собираем множество всех узлов
    all_nodes = set(children_map.keys()).union({b for _, b in pairs})

    # Массивы (A, B, C, D, E) для каждого узла
    rel_values = {node: [0, 0, 0, 0, 0] for node in all_nodes}

    def fetch_descendants(n, level=1):
        result = []
        for child in children_map[n]:
            result.append((child, level))
            result.extend(fetch_descendants(child, level + 1))
        return result
    
    def fetch_ancestors(n, level=1):
        res = []
        for prnt in parent_map[n]:
            res.append((prnt, level))
            res.extend(fetch_ancestors(prnt, level + 1))
        return res

    for item in all_nodes:
        # r1 и r2: количество детей (r1), количество родителей (r2)
        for kid in children_map[item]:
            rel_values[item][0] += 1
            rel_values[kid][1] += 1

        # r3 и r4: количество потомков (r3), количество предков (r4)
        desc = fetch_descendants(item)
        for node_id, lvl in desc:
            if lvl > 1:
                rel_values[item][2] += 1
                rel_values[node_id][3] += 1

        # r5: количество «братьев/сестер»
        if parent_map[item]:
            parent_node = parent_map[item][0]
            siblings = [s for s in children_map[parent_node] if s != item]
            rel_values[item][4] += len(siblings)

    # Формируем строковый результат с заголовками
    output_lines = ["\tA\tB\tC\tD\tE"]
    index = 0
    for sorted_node in sorted(all_nodes):
        index += 1
        output_lines.append(f"{index}\t" + "\t".join(map(str, rel_values[sorted_node])))

    return "\n".join(output_lines)

if __name__ == "__main__":
    test_csv_data = """1,2
                       1,3
                       3,4
                       3,5"""
    result_str = main(test_csv_data)
    print(result_str)
