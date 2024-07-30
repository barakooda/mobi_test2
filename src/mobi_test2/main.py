import json
from visualize import visualize_lanes
import pathlib


def load_json_as_dict(file_path: str) ->dict:

    with open(file_path, 'r') as file:
        data = json.load(file)
        return data


def main():

    file_path = r"C:\temp\mobi_test2\output_path.json"  # Replace with your actual file path
    data = load_json_as_dict(file_path)
    

    visualize_lanes(data.get('lanes'))






   

    

if __name__ == '__main__':
    main()