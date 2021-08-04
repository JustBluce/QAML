#Cai and Raj
# Description of this file:
# 1. Finding the top 5 guesses of the tf-idf vectorizer

import sys
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
                                "id":q_id,
                                "data":{
                                    "Timestamp_frontend":date_incoming, 
                                    "Timestamp_backend": date_outgoing, 
                                    "guesses":answer,
                                    "Question":question,
                                    "answer":ans,
                                    "ans_pos": state_machine_guess[q_id]["ans_pos"]
                                    }
                                })
    else:
        if ans in array_of_top_guesses_strings:
            if(state_machine_guess[q_id]["ans_pos"] != array_of_top_guesses_strings.index(ans)):
                state_machine_guess[q_id]["ans_pos"] = array_of_top_guesses_strings.index(ans)
                machine_guess[q_id].append({
                                        "id":q_id,
                                        "data":{
                                            "Timestamp_frontend":date_incoming, 
                                            "Timestamp_backend": date_outgoing, 
                                            "guesses":answer,
                                            "Question":question,
                                            "answer":ans,
                                            "ans_pos": state_machine_guess[q_id]["ans_pos"]
                                            }
                                        })


machine_guess = {}
state_machine_guess = {}
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
    start = time.time()
    answer = guess(question=[question])
    array_of_top_guesses_strings = [str(x[0]) for x in answer]
    answer = [{"guess": str(x[0]),"score":str(x[1])} for x in answer]
    
    end = time.time()
    # print(end - start)
    print("----TIME (s) : /func/act---", end - start)
    date_outgoing = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    add_to_db(q_id, date_incoming, date_outgoing, answer, question, ans, array_of_top_guesses_strings)
    # print(machine_guess.keys)
    print(machine_guess[q_id][-2:])
    print(sys.getsizeof(machine_guess)) 

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
    if request.method == "POST":
        question = request.form.get("text")
        ans = request.form.get("answer_text")
    print(question, ans)
    answer = guess(question=[question])
    qa_table = metadata.tables["qa"]
    db.session.execute(qa_table.insert().values(Question=question, Answer=ans))
    
    return "submitted"
