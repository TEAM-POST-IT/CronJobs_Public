"""
    Author : HanJaehee
    date : 2021/4/1
"""
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle
import joblib
from pymongo import MongoClient
import urllib.parse
import os

# mongodb info
host = os.environ['DB_HOST']
port = os.environ['DB_PORT']
user_name = os.environ['DB_USERNAMAE']
pass_word = os.environ['DB_PASSWORD']

db_name = os.environ['DB_NAME'] # database name to authenticate

# if you are password has '@' then you might need to escape hence we are using "urllib.parse.quote_plus()"
client = MongoClient(
    f"mongodb://{user_name}:{urllib.parse.quote_plus(pass_word)}@{host}:{port}/{db_name}"
)

# db
db = client[db_name]
# 컬렉션
collection = db["train"]

result = []
for x in collection.find():
    result.append(x)

data_x = []
data_y = []

for row in result:
    data_x.append(" ".join(set(row["words"])))
    data_y.append(row["category"])

# Split case
train_x, test_x, train_y, test_y = train_test_split(data_x, data_y, test_size=0.2)

# TF-IDF
tv = TfidfVectorizer(
    ngram_range=(1, 2), max_features=50000, sublinear_tf=True, min_df=1
).fit(train_x)

## TfidfVectorizer save
pickle.dump(tv, open("tfidf_vectorizer.p", "wb"))

## transform data
tv_train_x = tv.transform(train_x)
tv_test_x = tv.transform(test_x)

# fit model
# 다항 로지스틱 회귀 , multi_class = multinomial 고정
# C : Train Strenth -> 클수록 규제(regularization)가 약하대요

model = LogisticRegression(multi_class="multinomial", C=100000, solver="newton-cg").fit(
    tv_train_x, train_y
)

joblib.dump(model, "Learned_model")
