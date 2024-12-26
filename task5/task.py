import json

def build_index_map(rank_list):
    index_map = {}
    rank_counter = 0
    for group in rank_list:
        if isinstance(group, list):
            for item in group:
                index_map[item] = rank_counter
        else:
            index_map[group] = rank_counter
        rank_counter += 1
    return index_map

def matrix_multiply(m1, m2, do_transpose=False):
    size = len(m1)
    result_m = [[0]*size for _ in range(size)]
    
    # При необходимости транспонируем
    mat1 = m1
    mat2 = m2
    if do_transpose:
        mat1 = list(map(list, zip(*mat1)))
        mat2 = list(map(list, zip(*mat2)))

    for r in range(size):
        for c in range(size):
            result_m[r][c] = mat1[r][c] * mat2[r][c]
    return result_m

def make_relation(index_map):
    n = len(index_map)
    out_matrix = [[0]*n for _ in range(n)]

    for r in range(n):
        for c in range(n):
            if index_map.get(r+1, n) >= index_map.get(c+1, n):
                out_matrix[r][c] = 1
    return out_matrix

def find_conflict_core(m1, m2):
    conflict_pairs = []
    for r_idx in range(len(m1)):
        for c_idx in range(r_idx+1, len(m1[r_idx])):
            if m1[r_idx][c_idx] + m2[r_idx][c_idx] == 0:
                conflict_pairs.append([r_idx+1, c_idx+1])
    return conflict_pairs

def main(ranking_a_json: str, ranking_b_json: str) -> str:
    parsed_a = json.loads(ranking_a_json)
    parsed_b = json.loads(ranking_b_json)

    rel_a = make_relation(build_index_map(parsed_a))
    rel_b = make_relation(build_index_map(parsed_b))

    combined_m = matrix_multiply(rel_a, rel_b)
    transposed_m = matrix_multiply(rel_a, rel_b, do_transpose=True)

    core_data = find_conflict_core(combined_m, transposed_m)
    return json.dumps(core_data)

if __name__ == "__main__":
    example_a = "[1,[2,3],4,[5,6,7],8,9,10]"
    example_b = "[[1,2],[3,4,5],6,7,9,[8,10]]"
    print(main(example_a, example_b))
