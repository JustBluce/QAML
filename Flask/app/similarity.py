import sys
sys.path.append("..")
sys.path.insert(0, './app')

from app import util, import_libraries
from import_libraries import *
from util import *


stopWords = stopwords.words('english')

f = open('app/qanta.json')
data = json.load(f)['questions']


questions = []
answers = []
for i in range(0, len(data)):
    questions.append(data[i]['text'])

tfidf_vectorizer = TfidfVectorizer(stop_words = stopWords)
tfidf_matrix = tfidf_vectorizer.fit_transform(questions)

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


similar_question = Blueprint('similar_question', __name__)
@similar_question.route("/retrieve_similar_question", methods=["POST"])
def retrieve_similar_question():
    """
    
    Parameters
    ----------
    None

    Returns
    --------
    Json object of the following format is returned:
    {
        "similar_questions": 
        [
            Flag (True or False, True if there is any question whose similarity is above a threshold in the dataset)
            [   Top five similar questions and answers
                (Question, Answer),
                ...

            ]
        ]
    }

    Prints
    --------
    The time taken of the two sub-modules in the terminal:
    1. Similarity of the question
    """
    if request.method == "POST":
        question = request.form.get("text")
    start =time.time()
    questions.append(question)
    repre = tfidf_vectorizer.transform([question])
    matrix = tfidf_matrix.dot(repre.T).T
    matrix = matrix.toarray()
    # cosine = cosine_similarity(tfidf_matrix[len(questions)-1], tfidf_matrix)[0]
    max_cosine = max(matrix[0])
    # print(matrix)
    top_5_idx = np.flipud(np.argsort(matrix[0])[-5:])
    # print([matrix[0][index] for index in top_5_idx])
    
    isSimilar = False
    if max_cosine > threshold_similar:
        isSimilar = True
        # print([max_cosine, questions[max_index[0]]])
    end = time.time()
    print(data[0])
    print("----TIME (s) : /similar_question/retrieve_similar_question---",end - start)
    return jsonify({"similar_question": [isSimilar, [data[index] for index in top_5_idx]]})