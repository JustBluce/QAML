import sys
sys.path.append("..")
sys.path.insert(0, 'C:/Users/rajsa/Desktop/qanta-codalab-master/TryoutProject/Flask/app')

from app import util
from util import *

def guess_top_5(question, max=12):
    vectorizer, Matrix, ans = get_pretrained_tfidf_vectorizer()
    answer = []
    repre = vectorizer.transform(question)
    matrix = Matrix.dot(repre.T).T
    indices = (-matrix).toarray().argsort(axis=1)[:, 0:max]
    for i in range(len(question)):
        answer.append([(ans[j], matrix[i, j]) for j in indices[i]])
    # print(answer)
    return answer[0][0:5]

def guess_by_sentences(question):
    answer = []
    question_sentence = ""
    temp_sentence_array = break_into_sentences(question)
    break_index = -1
    for i in range(len(temp_sentence_array)):
        question_sentence = question_sentence + " " +temp_sentence_array[i] 
        temp_var = guess_top_5(question = [question_sentence])
        # print(temp_var)
        if (temp_var[0][1]>threshold):
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
            if (temp_var[0][1]>threshold):
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

def check_drop_in_confidence(question, max=12, ind = -1):
    answer = []
    repre = vectorizer.transform(question)
    matrix = Matrix.dot(repre.T).T
    indices = (-matrix).toarray().argsort(axis=1)[:, 0:max]
    for i in range(len(question)):
        idx = indices[i]
        answer.append([(ans[j], matrix[i, j]) for j in idx])
        if(ind == idx[0]):
            return answer[0][i][1]
    return 0

def make_colored(score, text , max, min):
    colored_text = colored(int(255 * (1 - (score -min)/(max-min))) , 255, int(255 * (1 - (score -min)/(max-min))), text)
    return colored_text

def get_importance_of_each_sentence(question):
    actual_answer, index_of_answer = get_actual_guess_with_index(question = [question])
    print(actual_answer)
    actual_confidence = actual_answer[1]
    temp_sentence_array = break_into_sentences(question)
    highest_confidence = -10
    least_confidence = 10
    highest_confidence_sentence = -1
    array_of_importances = []
    for i in range(len(temp_sentence_array)):
        temp_sentence = temp_sentence_array[:i] + temp_sentence_array[i+1:]
        temp_sentence_string = ' '.join(temp_sentence)
        drop_in_confidence = check_drop_in_confidence(question = [temp_sentence_string], ind = index_of_answer)
        print("Importance of sentence number "+ str(i)+ "= ", actual_confidence-drop_in_confidence)
        array_of_importances.append(actual_confidence-drop_in_confidence)
        if(least_confidence > (actual_confidence-drop_in_confidence)):
            least_confidence = (actual_confidence-drop_in_confidence)
        if(highest_confidence< (actual_confidence-drop_in_confidence)):
            highest_confidence_sentence = i
            highest_confidence = (actual_confidence-drop_in_confidence)
    print("Sentence number with the most importance: "+ str(highest_confidence_sentence) + " "+str( highest_confidence))
    colored_string = ""
    for i in range(len(temp_sentence_array)):
        colored_string = colored_string + " " + make_colored(array_of_importances[i],temp_sentence_array[i], highest_confidence, least_confidence)
    print(colored( 0, 1, 0,""))
    print(colored_string)
    print(colored(255,255,255,""))
    return

def get_importance_of_each_word(question):
    actual_answer, index_of_answer = get_actual_guess_with_index(question = [question])
    print(actual_answer)
    actual_confidence = actual_answer[1]
    temp_sentence_array = break_into_words(question)
    highest_confidence = -10
    least_confidence = 10
    highest_confidence_word = ""
    array_of_importances = []
    for i in range(len(temp_sentence_array)):
        temp_sentence = temp_sentence_array[:i] + temp_sentence_array[i+1:]
        temp_sentence_string = ' '.join(temp_sentence)
        drop_in_confidence = check_drop_in_confidence(question = [temp_sentence_string], ind = index_of_answer)
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
# Raj End -------------------