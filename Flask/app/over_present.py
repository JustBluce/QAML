# Cai
import sys
sys.path.append("..")
sys.path.insert(0, './app')

from app import util, import_libraries
from util import *
from import_libraries import *

def get_actual_guess_with_index(question, max=12):
    """
    Parameters
    ----------
    question: This contains a list of the strings containing the trivia question(s).
    max: The top max number of results to be considered for ranking.

    Returns
    --------
    answer[0][0][0:]: Retrieves the top guess from the tf-idf model in the following format: tuple ("name_of_wikipedia_document", confidence_score)
    indices[0][0]: The index of the top guess in the corpus.

    """
    vectorizer, Matrix, ans = params[0], params[1], params[2]
    answer = []
    repre = vectorizer.transform(question)
    matrix = Matrix.dot(repre.T).T
    indices = (-matrix).toarray().argsort(axis=1)[:, 0:max]
    for i in range(len(question)):
        idx = indices[i]
        answer.append([(ans[j], matrix[i, j]) for j in idx])
    return answer[0][0][0:], indices[0][0]

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


over_present = Blueprint('over_present', __name__)


@over_present.route("highlight", methods=["POST"])
def high_light():
    if request.method == "POST":
        question = request.form.get("text")
        answer = request.form.get("answer_text")
    start = time.time()
    if not answer:
        return jsonify({"highlight_text": ""})
    temp_var = guess_top_n(question=[question], params=params, n=1)[0][0]
    print(temp_var)
    if answer != temp_var:
        return jsonify({"highlight_text": ""})
    print(answer,temp_var)
    text=question
    array_of_important_word_to_delay_buzzer, array_of_important_word_to_right_answer = get_important_word_to_delay_the_buzzer(question, answer)
    array_of_important_sentence_to_right_answer = get_important_sentence_to_get_right_answer(question, answer)

    highligh=Highlight()
    highlight_text=highligh.highlight_text(text=text, keywords=array_of_important_word_to_delay_buzzer, color='red')
    highlight_text=highligh.highlight_text(text=highlight_text, keywords=array_of_important_sentence_to_right_answer, color='yellow')
    print(highlight_text)
    end = time.time()
    print("----TIME (s) : /overpresent/highlight---", end - start)
    return jsonify({"highlight_text": highlight_text})
