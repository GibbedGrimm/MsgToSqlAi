import os
import json

# Определяем путь к файлу относительно расположения скрипта
file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'traindata.json')

# Загружаем данные из JSON
with open(file_path, "r", encoding="utf-8") as f:
    json_data = json.load(f)

# Конвертируем данные в необходимый формат
converted_data = []
for item in json_data["annotations"]:
    text, annotation = item
    entities = annotation["entities"]
    converted_data.append((text, entities))

# Сохраняем результат в training_data.txt
with open("training_data.txt", "w", encoding="utf-8") as f:
    for entry in converted_data:
        f.write(f"{entry}\n")
