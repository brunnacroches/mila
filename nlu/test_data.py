import yml

data = yml.safe_load(open('nlu\\train.yml', 'r', encoding='utf-8').read())

# deve passar o diretório dela

print(data)

#  python3.8 nlu\test_data.py