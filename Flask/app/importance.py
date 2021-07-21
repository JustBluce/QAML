# Raj
# <<<-------DEPRECIATED FILE-------->>>
# Description of this file: 
# 1. Contains functions for calculating the importance of words and sentences

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
        question_sentence = question_sentence + " " +temp_sentence_array[i] 
        temp_var = guess_top_5(question = [question_sentence])
        # print(temp_var)
        if (temp_var[0][1]>threshold_buzz):
            print("Ring buzzer on sentence number " + str(i+1))
            break_index = i+1
            question_sentence = question_sentence + "||[[BUZZER]]||"
            print("[[Question Start]]"+question_sentence)
            print("The guess is: " + temp_var[0][0] + " with score: " + str(temp_var[0][1]) + "\n")
            break
    return temp_var

def guess_by_words(question):
    answer = []
    question_sentence = ""
    temp_word_array = break_into_words(question)
    break_index = -1
    temp_var = 1
    for i in range(len(temp_word_array)):
        question_sentence = question_sentence + " " +temp_word_array[i] 
        if(((i+1)%8 == 0) or (i+1) == len(temp_word_array)):
            temp_var = guess_top_5(question = [question_sentence])
            # print(temp_var)
            if (temp_var[0][1]>threshold_buzz):
                print("Ring buzzer on word number " + str(i+1))
                break_index = i+1
                question_sentence = question_sentence + "||[[BUZZER]]||"
                print("[[Question Start]]"+question_sentence)
                print("The guess is: " + temp_var[0][0] + " with score: " + str(temp_var[0][1]) + "\n")
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

def check_drop_in_confidence(question, actual_confidence, max=50, ind = -1):
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

def make_colored(score, text , max, min):
    colored_text = colored(int(255 * (1 - (score -min)/(max-min))) , 255, int(255 * (1 - (score -min)/(max-min))), text)
    return colored_text

def get_importance_of_each_word(question):
    actual_answer, index_of_answer = get_actual_guess_with_index(question = [question])
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
        drop_in_confidence = check_drop_in_confidence(question = [temp_sentence_string], ind = index_of_answer, actual_confidence = actual_confidence)
        print("Importance of word "+ temp_sentence_array[i] + "= ", actual_confidence-drop_in_confidence)
        array_of_importances.append(actual_confidence-drop_in_confidence)
        if(least_confidence > (actual_confidence-drop_in_confidence)):
            least_confidence = (actual_confidence-drop_in_confidence)
        if(highest_confidence< (actual_confidence-drop_in_confidence)):
            highest_confidence_word = temp_sentence_array[i]
            highest_confidence = (actual_confidence-drop_in_confidence)
    print("Word with the most importance: "+ str(highest_confidence_word) + " "+str( highest_confidence))
    colored_string = " "
    for i in range(len(temp_sentence_array)):
        colored_string = colored_string + " " + make_colored(array_of_importances[i],temp_sentence_array[i], highest_confidence, least_confidence)
    print(colored_string)
    print(colored(255,255,255,""))
    return

def get_importance_of_each_sentence(question):
    actual_answer, index_of_answer = get_actual_guess_with_index(question = [question])
    actual_confidence = actual_answer[1]
    temp_sentence_array = break_into_sentences(question)
    highest_confidence = -10
    least_confidence = 10
    highest_confidence_sentence = -1
    array_of_importances = []
    for i in range(len(temp_sentence_array)):
        temp_sentence = temp_sentence_array[:i] + temp_sentence_array[i+1:]
        temp_sentence_string = ' '.join(temp_sentence)
        drop_in_confidence = check_drop_in_confidence(question = [temp_sentence_string], ind = index_of_answer,actual_confidence=actual_confidence)
        score = float(actual_confidence-drop_in_confidence)
        # print(actual_confidence, drop_in_confidence, score)
        array_of_importances.append(score)
        if(least_confidence > (score)):
            least_confidence = (score)
        if(highest_confidence< (score)):
            highest_confidence_sentence = i
            highest_confidence = (score)
    # colored_string = ""
    # for i in range(len(temp_sentence_array)):
    #     colored_string = colored_string + " " + make_colored(array_of_importances[i],temp_sentence_array[i], highest_confidence, least_confidence)
    most_important = []
    for i in range(len(array_of_importances)):
        a = break_into_words(temp_sentence_array[i])
        most_important.append({"sentence":a[0] + " ... " + a[-1], "importance":array_of_importances[i]})
    return most_important
    # return temp_sentence_array[highest_confidence_sentence]



# def vectorizer(string):
#   vectors = []
#   string_vec = np.zeros(300)
#   array_of_words = break_into_words_with_capital(string)
#   # print(array_of_words)
#   for i in range(len(array_of_words)):
#     if array_of_words[i] in pre_ft_vectors:
      
#       vec = pre_ft_vectors[array_of_words[i]]
#       string_vec = string_vec + vec
#     else:
#       vec = np.zeros(300)
#     vectors.append(vec)
#   string_vec = string_vec/len(array_of_words)
#   return string_vec

# Raj End -------------------