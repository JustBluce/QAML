import sys

sys.path.append("..")
sys.path.insert(0, "./app")
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
    array_of_words = [i for i in array_of_words if i]
    return array_of_words


def get_pretrained_tfidf_vectorizer():
    """

    Parameters
    ----------
    None

    Returns
    --------
    tf-idf vectorizer from qanta

    """
    with open("./model/model.pickle", "rb") as f:
        params = pickle.load(f)

    vectorizer = params["tfidf_vectorizer"]
    Matrix = params["tfidf_matrix"]
    ans = params["i_to_ans"]
    return vectorizer, Matrix, ans


def get_pronunciation_models():
    """

    Parameters
    ----------
    None

    Returns
    --------
    tf-idf vectorizer on pronunciation
    Logistic regression classifier

    """
    # TODO pronunciation_tf-idf.pickle
    with open("./model/pronunciation_models/pronunciation_tf-idf.pickle", "rb") as f:
        pron_vectorizer = pickle.load(f)
    with open(
        "./model/pronunciation_models/pronunciation_regression.pickle", "rb"
    ) as f1:
        pron_regression = pickle.load(f1)
    with open("./model/pronunciation_models/word_freq.pickle", "rb") as f2:
        pron_word_freq = pickle.load(f2)
    return pron_vectorizer, pron_regression, pron_word_freq


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
    model_difficulty = DistilBertForSequenceClassification.from_pretrained(
        './model/difficulty_models/DistilBERT_full_question')
    tokenizer_difficulty = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    return tokenizer_difficulty, model_difficulty


class Highlight(object):
    """
    Name:                   highlight
    Author:                 CaiZefan
    Required parameters:    text, keywords
    Optional parameters:    color, count
    Function:               Follow the number given by the parameter count to highlight the first few keywords.
                            If parameter count is not given, then the function will highlight every keyword.
    Example:
                            text="I have an apple. I have 3 apples."
                            keywords=["apple"]
                            highlight=Highlight()
                            highlight_text=highlight.highlight_text(text=text, keywords=keywords, color="yellow", count=1)
                            highlight_text='<font color="#333333"><strong style="background:yellow"><em></em></strong></font>I have an apple. I have 3 apples.'
    """

    def __init__(self, **kw):
        self.iText = ""
        self.iKeywords = []
        self.iColor = "red"
        self.iCount = 0
        if "text" in kw:
            self.iText = kw["text"]
        if "keywords" in kw:
            self.iKeywords = kw["keywords"]

    def highlight_text(self, text, keywords, **kw):
        self.iText = text
        self.iKeywords = keywords
        if "color" in kw:
            self.iColor = kw["color"]
        if "count" in kw:
            self.iCount = kw["count"]
        for iKeyword in self.iKeywords:
            self.iText = re.sub(
                iKeyword,
                '<mark class="' + self.iColor + '">' + iKeyword + "</mark>",
                self.iText,
                count=self.iCount,
            )
        # print(highlight_text)
        print(self.iText)
        return self.iText


# def highlight_json(items = None, color = None):
#     '''
#     Organize the json structure for text highlighting in frontend
#     highlight: [
#         { text: "American", style: "background-color:#f37373" },
#         { text: "India", style: "background-color:#f37373" },
#         { text: "Jack", style: "background-color:#fff05e" },
#         { text: "Mary", style: "background-color:#fff05e" },
#       ],
#     '''
#     highlight = []
#     for item in items:
#         temp = {}
#         temp['text'] = item
#         temp['style'] = "background-color:"+color
#         highlight.append(temp)
#     return highlight


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
    # model_name = "bert-large-uncased-whole-word-masking-finetuned-squad"
    model_name = "distilbert-base-cased-distilled-squad"
    tokenizer_country = AutoTokenizer.from_pretrained(model_name, do_lower_case=True)
    model_country = AutoModelForPreTraining.from_pretrained(
        model_name, output_attentions=False, output_hidden_states=True
    )
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
    model = BertForSequenceClassification.from_pretrained(
        "./model/genre_classifier_models/BERT_genre_classifier", num_labels=11
    )
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
    model = BertForSequenceClassification.from_pretrained(
        "./model/genre_classifier_models/Science_Genre_classifier", num_labels=4
    )
    return model


def load_pron_model_pronunciation():
    model_name = "./model/pronunciation_models/pronunciation"
    tokenizer_pronunciation = AutoTokenizer.from_pretrained(
        "squeezebert/squeezebert-uncased", do_lower_case=True
    )
    model_pronunciation = AutoModelForSequenceClassification.from_pretrained(
        "./model/pronunciation_models/pronunciation-squeezebert", num_labels=2
    )
    return tokenizer_pronunciation, model_pronunciation


tokenizer_difficulty, model_difficulty = load_bert_model_difficulty()
params = get_pretrained_tfidf_vectorizer()
tokenizer_country, model_country = load_bert_country_model()
pron_vectorizer, pron_regression, pron_word_freq = get_pronunciation_models()
# tokenizer_pronunciation, model_pronunciation = load_pron_model_pronunciation()

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


# Lets make the dictionaries global
country_represent_json = {}
state_country_represent_json = {}

machine_guess = {}
state_machine_guess = {}

difficulty = {}

pronunciation_dict = {}
state_pronunciation = {}

time_stamps = {}
questions_all_time_stamps = {}
ans_all_time_stamps = {}
similarity = {}
state_similarity = {}

buzzer = {}
state_buzzer = {}
# Raj: Might synchronize using locks
# This is when I will access using the following method: 
modules_responsible = {}
