# Raj

# Description of this file: 
# 1. Buzzer implementation based on binary search
# 2. Importance of sentence implementation
import sys
sys.path.append("..")
sys.path.insert(0, './app')
from app import import_libraries, util
from import_libraries import *
from util import * # Imports the tf-idf vectorizer used in qanta

binary_search_based_buzzer = Blueprint('binary_search_based_buzzer', __name__)


def buzz(question, ans, min_index=5):
    """
    
    Parameters
    ----------
    question: This contains the string of containing the trivia question.
    min_index: The index of the string to the binary search from.


    Returns
    --------
    question_sentence: The substring on which the tf-idf model buzzes.
    rest_of_sentence: The remaining substring of the question.
    Flag: True/ False, True siginifies that the buzzer crosses the threshold.

    """
    answer = []
    temp_word_array = question.split(' ')
    # check if buzzer ever goes above threshold
    index_of_bin_search = len(temp_word_array)
    
    if(len(temp_word_array)<10):
        return "The string is too short", "", False, "", -1, -1
    if(len(temp_word_array)<20):
        question_sentence = question
        temp_var = guess_top_n(question=[question_sentence], params=params, max=3, n=1)
        if (temp_var[0][1] < threshold_buzz):
            return "The string does not cross the threshold", "", False, "", -1, -1
    # print(temp_word_array)
    max_index = index_of_bin_search - 1
    max_index = int(max_index/10)*10
    # print(max_index,temp_word_array)
    # while max_index >= min_index:
    set_flag = 0
    first_question_sentence = ''
    first_index_of_bin_search = -1
    for i in range(10, max_index+1, 10):
        # print(i, max_index)
        index_of_bin_search = i
        question_sentence = " ".join(temp_word_array[:index_of_bin_search])
        temp_var = guess_top_n(question=[question_sentence], params=params, max=3, n=1)
        if (temp_var[0][1] > threshold_buzz):
            if(temp_var[0][0] == ans.replace(' ','_')):
                set_flag = 1
                break
            elif(set_flag!=2):
                set_flag = 2
                first_question_sentence = question_sentence
                first_index_of_bin_search = index_of_bin_search


        elif(i == max_index):
            return "Buzzer does not cross the threshold", "", False, "", -1, -1
    if(set_flag == 2):
        question_sentence = first_question_sentence
        index_of_bin_search = first_index_of_bin_search

    rest_of_sentence = " ".join(temp_word_array[index_of_bin_search:])
    return question_sentence, rest_of_sentence, True, temp_var[0][0], set_flag, index_of_bin_search

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

def check_drop_in_confidence(question, actual_confidence, max=50, ind = -1):
    """
    Parameters
    ----------
    question: This contains a list of the strings containing the trivia question(s).
    max: The top max number of results to be considered for ranking.
    actual_confidence: The confidence of the top guess from the tf-idf model.
    ind: The index of the top guess in the corpus.

    Returns
    --------
    confidence: confidence of the top guess of the corpus.
    
    """
    vectorizer, Matrix, ans = params[0], params[1], params[2]
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

def get_importance_of_each_sentence(question):
    """
    Parameters
    ----------
    question: This contains the string of containing the trivia question.

    Returns
    --------
    list of key:value pairs of the following format:
    [
        {
            "sentence": "first_word ... second_word",
            "importance": confidence_of_the_sentence
        }
    ]
    
    """
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
        array_of_importances.append(score)
        if(least_confidence > (score)):
            least_confidence = (score)
        if(highest_confidence< (score)):
            highest_confidence_sentence = i
            highest_confidence = (score)
    most_important = []
    for i in range(len(array_of_importances)):
        a = break_into_words(temp_sentence_array[i])
        most_important.append({"sentence":a[0] + " ... " + a[-1], "importance":round(array_of_importances[i],3)})
    return most_important, temp_sentence_array[highest_confidence_sentence], highest_confidence_sentence+1

def insert_into_db(q_id, date_incoming, date_outgoing, question, ans, buzzer_string, buzzer_sentence_number, buzzer_word_number, most_important_sentence_number, most_important_sentence, if_ans_found):
    ans = ans.replace(" ","_")
    if q_id not in buzzer:
        buzzer[q_id]=[]
        state_buzzer[q_id] = {
            "ans":False,
            "pos":-1
        }
    is_relevant = False
    string_new = ""
    previous_pos = state_buzzer[q_id]["pos"]
    if state_buzzer[q_id]["ans"]==True:
        if state_buzzer[q_id]["pos"]<buzzer_word_number and if_ans_found==2:
            is_relevant = False
            state_buzzer[q_id]["ans"] = False
            string_new = "Buzzer shifted to right but not for the correct answer"
            
    else:
        if if_ans_found == 1:
            is_relevant = True
            state_buzzer[q_id]["ans"] = True
            state_buzzer[q_id]["pos"] = buzzer_word_number
            if(previous_pos!=-1):
                if(buzzer_word_number<previous_pos):
                    string_new = "Buzzer buzzed earlier than previous position by " + str(previous_pos - buzzer_word_number) + "postions"
                else:
                    string_new = "Buzzer buzzed later than previous position by " + str( buzzer_word_number - previous_pos) + "postions"
            else:
                string_new = "Buzzer buzzed on the correct answer for the first time"
    buzzer[q_id].append({
                                "edit_history":
                                            {
                                                "change_in_position": string_new,
                                                "isRelevant": is_relevant,
                                            },
                                "Timestamp_frontend":date_incoming, 
                                "Timestamp_backend": date_outgoing,
                                "buzzer_string":buzzer_string,
                                "buzzer_sentence_number": buzzer_sentence_number,
                                "buzzer_word_number": buzzer_word_number,
                                "most_important_sentence_number": most_important_sentence_number,
                                "most_important_sentence": most_important_sentence,
                                "if_ans_found":if_ans_found,
                                "is_relevant": is_relevant,
                                "prev_pos": previous_pos,
                                
                            })


@binary_search_based_buzzer.route("/buzz_full_question", methods=["POST"])
def buzz_full_question():
    """
    
    Parameters
    ----------
    None

    Returns
    --------
    Json object of the following format is returned:
    {
        "buzz": buzzer_string, #The substring on which the tf-idf model buzzes.
        "buzz_word": buzz_word, #The last ten characters of the substring on which the tf-idf model buzzes.
        "flag":flag, #Flag which tells us whether the model buzzes or not.
        "importance": importance_sentence #Importance of each individual sentence in terms of drop in tf-idf model score due to the absence of the particular sentence.
    }

    Prints
    --------
    The time taken of the two sub-modules in the terminal:
    1. Binary search based buzzer
    2. Importance of each sentence
    """
    if request.method == "POST":
        question = request.form.get("text")
        date_incoming = request.form.get("date")
        ans = request.form.get("answer_text")
        q_id = request.form.get("id")
    ans = ans.strip()
    if(question.strip()==""):
        return jsonify({"buzz": "", "buzz_word": "", "flag": False, "top_guess" : "", "importance": [{"sentence":"-", "importance":-1}] })
    start = time.time()
    buzzer_string, rest_of_sentence, flag, top_guess, set_flag, buzzer_word_number = buzz(question, ans)

    end = time.time()
    buzz_word = []
    print("----TIME (s) : /binary_search_based_buzzer/buzz_full_question---", end - start)
 
    start = time.time()
    buzzer_last_word =""
    if(flag):
        importance_sentence, sentence_string, sentence_number = get_importance_of_each_sentence(buzzer_string)
        buzzer_last_word=buzzer_string[-10:]
        buzz_word.append(buzzer_last_word)
        date_outgoing = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        date_outgoing.replace(', 00',', 24')
        insert_into_db(q_id, date_incoming, date_outgoing, question, ans, buzzer_string, len(break_into_sentences(buzzer_string)), buzzer_word_number, sentence_number, sentence_string, set_flag)
        buzzer_string = buzzer_string + ' 🔔BUZZ '
    else:

        importance_sentence, sentence_string, sentence_number = get_importance_of_each_sentence(question)
    end = time.time()
    print("----TIME (s) : /binary_search_based_buzzer/get_importance_sentence---", end - start)
    
    return jsonify({"buzz": buzzer_string, "buzz_word": buzz_word, "flag": flag, "top_guess" : top_guess, "importance": importance_sentence,"buzzer_last_word":buzzer_last_word})