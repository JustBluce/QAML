import sys
sys.path.append("..")
sys.path.insert(0, './app')
from app import import_libraries
from import_libraries import *
threshold_buzz = 0.2
threshold_similar = 0.5
threshold_pronunciation = 0.4



def colored(r, g, b, text):
    """
    Function to print with color in terminal
    Parameters
    ----------
    r: amount of red,
    g: amount of green,
    b: amount of blue,
    text: text to print in color

    Returns
    --------
    string with necessary suffixes and prefixes for color

    """
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255".format(r, g, b, text)


def break_into_sentences(question):
    """
    Function to break a string into a list of sentences
    Parameters
    ----------
    question: string containing the question

    Returns
    --------
    list of strings(sentences)

    """
    array_of_sentences_in_question = nltk.tokenize.sent_tokenize(question)
    return array_of_sentences_in_question


def break_into_words(question):
    """
    Function to break a string into a list of words
    Parameters
    ----------
    question: string containing the question

    Returns
    --------
    list of strings(words)

    """
    array_of_words = question.split(' ')
    return array_of_words


def get_pretrained_tfidf_vectorizer():
    """
    
    Parameters
    ----------
    None

    Returns
    --------
    tf-idf vectorizer

    """
    with open("./model/model.pickle", "rb") as f:
        params = pickle.load(f)

    vectorizer = params["tfidf_vectorizer"]
    Matrix = params["tfidf_matrix"]
    ans = params["i_to_ans"]
    return vectorizer, Matrix, ans


def guess_top_n(question, params, max=12, n=3):
    """
    Parameters
    ----------
    question: This contains a list of the strings containing the trivia question(s).
    max: The top max number of results to be considered for ranking.
    n: number of top guesses to return.
    params: tf-idf vectorizer to use

    Returns
    --------
    answer[0][0:n]: Retrieves the top n guesses from the tf-idf model in the following format: tuple ("name_of_wikipedia_document", confidence_score)

    """
    vectorizer, Matrix, ans = params[0], params[1], params[2]
    answer = []
    repre = vectorizer.transform(question)
    matrix = Matrix.dot(repre.T).T
    indices = (-matrix).toarray().argsort(axis=1)[:, 0:max]
    for i in range(len(question)):
        answer.append([(ans[j], matrix[i, j]) for j in indices[i]])
    return answer[0][0:n]

def guess_top_1(question, params, max=12, n=1):
    """
    Parameters
    ----------
    question: This contains a list of the strings containing the trivia question(s).
    max: The top max number of results to be considered for ranking.
    params: tf-idf vectorizer to use

    Returns
    --------
    answer[0][0:n]: Retrieves the top 1 guesses from the tf-idf model in the following format: tuple ("name_of_wikipedia_document", confidence_score)

    """
    vectorizer, Matrix, ans = params[0], params[1], params[2]
    answer = []
    repre = vectorizer.transform(question)
    matrix = Matrix.dot(repre.T).T
    indices = (-matrix).toarray().argsort(axis=1)[:, 0:max]
    for i in range(len(question)):
        answer.append([[ans[j], matrix[i, j]] for j in indices[i]])
    return answer[0][0:n]


def load_bert_model_difficulty():
    """
    
    Parameters
    ----------
    None

    Returns
    --------
    Bert model and tokenizer of difficulty of questions

    """
    model_difficulty = BertForSequenceClassification.from_pretrained(
        './model/difficulty_models/BERT_full_question')
    tokenizer_difficulty = BertTokenizer.from_pretrained('bert-base-uncased')
    return tokenizer_difficulty, model_difficulty


def highlight_json(items = None, color = None):
    '''
    Organize the json structure for text highlighting in frontend
    highlight: [
        { text: "American", style: "background-color:#f37373" },
        { text: "India", style: "background-color:#f37373" },
        { text: "Jack", style: "background-color:#fff05e" },
        { text: "Mary", style: "background-color:#fff05e" },
      ],
    '''
    highlight = []
    for item in items:
        temp = {}
        temp['text'] = item
        temp['style'] = "background-color:"+color
        highlight.append(temp)
    return highlight

def load_bert_country_model():
    """
    
    Parameters
    ----------
    None

    Returns
    --------
    Bert model and tokenizer of country underrepresentation module

    """
    # model_name = "bert-base-multilingual-uncased"
    model_name = "bert-large-uncased-whole-word-masking-finetuned-squad"
    from transformers import AutoTokenizer,AutoModelForSequenceClassification, AutoModelForPreTraining
    tokenizer_country = AutoTokenizer.from_pretrained(model_name, do_lower_case=True)
    model_country = AutoModelForPreTraining.from_pretrained(model_name, output_attentions=False, output_hidden_states=True)
    return tokenizer_country, model_country

def load_genre_model():
    """
    
    Parameters
    ----------
    None

    Returns
    --------
    Bert model and tokenizer for genre classifier

    """
    model = BertForSequenceClassification.from_pretrained('./model/genre_classifier_models/BERT_genre_classifier', num_labels = 11)
    return model

def load_science_genre_model():
    """
    
    Parameters
    ----------
    None

    Returns
    --------
    Bert model and tokenizer for science sub-genre classifier

    """
    model = BertForSequenceClassification.from_pretrained('./model/genre_classifier_models/Science_Genre_classifier', num_labels = 4)
    return model


tokenizer_difficulty, model_difficulty = load_bert_model_difficulty()
params = get_pretrained_tfidf_vectorizer()
tokenizer_country, model_country = load_bert_country_model()

sub_genres = {
            'Philosophy': [['Norse', 354], ['Other', 345], ['Philosophy', 5], ['European', 3], ['American', 2], ['Religion/Mythology', 1]],
            'History' : [['American', 3514], ['World', 3103], ['European', 3100], ['British', 685], ['Classical', 607], ['Ancient', 345], ['Other', 541], ['Classic', 105], ['Norse', 48], ['Geography', 2], ['Religion/Mythology', 1]],
            'Literature': [[ 'American', 3463], ['European', 3194], ['British', 2052], ['World', 1934], ['Europe', 421],  ['Other', 629], ['Classical', 249], ['Classic', 58], ['Norse', 40], ['Language Arts', 19], ['Religion/Mythology', 1], ['Pop Culture', 1], ['Art', 1]],
            'Mythology': [[ 'Norse', 365], ['Religion/Mythology', 15], ['American', 6], ['Greco-Roman', 2], ['Earth Science', 1], ['Japanese', 1], ['Music', 1]],
            'Current Events' : [['None', 362]],
            'Religion': [['Norse', 318], ['Religion/Mythology', 6], ['Other', 377], ['American', 3], ['East Asian', 2], ['Ancient', 1], ['World', 1]],
            'Trash' : [['Pop Culture', 349], ['Norse', 313], ['Other', 545], ['American', 5], ['World', 1], ['Movies', 1], ['Classic', 1]],
            'Social Science': [['Religion/Mythology', 1017], ['Philosophy', 540], ['Geography', 480], ['None', 322], ['Psychology', 203], ['Economics', 172], ['Anthropology', 154], ['Norse', 100],  ['Other', 77], ['World', 1], ['Language Arts', 1], ['American', 1], ['European', 1]],
            'Science': [['Biology', 2727], ['Physics', 2413], ['Chemistry', 2281], ['Math', 1268], ['Other', 1523], ['Computer Science', 297], ['Astronomy', 204], ['Earth Science', 157], ['Norse', 71], ['Religion/Mythology', 1], ['Psychology', 1], ['Pop Culture', 1], ['World', 1]],
            'Fine Arts': [['Visual', 1980], ['Auditory', 1233], ['Other', 1400], ['Music', 1039], ['Audiovisual', 769], ['Art', 587], ['Norse', 7], ['American', 2]],
            'Geography': [['Norse', 238], ['Other', 287], ['Geography', 15], ['World', 3], ['American', 1]]

        }
genres = ['Philosophy', 'History', 'Literature', 'Mythology', 'Current Events', 'Religion', 'Trash', 'Social Science', 'Science', 'Fine Arts', 'Geography']



