import csv
from consts import *
import sys
sys.path.append("../")

name_to_screen = {}
screen_to_name = {}
users_data = {}



def load_users_from_csv():
    try:
        with open(CSV_PATH, 'rb') as csvfile:
            csv_data = csv.DictReader(csvfile)
            for row in csv_data:
                real_name = row["real_name"]
                screen_name = row["screen_name"]
                if real_name != "" and screen_name != "":
                    name_to_screen[real_name] = screen_name
                    screen_to_name[screen_name] = real_name
    except Exception as ex:
        print 'Error in parsing CSV file! dictionaries will be Empty!'
        print ex.message

def load_users_dict():
    try:
        with open(CSV_PATH, 'rb') as csvfile:
            csv_data = csv.DictReader(csvfile)
            for row in csv_data:
                users_data[row["screen_name"]] = row
    except Exception as ex:
        print 'Error in parsing CSV file! dictionaries will be Empty!'
        print ex.message


load_users_from_csv()
load_users_dict()
users_data_sorted = sorted(name_to_screen.items(), key=lambda item: item[0])
