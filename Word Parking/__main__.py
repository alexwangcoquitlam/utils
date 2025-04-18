import csv
import pprint
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DEFAULT = '\033[39m'

with open("lists\\tags.txt", 'r') as tags_file:
    allowed_tags = tags_file.read().splitlines()

with open("lists\\types.txt", 'r') as types_file:
    allowed_types = types_file.read().splitlines()

def run_list_sort(dictionary_list):
    try:
        sorted_list = sorted(dictionary_list, key=lambda x: x['word'])
        with open("dictionary.csv", 'w', newline='') as csv_file:
                    writer = csv.DictWriter(csv_file, sorted_list[0].keys(), delimiter=';')
                    writer.writeheader()
                    writer.writerows(sorted_list)

        print(f"{bcolors.OKGREEN}Successfully sorted list and outputted to dictionary.csv{bcolors.DEFAULT}")
    except Exception as e:
        print(f"{bcolors.FAIL}Exception occurred in sort operation: {e}{bcolors.DEFAULT}")


def run_lookup_prompts(dictionary_list):
    allowed_actions = ['word', 'definition', 'type', 'tags', 'links', 'back']
    while True:
        action = input(f"What key would you like to lookup? {allowed_actions}\n").lower()
        if action not in allowed_actions:
            print(f"{bcolors.FAIL}That action is not allowed.{bcolors.DEFAULT}")
        elif action == 'back':
            break
        else:
            if action == 'tags':
                print(f"The following tags are available: {sorted(allowed_tags)}")
            elif action == 'type':
                print(f"The following types are available: {sorted(allowed_types)}")
            search_term = input("What would you like to search for?\n").lower()
            refined_list = [row for row in dictionary_list if search_term.lower() in row[action].lower()]
            pprint.pprint(refined_list)
            return refined_list

if __name__ == "__main__":
    allowed_actions = ['sort', 'lookup', 'exit']

    with open('dictionary.csv', newline='') as dictionary_file:
        reader = csv.DictReader(dictionary_file, delimiter=';')
        data = list(reader)
    
    while True:
        action = input(f"What would you like to do? {allowed_actions}\n").lower()
        if action not in allowed_actions:
            print(f"{bcolors.FAIL}That action is not allowed.{bcolors.DEFAULT}")
        elif action == 'sort':
            run_list_sort(data)
        elif action == "lookup":
            refined_list = run_lookup_prompts(data)
            while True:
                action = input("Would you like to refine the search? [Y, N]\n")
                if action == 'y':
                    run_lookup_prompts(refined_list)
                elif action == 'n':
                    break
        elif action == 'exit':
            break