# Atith
# Description of this file: 
# 1. Finding the difficulty of each question based on education levels

import sys
sys.path.append("..")
sys.path.insert(0, './app')
from app import import_libraries, util
from util import *
from import_libraries import *

def add_to_db(q_id, date_incoming, date_outgoing, question, ans, diff_level):
    ans = ans.replace(" ","_")    
    if q_id not in difficulty:
        difficulty[q_id]=[]
    difficulty[q_id].append({
                                    
                                        "Timestamp_frontend":date_incoming, 
                                        "Timestamp_backend": date_outgoing, 
                                        "difficulty":diff_level,
                                        
                                    })
    
  
difficulty_classifier = Blueprint('difficulty_classifier', __name__)
@difficulty_classifier.route("/classify", methods=["POST"])
def classify():
    """
    Parameters
    ----------
    None

    Returns
    --------
    returns a json of the following format:
    {
        "difficulty": "Hard/Easy/Error"
    }
    
    """
    if request.method == "POST":
        question = request.form.get("text")
        ans = request.form.get("answer_text")
        date_incoming = request.form.get("date")
        q_id = request.form.get("qid")
    start = time.time()
    inputs = tokenizer_difficulty(question, return_tensors="pt")
    outputs = model_difficulty(**inputs)
    logits = outputs.logits.detach().cpu().numpy()
    difficulty = np.argmax(logits).flatten()
    end = time.time()
    print("----TIME (s) : /difficulty_classifier/classify---",end - start)
    date_outgoing = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    date_outgoing.replace(', 00',', 24')
    if(difficulty == 0):
        add_to_db(q_id, date_incoming, date_outgoing, question, ans, "Easy")
        return jsonify({"difficulty": "Easy"})
    elif (difficulty == 1):
        add_to_db(q_id, date_incoming, date_outgoing, question, ans, "Hard")
        return jsonify({"difficulty": "Hard"})
    add_to_db(q_id, date_incoming, date_outgoing, question, ans, "Error")
    return jsonify({"difficulty": "error"})
    