import spacy
from spacy.tokens import DocBin
from collections import defaultdict
import math
import random

# Загружаем модель SpaCy
nlp = spacy.blank("ru")

# Функция для конвертации данных в формат spacy
def convert_to_spacy_format(data, nlp):
    doc_bin = DocBin()
    for item in data:
        text, annotations = item
        doc = nlp.make_doc(text)
        ents = []
        for start, end, label in annotations:
            span = doc.char_span(start, end, label=label)
            if span:
                ents.append(span)
        doc.ents = ents
        doc_bin.add(doc)
    return doc_bin

# Чтение данных на конвертацию из файла
data = [
    eval(line.strip().rstrip(","))
    for line in open("training_data.txt", encoding="utf-8")
]

# Группируем данные по классам
class_data = defaultdict(list)
for item in data:
    if isinstance(item, tuple) and len(item) == 2:
        _, annotations = item
        for _, _, label in annotations:
            class_data[label].append(item)
            break  # Предполагаем, что каждый текст относится к одному классу

# Устанавливаем соотношение для train, dev и test наборов
train_ratio = 0.7
dev_ratio = 0.2
test_ratio = 0.1

train_data = []
dev_data = []
test_data = []

# Вычисляем количество элементов для каждого класса
for label, items in class_data.items():
    n_items = len(items)
    n_train = math.ceil(train_ratio * n_items)
    n_dev = math.ceil(dev_ratio * n_items)
    n_test = n_items - n_train - n_dev  # Оставшееся количество идёт в тестовый набор

    # Добавляем данные в наборы
    train_data.extend(items[:n_train])
    dev_data.extend(items[n_train:n_train + n_dev])
    test_data.extend(items[n_train + n_dev:])

# Перемешиваем данные внутри каждого набора для случайного распределения
random.shuffle(train_data)
random.shuffle(dev_data)
random.shuffle(test_data)

# Конвертируем данные в формат spacy и сохраняем
train_doc_bin = convert_to_spacy_format(train_data, nlp)
train_doc_bin.to_disk("train.spacy")

dev_doc_bin = convert_to_spacy_format(dev_data, nlp)
dev_doc_bin.to_disk("dev.spacy")

test_doc_bin = convert_to_spacy_format(test_data, nlp)
test_doc_bin.to_disk("test.spacy")