import json

def linear_interpolate(x_value, points_set):
    for idx in range(len(points_set) - 1):
        start_x, start_y = points_set[idx]
        end_x, end_y = points_set[idx + 1]
        if start_x <= x_value <= end_x:
            return start_y + (end_y - start_y) * (x_value - start_x) / (end_x - start_x)
    return 0

def fuzzy_membership(val, fuzzy_intervals):
    return linear_interpolate(val, fuzzy_intervals)

def compute_membership(val, fuzzy_config):
    return {item["id"]: fuzzy_membership(val, item["points"]) for item in fuzzy_config}

def apply_fuzzy_rules(temp_degs, heat_degs, rule_map):
    accum = 0.0
    weight_sum = 0.0

    for t_term, h_term in rule_map:
        t_val = temp_degs.get(t_term, 0)
        h_val = heat_degs.get(h_term, 0)
        
        w = min(t_val, h_val)
        accum += w * h_val
        weight_sum += w
    
    return accum / weight_sum if weight_sum > 0 else 0

def main(json_temp, json_heat, json_rules, curr_temp):
    parsed_temp = json.loads(json_temp)["температура"]
    parsed_heat = json.loads(json_heat)["температура"]
    parsed_rules = json.loads(json_rules)
    
    temp_deg = compute_membership(curr_temp, parsed_temp)
    heat_deg = compute_membership(curr_temp, parsed_heat)
    
    outcome = apply_fuzzy_rules(temp_deg, heat_deg, parsed_rules)
    return outcome

if __name__ == "__main__":
    data_temp_json = '''{
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

    data_heat_json = '''{
      "температура": [
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

    data_rules_json = '''[
      ["холодно", "интенсивный"],
      ["комфортно", "умеренный"],
      ["жарко", "слабый"]
    ]'''

    current_temp = 20
    result_value = main(data_temp_json, data_heat_json, data_rules_json, current_temp)
    print(f"Значения оптимального управления: {result_value}")
