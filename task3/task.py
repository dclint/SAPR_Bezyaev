import csv
import math

def main(data_csv: str) -> float:
    # Читаем строки как CSV
    lines = data_csv.strip().splitlines()
    matrix_data = csv.reader(lines)
    matrix = [[int(val) for val in row] for row in matrix_data]

    row_count = len(matrix)
    col_count = len(matrix[0])
    calc_entropy = 0.0
    
    # Рассчитываем энтропию
    for col_index in range(col_count):
        for row_index in range(row_count):
            val_ij = matrix[row_index][col_index]
            if val_ij > 0:
                prob = val_ij / (row_count - 1)
                calc_entropy -= prob * math.log2(prob)

    return round(calc_entropy, 1)

if __name__ == "__main__":
    test_csv_string = """2,0,2,0,0
    0,1,0,0,1
    2,1,0,0,1
    0,1,0,1,1
    0,1,0,1,1"""
    outcome = main(test_csv_string)
    print(outcome)
