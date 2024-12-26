import math

def build_frequencies():
    freq_sum = {}
    freq_prod = {}
    freq_combined = {}

    # Перебираем все варианты бросков двух кубиков
    for dice_a in range(1, 7):
        for dice_b in range(1, 7):
            s_value = dice_a + dice_b
            p_value = dice_a * dice_b
            combo_key = f"{s_value}-{p_value}"

            freq_sum[s_value] = freq_sum.get(s_value, 0) + 1
            freq_prod[p_value] = freq_prod.get(p_value, 0) + 1
            freq_combined[combo_key] = freq_combined.get(combo_key, 0) + 1

    return freq_sum, freq_prod, freq_combined

def measure_entropy(distribution_map):
    total_count = sum(distribution_map.values())
    e_value = 0.0

    for count in distribution_map.values():
        prob = count / total_count
        e_value -= prob * math.log2(prob)

    return e_value

def main():
    s_map, p_map, combo_map = build_frequencies()

    combo_entropy = measure_entropy(combo_map)
    s_entropy = measure_entropy(s_map)
    p_entropy = measure_entropy(p_map)

    # Условная энтропия
    cond_entropy = combo_entropy - s_entropy
    # Взаимная информация
    mutual_info = p_entropy - cond_entropy

    return [
        round(combo_entropy, 2),
        round(s_entropy, 2),
        round(p_entropy, 2),
        round(cond_entropy, 2),
        round(mutual_info, 2)
    ]

if __name__ == "__main__":
    result_values = main()
    print(result_values)
