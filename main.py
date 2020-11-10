# -*- coding: utf-8 -*-

# pip install selenium
# download geckodriver (https://github.com/mozilla/geckodriver/releases)

from selenium import webdriver
import time
import random
import json


def database_adjustment(database):
    for q in range(len(database)):
        if database[q]['TrueFlag'] == 1:
            database[q]['IndexesIncorect'].clear()
            database[q]['Answers'].clear()
        elif len(database[q]['IndexesIncorect']) == 3:
            indexes = [0, 1, 2, 3]
            for k in range(3):
                indexes.remove(database[q]['IndexesIncorect'][k])
            ind = indexes[0]
            database[q]['TrueFlag'] = 1
            database[q]['TrueAnswer'] = database[q]['Answers'][ind]
            database[q]['IndexesIncorect'].clear()
            database[q]['Answers'].clear()

"""
    QUESTION - Current Question[k] from DataBase
    CurrentAnswers - Answers from Current Question in GameRound
HelpFunction for QuestionCoincide(*, *)
"""


def HelpFunction1(QUESTION, current_answers, i):
    for j in range(0, 4):
        if QUESTION['Answers'][i] == current_answers[j].text:
            current_answers[j].click()
            try:
                if browser.find_element_by_css_selector("div[class='game__answer selected right']"):
                    QUESTION['TrueFlag'] = 1
                    QUESTION['TrueAnswer'] = current_answers[j].text
                    QUESTION['Answers'].clear()
                    QUESTION['IndexesIncorect'].clear()
                    break
            except:
                QUESTION['IndexesIncorect'].append(i)
"""
    QUESTION - Current Question[k] from DataBase
    CurrentAnswers - Answers from Current Question in GameRound
When the desired question is found in Database
Function to process the selected answer and correct the question in the database
"""
def QuestionCoincide(QUESTION, current_answers):
    if QUESTION['TrueFlag'] == 1:
        for j in range(4):
            if QUESTION['TrueAnswer'] == current_answers[j].text:
                current_answers[j].click()
    else:
        if len(QUESTION['IndexesIncorect']) == 0:
            i = random.randint(0, 3)
            HelpFunction1(QUESTION, current_answers, i)
        else:
            indexes = [0, 1, 2, 3]
            for k in range(len(QUESTION['IndexesIncorect'])):
                indexes.remove(QUESTION['IndexesIncorect'][k])
            i = random.choice(indexes)
            HelpFunction1(QUESTION, current_answers, i)


def ADD_Question(QUESTIONS, Question, current_answers):
    k = random.randint(0, 3)
    current_answers[k].click()
    IndIncorrect = []
    try:
        if browser.find_element_by_css_selector("div[class='game__answer selected right']"):
            truef = 1
            TrueAnswer = current_answers[k].text
            IndIncorrect.clear()
    except:
        truef = 0
        TrueAnswer = ""
        IndIncorrect.append(k)
    Quiz = {
        "Question": Question,
        "TrueFlag": truef,
        "TrueAnswer": TrueAnswer,
        "IndexesIncorect": IndIncorrect,
        "Answers": [current_answers[0].text, current_answers[1].text, current_answers[2].text, current_answers[3].text]
    }
    QUESTIONS.append(Quiz)
"""
    QUESTIONS - Question DataBase from file
    Question - Question from Current GameRound
    CurrentAnswers - Answers from Current Question in GameRound
Function to find a question in the QUESTION Base
If the Question is missing from the database, it is added to the database
"""
def QualitativeQuestion(QUESTIONS, Question, current_answers):
    flag = 0
    if len(QUESTIONS) != 0:
        for i in range(len(QUESTIONS)):
            if QUESTIONS[i]['Question'] == Question:
                flag = 1
                QuestionCoincide(QUESTIONS[i], current_answers)
                break
            else:
                continue
    else:
        ADD_Question(QUESTIONS, Question, current_answers)
    if flag == 0:
        ADD_Question(QUESTIONS, Question, current_answers)


def waiting():
    while 1:
        if browser.find_elements_by_class_name('game__answer'):
            break


IP_BaA = "IP_BasicsAndAddressing.json"


def save_questions():
    with open(IP_BaA, "w", encoding="utf-8") as fi:
        json.dump(QUESTIONS_database, fi, indent=2, ensure_ascii=False)


try:
    QUESTIONS_database = json.load(open(IP_BaA, encoding='utf-8'))
except:
    QUESTIONS_database = []

database_adjustment(QUESTIONS_database)
save_questions()
# get a token
TOKEN = 'https://quiz.honorcup.ru/app/?id=45815&sign=45bf30ca51861aff2af95aa6ecb42e5b'

# open a browser (Firefox)
browser = webdriver.Firefox(executable_path='geckodriver.exe')
browser.get(TOKEN)
time.sleep(2)

# #click battle_button
battle_button = browser.find_element_by_class_name('about__buttons')
battle_button.click()
time.sleep(2)

# #choose a category and theme
category = browser.find_elements_by_class_name('slider__item')
category[1].click()
time.sleep(2)
theme = browser.find_elements_by_class_name('profile__theme')
theme[0].click()
time.sleep(2)

# button Play
# Theme 0:
# categories_play_button = browser.find_element_by_xpath('/html/body/app/div[1]/nomination/div/div/div[2]/div[3]/div[0]/div/div/div[2]/div')#('button-group-2x')
# Theme 1:
categories_play_button = browser.find_element_by_xpath('/html/body/app/div[1]/nomination/div/div/div[2]/div[3]/div[1]/div/div/div[2]/div')#('button-group-2x')
# Theme 2:
# categories_play_button = browser.find_element_by_xpath('/html/body/app/div[1]/nomination/div/div/div[2]/div[3]/div[2]/div/div/div[2]/div')#('button-group-2x')
# Theme 3:
# categories_play_button = browser.find_element_by_xpath('/html/body/app/div[1]/nomination/div/div/div[2]/div[3]/div[3]/div/div/div[2]/div')#('button-group-2x')

categories_play_button.click()
countGame = 0
while 1:
    waiting()
    for i in range(5):
        round_question = browser.find_element_by_class_name('game__question-text')
        round_answers = browser.find_elements_by_class_name('game__answer')
        QualitativeQuestion(QUESTIONS_database, round_question.text, round_answers)
        while browser.find_elements_by_class_name('game__answer'):
            continue
        time.sleep(5)
    countGame += 1
    save_questions()
    if countGame % 5 == 0:
        database_adjustment(QUESTIONS_database)
        save_questions()
    if countGame % 20 == 0:
        break
    restart = browser.find_element_by_xpath('/html/body/app/div[1]/result/div/div/div[9]/div[1]')
    restart.click()

save_questions()
browser.close()
