import tensorflow as tf
from tensorflow.keras.layers import LSTM, Embedding, Dense, TimeDistributed, Dropout, Bidirectional, Input
from tensorflow.keras.models import Model
from tensorflow_addons.layers import CRF

def create_model(n_words, n_tags, maxlen=50):
    input = Input(shape=(maxlen,))
    model = Embedding(input_dim=n_words, output_dim=50, input_length=maxlen)(input)
    model = Dropout(0.1)(model)
    model = Bidirectional(LSTM(units=100, return_sequences=True, recurrent_dropout=0.1))(model)
    model = TimeDistributed(Dense(100, activation="relu"))(model)
    crf = CRF(n_tags)
    out = crf(model)
    model = Model(input, out)
    model.compile(optimizer="adam", loss=crf.loss, metrics=[crf.accuracy])
    return model
