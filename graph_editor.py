import json
from typing import Union

def load_jsonld(filepath: str) -> Union[str, None]:
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            jsonld_data = json.load(file)
        return json.dumps(jsonld_data, indent=2)
    except Exception as e:
        print(f"Error loading JSON-LD file: {e}")
        return None

def save_jsonld(filepath: str, jsonld_data: str) -> bool:
    try:
        data = json.loads(jsonld_data)
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2)
        return True
    except Exception as e:
        print(f"Error saving JSON-LD file: {e}")
        return False

def edit_jsonld(jsonld_data: str) -> str:
    # Implement the editing logic as needed.
    # For example, you could modify certain fields or add/remove elements from the JSON-LD structure.
    # In this example, I am not doing any actual editing; I am just returning the original data.
    return jsonld_data

def extract_information(jsonld_data, schema_dict):
    result = {}  # słownik wynikowy, który zawiera informacje wyciągnięte z danych JSON-LD

    # Przechodzenie przez elementy schematu, aby znaleźć odpowiedni fragment danych
    for element_type, element_info in schema_dict.items():
        current_elements = [jsonld_data]

        for path_element in element_info["path"][:-1]:
            next_elements = []
            for current_element in current_elements:
                if isinstance(current_element, dict) and path_element in current_element:
                    value = current_element[path_element]
                    if isinstance(value, list):
                        next_elements.extend(value)
                    else:
                        next_elements.append(value)
            current_elements = next_elements

        if not current_elements:
            continue

        # Wyszukiwanie wartości dla ostatniego elementu ścieżki
        elements_list = []
        for current_element in current_elements:
            if isinstance(current_element, dict) and element_info["path"][-1] in current_element:
                value = current_element[element_info["path"][-1]]
                if isinstance(value, list):
                    elements_list.extend(value)
                else:
                    elements_list.append(value)

        result_elements = []

        # Tworzenie słownika dla każdego znalezionego elementu
        for element in elements_list:
            if not isinstance(element, dict):
                continue

            result_element = {}

            # Dodawanie atrybutów do słownika wynikowego
            for attribute in element_info["attributes"]:
                result_element[attribute] = element.get(attribute, None)

            result_elements.append(result_element)

        # Dodawanie elementów wynikowych do słownika wynikowego
        result[element_type] = result_elements

    return result  # zwracanie słownika zawierającego informacje wyciągnięte z danych JSON-LD


#def filter_by_name(data, name):
#    return [item for item in data if item.get('proj:name') == name]
#result = extract_information(jsonld_data, schema_dict)
#filtered_result = filter_by_name(result['func'], 'connect_to_neo4j')
