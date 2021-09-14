#Damian and Raj
import sys

from nltk.corpus.reader import wordlist
sys.path.append("..")
sys.path.insert(0, './app')
from app import util, import_libraries
from util import *
from import_libraries import *

from os.path import join, dirname



authenticator = IAMAuthenticator('Xqq84EWoiOAtKLuKcsA9OUtsekbXDBCgS7FLi2EnNV7i')
speech_to_text = SpeechToTextV1(
    authenticator=authenticator
)

speech_to_text.set_service_url('https://api.us-east.speech-to-text.watson.cloud.ibm.com/instances/21d86f7c-04ec-4029-bef1-abb1ba6586cb')

class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_data(self, data):
        print(json.dumps(data, indent=2))

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))
    


def checktexts():
    """
    
    Parameters
    ----------
    None


    Returns
    --------
    Compare new and old txt files and return score

    """
    question_text = open("question.txt").read()
    speech_text = open("speech-text.txt").read()
    m = SequenceMatcher(None, question_text, speech_text)
    decimal = m.ratio()
    percentage = decimal * 100
    as_string = str(percentage)
    print("RATIO OF DIFFERENCE: %s" % as_string)
    return percentage



def break_into_character_n_grams(word, n = 4):
    """
    
    Parameters
    ----------
    None


    Returns
    --------
    String made of joined N grams:
    Example
    for 3- grams

    Modernity -> "mod ode der ern nit ity"

    """
    if(len(word)<n):
        return word
    return " ".join([word[i:i+n] for i in range(len(word)-n+1)])

def Sort(sub_li):
    """
    
    Parameters
    ----------
    sub_li: A list of lists of the following format
    [
        [
            country_name, score
        ]
    ]

    Returns
    --------
    Sorted list of lists in the ascending order on the basis of score
    """
    return(sorted(sub_li, key = lambda x: x[1], reverse = False))   

def classify(list_of_words):
    """
    
    Parameters
    ----------
    list of words

    Returns
    --------
    list of hard to pronounce words
    """
    ans = []
    ## ---------------------
    
    ## ---------------------
    new_list_of_words = []
    indices_of_new_list_of_words = []
    for i in range(len(list_of_words)):
        if re.sub(r'[^\w\s]', '', list_of_words[i].lower()) not in pron_word_freq:
            new_list_of_words.append(re.sub(r'[^\w\s]', '', list_of_words[i].lower()))
            indices_of_new_list_of_words.append(i)
            continue
        elif pron_word_freq[re.sub(r'[^\w\s]', '', list_of_words[i].lower())]<10:
            new_list_of_words.append(re.sub(r'[^\w\s]', '', list_of_words[i].lower()))
            indices_of_new_list_of_words.append(i)
            continue
    # arr = [break_into_character_n_grams(i,4) for i in new_list_of_words]
    # for i in range(len(arr)):
    #     inputs = tokenizer_pronunciation(arr[i], return_tensors="pt")
    #     outputs = model_pronunciation(**inputs)
    #     logits = outputs.logits.detach().cpu().numpy()
    #     pronunciation_output = np.argmax(logits).flatten()
    #     if(pronunciation_output == 1):
    #         ans.append({"Word":list_of_words[indices_of_new_list_of_words[i]]})
    
    # print(new_list_of_words)
    if len(new_list_of_words)>0:
        predictions = pron_regression.predict(pron_vectorizer.transform([break_into_character_n_grams(i,4) for i in new_list_of_words]))
    else:
        return ans, []
    # print(predictions)
    word_list = []
    for i in range(len(predictions)):
        if predictions[i] == 1:
            ans.append({"Word":list_of_words[indices_of_new_list_of_words[i]]})
            word_list.append(new_list_of_words[i])
    
    return ans, word_list
    
pronunciation = Blueprint('pronunciation', __name__)
myRecognizeCallback = MyRecognizeCallback()

r = sr.Recognizer()
#question = request.form.get("text")
vectorizer, Matrix, ans = params[0], params[1], params[2]

def add_to_db(q_id, date_incoming, date_outgoing, ret_value, word_list, question, ans):
    ans = ans.replace(" ","_") 
    if q_id not in pronunciation_dict:
        pronunciation_dict[q_id]=[]
    if q_id not in state_pronunciation:
        state_pronunciation[q_id]= []
    # print(set(word_list))
    # print(set(state_pronunciation[q_id]))
    list_B = []
    if set(word_list)!= set(state_pronunciation[q_id]):   
        set_A = set(word_list)
        set_B = set(state_pronunciation[q_id])
        list_A = list(set_A.difference(set_B))
        list_B = list(set_B.difference(set_A))
        pronunciation_dict[q_id].append({
                                    "edit_history":
                                    {
                                        "new_words_added_to_pronunciation": list_A,
                                        "old_words_removed_from_pronunication": list_B
                                    },
                                    "Timestamp_frontend":date_incoming, 
                                    "Timestamp_backend": date_outgoing, 
                                    "word_2_pronounce":ret_value,
                                    
                                    })
        state_pronunciation[q_id] = word_list
    return list_B
@pronunciation.route('/get_pronunciation', methods=["POST"])
def getpronuncation():
    """
    Depreciated
    
    Parameters
    ----------
    None

    Returns
    --------
    List of words 
    """
    if request.method == "POST":
        question = request.form.get("text")
        ans = request.form.get("answer_text")
        date_incoming = request.form.get("date")
        q_id = request.form.get("qid")

    start = time.time()
    # question = question.replace("-"," ")
    array_of_words = break_into_words(question)
    if(len(array_of_words)==0):
        jsonify({"message": ""})
    
    ret_value, word_list = classify(array_of_words)
    # for i in range(len(ret_value)):
    #     ret_value[i]["Word"] = re.sub(r'[^\w\s]','',ret_value[i]["Word"])

    end = time.time()
    print("----TIME (s) : /pronunciation/get_pronunciation---", end - start)
    date_outgoing = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    date_outgoing.replace(', 00',', 24')
    list_of_words_to_remove = []
    if len(word_list)>0:
        list_of_words_to_remove = add_to_db(q_id, date_incoming, date_outgoing, ret_value, word_list, question, ans)
    else:
        if q_id in state_pronunciation:
            list_of_words_to_remove = state_pronunciation[q_id]
    # print(list_of_words_to_remove)
    list_of_words_to_remove = list_of_words_to_remove + [x.capitalize() for x in list_of_words_to_remove]
    return jsonify({"message": ret_value, "list_of_words_to_remove":list_of_words_to_remove})


# def getpronunciation():
#     """
#     Depreciated
    
#     Parameters
#     ----------
#     None

#     Returns
#     --------
#     {
#         "pronunciation":
#         [
#             {
#             "Original Word",
#             "Transcribed Word",
#             "Score of Transcribed Word"
#             },
#             ...
#         ]
#         "message": "This question needs a pronunciation guide"
#     }
#     """
#     if request.method == "POST":
#         question = request.form.get("text")

#     start = time.time()
#     if not question:
#         return jsonify({"pronunciation": [{"Word": "-", "Score":"-"}], "message":""})

#     # question = " " + question
#     language = 'en'
#     myobj = gTTS(text=question, lang=language, slow=False)
#     myobj.save("app/pronunciation.mp3")
    
# #     # question_file = open("app/question.txt","w")
# #     # question_file.write(str(question))
# #     # question_file.close()
    

#     with open(join(dirname(__file__), './.', "pronunciation.mp3"),'rb') as audio_file:
#         speech_recognition_results = speech_to_text.recognize(
#             audio=audio_file,
#             content_type='audio/mp3',
#             word_alternatives_threshold=0.9,
#             word_confidence = True
#         ).get_result()
    
#     transcribed_text = speech_recognition_results["results"][0]["alternatives"][0]["transcript"]
#     confidence = speech_recognition_results["results"][0]["alternatives"][0]["confidence"]
#     array_of_word_confidence = []
#     for i in speech_recognition_results["results"][0]["alternatives"][0]["word_confidence"]:
#         array_of_word_confidence.append([i[0],i[1]])

#     repre = vectorizer.transform([question])
#     repre_transcribed = vectorizer.transform([transcribed_text])
#     # print(repre)
#     matrix = repre.dot(repre_transcribed.T).T
#     cosine_similarity = matrix.toarray()[0][0]
#     temp_word_array = break_into_words(question)
#     while("" in temp_word_array) :
#         temp_word_array.remove("")
#     print(temp_word_array)
#     print(array_of_word_confidence)
#     count = 0
#     array = []
#     print("similarity =", cosine_similarity)
#     for i in range(len(array_of_word_confidence)):
#         array.append([ array_of_word_confidence[i][0], array_of_word_confidence[i][1]])
#     most_difficult_to_pronounce_words = Sort(array)[:3]
#     answer = []
#     for i in range(len(most_difficult_to_pronounce_words)):
#         answer.append({"Transcribed_Word": most_difficult_to_pronounce_words[i][0], "Score":most_difficult_to_pronounce_words[i][1]})
#     end = time.time()
#     print("----TIME (s) : /pronunciation/get_pronunciation---", end - start)
#     if(cosine_similarity < threshold_pronunciation):
#         return jsonify({"pronunciation": answer,"message": "This question needs a pronunciation guide"})
#     else:
#         return jsonify({"pronunciation": answer,"message": "No pronunciation guide needed"})

    
#     return jsonify({"pronunciation": [{"Word": "-", "Score":"-"}],"message": ""})
