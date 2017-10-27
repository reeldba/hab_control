def get_config_json(file_name):
    """
    """
    import sys
    import json

    try:
            with open(file_name,'r') as json_data_file:
                    config=json.load(json_data_file)

            return config

    except IOError:
            print("Cannot find habitat.json or read data from it.")
            exit(1)
