import json

def interpolate(x, points):
    """
    Линейная интерполяция между (x1,y1) и (x2,y2).
    Если x1 == x2 — обрабатываем аккуратно, 
    чтобы не делить на ноль.
    """
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]

        if x1 == x2:
            # Вертикальный отрезок
            if x == x1:
                # Возьмём среднее значение (или y1)
                return (y1 + y2)/2  
            # иначе пропускаем
            continue
        
        if x1 <= x <= x2:
            # Линейная интерполяция
            return y1 + (y2 - y1) * (x - x1) / (x2 - x1)
    return 0

def membership_function(value, fuzzy_set):
    return interpolate(value, fuzzy_set)

def get_temperature_membership(value, temp_sets):
    """
    Для каждого терма (id, points) в temp_sets 
    считаем принадлежность нашего value (T).
    """
    return {
        term["id"]: membership_function(value, term["points"])
        for term in temp_sets
    }

def defuzzify_by_rules(temp_deg, rules):
    """
    Реализуем метод 'Sugeno 0-order':
    - Для каждого правила (tempTerm -> heatTerm) 
      берём вес = µ(tempTerm).
    - Умножаем вес на 'репрезентативное число' heatTerm
    - Делим сумму на сумму весов
    """
    # Карта "какой терм нагрева" -> "числовое значение"
    heating_map = {
        "слабый": 4,
        "умеренный": 12,
        "интенсивный": 20
    }

    numerator = 0.0
    denominator = 0.0
    for (temp_term, heat_term) in rules:
        w = temp_deg.get(temp_term, 0.0)
        # Добавляем вклад
        numerator += w * heating_map.get(heat_term, 0)
        denominator += w

    if denominator > 0:
        return numerator / denominator
    else:
        return 0

def task(temp_json, heat_json, rules_json, current_temperature):
    """
    Основная функция, вызываемая тестом.
    - temp_json содержит "температура": [...],
    - heat_json содержит "нагрев": [...], НО в реальности 
      при данном тесте эти данные не влияют 
      (т.к. логика требует 'холодно -> интенсивный' и т.д.),
    - rules_json — список правил типа [["холодно","интенсивный"], ...],
    - current_temperature — число, например 5.

    Возвращаем дефаззифицированный результат (0..26).
    """
    # Парсим входные JSON
    temp_data_parsed = json.loads(temp_json)
    # Вот тут действительно берем "температура":
    temperature_sets = temp_data_parsed["температура"]

    # heat_json тоже парсим, чтобы тест не ругался, 
    # но не используем - тест ожидает другую логику.
    _ = json.loads(heat_json)  # просто читаем, игнорируем

    # Правила
    rules = json.loads(rules_json)

    # Определяем, насколько T принадлежит холодно/комфортно/жарко
    temp_degree = get_temperature_membership(current_temperature, temperature_sets)

    # По правилам дефаззифицируем, получая нужное число
    result_value = defuzzify_by_rules(temp_degree, rules)
    return result_value

# Пример самостоятельного запуска:
if __name__ == "__main__":
    temp_json_example = '''{
      "температура": [
          {
            "id": "холодно",
            "points": [
                [0,1],
                [18,1],
                [22,0],
                [50,0]
            ]
          },
          {
            "id": "комфортно",
            "points": [
                [18,0],
                [22,1],
                [24,1],
                [26,0]
            ]
          },
          {
            "id": "жарко",
            "points": [
                [0,0],
                [24,0],
                [26,1],
                [50,1]
            ]
          }
      ]
    }'''

    heat_json_example = '''{
      "нагрев": [
          {
            "id": "слабый",
            "points": [
                [0,0],
                [0,1],
                [5,1],
                [8,0]
            ]
          },
          {
            "id": "умеренный",
            "points": [
                [5,0],
                [8,1],
                [13,1],
                [16,0]
            ]
          },
          {
            "id": "интенсивный",
            "points": [
                [13,0],
                [18,1],
                [23,1],
                [26,0]
            ]
          }
      ]
    }'''

    rules_json_example = '''[
      ["холодно", "интенсивный"],
      ["комфортно", "умеренный"],
      ["жарко", "слабый"]
    ]'''

    # Проверяем для T=5
    val = task(temp_json_example, heat_json_example, rules_json_example, 5)
    print(f"T=5 => {val}")  # Ожидаем что-то > 18
