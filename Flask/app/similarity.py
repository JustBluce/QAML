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

def add_to_db(q_id, date_incoming, date_outgoing, question, ans, isSimilar, array_of_data):
    ans = ans.replace(" ","_")
    if q_id not in similarity:
        similarity[q_id]=[]
        state_similarity[q_id] ={
                                    "wasSimilar":False,
                                    "prev_top_3": []

                                }
    if isSimilar != state_similarity[q_id]["wasSimilar"]:
        similarity[q_id].append({
                                    "edit_history":
                                            {
                                                "wasSimilar": state_similarity[q_id]["wasSimilar"],
                                                "isSimilar": isSimilar,
                                                "change_in_most_similar": "Not Relevant" ,
                                            },
                                    "Timestamp_frontend":date_incoming, 
                                    "Timestamp_backend": date_outgoing, 
                                    "top_3_positions": array_of_data
                                    
                                })
        state_similarity[q_id] ={
                                    "wasSimilar":isSimilar,
                                    "prev_top_3": array_of_data

                                }
        return
            
    if len(state_similarity[q_id]["prev_top_3"])>0 and array_of_data[0]!= state_similarity[q_id]["prev_top_3"][0] and isSimilar:
        pos = -1
        for i in range(len(array_of_data)):
            if array_of_data[i]==state_similarity[q_id]["prev_top_3"]:
                pos = i 
                break
        string_new = ""
        if (pos ==-1):
            string_new = "The previous most similar question is no longer in the top 3"
        else:
            string_new = "The previous most similar question is now on position" + str(i)
        similarity[q_id].append({
                               
                                    "edit_history":
                                            {
                                                "wasSimilar": True,
                                                "isSimilar": isSimilar,
                                                "change_in_most_similar": string_new ,
                                            },
                                    "Timestamp_frontend":date_incoming, 
                                    "Timestamp_backend": date_outgoing, 
                                    "top_3_positions": array_of_data
                                    
                                })
        state_similarity[q_id] ={
                                    "wasSimilar":isSimilar,
                                    "prev_top_3": array_of_data

                                }


    


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
        ans = request.form.get("answer_text")
        q_id = request.form.get("qid")
        date_incoming = request.form.get("date")
    if question.strip()=="":
        return jsonify({"similar_question": [False, [ {'answer':"", 'text':""}]]})
    start =time.time()
    questions.append(question)
    repre = tfidf_vectorizer.transform([question])
    matrix = tfidf_matrix.dot(repre.T).T
    matrix = matrix.toarray()
    # cosine = cosine_similarity(tfidf_matrix[len(questions)-1], tfidf_matrix)[0]
    max_cosine = max(matrix[0])
    # print(matrix)
    top_3_idx = np.flipud(np.argsort(matrix[0])[-3:])
    # print([matrix[0][index] for index in top_5_idx])
    
    isSimilar = False
    if max_cosine > threshold_similar:
        isSimilar = True
        # print([max_cosine, questions[max_index[0]]])
    end = time.time()
    # print(data[0])
    date_outgoing = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    date_outgoing.replace(', 00',', 24')
    add_to_db(q_id, date_incoming, date_outgoing, question, ans, isSimilar, [data[index]['answer'] for index in top_3_idx])
    print("----TIME (s) : /similar_question/retrieve_similar_question---",end - start)
    return jsonify({"similar_question": [isSimilar, [ {'answer':"Answer: " + data[index]['answer'], 'text':data[index]['text']} for index in top_3_idx]]})