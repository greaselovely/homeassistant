import sys
import json
import argparse
from pathlib import Path
from homeassistant_api import Client

def parse_arguments():
    parser = argparse.ArgumentParser(description='Turn on a light with a specific color name using Home Assistant')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--color', metavar='COLOR', help='Enable color')
    group.add_argument('-o', '--off', action='store_true', help='Turn light off')
    return parser.parse_args()

def load_config():
    """
    Used to reference an external json file for
    custom config items
    """
    file_name = 'config.json'
    local_path = Path(__file__).resolve().parent
    config_path = Path.joinpath(local_path, file_name)
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        """
        We'll build an empty config.json file.
        """
        config_init_starter = {"hass" : {"hass_access_token" : "", "hass_url": "http://127.0.0.1:8123/api", "light": "light.name_here"}}
        with open(config_path, 'w') as file:
            json.dump(config_init_starter, file, indent=2)
         # recursion, load the config file since it wasn't found earlier
        return load_config()
    except json.JSONDecodeError:
        print(f"Error decoding JSON in '{config_path}'.")
        return None

def light_on(color):
    with Client(URL, ACCESS_TOKEN) as client:
        light = client.get_domain("light")
        light.turn_on(entity_id=LIGHT, color_name=color)

def light_off():    
    with Client(URL, ACCESS_TOKEN) as client:
        light = client.get_domain("light")
        light.turn_off(entity_id=LIGHT)


def main():
    global URL, ACCESS_TOKEN, LIGHT
    config = load_config()
    ACCESS_TOKEN = config.get('hass').get('hass_access_token')
    URL = config.get('hass').get('hass_url')
    LIGHT = config.get('hass').get('light')
    if not ACCESS_TOKEN:
        print("[!]\tNo API Token Read from config.json.  Exiting.")
        sys.exit()
    args = parse_arguments()
    if args.color:
        light_on(args.color)
    elif args.off:
        light_off()
    else:
        print("[i]\tNo arguments passed, doing nothing.")
        

if __name__ == '__main__':
    main()