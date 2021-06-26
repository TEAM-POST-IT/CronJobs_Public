# CronJobs_Public

### CronJobs 공개용 레포지토리

* Python, Github Actions
* Youtube, Blog, Stack Overflow 크롤링 및 Classification 작업



### .git/workflows ( Github Actions )

1. SOF_Crawl.yml : Stack Overflow 크롤링, 형태소 분석해 명사 추출 후 DB 저장 , 매일 오전 1시 (KST)
2. create_report.yml : 추출된 명사들을 기반으로 각 명사들 간 연관관계 분석 결과 리포트 생성, 매주 월요일 1시 30분 (KST)
3. youtube_blog_crawling.yml : IT 기업 또는 유명 인사들의 유튜브와 블로그 크롤링, 매일 오전 1시 (KST)

### Crawler ( Stack Overflow, Youtube, Blog Crawler )

1. SOF_Crawler_NLP.py
2. tech_blog_crawler.py
3. youtube_crawler.py

### Report Creator

1. Classification_Model.py : 분류 모델 생성 코드
   * NLP_Train_Data.py를 통해 생성한 Train Data 이용 ( ex, 빅데이터, 클라우드, 머신러닝, 웹, 모바일 등 )
   * 모든 글들을 TF-IDF를 이용해 벡터화
   * 벡터화된 수치들과 지정해둔 카테고리를 다항 로지스틱 회귀로 Trian, 모델 생성 및 추출
2. Learned_model, tfidf_vectorizer.p
   * 추출된 분류 모델과 TF-IDF 수치
3. NLP_Train_Data.py : 분류모델 Train Data 생성 코드
   * Stack Overflow 파싱
   * 슬래쉬, 점 등 특수문자 제거 및 명사 추출
   * 추출된 명사와 미리 카테고리화한 키워드들을 대조해 해당 글의 카테고리 지정
4. Create_Report.py : 보고서 생성


<br/>
<br/>

모델 선정 기준 및 더 자세한 정보는 [POST-IT Notion](https://www.notion.so/POST-IT-156636b1c0ec4d8fabeeb4fd1470fb6a) 를 방문해주세요!
