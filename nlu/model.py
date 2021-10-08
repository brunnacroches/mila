import yaml
import numpy as np
import tensorflow as tf  # ===> ADD A LINGUAGEM DE APRENDIZADO TENSORFLOW (MARCHING LEARNING)
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.utils import to_categorical # essa função vai transformar as nossas labels em índice 

data = yaml.safe_load(open('nlu/train.yml', 'r', encoding='utf-8').read())

# criando duas listas e armazenar as entradas e as saídas
inputs, outputs = [], []

for command in data['commands']:
  inputs.append(command['input'].lower())
  outputs.append('{}\{}'.format(command['entity'], command['action']))

# Lista de Caracteres 
# Processar texto: palavras, caracteres, bytes, sub-palavras

# criando um set
chars = set()

for input in inputs + outputs:
  for ch in input:
    if ch not in chars:
      chars.add(ch)


# Mapear char-idx
chr2idx= {}
idx2chr = {}

for i, ch in enumerate(chars):
  chr2idx[ch] = i
  idx2chr[i] = ch

# cada exemplo em entrada
max_seq = max([len(x)for x in inputs])

print('Número de chars:', len(chars))
print('Maior seq:', max_seq)

# Criar o DataSet one-hot (dados de textos para números usando deep learning) (número de exemplos, tamanho da sequencia, número de caracteres)
# Criar dataset sparso (disperso => (número de exemplos, tamanho da sequencia, número de caracteres))
input_data = np.zeros((len(inputs), max_seq, len(chars)), dtype='int32')
output_data = to_categorical(outputs, len(outputs)) # ===> ADD A LINGUAGEM DE APRENDIZADO TENSORFLOW (MARCHING LEARNING)

for i, input in enumerate(inputs):
  for k, ch in enumerate(input):
    input_data[i, k, chr2idx[ch]] = 1.0

print(output_data[0])


# print(inputs)
# print(outputs)


# deve passar o diretório dela

# TESTE > terminal
# python3.8 nlu/model.py

# print(data)


# Criando o framework básico para que a gente possa fazer reconhecimento de comandos de forma dinamica
# ADD dados e criar funções da dataset e treinar 
# Focar nas partes corretas. 
# time: 20:10

# PARA FAZER CLASSIFICAÇÃO DE SENTIMENTOS
# https://keras.io/examples/nlp/text_classification_from_scratch/

# FAZENDO UMA CLASSIFIÇÃO DE ENTIDADE
# dar um texto, um DataSete e vamos prever qual entidade o texto pertence
# método para calcular a confinça 
