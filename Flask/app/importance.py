# Raj
# <-----Depreciated Files---->
from flask import Flask, jsonify, request
from util import *
from app import util
from flask import Blueprint, render_template, redirect
import sys
sys.path.append("..")
sys.path.insert(0, './app')
from app import util, import_libraries
from util import *
from import_libraries import *
vectorizer, Matrix, ans = params[0], params[1], params[2]

importance = Blueprint('importance', __name__)


def guess_by_sentences(question):
    answer = []
    question_sentence = ""
    temp_sentence_array = break_into_sentences(question)
    break_index = -1
    for i in range(len(temp_sentence_array)):
        question_sentence = question_sentence + " " + temp_sentence_array[i]
        temp_var = guess_top_5(question=[question_sentence])
        # print(temp_var)
        if (temp_var[0][1] > threshold_buzz):
            print("Ring buzzer on sentence number " + str(i+1))
            break_index = i+1
            question_sentence = question_sentence + "||[[BUZZER]]||"
            print("[[Question Start]]"+question_sentence)
            print("The guess is: " +
                  temp_var[0][0] + " with score: " + str(temp_var[0][1]) + "\n")
            break
    return temp_var


def guess_by_words(question):
    answer = []
    question_sentence = ""
    temp_word_array = break_into_words(question)
    break_index = -1
    temp_var = 1
    for i in range(len(temp_word_array)):
        question_sentence = question_sentence + " " + temp_word_array[i]
        if(((i+1) % 8 == 0) or (i+1) == len(temp_word_array)):
            temp_var = guess_top_5(question=[question_sentence])
            # print(temp_var)
            if (temp_var[0][1] > threshold_buzz):
                print("Ring buzzer on word number " + str(i+1))
                break_index = i+1
                question_sentence = question_sentence + "||[[BUZZER]]||"
                print("[[Question Start]]"+question_sentence)
                print("The guess is: " +
                      temp_var[0][0] + " with score: " + str(temp_var[0][1]) + "\n")
                break
    return temp_var


def get_actual_guess_with_index(question, max=12):
    answer = []
    repre = vectorizer.transform(question)
    matrix = Matrix.dot(repre.T).T
    indices = (-matrix).toarray().argsort(axis=1)[:, 0:max]
    for i in range(len(question)):
        idx = indices[i]
        answer.append([(ans[j], matrix[i, j]) for j in idx])
    return answer[0][0][0:], indices[0][0]


def check_drop_in_confidence(question, actual_confidence, max=50, ind=-1):
    answer = []
    repre = vectorizer.transform(question)
    matrix = Matrix.dot(repre.T).T
    indices = (-matrix).toarray().argsort(axis=1)[:, 0:max]
    if (not(question[0].strip())):
        return 0.0
    for i in range(len(question)):
        idx = indices[i]
        answer.append([(ans[j], matrix[i, j]) for j in idx])
        if(ind == idx[0]):
            return answer[0][i][1]
    return actual_confidence


def make_colored(score, text, max, min):
    colored_text = colored(int(255 * (1 - (score - min)/(max-min))),
                           255, int(255 * (1 - (score - min)/(max-min))), text)
    return colored_text


def get_importance_of_each_word(question):
    actual_answer, index_of_answer = get_actual_guess_with_index(question=[question])
    # print(actual_answer)
    actual_confidence = actual_answer[1]
    temp_sentence_array = break_into_words(question)
    highest_confidence = -10
    least_confidence = 10
    highest_confidence_word = ""
    array_of_importances = []
    for i in range(len(temp_sentence_array)):
        temp_sentence = temp_sentence_array[:i] + temp_sentence_array[i+1:]
        temp_sentence_string = ' '.join(temp_sentence)
        drop_in_confidence = check_drop_in_confidence(question=[temp_sentence_string], ind=index_of_answer, actual_confidence=actual_confidence)
        print("Importance of word " +
              temp_sentence_array[i] + "= ", actual_confidence-drop_in_confidence)
        array_of_importances.append(actual_confidence-drop_in_confidence)
        if(least_confidence > (actual_confidence-drop_in_confidence)):
            least_confidence = (actual_confidence-drop_in_confidence)
        if(highest_confidence < (actual_confidence-drop_in_confidence)):
            highest_confidence_word = temp_sentence_array[i]
            highest_confidence = (actual_confidence-drop_in_confidence)
    print("Word with the most importance: " + str(highest_confidence_word) + " "+str(highest_confidence))
    colored_string = " "
    for i in range(len(temp_sentence_array)):
        colored_string = colored_string + " " + \
            make_colored(
                array_of_importances[i], temp_sentence_array[i], highest_confidence, least_confidence)
    print(colored_string)
    print(colored(255, 255, 255, ""))
    return


def get_importance_of_each_sentence(question):
    actual_answer, index_of_answer = get_actual_guess_with_index(question=[question])
    actual_confidence = actual_answer[1]
    temp_sentence_array = break_into_sentences(question)
    highest_confidence = -10
    least_confidence = 10
    highest_confidence_sentence = -1
    array_of_importances = []
    for i in range(len(temp_sentence_array)):
        temp_sentence = temp_sentence_array[:i] + temp_sentence_array[i+1:]
        temp_sentence_string = ' '.join(temp_sentence)
        drop_in_confidence = check_drop_in_confidence(
            question=[temp_sentence_string], ind=index_of_answer, actual_confidence=actual_confidence)
        # 删掉这个句子以后的得分
        score = float(actual_confidence-drop_in_confidence)
        # print(actual_confidence, drop_in_confidence, score)
        array_of_importances.append(score)
        if(least_confidence > (score)):
            least_confidence = (score)
        if(highest_confidence < (score)):
            highest_confidence_sentence = i
            highest_confidence = (score)
    # colored_string = ""
    # for i in range(len(temp_sentence_array)):
    #     colored_string = colored_string + " " + make_colored(array_of_importances[i],temp_sentence_array[i], highest_confidence, least_confidence)
    most_important = []
    for i in range(len(array_of_importances)):
        a = break_into_words(temp_sentence_array[i])
        most_important.append(
            {"sentence": a[0] + " ... " + a[-1], "importance": array_of_importances[i]})
    return most_important
    # return temp_sentence_array[highest_confidence_sentence]


# Raj End -------------------

'''
Name: get_important_sentence_to_get_right_answer
Function: This module aims at finding the important sentence to get the right answer.
        It means that without this sentence, the tfidf guesser will get wrong answer.
Author: Cai
Input: question(str), answer(str)
Output: array_of_important_sentence(list)
'''
def get_important_sentence_to_get_right_answer(question, answer):
    temp_sentence_array = break_into_sentences(question)
    array_of_important_sentence = []
    for i in range(len(temp_sentence_array)):
        temp_sentence = temp_sentence_array[:i] + temp_sentence_array[i+1:]
        temp_sentence_string = ' '.join(temp_sentence)
        curr_answer, index_of_answer = get_actual_guess_with_index(question=[temp_sentence_string])
        print("The %d sentence" % i)
        print(curr_answer)
        if curr_answer[0] != answer:
            array_of_important_sentence.append(temp_sentence_array[i])
    return array_of_important_sentence

'''
Name: get_important_word_to_delay_the_buzzer
Function: This module aims at finding the important word to delay the buzzer.
        It means that without this word, the tfidf guesser will get the right answer after being input more words.
Author: Cai
Input: question(str), answer(str)
Output: array_of_important_word(list)
'''
def get_important_word_to_delay_the_buzzer(question, answer):
    temp_word_array = question.split(' ')
    array_of_important_word_to_delay_buzzer = []
    array_of_important_word_to_right_answer = []
    init_question_sentence, index_buzzer, init_rest_of_sentence, flag = buzz_Cai(
        question=question, answer=answer)
    if flag == False:
        return array_of_important_word_to_delay_buzzer, array_of_important_word_to_right_answer
    length = len(init_question_sentence)
    for i in range(int(index_buzzer)//2+1):
        if len(temp_word_array[i]) < 6:
            continue
        temp_sentence = temp_word_array[:i*2] + temp_word_array[i*2+2:]
        temp_sentence_string = ' '.join(temp_sentence)
        question_sentence, index_buzzer_nouse, rest_of_sentence, flag = buzz_Cai(
            question=temp_sentence_string, answer=answer)
        if flag == True and len(question_sentence) > length:
            array_of_important_word_to_delay_buzzer.append(temp_word_array[i*2]+' '+temp_word_array[i*2+1])
        elif flag == False and rest_of_sentence == "2":
            array_of_important_word_to_right_answer.append(temp_word_array[i])
        elif flag == False and rest_of_sentence == "1":
            array_of_important_word_to_right_answer.append(temp_word_array[i])
        else:
            pass
    return array_of_important_word_to_delay_buzzer, array_of_important_word_to_right_answer


def buzz_Cai(question, answer, min_index=0, threshold_buzz=0.3):
    temp_word_array = question.split(' ')
    # check if buzzer ever goes above threshold
    index_of_bin_search = len(temp_word_array)
    question_sentence = question
    temp_var = guess_top_n(question=[question_sentence], params=params, max=3, n=1)
    if(temp_var[0][1] < threshold_buzz and temp_var[0][0] == answer):
        return "", "1", False
    elif(temp_var[0][0] != answer):
        return "", "2", False
    else:
        pass
    max_index = index_of_bin_search - 1

    while max_index >= min_index:
        index_of_bin_search = (max_index+min_index)//2
        question_sentence = " ".join(temp_word_array[:index_of_bin_search])
        temp_var = guess_top_n(question=[question_sentence], params=params, max=1, n=1)
        if (temp_var[0][1] > threshold_buzz):
            max_index = index_of_bin_search-1
        else:
            min_index = index_of_bin_search+1
    rest_of_sentence = " ".join(temp_word_array[index_of_bin_search:])
    return question_sentence, index_of_bin_search, rest_of_sentence, True
