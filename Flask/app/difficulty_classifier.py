# Atith
# Description of this file: 
# 1. Finding the difficulty of each question based on education levels

import sys
sys.path.append("..")
sys.path.insert(0, './app')
from app import import_libraries, util
from util import *
from import_libraries import *

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
    start = time.time()
    inputs = tokenizer_difficulty(question, return_tensors="pt")
    outputs = model_difficulty(**inputs)
    logits = outputs.logits.detach().cpu().numpy()
    difficulty = np.argmax(logits).flatten()
    end = time.time()
    print("----TIME (s) : /difficulty_classifier/classify---",end - start)
    if(difficulty == 0):
        return jsonify({"difficulty": "Easy"})
    elif (difficulty == 1):
        return jsonify({"difficulty": "Hard"})

    return jsonify({"difficulty": "error"})
    