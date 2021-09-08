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
    feature_names = vectorizer.get_feature_names()
    return vectorizer, Matrix, ans, feature_names



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


def guess_top_n(question, params, max=5, n=3):
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
    # start=time.time()
    vectorizer, Matrix, ans = params[0], params[1], params[2]
    answer = []
    repre = vectorizer.transform(question)
    matrix = Matrix.dot(repre.T).T
    indices = (-matrix).toarray().argsort(axis=1)[:, 0:max]
    for i in range(len(question)):
        answer.append([(ans[j], matrix[i, j]) for j in indices[i]])
    # end = time.time()
    # print("__________________TEST____________________",end-start)
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

# def ld(s1, s2):  # Levenshtein Distance word level
#     len1 = len(s1)+1
#     len2 = len(s2)+1
#     lt = [[0 for i2 in range(len2)] for i1 in range(len1)]  # lt - levenshtein_table
#     lt[0] = list(range(len2))
#     i = 0
#     for l in lt:
#         l[0] = i
#         i += 1
#     for i1 in range(1, len1):
#         for i2 in range(1, len2):
#             if s1[i1-1] == s2[i2-1]:
#                 v = 0
#             else:
#                 v = 1
#             lt[i1][i2] = min(lt[i1][i2-1]+1, lt[i1-1][i2]+1, lt[i1-1][i2-1]+v)
#     return lt[-1][-1]


def merge_stop_words(s1):
  s1_new = []
  i = 0
  while i < len(s1):
      # print(i,s1)
      t1 = s1[i]

      if s1[i] in stop_words:
        temp1 = i
        for j in range(temp1+1, len(s1)):
          if s1[j] in stop_words:
            t1 = t1+" "+s1[j]
            i = j
          else:
            i = j-1
            break
      
      s1_new.append(t1)
      i = i+1
      # print(t1, i)
  return s1_new

def ld(s1, s2):  # Levenshtein Distance word level
    stop_words = set(stopwords.words('english'))
    for i in range(len(s1)):
        s1[i] = re.sub(r'([^\w\s])', ' '+ r'\1', s1[i])
    for i in range(len(s2)):
        s2[i] = re.sub(r'([^\w\s])', ' '+ r'\1', s2[i])
    # s1 = merge_stop_words(s1)
    # s2 = merge_stop_words(s2)
    # reverse_1 = [i for i in reversed(s1) if not i.lower() in stop_words]
    # reverse_2 = [i for i in reversed(s2) if not i.lower() in stop_words]
    reverse_1 = [i for i in reversed(s1)]
    reverse_2 = [i for i in reversed(s2)]
    word_tok = ""
    steps = []
    # print(s1,s2)
    for i in reverse_1:
      for j in reverse_2: 
        if i == j:
          word_tok = j
          break
      if (word_tok != ""):
        break
    # print(word_tok)
    if (word_tok != ""):
      len1 = len(s1) + 2 - 1 - s1[::-1].index(word_tok)
      len2 = len(s2) + 2 - 1 - s2[::-1].index(word_tok)
      
    else:
      len1 = len(s1)+1
      len2 = len(s2)+1

    # print(len1, len2)
    addition = len(s2) + 1 - len2
    removal = len(s1) + 1 - len1
    word_list_removal = []
    word_list_addition = []
    if addition == 0:
      word_list_addition = []
    else:
      word_list_addition = s2[-addition:]
    if removal == 0:
      word_list_removal = []
    else:
      word_list_removal = s1[-removal:]
    # print(word_list_addition, word_list_removal)
    if len(s1)==0 and len(s2)==0:
      return 0 + len(word_list_addition) + len(word_list_removal), [], []
    elif len(s1)==0:
      return 0 + len(word_list_addition) + len(word_list_removal), word_list_addition, s2 
    elif len(s2)==0:
      return 0 + len(word_list_addition) + len(word_list_removal), s1, word_list_removal 
    lt = [[0 for i2 in range(len2)] for i1 in range(len1)]  # lt - levenshtein_table
    lt[0] = list(range(len2))
    i = 0
    for l in lt:
        l[0] = i
        i += 1
    for i1 in range(1, len1):
        for i2 in range(1, len2):
            if s1[i1-1] == s2[i2-1]:
                v = 0
            else:
                v = 1
            lt[i1][i2] = min(lt[i1][i2-1]+1, lt[i1-1][i2]+1, lt[i1-1][i2-1]+v)
    
    i = len(lt)-1
    j = len(lt[0])-1
    remove = []
    add = []
    while i!=0 and j!=0:
      # print("step ----", s1[i-1],s2[j-1], i ,j)
      if s1[i-1] == s2[j-1]:
        i-=1
        j-=1
      else:
        if lt[i-1][j]<=lt[i-1][j-1] and lt[i-1][j] <= lt[i][j-1]:
          remove.append(s1[i-1])
          # print("removed: ", s1[i-1])
          steps.append((1,(j-1,j),s1[i-1]))
          i-=1
        elif lt[i][j-1]<=lt[i-1][j-1] and lt[i][j-1] <= lt[i-1][j]:
          add.append(s2[j-1])
          # print("added: ", s2[j-1])
          steps.append((3,j-1,s2[j-1]))
          j-=1
        else:
          
          remove.append(s1[i-1])
          # print("removed: ", s1[i-1])
          
          add.append(s2[j-1])
          # print("added: ", s2[j-1])
          steps.append((2,i-1,s1[i-1]))
          i-=1
          j-=1
    while (j!=0):
      # print("step ----")
      add.append(s2[j-1])
      # print("added: ", s2[j-1])
      steps.append((3,j-1,s2[j-1]))
      j-=1
    while(i!=0):
      # print("step ----")
      remove.append(s1[i-1])
      # print("removed: ", s1[i-1])
      steps.append((1,(j-1,j),s1[i-1]))
      i-=1
    # for x in lt:
      # print(*x, sep=' ')
    add = [i for i in reversed(add)] + word_list_addition
    remove = [i for i in reversed(remove)] + word_list_removal
    # print(word_list_addition,word_list_removal)
    remove_final = []
    add_final = []
    for i in remove:
      remove_final = remove_final + i.split()
    for i in add:
      add_final = add_final + i.split()
    word_list_addition_final = []
    for i in word_list_addition:
      word_list_addition_final = word_list_addition_final + i.split()
    word_list_removal_final = []
    for i in word_list_removal:
      word_list_removal_final = word_list_removal_final + i.split()
    return lt[-1][-1] + len(word_list_addition) + len(word_list_removal), add, remove, word_list_addition, word_list_removal, steps
    # return lt[-1][-1]+len(word_list_addition_final) + len(word_list_removal_final), add_final, remove_final


def recreate(s1, word_list_addition, word_list_removal, steps):
  len1 = len(s1)- len(word_list_addition)
  s2 = s1[:len1]
  # print(s2)
  for i in steps:
    if i[0]==1:
      s2.insert(i[1][1], i[2])

    elif i[0]==2:
      s2[i[1]] = i[2]
    elif i[0]==3:
      if (i[2] != s2.pop(i[1])):
        print("error i[0] = 3")
  s2 = s2 + word_list_removal
  return s2

def find_basic_diff(s1,s2):
  for i in range(len(s1)):
    s1[i] = re.sub(r'[^\w\s]', '', s1[i])
  for i in range(len(s2)):
    s2[i] = re.sub(r'[^\w\s]', '', s2[i])
  uniques1=set(s1)
  uniques2=set(s2)
  uniq = uniques1.union(uniques2)
  my_dict_1 = {}
  for i in s1:
    if i in my_dict_1:
      my_dict_1[i]=my_dict_1[i]+1
    else:
      my_dict_1[i]=1
  my_dict_2 = {}
  for i in s2:
    if i in my_dict_2:
      my_dict_2[i]=my_dict_2[i]+1
    else:
      my_dict_2[i]=1
  diff = 0
  remove = []
  add = []
  # print(list(uniq))
  # print(my_dict_1)
  # print(my_dict_2)
  for i in list(uniq):
    # print(add,remove)

    if i in my_dict_1:
      if i not in my_dict_2:
        diff+=my_dict_1[i]
        for j in range(my_dict_1[i]):
          remove.append(i)
    if i in my_dict_2:
      if i not in my_dict_1:
        diff+=my_dict_2[i]
        for j in range(my_dict_2[i]):
          add.append(i)
    if i in my_dict_1:
      if i in my_dict_2:
        if my_dict_1[i]>my_dict_2[i]:
          diff += my_dict_1[i]-my_dict_2[i]
          for j in range(my_dict_1[i]-my_dict_2[i]):
            remove.append(i)
        else:
          diff += my_dict_2[i]-my_dict_1[i]
          for j in range(my_dict_2[i]-my_dict_1[i]):
            add.append(i)
  return diff, add, remove    

tokenizer_difficulty, model_difficulty = load_bert_model_difficulty()
params = get_pretrained_tfidf_vectorizer()
tokenizer_country, model_country = load_bert_country_model()
pron_vectorizer, pron_regression, pron_word_freq = get_pronunciation_models()
# tokenizer_pronunciation, model_pronunciation = load_pron_model_pronunciation()

sub_genres = {
    "Philosophy": [
        ["Norse", 354],
        ["Other", 345],
        ["Philosophy", 5],
        ["European", 3],
        ["American", 2],
        ["Religion/Mythology", 1],
    ],
    "History": [
        ["American", 3514],
        ["World", 3103],
        ["European", 3100],
        ["British", 685],
        ["Classical", 607],
        ["Ancient", 345],
        ["Other", 541],
        ["Classic", 105],
        ["Norse", 48],
        ["Geography", 2],
        ["Religion/Mythology", 1],
    ],
    "Literature": [
        ["American", 3463],
        ["European", 3194],
        ["British", 2052],
        ["World", 1934],
        ["Europe", 421],
        ["Other", 629],
        ["Classical", 249],
        ["Classic", 58],
        ["Norse", 40],
        ["Language Arts", 19],
        ["Religion/Mythology", 1],
        ["Pop Culture", 1],
        ["Art", 1],
    ],
    "Mythology": [
        ["Norse", 365],
        ["Religion/Mythology", 15],
        ["American", 6],
        ["Greco-Roman", 2],
        ["Earth Science", 1],
        ["Japanese", 1],
        ["Music", 1],
    ],
    "Current Events": [["None", 362]],
    "Religion": [
        ["Norse", 318],
        ["Religion/Mythology", 6],
        ["Other", 377],
        ["American", 3],
        ["East Asian", 2],
        ["Ancient", 1],
        ["World", 1],
    ],
    "Trash": [
        ["Pop Culture", 349],
        ["Norse", 313],
        ["Other", 545],
        ["American", 5],
        ["World", 1],
        ["Movies", 1],
        ["Classic", 1],
    ],
    "Social Science": [
        ["Religion/Mythology", 1017],
        ["Philosophy", 540],
        ["Geography", 480],
        ["None", 322],
        ["Psychology", 203],
        ["Economics", 172],
        ["Anthropology", 154],
        ["Norse", 100],
        ["Other", 77],
        ["World", 1],
        ["Language Arts", 1],
        ["American", 1],
        ["European", 1],
    ],
    "Science": [
        ["Biology", 2727],
        ["Physics", 2413],
        ["Chemistry", 2281],
        ["Math", 1268],
        ["Other", 1523],
        ["Computer Science", 297],
        ["Astronomy", 204],
        ["Earth Science", 157],
        ["Norse", 71],
        ["Religion/Mythology", 1],
        ["Psychology", 1],
        ["Pop Culture", 1],
        ["World", 1],
    ],
    "Fine Arts": [
        ["Visual", 1980],
        ["Auditory", 1233],
        ["Other", 1400],
        ["Music", 1039],
        ["Audiovisual", 769],
        ["Art", 587],
        ["Norse", 7],
        ["American", 2],
    ],
    "Geography": [
        ["Norse", 238],
        ["Other", 287],
        ["Geography", 15],
        ["World", 3],
        ["American", 1],
    ],
}
genres = [
    "Philosophy",
    "History",
    "Literature",
    "Mythology",
    "Current Events",
    "Religion",
    "Trash",
    "Social Science",
    "Science",
    "Fine Arts",
    "Geography",
]


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

general_edit_history = {}
buzzer = {}
state_buzzer = {}
# Raj: Might synchronize using locks
# This is when I will access using the following method:
modules_responsible = {}
