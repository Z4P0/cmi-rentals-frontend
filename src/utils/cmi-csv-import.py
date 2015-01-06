import os
import csv
import json
import config


# process the config file, make sure we're setup properly
# ----------------------------------------
# CSV_EXISTS = False
# does the CSV file exist?
csv_filename = os.path.join(os.path.dirname(__file__), config.DATA_DIR + config.CSV_FILE)
print(csv_filename)
CSV_FILE = csv_filename
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), config.DATA_DIR + config.OUTPUT_FILE)

# internal vars
# ----------------------------------------
# first row is event description fields
# second row is the actual event description
EQUIPMENT_MODE = False  # we set this to true after Event Info and 4 lines

# we break into hte equipment after 4 blank lines
LINEBREAK_COUNTER = 0
LINEBREAK_LIMIT = 4


# write dictionary to json
data = {}
# these 2 will hold the final, processed data
processed_event_information = {}
processed_equipment_list = []
# these hold data straight from the CSV file
raw_event_information = {}
raw_event_information_list = []
raw_equipment_list = []


# some functions
# ----------------------------------------
def write_json(filename, data_dict):
    with open(filename, "w") as outfile:
        json.dump(data_dict, outfile)
        # json.dumps(data_dict, outfile, sort_keys=True, indent=4, separators=(',', ': '))
    print(filename + " ... done")


def lists_to_dicts(keys_list, values_list):
    tmp_dict = {}
    index = 0
    for raw_key in keys_list:
        # make sure we have values
        if raw_key != '':
            # lowercase and spaces to underscore
            key = raw_key.lower().replace(" ", "_")
            tmp_dict[key] = values_list[index]
        index = index + 1
    return tmp_dict


# process the CSV file
with open(CSV_FILE, "rb") as raw_csvfile:
    csvfile = csv.reader(raw_csvfile, quotechar='|')
    for row in csvfile:
        # handle the event informtion first
        if EQUIPMENT_MODE:
            raw_equipment_list.append(row)
        else:
            if row[0] == '':
                LINEBREAK_COUNTER = LINEBREAK_COUNTER + 1
                if LINEBREAK_COUNTER == LINEBREAK_LIMIT:
                    LINEBREAK_COUNTER = 0
                    EQUIPMENT_MODE = True
            else:
                raw_event_information_list.append(row)


# do the things
# ----------------------------------------
# process event information
processed_event_information = lists_to_dicts(raw_event_information_list[0], raw_event_information_list[1])

# process the rental list
rental_keys = raw_equipment_list.pop(0)  # table headers
for piece in raw_equipment_list:
    processed_equipment_list.append(lists_to_dicts(rental_keys, piece))


# populate the data dict
# ----------------------------------------
data['event_information'] = processed_event_information
data['rental_equipment'] = processed_equipment_list
print("")
print(data)
print("")


# write out the file
# ----------------------------------------
write_json(OUTPUT_FILE, data)
