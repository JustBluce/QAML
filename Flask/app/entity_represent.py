# By Raj and Atith

# Description of this file: 
# 1. Finding underrepresented entities with respect to the question and answer both.
import sys

from numpy.lib.function_base import insert
sys.path.append("..")
sys.path.insert(0, './app')

from app import util, import_libraries
from util import *
from import_libraries import *

import spacy
  
nlp = spacy.load('en_core_web_sm')
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
            entity_name, score
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
        tokenized_text, tokens_tensor, segments_tensors = bert_text_preparation(text, tokenizer_entity)
        list_token_embeddings = get_bert_embeddings(tokens_tensor, segments_tensors, model_entity)
        tweet_embedding = np.mean(np.array(list_token_embeddings), axis=0)
        target_tweet_embeddings.append(tweet_embedding)
    return target_tweet_embeddings

# Precomputationskir
nlp = en_core_web_sm.load()
stopWords = stopwords.words('english')
f = open('app/qanta.json')
data = json.load(f)['questions']

questions = []
for i in range(0, len(data)):
    questions.append(data[i]['text'])

f_pop = open('app/wiki_entities.json')
wiki_population = json.load(f_pop)

f_pop = open('app/entity_vectors.json')
entities_vector = json.load(f_pop)

entities =  [key for key,value in wiki_population.items() ]
no_instances =  [value for key,value in wiki_population.items() ]
total_instance = sum(wiki_population.values())

entity_represent = Blueprint('entity_represent', __name__)
# f_entity = open('app/entity.json')
# map_instance = json.load(f_entity)
# total_instance = sum(map_instance.values())

under_entities = []
ner_under_entities = []
over_entities = []
current_over_entities = {}
current_under_entities = {}
prev_under_entities = {}
prev_over_entities = {}
suggested_entities = {}

i = 0
for entity in entities:
    # if entity in question.lower():
    # if len(list(filter(lambda x: x['entityLabel'].lower() == entity.lower(), wiki_population))) != 0:
    if wiki_population[entity] <  total_instance/len(entities) and len(entity.split()[0]) > 4 :
        under_entities.append(entity)
        # if (len(nlp(entity).ents)) != 0:
        #     ner_under_entities.append(entity)
        i = i + 1
    else:
        over_entities.append(entity)

# print(len(under_entities))
# entities_vector = vectorize_albert(under_entities)
answer = []



def insert_into_db(q_id, date_incoming, date_outgoing, question, ans, edit_message, added_under_represented_entities, removed_over_represented_entities, added_over_represented_entities):
    ans = ans.replace(" ","_")
    if q_id not in entity_represent_json:
        entity_represent_json[q_id]=[]
        
    # added_change_in_over_represented_entities = list(set(current_over_entities)-set(prev_over_entities))
    # change_in_over_represented_entities = list(set(current_over_entities)-set(prev_over_entities))
    entity_represent_json[q_id].append({
                                "edit_history":
                                            {
                                                "added_under_represented_entities": added_under_represented_entities,
                                                "removed_over_represented_entities": removed_over_represented_entities,
                                                "added_over_represented_entities" : added_over_represented_entities
                                            },
                                "Timestamp_frontend":date_incoming, 
                                "Timestamp_backend": date_outgoing,
                                "edit_message" : edit_message,
                                "current_over_entities": current_over_entities[q_id],
                                "current_under_entities": current_under_entities[q_id],
                                "suggested_entities": suggested_entities[q_id] 
                                
                            })



@entity_represent.route("/entity_present", methods=["POST"])
def entity_present():
    """

    Parameters
    ----------
    None
    Returns
    --------
    Json object of the following format is returned:
    {
        "entity_representation": 
            {
                "entity": entity_name, "Score": Cosine_Similarity
            }
        "entity": List of entities and their populations according to wikipedia.
    }
    Prints
    --------
    The time taken of the two sub-modules in the terminal:
    1. entity Represent
    """
    if request.method == "POST":
        question = request.form.get("text")
        ans = request.form.get("answer_text")
        date_incoming = request.form.get("date")
        q_id = request.form.get("qid")
        if q_id not in current_under_entities:
            current_over_entities[q_id] = []
            current_under_entities[q_id] = []
            prev_under_entities[q_id] = []
            prev_over_entities[q_id] = []
            suggested_entities[q_id] = []
    start = time.time()
    message = ''
    question_vector = vectorize_albert([question])
    cosine_sim_ques_entity = []
    # print(ans)
    # if ans == "":
    #     return jsonify({"entity_representation": "", "entity": ""})
    prev_over_entities[q_id] = current_over_entities[q_id]
    prev_under_entities[q_id] = current_under_entities[q_id]
    current_over_entities[q_id] = []
    insert_db_flag = 0
    if q_id not in entity_represent_json:
        insert_db_flag = 1
    added_over_represented_entities = []
    removed_over_represented_entities = []
    added_under_represented_entities = []
    # try :
    page = wikipedia.page("\""+ans+"\"")
    # print("Title = ", page.title)
    related_entities = get_related_entities(page.title)
    # for i in range(len(related_entities)):
    #     if over_entities[i].lower().split()[0] in question.lower():
    #         current_over_entities[q_id].append(over_entities[i].lower())
    #         if over_entities[i].lower() not in prev_over_entities[q_id]: 
    #             added_over_represented_entities.append(over_entities[i].lower())
    #             insert_db_flag = 1
    #     elif over_entities[i].lower().split()[0] not in question.lower() and over_entities[i].lower() in prev_over_entities[q_id]: 
    #         insert_db_flag = 1
    #         removed_over_represented_entities.append(over_entities[i].lower())
        
    
    current_under_entities[q_id] = []
    for i in range(len(related_entities)):
        # b = " ".join(x for x in i)
        # if len(related_entities[i].lower().split()) >= 2 and len(related_entities[i].lower().split()[1]) > 4 and under_entities[i].lower().split()[1] in question.lower(): 
        if related_entities[i] in under_entities:
            if related_entities[i].lower() in question.lower(): 
                if related_entities[i] in suggested_entities[q_id]:
                    insert_db_flag = 1
                    added_under_represented_entities.append(related_entities[i])
                # print(related_entities[i])
                current_under_entities[q_id].append(related_entities[i].lower())

            # if len(related_entities[i].lower().split()) >= 2 and len(under_entities[i].lower().split()[1]) > 4 and under_entities[i].lower().split()[0] not in question.lower() and  under_entities[i].lower() in page.content.lower():
            if related_entities[i].lower() not in question.lower():
                idx = page.content.lower().find(related_entities[i].lower())
                if (idx == -1 and len(related_entities[i].lower().split())>=1):
                    idx = page.content.lower().find(related_entities[i].lower().split()[0])
                if (idx == -1 and len(related_entities[i].lower().split())>=2):
                    idx = page.content.lower().find(related_entities[i].lower().split()[1])
                if (idx == -1 and len(related_entities[i].lower().split())>=3):
                    idx = page.content.lower().find(related_entities[i].lower().split()[2])
                if idx != -1:
                    sub_part = page.content[max(idx-300, 0) : min(idx + 300, len(page.content) - 1)]
                   # print(related_entities[i])
                   # print(entities_vector[related_entities[i]])
                    cosine_sim_ques_entity.append([related_entities[i], 1 - cosine(question_vector[0], entities_vector[related_entities[i]]), sub_part ])
                # print(related_entities[i])

        elif related_entities[i] in over_entities:
            if related_entities[i].lower().split()[0] in question.lower():
                current_over_entities[q_id].append(related_entities[i].lower())
                if related_entities[i].lower() not in prev_over_entities[q_id]: 
                    added_over_represented_entities.append(related_entities[i].lower())
                    insert_db_flag = 1
            elif related_entities[i].lower().split()[0] not in question.lower() and over_entities[i].lower() in prev_over_entities[q_id]: 
                insert_db_flag = 1
        
    message = Sort(cosine_sim_ques_entity)
    
    answer.clear()
    suggested_entities[q_id] = []
    for i in message[:5]:
        answer.append({"answer": i[0], "Score":i[1], "text": i[2]})
        suggested_entities[q_id].append(i[0])
    # print('Message', message)
    if insert_db_flag == 1:
        date_outgoing = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        edit_message = ''
        if(len(added_under_represented_entities) != 0):
            edit_message = edit_message  + 'The under-represented entities "' + ' '.join(added_under_represented_entities) + '" was added on the basis of suggestion. '
        if(len(removed_over_represented_entities) != 0):
            edit_message = edit_message + 'The over-represented entities "' + ' '.join(removed_over_represented_entities) + '" was removed by the user. '
        if(len(added_over_represented_entities) != 0):
            edit_message = edit_message + 'The over-represented entities "' + ' '.join(added_over_represented_entities) + '" was added by the user.'
        insert_into_db(q_id, date_incoming, date_outgoing, question, ans, edit_message, added_under_represented_entities, removed_over_represented_entities, added_over_represented_entities)
        # print(entity_represent_json)
    # except: 
    #     message = "Couldn't find a related wikipedia article"
    end = time.time()
    entity_representation = answer
    # print(entity_representation)
    
    # print(current_over_entities[q_id])
    print("----TIME (s): /entity_represent/entity_present---", end - start)
    return jsonify({"entity_representation": entity_representation, "entity": entities, "current_over_entities" : [" " + x for x in current_over_entities[q_id]] + [" " + x.capitalize() for x in current_over_entities[q_id]]})

# def entity_present1(question):
# <<<------DEPRECIATED------>>>
#     start = time.time()
#     message = ''
#     # print(total_instance)
#     under_entities = []
#     over_entities = []
#     entities = []
#     for entity in map_instance.keys():
#         if entity in question.lower():
#             entities.append(entity)
#             if len(list(filter(lambda x: x['entityLabel'].lower() == entity.lower(), wiki_population))) != 0:
#                 if map_instance[entity.lower()]/total_instance < int(list(filter(lambda x: x['entityLabel'].lower() == entity.lower(), wiki_population))[0]['population'])/sum(population):
#                     under_entities.append(entity)
#                 else:
#                     over_entities.append(entity)
#     if len(under_entities) != 0:
#         message = message + 'The entity ' + \
#             ', '.join(under_entities) + \
#             ' in the question is/are from underrepresented group. The author will get 10 extra points. \n'
#     else:
#         message = message + 'The entity ' + \
#             ', '.join(over_entities) + ' in the question is/are from overrepresented group. The author can next time write question having underrepresented entities to earn extra points. \n'
#     end = time.time()
#     print("----TIME (s): /entity_represent/entity_present---", end - start)
#     entity_representation=message
#     return entity_representation, over_entities
