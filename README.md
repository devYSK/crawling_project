# crawling_project
## 1.	프로젝트 개요
 저는 주로 교보문고에서 IT 관련 도서를 E-Book이나 종이책으로 찾아보고 구매하는데,
제가 자주 이용하는 교보문고를 대화형으로 원하는 정보를 크롤링 하고 싶어 이 프로그램을 작성하였습니다.
자동화 및 편의성을 증가하기 위해  직접 인터넷에 들어가서 보는것이 아닌, 미리 만들어둔 프로그램으로 단순히콘솔
로 검색을 하여서 원하는 데이터들을 뽑을 수 있는 프로그램으로 만들었습니다.
책을 검색할 때 다양하게 리스트를 정해서 랭킹순대로 뽑고, 많이 팔리는 책들의 출판사가 무엇인지 빈도수 분석하여
분석한 데이터 기반으로 정제하여 출력하고, 책 제목에서 단어들이 빈도수가 얼마나 되는지 분석 하여 출력할 수 있
는 등의 다양한 방법으로 프로그램을 구현하였습니다.
 

### 1.1 사용한 모듈 및 라이브러리
  * 환경 : Windows10 Google Chrome Colab
  
  * 폰트 : NanumGothic.ttf

  * 라이브러리 : 
     - selenium,  
     - wordcloud,  
              * matplotlib.pylab,  
	      * pandas,  
	      * prettytable,  
	      * collections,  
	      * urllib.request,  
	      * os,  
	      * konlpy.tag,  
	      * re  

  colab환경 프로젝트 내 install한 라이브러리 및 모듈들 명령어
  ```
  # set up
	!apt update
	!pip install selenium
	!pip install matplotlib
	!pip install wordcloud
	!pip install pandas
	!apt install chromium-chromedriver
	!cp /usr/lib/chromium-browser/chromedriver /usr/bin
   
	# 한국어 형태소 추출 라이브러리용
	# 불용어 다운로드 및 전처리
	!wget --no-check-certificate "https://www.ranks.nl/stopwords/korean"

	!apt-get update
	!apt-get upgrade
	!apt-get install fonts-nanum*
	!apt-get install fontconfig
	!fc-cache -fv
	!cp /usr/share/fonts/truetype/nanum/Nanum /usr/local/Iib/python3.6/dist-packages/pytagcloud/fonts
	!rm -rf /content/.cache/pytagcloud/*

	!pip install konlpy
  !pip install pytagcloud pygame simplejson
  
  #!cp /usr/share/fonts/truetype/nanum/Nanum* /usr/local/lib/python3.6/dist-packages/pytagcloud/fonts
	!apt-get install fontconfig
	!fc-cache -fv
	!rm -rf /content/.cache/pytagcloud/* 
  ```

## 2. 모듈별 설계 내용

![image](https://user-images.githubusercontent.com/41531594/101987302-a000b180-3cd6-11eb-960c-d5d9ce39cd50.png)

![image](https://user-images.githubusercontent.com/41531594/101987309-a727bf80-3cd6-11eb-84fa-e52fb50706a9.png)

![image](https://user-images.githubusercontent.com/41531594/101987319-aee76400-3cd6-11eb-9299-449f7813a3ed.png)

## 3. 구현 단계별 제작내용 (이미지 캡쳐) 및 결과물 설명

![image](https://user-images.githubusercontent.com/41531594/101987373-143b5500-3cd7-11eb-8f88-a4a923140128.png)

![image](https://user-images.githubusercontent.com/41531594/101987378-1bfaf980-3cd7-11eb-9d69-aee15e6692a5.png)

![image](https://user-images.githubusercontent.com/41531594/101987384-274e2500-3cd7-11eb-85f4-9deaaa97b6ac.png)

![image](https://user-images.githubusercontent.com/41531594/101987406-3d5be580-3cd7-11eb-9d85-28befea1c48b.png)

![image](https://user-images.githubusercontent.com/41531594/101987413-451b8a00-3cd7-11eb-8e07-4ef8c7ee072e.png)

![image](https://user-images.githubusercontent.com/41531594/101987421-4ea4f200-3cd7-11eb-9942-53c9a7b00937.png)

![image](https://user-images.githubusercontent.com/41531594/101987424-56fd2d00-3cd7-11eb-9945-af5d54b27c62.png)

![image](https://user-images.githubusercontent.com/41531594/101987433-68463980-3cd7-11eb-9887-4c23b8ce9ce6.png)

