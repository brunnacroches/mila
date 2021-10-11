import yaml

data = yaml.safe_load(open('nlu|train.yml', 'r', encoding='utf-8').read())

for command in data['commands']:
    print(command)


# deve passar o diretório dela


# TESTE > terminal
# python3.8 nlu/test_data.py

# print(data)
