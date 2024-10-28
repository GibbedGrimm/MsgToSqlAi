import json

# Исходный JSON
data = open(input('Введите путь до JSON файла: ')).read()

# Загружаем данные из JSON
json_data = json.loads(data)

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