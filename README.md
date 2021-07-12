# Interface For Improving the Writing of Adversarial Quesitons

## Overview 

![GitHub repo size](https://img.shields.io/github/repo-size/JustBluce/TryoutProject?logo=Files&logoColor=white&style=for-the-badge)
![Lines of code](https://img.shields.io/tokei/lines/github/JustBluce/TryoutProject?color=royalblue&logo=Visual%20Studio%20Code&style=for-the-badge)

![GitHub language count](https://img.shields.io/github/languages/count/JustBluce/TryoutProject?color=lightgreen&style=for-the-badge) 
![GitHub contributors](https://img.shields.io/github/contributors/JustBluce/TryoutProject?color=lightgreen&style=for-the-badge)


This project tries to create a Vue/Flask app which is able to answer the given input question on the quanta QA [dataset](https://s3-us-west-2.amazonaws.com/pinafore-us-west-2/qanta-jmlr-datasets/qanta.train.2018.04.18.json). This project also tries to help question writers write more Adversarial quesitons.

Front end: Vue.js

Back end: Flask

Database: MySQL

## Preparations

### MySQL
- Install mysql in your computer with the guide https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/
  - pip uninstall mysql (or whatever other package you installed that way)
  - Visit https://dev.mysql.com/downloads/mysql/ and download proper mysql
  - Go through the setup process and REMEMBER your password(will be used later)
- Set up your database
  - open terminal
```
mysql -u root -p
CREATE DATABASE questions;
USE questions;
create table QA (id int auto_increment primary key, Question varchar(255) null, Answer varchar(255) null);
create table user_inf (User varchar(255) null, Password varchar(255) null);
```
- Edit the following file: `Flask/config.py` to use your mysql settings, change 'YOURPASSWORD' to the password you set up earlier

```
mysql+pymysql://root:YOURPASSWORD@localhost:3306/QA?charset=utf8
```

### Model Files
- Run https://github.com/Pinafore/qanta-codalab locally and you will get `qanta-codalab/src/tfidf.pickle`
- Remove and rename `qanta-codalab/src/tfidf.pickle` to `TRYOUT-PROJECT/Flask/model/model.pickle`
- Download the following [BERT_genre_classifier](https://drive.google.com/drive/folders/1lqVosgCPhRVH4A2m3bIaPdo5Ghggl9pQ?usp=sharing) and place it in TryoutProject\Flask\model\genre_classifier_models\BERT_genre_classifier folder. 
- Download the following [Science_Genre_Classifier](https://drive.google.com/drive/folders/15cGe--BEXq3wnhEfV1dQSaDJ4P5jocjw?usp=sharing) and place it in TryoutProject\Flask\model\genre_classifier_models\Science_Genre_Classifier

### Vue.js ( 2.6.14 )
- Follow [this](https://vuejs.org/v2/guide/installation.html) link to install vue.js
- We recommend using `npm install` as your instalation method

### Python Packages

We recomend that use a seperate Conda envorinment or pipenv environment for installing packages, however this is only a reconmendation. 

- `cd Flask`
- `pip3 install -r requirements.txt`
- `python -m spacy download en_core_web_sm`



## Running the Code

Run the below commands in the terminal for running the code:

### Run the Flask App (Back End)

1. Navigate to the root directory
2. ``cd Flask ``
3. Download pre-trained **BERT_full_question** model from [here](https://drive.google.com/drive/folders/18dGwaxI7kx4Yx7gTMTiCbUv2YLxzNPmZ?usp=sharing) and move it to model/difficulty_models/ folder
4. If the model/difficulty_models/ does not exsist feel free to add the proper folders
5. `` python run.py``


### Run the Vue Framework (Front End)

6. (In a seperate terminal) Navigate to the root directory
7. ``cd Vue``
8. ``npm install``
9. ``npm run dev``

## Examples

https://user-images.githubusercontent.com/37555910/124949034-38e27b80-dfdf-11eb-9279-b9530c7bf893.mov






