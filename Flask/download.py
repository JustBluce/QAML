# Created by Damian Rene
import requests
from tqdm import tqdm
import os


def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

## List of top level directories
parent_dir = "./model/"
directories = ['difficulty_models','pronunciation_models' ]

for directory in tqdm(directories):
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)
    print("Directory '% s' created" % directory)


## List of second level directories
directories = ['difficulty_models/DistilBERT_full_question']

for directory in tqdm(directories):
    path = os.path.join(parent_dir, directory)
    os.makedirs(path)
    print("Directory '% s' created" % directory)



##Names MUST match file ids in order
file_ids = ['1k1akEuLpW02tfZ-ApValJwlcxJji-riO','1-Povi368FMzWRVRXowS9DsrZLWcQBq1S','1-SjMB3dne0FnLX7HZwGih3HVkPaTYHug','16fb-dRHVRxK0JgUW8cT6zOSepIaikbEL','16fb-dRHVRxK0JgUW8cT6zOSepIaikbEL','1PzZMWm_jcJdz22TDvKI5MbBr9RBJKgLa' ]
destinations = ['./model/model.pickle','./model/difficulty_models/DistilBERT_full_question/config.json','./model/difficulty_models/DistilBERT_full_question/pytorch_model.bin','./model/pronunciation_models/pronunciation_regression.pickle','./model/pronunciation_models/pronunciation_tf-idf.pickle','./model/pronunciation_models/word_freq.pickle' ]


for i in tqdm(range(len(file_ids))):
    id = file_ids[i]
    dest = destinations[i]
    download_file_from_google_drive(id, dest)

print("downloads complete!")

