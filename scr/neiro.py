import spacy
import re
import openpyxl
import os

# Загрузите модель для русского языка, например, 'ru_core_news_sm'
nlp_ru = spacy.load(os.path.join(os.path.dirname(__file__), '..', 'models', 'model-best'))

f = open(os.path.join(os.path.dirname(__file__), '..', 'forUse', 'for_model.txt'), encoding="utf-8")
output_xlsx_file = os.path.join(os.path.dirname(__file__), '..', 'forUse', 'output_data.xlsx'), encoding="utf-8"


# Функция для извлечения сущностей заданного типа из документа
def extract_entities(doc, entity_type):
    return [ent.text for ent in doc.ents if ent.label_ == entity_type]


# Получаем список уникальных типов сущностей из модели
entity_types = nlp_ru.pipe_labels["ner"]

# Создаем workbook и worksheet для xlsx файла
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "NER Output"

# Записываем заголовок колонок
ws.append(["Input Text"] + entity_types)

for input in f:
    line = input.strip()
    doc_ru = nlp_ru(line)
    row_data = [line]

    # Извлекаем сущности для каждого типа и удаляем недопустимые компании
    for entity_type in entity_types:
        entities = extract_entities(doc_ru, entity_type)

        # Добавляем сущности в соответствующую колонку по их классу
        row_data.append(", ".join(list(set(entities))))

    # Записываем строку в xlsx файл
    ws.append(row_data)

# Закрываем вводной файл
f.close()

# Сохраняем и закрываем рабочую книгу
wb.save(output_xlsx_file)
wb.close()

print(f"Данные успешно сохранены в файл {output_xlsx_file}")