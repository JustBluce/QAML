#Cai and Raj
# Description of this file:
# 1. Finding the top 5 guesses of the tf-idf vectorizer

import sys

from numpy import divide
sys.path.append("..")
sys.path.insert(0, './app')
from app import util
from app.people import getPeoplesInfo1
# from app.country_represent import country_present1
# from app.util import highlight_json

from app import util, import_libraries
from import_libraries import *
from util import *
# from app.country_represent import country_represent
from app.similarity import retrieve_similar_question


def warn(*args, **kwargs):
    pass


warnings.warn = warn
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)


func = Blueprint('func', __name__)
def guess(question, max=12):
    """
    Parameters
    ----------
    question: This contains a list of the strings containing the trivia question(s).
    max: The top max number of results to be considered for ranking.

    Returns
    --------
    answer[0][0:5]: Retrieves the top five guesses from the tf-idf model in the following format: tuple ("name_of_wikipedia_document", confidence_score)

    """
    vectorizer, Matrix, ans = params[0], params[1], params[2]
    answer = []
    repre = vectorizer.transform(question)
    matrix = Matrix.dot(repre.T).T
    indices = (-matrix).toarray().argsort(axis=1)[:, 0:max]
    for i in range(len(question)):
        answer.append([(ans[j], matrix[i, j]) for j in indices[i]])
    return answer[0][0:5]

# Cai End -------------------

def minDistance(word1, word2):
        dp = list(range(len(word2) + 1))
        
        for i in range(1, len(word1) + 1):
            dp_next = [i] + [0] * len(word2)
            for j in range(1, len(word2) + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp_next[j] = dp[j - 1]
                else:
                    dp_next[j] = min(dp[j - 1], dp[j], dp_next[j - 1]) + 1
            dp = dp_next
        
        return dp[len(word2)]

def store_in_db (q_id, date_incoming, date_outgoing, question, ans):
    if ' ' in ans:
        ans = ans.replace(" ","_")
    if q_id not in general_edit_history:
        general_edit_history[q_id] = {
            "question_id"  : q_id,
            "entries" : [
                {
                    "question": question,
                    "answer" : ans,
                    "Timestamp_frontend":date_incoming, 
                    "Timestamp_backend": date_outgoing, 
                }
            ]
        }   
    else:
        if(minDistance(general_edit_history[q_id]["entries"][-1]["question"].split(), question.split())) > 5:
            general_edit_history[q_id]["entries"].append(
                {
                    "question": question,
                    "answer" : ans,
                    "Timestamp_frontend":date_incoming, 
                    "Timestamp_backend": date_outgoing, 
                }
            )
        
    # print(general_edit_history[q_id])

def add_to_db(q_id, date_incoming, date_outgoing, answer, question, ans, array_of_top_guesses_strings):
    ans = ans.replace(" ","_")
    isRelevant =  False
    if q_id not in machine_guess:
        machine_guess[q_id]=[]
        state_machine_guess[q_id]={
                                    "ans_pos": -1, 
                                    "current_guesses": array_of_top_guesses_strings
                                    }
        isRelevant = False
        if ans in array_of_top_guesses_strings:
            state_machine_guess[q_id]["ans_pos"] = array_of_top_guesses_strings.index(ans)
            isRelevant = True
        machine_guess[q_id].append({
                                    "edit_history":
                                    {
                                        "change_in_position": "First Entry",
                                        "isRelevant": isRelevant,
                                    },
                                    "Timestamp_frontend":date_incoming, 
                                    "Timestamp_backend": date_outgoing, 
                                    "guesses":answer,
                                    "ans_pos": state_machine_guess[q_id]["ans_pos"],
                                    "prev_pos": -1,
                                    
                                    
                                })
    else:
        # print(array_of_top_guesses_strings.index(ans))
        if ans in array_of_top_guesses_strings:
            isRelevant =  False
            if(state_machine_guess[q_id]["ans_pos"] != array_of_top_guesses_strings.index(ans)):
                prev_pos = state_machine_guess[q_id]["ans_pos"]
                
                state_machine_guess[q_id]["ans_pos"] = array_of_top_guesses_strings.index(ans)
                string_new = ""
                if prev_pos == -1:
                    string_new = string_new + "The machine did not guess previously"
                    isRelevant =  True
                elif(prev_pos < state_machine_guess[q_id]["ans_pos"]) :
                    string_new = string_new + "The previous position was " + str(prev_pos) + " and the new position is " + str(state_machine_guess[q_id]["ans_pos"])
                    isRelevant =  True
                else:
                    string_new = string_new + "The previous position was " + str(prev_pos) + " and the new position is " + str(state_machine_guess[q_id]["ans_pos"])
                    isRelevant =  False
                machine_guess[q_id].append({
                                            "edit_history":
                                            {
                                                "change_in_position": string_new,
                                                "isRelevant": isRelevant,
                                            },
                                            "Timestamp_frontend":date_incoming, 
                                            "Timestamp_backend": date_outgoing, 
                                            "guesses":answer,
                                            "ans_pos": state_machine_guess[q_id]["ans_pos"],
                                            "prev_pos": prev_pos,
                                        })



# machine_guess["guess"] = []
@func.route("/act", methods=["POST"])
def act():
    """
    Parameters
    ----------
    None

    Returns
    --------
    The top five tf-idf machine guesses in the following format:
    {
        "guess":
        [
            {
                "guess": wikipedia_page_name,
                "score": tf-idf cosine similarity score
            },
            ...
        ]
    }
    """
    if request.method == "POST":
        question = request.form.get("text")
        ans = request.form.get("answer_text")
        date_incoming = request.form.get("date")
        q_id = request.form.get("qid")
    if q_id not in time_stamps:
        time_stamps[q_id]=[]
        questions_all_time_stamps[q_id] = []
        ans_all_time_stamps[q_id] = []
    if question.strip()=="":
        return jsonify({"guess": [{"guess": "","score":""}]})
    time_stamps[q_id].append(date_incoming)
    questions_all_time_stamps[q_id].append(question)
    ans_all_time_stamps[q_id].append(ans)

    start = time.time()
    answer = guess(question=[question])
    array_of_top_guesses_strings = [str(x[0]) for x in answer]
    answer = [{"guess": str(x[0]),"score":str(round(x[1],3))} for x in answer]
    
    end = time.time()
    # print(end - start)
    print("----TIME (s) : /func/act---", end - start)
    date_outgoing = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    date_outgoing.replace(', 00',', 24')
    add_to_db(q_id, date_incoming, date_outgoing, answer, question, ans, array_of_top_guesses_strings)
    store_in_db (q_id, date_incoming, date_outgoing, question, ans)
    # print(machine_guess.keys)
    # print(machine_guess[q_id][-2:])
    # print(sys.getsizeof(machine_guess)) 

    return jsonify({"guess": answer})


@func.route("/timeup", methods=["GET"])
def timeup():
    """
    Parameters
    ----------
    None

    Returns
    --------
    None

    Prints
    --------
    "timeup"
    """
    print("timeup")
    return "OK"


# @func.route("country_people", methods=["POST"])
# def country_people():
#     """
#     Parameters
#     ----------
#     None

#     Returns
#     --------
#     {
#         "country_representation": country_representation, 
#         "Highlight": highlight
#     }

#     """
#     if request.method == "POST":
#         question = request.form.get("text")
#     country_representation, countries = country_present1(question)
#     highlight=highlight_json(countries)
#     return jsonify({"country_representation": country_representation, "Highlight": highlight})
class Question_json(db.Model):
    __tablename__ = 'Question_json'
    q_id = db.Column(db.String, primary_key=True)
    data = db.Column(db.JSON)
    points = db.Column(db.Integer)
    UID = db.Column(db.String)

class Question(db.Model):
    __tablename__ = 'Question'
    Question_id = db.Column(db.String, primary_key=True)
    Question = db.Column(db.String)
    Timestamp_frontend = db.Column(db.DateTime, primary_key=True)
    Answer = db.Column(db.String)
    UserId = db.Column(db.String)
    Timestamp_backend = db.Column(db.DateTime)
    Point = db.Column(db.Integer)
    Genre = db.Column(db.String)

@func.route("/insert", methods=["POST"])
def insert():
    """
    Parameters
    ----------
    None

    Returns
    --------
    Insert into database and return status

    """
    start = time.time()
    if request.method == "POST":
        question = request.form.get("text")
        ans = request.form.get("answer_text")
        q_id = request.form.get("qid")
        user_id = request.form.get("user_id")
        genre_1 = request.form.get("genre")
        date_incoming = request.form.get("date")
        
    # print(question, ans)
    # answer = guess(question=[question])
    # print(q_id)
    big_dict = {
        "q_id": q_id,
        "data":{},
        "points":0,
        "genre": genre_1,
    }
    small_dict = {
        "q_id": q_id,
        "data":{},
        "points":0,
        "genre": genre_1,
    }
    points = 0
    if q_id in state_machine_guess:
        if ans in state_machine_guess[q_id]["current_guesses"]:
            pos_ans = state_machine_guess[q_id]["current_guesses"].index(ans)
            if pos_ans == 0:
                points +=0
            elif pos_ans == 1:
                points +=5
            elif pos_ans == 2:
                points +=10
        else:
            points += 20
    else:
        points += 20
    if q_id in difficulty:
        if len(difficulty[q_id])>0:
            diff_level = difficulty[q_id][-1]["difficulty"]
            if diff_level=="Hard":
                points+=10
    if q_id in country_represent_json:
        if len(country_represent_json[q_id])>0:
            under_countries = country_represent_json[q_id][-1]["current_under_countries"]
            points+=len(under_countries)*10
    if q_id in similarity:
        if len(similarity[q_id])>0:
            similar_top_3 = similarity[q_id][-1]["edit_history"]["isSimilar"]
            if not similar_top_3:
                points+=10
    else:
        points+=10

    counter_guess = 0
    counter_pron = 0
    counter_country  = 0
    counter_difficulty = 0
    counter_buzz = 0
    counter_sim = 0
    if q_id in time_stamps:
        i = time_stamps[q_id][0]
        big_dict["data"][i] = {}
        # big_dict["data"][i]["Question"] = questions_all_time_stamps[q_id][0]
        big_dict["data"][i]["Answer"] = ans_all_time_stamps[q_id][0]
        big_dict["data"][i]["Relevant"] = "First Time Stamp"
        big_dict["data"][i]["word_list_addition"] = []
        big_dict["data"][i]["word_list_removal"] = []
        big_dict["data"][i]["add"] = []
        big_dict["data"][i]["remove"] = []
        big_dict["data"][i]["steps"] = []
        small_dict["data"][i] = {}
        small_dict["data"][i]["Question"] = questions_all_time_stamps[q_id][0]
        small_dict["data"][i]["Answer"] = ans_all_time_stamps[q_id][0]
        small_dict["data"][i]["Relevant"] = "First Time Stamp"
        if q_id in machine_guess and len(machine_guess[q_id])!=0:
            if i == machine_guess[q_id][counter_guess]["Timestamp_frontend"]:
                small_dict["data"][i]["machine_guess"] = machine_guess[q_id][counter_guess]
                counter_guess+=1
        if q_id in similarity and len(similarity[q_id])!=0:
            if counter_guess in similarity[q_id]:
                if i == similarity[q_id][counter_guess]["Timestamp_frontend"]:
                    small_dict["data"][i]["similarity"] = similarity[q_id][counter_sim]
                    counter_sim+=1
        if q_id in buzzer and len(buzzer[q_id])!=0:
            if i == buzzer[q_id][counter_buzz]["Timestamp_frontend"]:        
                small_dict["data"][i]["buzzer"] = buzzer[q_id][counter_buzz]
                counter_buzz+=1
        if q_id in difficulty and len(difficulty[q_id])!=0:
            if i == difficulty[q_id][counter_difficulty]["Timestamp_frontend"]:
                small_dict["data"][i]["difficulty"] = difficulty[q_id][counter_difficulty]
                counter_difficulty+=1
        if q_id in country_represent_json and len(country_represent_json[q_id])!=0:  
            if i == country_represent_json[q_id][counter_country]["Timestamp_frontend"]:
                small_dict["data"][i]["country_represent"] = country_represent_json[q_id][counter_country]
                counter_country+=1
        if q_id in pronunciation_dict and len(pronunciation_dict[q_id])!=0:
            if i == pronunciation_dict[q_id][counter_pron]["Timestamp_frontend"]:
                small_dict["data"][i]["pronunciation_dict"] = pronunciation_dict[q_id][counter_pron]    
                counter_pron+=1
        

        curr_value = questions_all_time_stamps[q_id][0].split()
        for j in range(1, len(time_stamps[q_id])):
            i = time_stamps[q_id][j]
            word_list_addition = []
            word_list_removal = [] 
            steps = []
            try:
                diff_val, add, remove, word_list_addition, word_list_removal, steps = ld(curr_value ,questions_all_time_stamps[q_id][j].split())
            except Exception:
                diff_val, add, remove = find_basic_diff(curr_value ,questions_all_time_stamps[q_id][j].split())
                
            if diff_val>5:
                Relevant = "{} words need to be added, deleted or replaced between diff".format(diff_val)
                isRelevant = True
                curr_value = questions_all_time_stamps[q_id][j].split()
                
            else:
                if j == len(time_stamps[q_id])-1:
                    Relevant = "Last Timestamp"
                    isRelevant = True
                else:
                    Relevant = "Not a big enough difference between strings"
                    isRelevant = False
            big_dict["data"][i] = {}
            if j == len(time_stamps[q_id])-1:
                    Relevant = "Last Timestamp"
                    isRelevant = True
                    # print(questions_all_time_stamps[q_id])
                    big_dict["data"][i]["Question"] = questions_all_time_stamps[q_id][j]

            # big_dict["data"][i] = {}
            big_dict["data"][i]["word_list_addition"] = word_list_addition
            big_dict["data"][i]["word_list_removal"] = word_list_removal
            big_dict["data"][i]["add"] = add
            big_dict["data"][i]["remove"] = remove
            big_dict["data"][i]["steps"] = steps
            small_dict["data"][i] = {}
            small_dict["data"][i]["Question"] = questions_all_time_stamps[q_id][j]
            small_dict["data"][i]["Answer"] = ans_all_time_stamps[q_id][j]
            # small_dict["data"][i]["Relevant"] = Relevant
            flag = 0
            Flag_String = ""
            try:
                if q_id in machine_guess and counter_guess < len(machine_guess[q_id]):
                    if i == machine_guess[q_id][counter_guess]["Timestamp_frontend"]:
                        flag = 1
                        small_dict["data"][i]["machine_guess"] = machine_guess[q_id][counter_guess]
                        big_dict["data"][i]["machine_guess"] = machine_guess[q_id][counter_guess]
                        Flag_String = Flag_String + "Machine Guess;"
                        counter_guess+=1
                if q_id in similarity and counter_sim < len(similarity[q_id]):
                    if i == similarity[q_id][counter_guess]["Timestamp_frontend"]:
                        flag = 1
                        small_dict["data"][i]["similarity"] = similarity[q_id][counter_sim]
                        big_dict["data"][i]["similarity"] = similarity[q_id][counter_sim]
                        Flag_String = Flag_String + "Similarity;" 
                        counter_sim+=1
                if q_id in buzzer and counter_buzz < len(buzzer[q_id]):
                    if i == buzzer[q_id][counter_buzz]["Timestamp_frontend"]:
                        flag = 1
                        if buzzer[q_id][counter_buzz]["is_relevant"]:
                            big_dict["data"][i]["buzzer"] = buzzer[q_id][counter_buzz]
                            Flag_String = Flag_String + "Buzzer;"
                        small_dict["data"][i]["buzzer"] = buzzer[q_id][counter_buzz]
                        counter_buzz+=1
                if q_id in difficulty and counter_difficulty < len(difficulty[q_id]):
                    if i == difficulty[q_id][counter_difficulty]["Timestamp_frontend"]:
                        flag = 1
                        small_dict["data"][i]["difficulty"] = difficulty[q_id][counter_difficulty]
                        big_dict["data"][i]["difficulty"] = difficulty[q_id][counter_difficulty]
                        Flag_String = Flag_String + "Difficulty;"
                        counter_difficulty+=1
                if q_id in country_represent_json and counter_country < len(country_represent_json[q_id]):
                    if i == country_represent_json[q_id][counter_country]["Timestamp_frontend"]:
                        flag = 1
                        small_dict["data"][i]["country_represent"] = country_represent_json[q_id][counter_country]
                        big_dict["data"][i]["country_represent"] = country_represent_json[q_id][counter_country]
                        Flag_String = Flag_String + "Country_Represent;"
                        counter_country+=1
                if q_id in pronunciation_dict and counter_pron < len(pronunciation_dict[q_id]):
                    if i == pronunciation_dict[q_id][counter_pron]["Timestamp_frontend"]:
                        flag = 1
                        small_dict["data"][i]["pronunciation_dict"] = pronunciation_dict[q_id][counter_pron]    
                        big_dict["data"][i]["pronunciation_dict"] = pronunciation_dict[q_id][counter_pron]   
                        Flag_String = Flag_String + "Pronunciation;" 
                        counter_pron+=1
            except:
                message = "List index out of range"
            big_dict["data"][i]["Relevant"] = Relevant + "  " + Flag_String
            if flag==0:
                if not isRelevant:
                    big_dict["data"].pop(i)
            
                
    # print(json.dumps(big_dict, indent = 10))
    with open('test.json', 'w') as outfile:
        json.dump(small_dict, outfile)
    with open('test_post_hoc.json', 'w') as outfile:
        json.dump(big_dict, outfile)
        try:
            me = Question_json(q_id=q_id, data=big_dict, UID=user_id, points=points)
            db.session.add(me)
            db.session.commit()
            message_json = "Successfully insert a new question_json record of the edit history of question"
        except:
            message_json = "Error insert a new question_json record of the edit history of question_json"
            print(message_json)
            db.session.rollback()

        try:
            me = Question(Question_id=q_id, Question=question, Timestamp_frontend=date_incoming, Answer=ans, UserId=user_id, Timestamp_backend=date_incoming , Point=points, Genre=genre_1)
            db.session.add(me)
            db.session.commit()
            message_json = "Successfully insert a new question_json record of the edit history of question"
        except:
            message_json = "Error insert a new question_json record of the edit history of question"
            print(message_json)
            db.session.rollback()

    with open('machine_guess.json', 'w') as outfile:
        json.dump(machine_guess, outfile, indent=2)
    with open('pronunciation_dict.json', 'w') as outfile:
        json.dump(pronunciation_dict, outfile, indent=2)
    with open('country_represent_json.json', 'w') as outfile:
        json.dump(country_represent_json, outfile)
    with open('difficulty.json', 'w') as outfile:
        json.dump(difficulty, outfile)
    with open('buzzer.json', 'w') as outfile:
        json.dump(buzzer, outfile, indent=2)
    with open('similarity.json', 'w') as outfile:
        json.dump(similarity, outfile, indent=2)
    with open('general_edit_history.json', 'w') as outfile:
        json.dump(general_edit_history, outfile, indent=2)
    if q_id in machine_guess:
        machine_guess.pop(q_id)
        state_machine_guess.pop(q_id)
    if q_id in pronunciation_dict:
        pronunciation_dict.pop(q_id)
        state_pronunciation.pop(q_id)
    if q_id in country_represent_json:
        country_represent_json.pop(q_id)
    if q_id in general_edit_history:
        general_edit_history.pop(q_id)
        # state_country_represent_json.pop(q_id)
    if q_id in difficulty:
        difficulty.pop(q_id)
    if q_id in buzzer:
        buzzer.pop(q_id)
        state_buzzer.pop(q_id)
    if q_id in similarity:
        similarity.pop(q_id)
        state_similarity.pop(q_id)
    small_dict["points"] = points
    big_dict["points"] = points
    end=time.time()
    print("----TIME (s) : /func/submit [SUBMIT]---",end-start)
    print(points)
    return jsonify({"status":"submitted", "points":points})
