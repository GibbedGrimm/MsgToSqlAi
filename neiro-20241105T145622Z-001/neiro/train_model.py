import numpy as np
from sklearn.model_selection import train_test_split
from model_definition import create_model
from data_preprocessing import preprocess_data

# Ваши данные (пример)
sentences = [["I", "live", "in", "New", "York"], ["She", "is", "from", "Paris"]]
tags = [["O", "O", "O", "B-LOC", "I-LOC"], ["O", "O", "O", "B-LOC"]]

# Словари и параметры
words = list(set([word for sentence in sentences for word in sentence])) + ["PAD"]
tags_set = list(set(tag for tag_seq in tags for tag in tag_seq))
word2idx = {w: i for i, w in enumerate(words)}
tag2idx = {t: i for i, t in enumerate(tags_set)}

# Предобработка
X, y = preprocess_data(sentences, tags, word2idx, tag2idx)

# Разделение на тренировочный и тестовый наборы
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

# Создание модели и обучение
model = create_model(len(words), len(tags_set))
history = model.fit(X_train, np.array(y_train), batch_size=32, epochs=5, validation_split=0.1)
