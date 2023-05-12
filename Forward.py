from keras.layers import Dense, SimpleRNN, Input
from keras.models import Sequential
from keras.preprocessing.text import Tokenizer
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np


class LieGPT:
    def __init__(self, text):

        self.text = text
        self.num_chars = 34
        # Создаём токен
        self.tokenizer = Tokenizer(num_words=34, char_level=True)

        # Задаём значение каждому символу
        self.tokenizer.fit_on_texts([text])
        print(self.tokenizer.word_index)

        # Генерируем матрицы
        self.inp_chars = 6
        self.data = self.tokenizer.texts_to_matrix(self.text)

        self.n = self.data.shape[0] - self.inp_chars

        self.X = np.array([self.data[i:i + self.inp_chars, :] for i in range(self.n)])
        self.Y = self.data[self.inp_chars:]  # предсказание следующего символа

    def gen_model(self):
        print(self.data.shape)

        self.model = Sequential()
        self.model.add(Input((self.inp_chars,
                         self.num_chars)))  # при тренировке в рекуррентные модели keras подается сразу вся последовательность, поэтому в input теперь два числа. 1-длина последовательности, 2-размер OHE
        self.model.add(SimpleRNN(128, activation='tanh'))  # рекуррентный слой на 500 нейронов
        self.model.add(Dense(self.num_chars, activation='softmax'))
        self.model.summary()

        self.model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')

        self.history = self.model.fit(self.X, self.Y, batch_size=32, epochs=100)

    def buildPhrase(self, inp_str, str_len=50):
        for i in range(str_len):
            x = []
            for j in range(i, i + self.inp_chars):
                x.append(self.tokenizer.texts_to_matrix(inp_str[j]))  # преобразуем символы в One-Hot-encoding

            x = np.array(x)
            inp = x.reshape(1, self.inp_chars, self.num_chars)

            pred = self.model.predict(inp)  # предсказываем OHE четвертого символа
            d = self.tokenizer.index_word[pred.argmax(axis=1)[0]]  # получаем ответ в символьном представлении

            inp_str += d  # дописываем строку

        return inp_str


b = ''

with open("a.txt", "r", encoding="utf-8") as file:
    b = file.read()
a = LieGPT(b)
a.gen_model()

print(a.buildPhrase("думайт"))


