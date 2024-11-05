import os

# Укажите путь к папке с вашими файлами
folder_path = "C:\\Users\\andre\\Downloads\\fak"

# Имя для итогового файла
output_file = "forDataSet.txt"

# Открываем файл на запись
with open(output_file, "w", encoding="utf-8") as outfile:
    # Проходимся по всем файлам в указанной папке
    for filename in sorted(os.listdir(folder_path)):
        # Проверяем, что это текстовый файл
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as infile:
                # Читаем содержимое и добавляем в итоговый файл
                outfile.write(infile.read())
                # Добавляем разделитель между файлами, если нужно (например, пустую строку)
                outfile.write("\n\n")

print(f"Все файлы объединены в '{output_file}'")
