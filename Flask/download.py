# Created by Damian Rene
# NEED TO ACTIVATE PROPER CONDA ENV FIRST OR ALL PACKAGES WILL INSTALL IN CURRENT ENV

import os
import subprocess
import time

downloads = True

##Definition of colors
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))


print("***************************")
prCyan("For the best experience we reccomend that you create a new anaconda environment and activate it before running this script.")
print("\n \n Y - To Continue" , end =' ' )
print("\n N - Stop Installation \n")
print("*************************** \n")

input = input("Your response: ")





if input.lower() == "y":


    ## Create Conda env and activate 
    ##subprocess.run(['conda create --name QAML python=3.9', 'conda activate QAML'], shell=True)

    ## install python pacakages required for download script
    prRed("Installing required python packages")
    subprocess.run(['pip install requests tqdm'], shell=True)
    import requests
    from tqdm import tqdm
    



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






    #Check if in Right Directory
    parent = os.getcwd()
    directory = parent[-5:]
    ##print(directory)

    if directory == 'Flask':
        prRed("Current Directory = FLASK")


        ## List of top level directories
        parent_dir = "./model/"
        directories = ['difficulty_models','pronunciation_models' ]

        for directory in directories:
            path = os.path.join(parent_dir, directory)
            os.mkdir(path)
            prRed("Directory '% s' created" % directory)


        ## List of second level directories
        directories = ['difficulty_models/DistilBERT_full_question']

        for directory in directories:
            path = os.path.join(parent_dir, directory)
            os.makedirs(path)
            prRed("Directory '% s' created" % directory)



        ##Names MUST match file ids in order
        file_ids = ['1k1akEuLpW02tfZ-ApValJwlcxJji-riO','1-Povi368FMzWRVRXowS9DsrZLWcQBq1S','1-SjMB3dne0FnLX7HZwGih3HVkPaTYHug','16fb-dRHVRxK0JgUW8cT6zOSepIaikbEL','16fb-dRHVRxK0JgUW8cT6zOSepIaikbEL','1PzZMWm_jcJdz22TDvKI5MbBr9RBJKgLa' ]
        destinations = ['./model/model.pickle','./model/difficulty_models/DistilBERT_full_question/config.json','./model/difficulty_models/DistilBERT_full_question/pytorch_model.bin','./model/pronunciation_models/pronunciation_regression.pickle','./model/pronunciation_models/pronunciation_tf-idf.pickle','./model/pronunciation_models/word_freq.pickle' ]


        for i in tqdm(range(len(file_ids))):
            id = file_ids[i]
            dest = destinations[i]
            download_file_from_google_drive(id, dest)

        #Install requirements.txt and Spacy
        subprocess.run(['pip install -r requirements.txt'], shell=True)
        subprocess.run('python -m spacy download en_core_web_sm', shell = True)

    else:
        downloads = False
        prRed ("Error: Wrong Directory ")






    ## Change directory to VUE
    parent = os.path.dirname(os.getcwd())
    os.chdir(parent)
    directory = os.path.join(os.getcwd() + '/Vue')
    directory = directory[-3:]


    ## Install VUE Components
   #if directory == "Vue":
    #    prRed("Current Direcgtory = VUE")
    #    commands = ['npm install', 'npm install -g @vue/cli', 'npm install -g vue@2.6.14']
    #    for i in tqdm(commands):
    #        subprocess.run(i, shell=True)
   # else:
    #    downloads = False
    #    prRed("Error: Wrong Directory")



print()
for directory in tqdm(directories):
    path = os.path.join(parent_dir, directory)
    os.makedirs(path)
    print("Directory '% s' created" % directory)


    ##Check if successfull
    if downloads == True:
        prRed("downloads complete!")
    else: 
        prRed("Downloads Failed!")



else: 
    prRed("\n Goodbye!")


