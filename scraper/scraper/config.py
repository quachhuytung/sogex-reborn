import yaml

config_data = dict()

with open("./scraper/config.yml", 'r') as stream:
    try:
        config_data = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
