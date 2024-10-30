import spacy
import re
import openpyxl
import os
import sqlite3
from word2number import w2n  # Для преобразования числа из слов
from natasha import Segmenter, Doc, MorphVocab  # Импортируем необходимые классы из natasha

# Инициализируем анализатор
segmenter = Segmenter()
morph_vocab = MorphVocab()

# Загрузите модель для русского языка
nlp_ru = spacy.load(os.path.join(os.path.dirname(__file__), '..', 'models', 'model-best'))

# Пути к файлам
input_txt_file = os.path.join(os.path.dirname(__file__), '..', 'forUse', 'for_model.txt')
output_xlsx_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'output_data.xlsx')

# Подключаемся к базе данных SQLite
conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), '..', 'data', 'database.db'))
cursor = conn.cursor()

# Создаём таблицу, если её нет
cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_name TEXT PRIMARY KEY,
        quantity INTEGER
    )
""")
conn.commit()

# Словарь для хранения общего количества каждого товара
product_counts = {}

# Функция для извлечения сущностей заданного типа из документа
def extract_entities(doc, entity_type):
    return [ent.text for ent in doc.ents if ent.label_ == entity_type]

# Функция для нормализации наименований товаров
def normalize_product_name(product_name):
    doc = Doc(product_name)
    doc.segment(segmenter)
    for token in doc.tokens:
        token.lemmatize(morph_vocab)  # Лемматизация с использованием MorphVocab
    return " ".join([token.lemma for token in doc.tokens])

# Функция для преобразования чисел, записанных словами, в цифры
def convert_word_to_number(word):
    try:
        return w2n.word_to_num(word)
    except ValueError:
        return None  # Если слово не является числом, возвращаем None

# Обрабатываем входной файл
with open(input_txt_file, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        doc_ru = nlp_ru(line)

        for entity_type in entity_types:
            entities = extract_entities(doc_ru, entity_type)
            for product in entities:
                # Лемматизация наименования товара
                normalized_product = normalize_product_name(product)

                # Проверяем наличие чисел в начале строки (например, "два яблока" -> "2 яблока")
                words = normalized_product.split()
                if len(words) > 1 and (quantity := convert_word_to_number(words[0])) is not None:
                    normalized_product = " ".join(words[1:])  # Убираем первое слово (число)
                else:
                    quantity = 1  # Если нет числа, то по умолчанию количество = 1

                # Увеличиваем счётчик для товара
                product_counts[normalized_product] = product_counts.get(normalized_product, 0) + quantity

# Обновляем базу данных
for product, quantity in product_counts.items():
    cursor.execute("""
        INSERT INTO products (product_name, quantity) VALUES (?, ?)
        ON CONFLICT(product_name) DO UPDATE SET quantity = quantity + excluded.quantity
    """, (product, quantity))

conn.commit()

# Сохраняем данные в xlsx
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "NER Output"
ws.append(["Product Name", "Quantity"])

for product, quantity in product_counts.items():
    ws.append([product, quantity])

wb.save(output_xlsx_file)
wb.close()
conn.close()

print(f"Данные успешно сохранены в файл {output_xlsx_file} и добавлены в базу данных.")
