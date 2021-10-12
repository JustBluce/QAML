# By Raj and Atith

# Description of this file: 
# 1. Finding underrepresented countries with respect to the question and answer both.
import sys

from numpy.lib.function_base import insert
sys.path.append("..")
sys.path.insert(0, './app')

from app import util, import_libraries
from util import *
from import_libraries import *

def guess(question, max=12):
    """

    Parameters
    ----------
    question: This contains a list of the strings containing the trivia question(s).
    max: The top max number of results to be considered for ranking.
    Returns
    --------
    answer[0][0]: Retrieves the top max number of guesses from the tf-idf model in the following format: tuple ("name_of_wikipedia_document", confidence_score)
    """
    answer = []
    repre = vectorizer.transform(question)
    matrix = Matrix.dot(repre.T).T
    indices = (-matrix).toarray().argsort(axis=1)[:, 0:max]
    for i in range(len(question)):
        answer.append([(ans[j], matrix[i, j]) for j in indices[i]])
    return answer[0][0]

def break_into_words_with_capital(question):
    """

    Parameters
    ----------
    question: This contains the string of containing the trivia question.

    Returns
    --------
    Separates a string in the following manner and returns a list:
    Hello, How areYou -> ["Hello", ",", "How", "are", "You"]

    """
    array_of_words =re.split('(?=[A-Z]| )', question)
    return list(filter(None, [x.strip() for x in array_of_words])) 



def bert_text_preparation(text, tokenizer):
    """
    Preparing the input for BERT

    Takes a string argument and performs
    pre-processing like adding special tokens,
    tokenization, tokens to ids, and tokens to
    segment ids. All tokens are mapped to seg-
    ment id = 1.
    Parameters
        text (str): Text to be converted
        tokenizer (obj): Tokenizer object
            to convert text into BERT-re-
            adable tokens and ids
    Returns
        list: List of BERT-readable tokens
        obj: Torch tensor with token ids
        obj: Torch tensor segment ids
    """
    marked_text = "[CLS] " + text + " [SEP]"
    tokenized_text = tokenizer.tokenize(marked_text)
    indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
    segments_ids = [1]*len(indexed_tokens)

    # Convert inputs to PyTorch tensors
    tokens_tensor = torch.tensor([indexed_tokens])
    segments_tensors = torch.tensor([segments_ids])

    return tokenized_text, tokens_tensor, segments_tensors

def get_bert_embeddings(tokens_tensor, segments_tensors, model):
    """Get embeddings from an embedding model
    Args:
        tokens_tensor (obj): Torch tensor size [n_tokens]
            with token ids for each token in text
        segments_tensors (obj): Torch tensor size [n_tokens]
            with segment ids for each token in text
        model (obj): Embedding model to generate embeddings
            from token and segment ids
    Returns:
        list: List of list of floats of size
            [n_tokens, n_embedding_dimensions]
            containing embeddings for each token
    """
    with torch.no_grad():
        outputs = model(tokens_tensor, segments_tensors)
        hidden_states = outputs.hidden_states[1:]

    token_vecs = hidden_states[0]
    sentence_embedding = torch.mean(token_vecs, dim=0)
    return sentence_embedding

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
    Sorted list of lists in the descending order on the basis of score
    """
    # reverse = None (Sorts in Ascending order)
    # key is set to sort using second element of
    # sublist lambda has been used
    return(sorted(sub_li, key=lambda x: x[1], reverse=True))

def vectorize_albert(texts):
    """

    Parameters
    ----------
    texts: a list of strings to obtain the bert embeddings for.
    Returns
    --------
    target_tweet_embeddings: A list containing the embeddings for each string in the list texts.
    """
    target_tweet_embeddings = []
    for text in texts:
        text = " ".join([word for word in break_into_words_with_capital(text) if word not in stopWords])
        tokenized_text, tokens_tensor, segments_tensors = bert_text_preparation(text, tokenizer_country)
        list_token_embeddings = get_bert_embeddings(tokens_tensor, segments_tensors, model_country)
        tweet_embedding = np.mean(np.array(list_token_embeddings), axis=0)
        target_tweet_embeddings.append(tweet_embedding)
    return target_tweet_embeddings

# Precomputations
nlp = en_core_web_sm.load()
stopWords = stopwords.words('english')
f = open('app/qanta.json')
data = json.load(f)['questions']

questions = []
for i in range(0, len(data)):
    questions.append(data[i]['text'])


f_pop = open('app/query.json')
wiki_population = json.load(f_pop)

countries = list(map(lambda x: x['countryLabel'].lower(), wiki_population))
population = list(map(lambda x: int(x['population']), wiki_population))

country_represent = Blueprint('country_represent', __name__)
f_country = open('app/country.json')
map_instance = json.load(f_country)
total_instance = sum(map_instance.values())

under_countries = []
over_countries = []
current_over_countries = {}
current_under_countries = {}
prev_under_countries = {}
prev_over_countries = {}
suggested_countries = {}
for country in map_instance.keys():
    # if country in question.lower():
    if len(list(filter(lambda x: x['countryLabel'].lower() == country.lower(), wiki_population))) != 0:
        if map_instance[country.lower()]/total_instance < int(list(filter(lambda x: x['countryLabel'].lower() == country.lower(), wiki_population))[0]['population'])/sum(population):
            under_countries.append(country)
        else:
            over_countries.append(country)
countries_vector = vectorize_albert(under_countries)
answer = []



def insert_into_db(q_id, date_incoming, date_outgoing, question, ans, edit_message, added_under_represented_countries, removed_over_represented_countries, added_over_represented_countries):
    ans = ans.replace(" ","_")
    if q_id not in country_represent_json:
        country_represent_json[q_id]=[]
        
    # added_change_in_over_represented_countries = list(set(current_over_countries)-set(prev_over_countries))
    # change_in_over_represented_countries = list(set(current_over_countries)-set(prev_over_countries))
    country_represent_json[q_id].append({
                                "edit_history":
                                            {
                                                "added_under_represented_countries": added_under_represented_countries,
                                                "removed_over_represented_countries": removed_over_represented_countries,
                                                "added_over_represented_countries" : added_over_represented_countries
                                            },
                                "Timestamp_frontend":date_incoming, 
                                "Timestamp_backend": date_outgoing,
                                "edit_message" : edit_message,
                                "current_over_countries": current_over_countries[q_id],
                                "current_under_countries": current_under_countries[q_id],
                                "suggested_countries": suggested_countries[q_id] 
                                
                            })



@country_represent.route("/country_present", methods=["POST"])
def country_present():
    """

    Parameters
    ----------
    None
    Returns
    --------
    Json object of the following format is returned:
    {
        "country_representation": 
            {
                "Country": Country_name, "Score": Cosine_Similarity
            }
        "country": List of countries and their populations according to wikipedia.
    }
    Prints
    --------
    The time taken of the two sub-modules in the terminal:
    1. Country Represent
    """
    if request.method == "POST":
        question = request.form.get("text")
        ans = request.form.get("answer_text")
        date_incoming = request.form.get("date")
        q_id = request.form.get("qid")
        if q_id not in current_under_countries:
            current_over_countries[q_id] = []
            current_under_countries[q_id] = []
            prev_under_countries[q_id] = []
            prev_over_countries[q_id] = []
            suggested_countries[q_id] = []
    start = time.time()
    message = ''
    question_vector = vectorize_albert([question])
    cosine_sim_ques_country = []
    # print(ans)
    # if ans == "":
    #     return jsonify({"country_representation": "", "country": ""})
    prev_over_countries[q_id] = current_over_countries[q_id]
    prev_under_countries[q_id] = current_under_countries[q_id]
    current_over_countries[q_id] = []
    insert_db_flag = 0
    if q_id not in country_represent_json:
        insert_db_flag = 1
    added_over_represented_countries = []
    removed_over_represented_countries = []
    added_under_represented_countries = []
    try :
        page = wikipedia.page("\""+ans+"\"")
        
        for i in range(len(over_countries)):
            if over_countries[i].lower() in question.lower():
                current_over_countries[q_id].append(over_countries[i].lower())
                if over_countries[i].lower() not in prev_over_countries[q_id]: 
                    added_over_represented_countries.append(over_countries[i].lower())
                    insert_db_flag = 1
            elif over_countries[i].lower() not in question.lower() and over_countries[i].lower() in prev_over_countries[q_id]: 
                insert_db_flag = 1
                removed_over_represented_countries.append(over_countries[i].lower())
            
        
        current_under_countries[q_id] = []
        for i in range(len(under_countries)):
            # b = " ".join(x for x in i)
            if under_countries[i].lower() in question.lower(): 
                
                if under_countries[i].lower() in suggested_countries[q_id]:
                    insert_db_flag = 1
                    added_under_represented_countries.append(under_countries[i].lower())
                
                current_under_countries[q_id].append(under_countries[i].lower())

            if under_countries[i].lower() not in question.lower() and under_countries[i].lower() in page.content.lower():
                idx = page.content.lower().find(under_countries[i].lower())
                sub_part = page.content[max(idx-300, 0) : min(idx + 300, len(page.content) - 1)]
                cosine_sim_ques_country.append([under_countries[i], 1 - cosine(question_vector[0], countries_vector[i]), sub_part ])
    
        message = Sort(cosine_sim_ques_country)

        answer = []
        suggested_countries[q_id] = []
        for i in message[:5]:
            answer.append({"answer": i[0], "Score":i[1], "text": i[2]})
            suggested_countries[q_id].append(i[0])
        
        if insert_db_flag == 1:
            date_outgoing = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            edit_message = ''
            if(len(added_under_represented_countries) != 0):
                edit_message = edit_message  + 'The under-represented countries "' + ' '.join(added_under_represented_countries) + '" was added on the basis of suggestion. '
            if(len(removed_over_represented_countries) != 0):
                edit_message = edit_message + 'The over-represented countries "' + ' '.join(removed_over_represented_countries) + '" was removed by the user. '
            if(len(added_over_represented_countries) != 0):
                edit_message = edit_message + 'The over-represented countries "' + ' '.join(added_over_represented_countries) + '" was added by the user.'
            insert_into_db(q_id, date_incoming, date_outgoing, question, ans, edit_message, added_under_represented_countries, removed_over_represented_countries, added_over_represented_countries)
            # print(country_represent_json)
    except: 
        message = "Couldn't find a related wikipedia article"
    end = time.time()
    # print(current_over_countries[q_id])
    print("----TIME (s): /country_represent/country_present---", end - start)
    return jsonify({"country_representation": answer, "country": countries, "current_over_countries" : [" " + x for x in current_over_countries[q_id]] + [" " + x.capitalize() for x in current_over_countries[q_id]]})

# def country_present1(question):
# <<<------DEPRECIATED------>>>
#     start = time.time()
#     message = ''
#     # print(total_instance)
#     under_countries = []
#     over_countries = []
#     countries = []
#     for country in map_instance.keys():
#         if country in question.lower():
#             countries.append(country)
#             if len(list(filter(lambda x: x['countryLabel'].lower() == country.lower(), wiki_population))) != 0:
#                 if map_instance[country.lower()]/total_instance < int(list(filter(lambda x: x['countryLabel'].lower() == country.lower(), wiki_population))[0]['population'])/sum(population):
#                     under_countries.append(country)
#                 else:
#                     over_countries.append(country)
#     if len(under_countries) != 0:
#         message = message + 'The country ' + \
#             ', '.join(under_countries) + \
#             ' in the question is/are from underrepresented group. The author will get 10 extra points. \n'
#     else:
#         message = message + 'The country ' + \
#             ', '.join(over_countries) + ' in the question is/are from overrepresented group. The author can next time write question having underrepresented countries to earn extra points. \n'
#     end = time.time()
#     print("----TIME (s): /country_represent/country_present---", end - start)
#     country_representation=message
#     return country_representation, over_countries