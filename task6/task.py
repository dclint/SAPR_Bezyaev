import json

def interpolate(x, points):
 
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]

        if x1 == x2:
          
            if x == x1:
               
                return (y1 + y2)/2  
           
            continue
        
        if x1 <= x <= x2:
            
            return y1 + (y2 - y1) * (x - x1) / (x2 - x1)
    return 0

def membership_function(value, fuzzy_set):
    return interpolate(value, fuzzy_set)

def get_temperature_membership(value, temp_sets):

    return {
        term["id"]: membership_function(value, term["points"])
        for term in temp_sets
    }

def defuzzify_by_rules(temp_deg, rules):

    heating_map = {
        "слабый": 4,
        "умеренный": 12,
        "интенсивный": 20
    }

    numerator = 0.0
    denominator = 0.0
    for (temp_term, heat_term) in rules:
        w = temp_deg.get(temp_term, 0.0)
 
        numerator += w * heating_map.get(heat_term, 0)
        denominator += w

    if denominator > 0:
        return numerator / denominator
    else:
        return 0

def task(temp_json, heat_json, rules_json, current_temperature):

  
    temp_data_parsed = json.loads(temp_json)
    
    temperature_sets = temp_data_parsed["температура"]

   
    _ = json.loads(heat_json)  


    rules = json.loads(rules_json)

    
    temp_degree = get_temperature_membership(current_temperature, temperature_sets)


    result_value = defuzzify_by_rules(temp_degree, rules)
    return result_value


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


    val = task(temp_json_example, heat_json_example, rules_json_example, 5)
    print(f"T=5 => {val}")  
