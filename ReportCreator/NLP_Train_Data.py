import pandas as pd
from bs4 import BeautifulSoup
import re
import nltk  # pip install nltk
import urllib.parse
from pymongo import MongoClient
import os

df = pd.read_csv("sof_ml.csv")
df['up_vote_count'] = df['favorite_count']


df['t-body'] = '<p>' + df['title'] + '</p>' + df['body']
df = df.dropna(subset=['tags'])  # tags가 nan인 데이터는 삭제.

# 카테고리 분류 키워드
a = "python java javascript c# python-3.x typescript php dart c++ kotlin go c rust scala ruby js cpp"
b  = "reactjs angular vue.js html css react-hooks webpack next.js material-ui jestjs api jquery axios blazor angular-material unit-testing vuetify.js authentication graphql nuxt.js vuejs2 redux rest react-navigation react-redux bootstrap-4 angular8 react-router angular9 websocket cookies async-await gatsby antd sass create-react-app xml json"
c = "android flutter react-native ios swift json ionic-framework expo authentication flutter-layout rest react-navigation xamarin.forms react-native-android xamarin flutter-dependencies swiftui vue react nuxtjs nextjs angular bootstrap"
d = "node.js spring-boot laravel spring django json npm jestjs express api discord.js gradle .net blazor flask unit-testing maven nestjs authentication graphql rest ruby-on-rails jwt hibernate cors async-await swagger typeorm jwt"
e = "docker amazon-web-services firebase kubernetes azure linux docker-compose azure-devops google-cloud-firestore nginx google-cloud-platform aws-lambda amazon-s3 terraform jenkins dockerfile azure-pipelines ansible azure-active-directory kubernetes-helm firebase-authentication google-cloud-functions azure-functions amazon-ec2 firebase-cloud-messaging heroku github-actions s3 ec2 aws"
f = "tensorflow pandas keras pytorch mongodb opencv selenium machine-learning apache-spark apache-kafka numpy matplotlib dataframe deep-learning pyspark anaconda scikit-learn google-colaboratory plotly selenium-webdriver powerbi tensorflow2.0 web-scraping image-processing airflow conda"
g = "mysql postgresql sql sql-server oracle elasticsearch database redis"
h = "visual-studio-code android-studio xcode visual-studio jupyter-notebook intellij-idea eslint visual-studio-2019 vscode intellij"
i = "linux macos windows ubuntu powershell bash windows-subsystem-for-linux"
j = "discord git github discord.js discord.py google-sheets discord.py-rewrite"

a = a.split(" ")
b = b.split(" ")
c = c.split(" ")
d = d.split(" ")
e = e.split(" ")
f = f.split(" ")
g = g.split(" ")
h = h.split(" ")
i = i.split(" ")
j = j.split(" ")

dict = {}  # category 점수화 할 딕셔너리
for word in a:
    dict[word] = 0
for word in b:
    dict[word] = 1
for word in c:
    dict[word] = 2
for word in d:
    dict[word] = 3
for word in e:
    dict[word] = 4
for word in f:
    dict[word] = 5
for word in g:
    dict[word] = 6
for word in h:
    dict[word] = 7
for word in i:
    dict[word] = 8
for word in j:
    dict[word] = 9


result = [] # 결과를 담을 배열
for row_index, row in df.iterrows():  # 15만개
    categoryCnt = [0,0,0,0,0,0,0,0,0,0,0] # 카테고리 점수화 할 배열
    soup = BeautifulSoup(row["t-body"], 'html.parser')
    tags = BeautifulSoup(row["tags"], 'html.parser')
    view_count_row = row["view_count"]
    tags = str(tags).lower().split("|")
    # p태그만 가져오기
    a = str(soup.find_all("p"))
    # print(a)
    # code 태그 지우기
    while a.find('<code>') >= 0:
        a = a.replace(a[a.find('<code>'):a.find('</code>')+7], '')
# regular expression을 이용하여 태그 다 지우기.
    a = re.sub('<.+?>', '', a, 0).strip()
# 특수문자 제거 re.sub('패턴', 교체함수, '문자열', 바꿀횟수)
# ex) html/css/javascript 를 htmlcssjavascript로 분리하길래 '' -> ' '로 바꿈(공백 추가)
    a = re.sub('[=\\\\,/\?:^$@*\"※~&;%ㆍ!』\\‘|\(\)\[\]\<\>`\…》0-9]', ' ', a)
    tokens = nltk.word_tokenize(a)

    tmp = []
    # nltk.download('punkt') 를 실행하여 Punket Tokenizer Models (13MB) 를 다운로드 해줍니다.
    # 품사 태깅을 하려면 먼저 nltk.download('averaged_perceptron_tagger') 로 태깅에 필요한 자원을 다운로드 해줍니다.
    tagged = nltk.pos_tag(tokens)
    for tag in tagged:
        if tag[1] == 'NN' or tag[1] == 'NNP':
            tmp.append(tag[0])
            
    # category 점수계산
    for word in tags:
        num = num = dict.get(word.lower(),10)
        if num == 10:
            continue
        categoryCnt[num] += 1
    
    for word in tmp:
        num = num = dict.get(word.lower(),10)
        if num == 10:
            continue
        categoryCnt[num] += 1
        
    # 분류된 단어들이(tags, tmp) 카테고리화 할 단어(dict에 들어있는 단어)와 연관성이 전혀 없을 때 -> 포함 안 시킴
    if max(categoryCnt) == 0:
        continue
    
    result.append({'contentId': row["id"], 'words': tmp+tags, 'tags': tags, 'view_count': view_count_row,
                   'up_vote_count': row['up_vote_count'], 'title': row["title"], 'creation_date': row['creation_date'], 'category': categoryCnt.index(max(categoryCnt))})


#  mongoDB config
host = os.environ['DB_HOST']
port = os.environ['DB_PORT']
user_name = os.environ['DB_USERNAMAE']
pass_word = os.environ['DB_PASSWORD']

db_name = os.environ['DB_NAME']  # database name to authenticate

# if you are password has '@' then you might need to escape hence we are using "urllib.parse.quote_plus()"
client = MongoClient(
    f"mongodb://{user_name}:{urllib.parse.quote_plus(pass_word)}@{host}:{port}/{db_name}"
)

# db
db = client[db_name]
# 컬렉션
collection = db["train"]
collection.insert_many(result)