from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from wordcloud import WordCloud
from matplotlib.pylab import plt
import pandas as pd
from prettytable import PrettyTable
from collections import Counter
from urllib.request import urlretrieve
import os

from konlpy.tag import Okt
import re

class Book:

    def __init__(self, book_name=None, author=None, publisher=None, org_price=None, sell_price=None, buy_link=None,
                 review_point=None, book_image_url=None):
        self.__book_name = book_name  # 책 이름
        self.__author = author  # 저자
        self.__publisher = publisher  # 출판사
        self.__org_price = org_price  # 원래 가격
        self.__sell_price = sell_price  # 할인 가격
        self.__buy_link = buy_link  # 구매 링크
        self.__review_point = review_point  # 리뷰 점수
        self.__book_image_url = book_image_url  # 북 이미지 url

    @property
    def book_name(self):
        return self.__book_name 

    @book_name.setter
    def book_name(self, value):
        self.__book_name = value

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, value):
        self.__author = value

    @property
    def publisher(self):
        return self.__publisher

    @publisher.setter
    def publisher(self, value):
        self.__publisher = value

    @property
    def org_price(self):
        return self.__org_price

    @org_price.setter
    def org_price(self, value):
        self.__org_price = value

    @property
    def sell_price(self):
        return self.__sell_price

    @sell_price.setter
    def sell_price(self, value):
        self.__sell_price = value

    @property
    def buy_link(self):
        return self.__buy_link

    @buy_link.setter
    def buy_link(self, value):
        self.__buy_link = value

    @property
    def review_point(self):
        return self.__review_point

    @review_point.setter
    def review_point(self, value):
        self.__review_point = value

    @property
    def book_image_url(self):
        return self.__book_image_url

    @book_image_url.setter
    def book_image_url(self, value):
        self.__book_image_url = value

    def __str__(self):
        return " %-4s : %-20s\n %-5s : %-10s\n %-5s : %-10s\n %-5s : %-10s\n %-4s : %-10s\n %-4s : %s\n %-12s : %s\n " \
               % ("책이름", self.book_name,
                  "저자", self.author,
                  "출판사", self.publisher,
                  "가격", self.org_price,
                  "리뷰점수", self.review_point,
                  "구매링크", self.buy_link,
                  "책 이미지 url", self.book_image_url) + ("----" * 30)


class BookManager:

    def __init__(self):
        self.count = 0  # 책 권 수
        self.books = []  # 책 리스트

    def print_list(self):  # 책 내용 프린팅
        for book in self.books:
            print(book)

    def add_book(self, book):  # 멤버 변수 books에 추가
        self.books.append(book)
        self.count += 1

    def init_list(self):  # 리스트와 책 수를 초기화
        self.count = 0
        self.books = []

    def show_word_cloud(self):
        text = []

        for book in self.books:
            text.append(book.publisher.strip())

        publisher_dic = dict(Counter(text).most_common())

        new_publisher_dic = {}

        for key in publisher_dic.keys():  # 딕셔너리 key 값 수정
            new_publisher_dic[str(publisher_dic[key]) + " 권 " + key] = publisher_dic[key]

        for element in new_publisher_dic:
            print(element)

        print("\n")

        word_s = WordCloud(width=500, height=500,
                           font_path="/usr/share/fonts/truetype/nanum/NanumGothic.ttf").generate_from_frequencies(
            new_publisher_dic)

        plt.figure(figsize=(8, 8))
        plt.imshow(word_s)
        plt.show()

    def show_data_frame(self):

        dataset = {"책이름": [book.book_name for book in self.books],
                   "저자": [book.author for book in self.books],
                   "출판사": [book.publisher for book in self.books],
                   "원가격": [book.org_price for book in self.books],
                   "할인가격": [book.sell_price for book in self.books],
                   "구매링크": [book.buy_link for book in self.books]}

        df = pd.DataFrame(dataset)

        df_table_print(df)
        save_csv_ask = input("주어진 DataFrame을 csv 파일로 저장하시겠습니까? 1. 예 2. 아니요\n>>>> ")

        if int(save_csv_ask) == 1:
            print("현재 작업 디렉토리에 data.csv 파일로 저장하였습니다. ")
            df.to_csv("data.csv", encoding="utf-8")  # data.csv로 데이터 저장

    def save_image(self):

        image_dir = "이미지저장폴더"

        if not (os.path.isdir(image_dir)):
            os.makedirs(image_dir)

        for book in self.books:
            url = book.book_image_url

            if '/' in book.book_name:  # 책 이름에 "/" 가 들어있는 경우 리플레이스
                book.book_name = book.book_name.replace("/", " ")

            print(book.book_image_url)
            urlretrieve(book.book_image_url, image_dir + "/" + book.book_name + ".jpg")

    def title_analysis_wordcloud_print(self):

        with open("/content/korean", encoding="utf-8") as f:
            text = f.read()
            stopwords = text_cleaning(text)

        pos_tagger = Okt()
        title_text = ""

        for book in self.books:
            title_text += book.book_name

        title = pos_tagger.nouns(title_text)

        word_title_text = [x for x in title if len(x) > 1 and x not in stopwords]

        title_dic = dict(Counter(word_title_text).most_common())

        word_s = WordCloud(width=500, height=500,
                           font_path="/usr/share/fonts/truetype/nanum/NanumGothic.ttf").generate_from_frequencies(
            title_dic)

        plt.figure(figsize=(12, 12))
        plt.imshow(word_s)
        plt.show()

    def searching(self, book_name, select):  # 사용자가 선택한 책 이름과 메뉴 넘버
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        browser = webdriver.Chrome('chromedriver', chrome_options=chrome_options)
        select = int(select) - 1  # 교보문고 url search 쿼리에서 0부터 설정하였기 때문에 -1 해주었습니다.

        # url 재조립
        url = "https://search.kyobobook.co.kr/web/search?vPstrKeyWord=" \
              + book_name + "&vPstrTab=PRODUCT&searchPcondition=1&searchOrder=" \
              + str(select) + "&currentPage=1&orderClick=LAG"

        browser.get(url)

        tag_names = browser.find_element_by_class_name("type_list").find_elements_by_tag_name("tr")

        for tag in tag_names:
            book = Book()
            book.book_name = tag.find_element_by_class_name("title").find_element_by_tag_name("strong").text  # title
            book.author = tag.find_element_by_class_name("author").find_element_by_tag_name("a").text  # author
            author_attrs_text = tag.find_element_by_class_name("author").text.split("|")  # 출판사를 뽑기위한 텍스트
            book.book_image_url = tag.find_element_by_class_name("cover").find_element_by_tag_name("img").get_attribute(
                "src")

            # 출판사명을 뽑아내기 위한 루프
            for i in range(1, len(author_attrs_text)):
                if "옮김" in author_attrs_text[i]:
                    book.publisher = author_attrs_text[i + 1].strip()
                    break
                else:
                    book.publisher = author_attrs_text[i].strip()
                    break

            try:  # org_price 클래스에 간혹 데이터가 없는 경우가 있어 예외처리 하였습니다
                book.org_price = tag.find_element_by_class_name("price").find_element_by_class_name(
                    "org_price").text  # org_price

            except NoSuchElementException:
                print("\n" + str(self.count + 1) + " 번째 org.price 클래스가 없으므로 '정보 없음'으로 대체\n")
                book.org_price = '정보 없음'

            book.sell_price = tag.find_element_by_class_name("price").find_element_by_class_name(
                "sell_price").text  # sell_price
            book.buy_link = tag.find_element_by_class_name("title").find_element_by_tag_name("a").get_attribute(
                "href")  # buy_link

            book.review_point = float(
                tag.find_element_by_class_name("info").find_element_by_tag_name("b").text)  # 혹시모를 정렬을 대비하여 플로팅 하였습니다

            self.add_book(book)

            if self.count > 20:  # 책을 10권까지만 받기
                break

        browser.close()


def text_cleaning(text):  # 텍스트 전처리용 함수
    result = re.sub('[^ ㄱ-ㅎ | 가-힣]+', ' ', text)
    return result


def df_table_print(df):  # prettytable을 이용하여  보기 좋게 데이터셋 출력해주는 함수

    if isinstance(df, pd.core.frame.DataFrame):
        # print(df.shape)
        print("\n" + "데이터 프레임 출력" + ("---" * 30) + "\n")
        table = PrettyTable(['순위'] + list(df.columns))

        for row in df.itertuples():
            table.add_row(row)

        print(str(table))

    else:
        print(df)

    print("\n")


def run():

    select_list = ["인기순", "판매량", "신상품", "할인율", "낮은가격", "높은가격", "상품명", "북로그 리뷰", "리뷰 수"]

    select_print_list = ["콘솔로 프린트", "많이 판매되는  출판사들의 빈도수대로 wordcloud 출력",
                         "데이터 셋을 정제하여 데이터 프레임 방식으로 출력"]

    manager = BookManager()

    while True:

        ask1 = """
책을 어떤 방식으로 조회하시겠습니까? 

1. 인기순     2. 판매량   3. 신상품       4. 할인율  5. 낮은가격  

6. 높은가격   7. 상품명   8. 북로그 리뷰  9. 리뷰수  10. 종료

>>>   """
        ask2 = "\n검색할 책 키워드는? : "

        select = input(ask1)

        if not select.isdigit():  # 숫자가 아닐 경우 재입력
            print("숫자만 입력하세요")
            continue

        if int(select) == 10:  # 종료 번호 입력시 break
            print("종료합니다.")
            break

        book_name = input(ask2).strip()  # 양쪽 공백 제거

        print("접속중------------------------------------------------------------------------------\n")
        manager.searching(book_name, select)  # 크롤링 시작

        # 책 조회 완료 ----

        ask3 = """
조회한 결과를 어떤 방식으로 출력 하시겠습니까?

  1. 콘솔로 프린트  2. 많이 판매되는 출판사들의 빈도수대로 wordcloud 출력        3. 데이터 셋을 정제하여 데이터 프레임 방식으로 출력

  4. 이미지 저장    5. 책 제목들로 명사 형태소 추출, 분석하여 wordcloud 출력     6. 다시 검색하기  7. 종료

        """

        while True:
            select_print_num = input(ask3)

            if not select_print_num.isdigit():  # 숫자가 아닐 경우 재입력
                print("숫자만 입력하세요")
                continue

            select_print_num = int(select_print_num)  # 정수형으로 형변환

            if select_print_num == 7:  # 프로그램 종료
                import sys
                sys.exit()

            elif select_print_num == 6:  # 검색 번호 입력시 break 하고 재검색
                print("다시 책을 검색 합니다.")
                manager.init_list()
                break

            elif select_print_num == 5:
                print("책 제목들로 명사 형태소 추출, 분석하여 wordcloud 출력합니다 ")
                manager.title_analysis_wordcloud_print()

            elif select_print_num == 4:
                print("이미지를 현재 폴더 밑 이미지저장폴더에 저장합니다 ")
                manager.save_image()

            else:

                print("출력결과-----------------------------------\n")
                print(book_name + " 을(를) " + select_list[int(select) - 1] + " 으로 " + select_print_list[
                    select_print_num - 1] + "한 결과입니다 \n")

                if select_print_num == 1:
                    manager.print_list()

                elif select_print_num == 2:
                    manager.show_word_cloud()

                elif select_print_num == 3:
                    manager.show_data_frame()

                else:
                    print("목록에 맞게 번호를 입력해 주세요 ")


# 실행 함수
run()
