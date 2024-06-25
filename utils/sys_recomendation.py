import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_distances


class SysRecommendation:
    def __init__(self, dataframe, content_col):
        self.df = dataframe
        self.content_col = content_col

    def fit(self):
        content_data = self.df[
            self.content_col
        ].tolist()  # Mengambil teks konten dari kolom
        self.encoder = CountVectorizer(
            stop_words="english", tokenizer=word_tokenize, token_pattern=None
        )
        self.bank = self.encoder.fit_transform(content_data)

    def predict(self, idx, topf=5):
        content = self.df.loc[idx, self.content_col]
        code = self.encoder.transform([content])
        dist = cosine_distances(code, self.bank)
        rec_idx = dist.argsort()[0, 1 : (topf + 1)]
        return self.df.loc[rec_idx]
