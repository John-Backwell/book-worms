import json
import os
import glob

def check_book_data_json(file_path):
    
    with open(file_path,'r') as f:
        is_field_empty = {}
        book_data_dict = json.load(f)
    for key,value in book_data_dict.items():
        if value == "" or (not value):
            is_field_empty[key] = 1
        else:
            is_field_empty[key] = 0
    return is_field_empty

def check_all_books(directory_string):
    total_empty_fields = {}
    for file_path in glob.glob(os.path.join(directory_string,'*.json')):
        individual_book_data = check_book_data_json(file_path)
        for key,value in individual_book_data.items():
            if key in total_empty_fields.keys():
                total_empty_fields[key] = total_empty_fields[key] + individual_book_data[key]
            else:
                total_empty_fields[key] = individual_book_data[key]
    return total_empty_fields


if __name__ == "__main__":
    print(check_all_books("sci_fi_fantasy_data"))