import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

def preprocess_data(sentences, tags, word2idx, tag2idx, maxlen=50):
    X = [[word2idx.get(w, word2idx["PAD"]) for w in s] for s in sentences]
    y = [[tag2idx[t] for t in ts] for ts in tags]
    X = pad_sequences(X, maxlen=maxlen, padding="post")
    y = pad_sequences(y, maxlen=maxlen, padding="post")
    y = [to_categorical(i, num_classes=len(tag2idx)) for i in y]
    return X, y
