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

def add_to_db(q_id, date_incoming, date_outgoing, answer, question, ans, array_of_top_guesses_strings):
    ans = ans.replace(" ","_")
    if q_id not in machine_guess:
        machine_guess[q_id]=[]
        state_machine_guess[q_id]={
                                    "ans_pos": -1, 
                                    "current_guesses": array_of_top_guesses_strings
                                    }
        if ans in array_of_top_guesses_strings:
            state_machine_guess[q_id]["ans_pos"] = array_of_top_guesses_strings.index(ans)
        
        machine_guess[q_id].append({
                                
                                    "Timestamp_frontend":date_incoming, 
                                    "Timestamp_backend": date_outgoing, 
                                    "guesses":answer,
                                    "ans_pos": state_machine_guess[q_id]["ans_pos"]
                                    
                                })
    else:
        if ans in array_of_top_guesses_strings:
            if(state_machine_guess[q_id]["ans_pos"] != array_of_top_guesses_strings.index(ans)):
                state_machine_guess[q_id]["ans_pos"] = array_of_top_guesses_strings.index(ans)
                machine_guess[q_id].append({
                                        
                                            "Timestamp_frontend":date_incoming, 
                                            "Timestamp_backend": date_outgoing, 
                                            "guesses":answer,
                                            "ans_pos": state_machine_guess[q_id]["ans_pos"]
                                            
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
        q_id = request.form.get("id")
    if q_id not in time_stamps:
        time_stamps[q_id]=[]
        questions_all_time_stamps[q_id] = []
        ans_all_time_stamps[q_id] = []
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
        q_id = request.form.get("id")
    # print(question, ans)
    # answer = guess(question=[question])
    # print(q_id)
    big_dict = {
        "q_id": q_id,
        "data":{}
    }
    counter_guess = 0
    counter_pron = 0
    counter_country  = 0
    counter_difficulty = 0
    counter_buzz = 0
    counter_sim = 0
    if q_id in time_stamps:
        for j in range(len(time_stamps[q_id])):
            i = time_stamps[q_id][j]
            big_dict["data"][i] = {}
            big_dict["data"][i]["Question"] = questions_all_time_stamps[q_id][j]
            big_dict["data"][i]["Answer"] = ans_all_time_stamps[q_id][j]
            flag = 0
            if q_id in machine_guess and counter_guess < len(machine_guess[q_id]):
                if i == machine_guess[q_id][counter_guess]["Timestamp_frontend"]:
                    flag = 1
                    big_dict["data"][i]["machine_guess"] = machine_guess[q_id][counter_guess]
                    counter_guess+=1
            if q_id in similarity and counter_sim < len(similarity[q_id]):
                if i == similarity[q_id][counter_guess]["Timestamp_frontend"]:
                    flag = 1
                    big_dict["data"][i]["similarity"] = similarity[q_id][counter_sim]
                    counter_sim+=1
            if q_id in buzzer and counter_buzz < len(buzzer[q_id]):
                if i == buzzer[q_id][counter_buzz]["Timestamp_frontend"]:
                    flag = 1
                    # if buzzer[q_id][counter_buzz]["is_relevant"]:
                    big_dict["data"][i]["buzzer"] = buzzer[q_id][counter_buzz]
                    counter_buzz+=1
            if q_id in difficulty and counter_difficulty < len(difficulty[q_id]):
                if i == difficulty[q_id][counter_difficulty]["Timestamp_frontend"]:
                    flag = 1
                    big_dict["data"][i]["difficulty"] = difficulty[q_id][counter_difficulty]
                    counter_difficulty+=1
            if q_id in country_represent_json and counter_country < len(country_represent_json[q_id]):
                if i == country_represent_json[q_id][counter_country]["Timestamp_frontend"]:
                    flag = 1
                    big_dict["data"][i]["country_represent"] = country_represent_json[q_id][counter_country]
                    counter_country+=1
            if q_id in pronunciation_dict and counter_pron < len(pronunciation_dict[q_id]):
                if i == pronunciation_dict[q_id][counter_pron]["Timestamp_frontend"]:
                    flag = 1
                    big_dict["data"][i]["pronunciation_dict"] = pronunciation_dict[q_id][counter_pron]    
                    counter_pron+=1
            if flag==0:
                big_dict["data"].pop(i)
            
                
    print(json.dumps(big_dict, indent = 10))
    with open('test.json', 'w') as outfile:
        json.dump(big_dict, outfile)
    with open('machine_guess.json', 'w') as outfile:
        json.dump(machine_guess, outfile)
    with open('pronunciation_dict.json', 'w') as outfile:
        json.dump(pronunciation_dict, outfile)
    with open('country_represent_json.json', 'w') as outfile:
        json.dump(country_represent_json, outfile)
    with open('buzzer.json', 'w') as outfile:
        json.dump(buzzer, outfile)
    with open('similarity.json', 'w') as outfile:
        json.dump(similarity, outfile)
    if q_id in machine_guess:
        machine_guess.pop(q_id)
        state_machine_guess.pop(q_id)
    if q_id in pronunciation_dict:
        pronunciation_dict.pop(q_id)
        state_pronunciation.pop(q_id)
    if q_id in country_represent_json:
        country_represent_json.pop(q_id)
        # state_country_represent_json.pop(q_id)
    if q_id in difficulty:
        difficulty.pop(q_id)
    if q_id in buzzer:
        buzzer.pop(q_id)
        state_buzzer.pop(q_id)
    if q_id in similarity:
        similarity.pop(q_id)
        state_similarity.pop(q_id)
    # if q_id in pronunciation_dict:
    #     print(json.dumps(pronunciation_dict[q_id], indent = 7))
    # if q_id in country_represent_json:
    #     print(json.dumps(country_represent_json[q_id], indent = 7))
    qa_table = metadata.tables["qa"]
    db.session.execute(qa_table.insert().values(Question=question, Answer=ans))
    end=time.time()
    print("----TIME (s) : /func/submit [SUBMIT]---",end-start)
    return "submitted"
