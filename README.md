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

- Make sure that there is a mysql database installed in your computer.
  - cureently used version is 8.0.21
- If mysql hasn't been installed in your devoce, please install mysql in your computer with the [following guide](https://dev.mysql.com/doc/mysql-installation-excerpt/8.0/en/) choose the one for your operating system.

  - Or visit https://dev.mysql.com/downloads/mysql/ and download proper mysql
  - REMEMBER your password (will be used later)

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

- Download the following [model.pickle](https://drive.google.com/file/d/1k1akEuLpW02tfZ-ApValJwlcxJji-riO/view?usp=sharing) Unzip it and place it in TryoutProject\Flask\model folder.
- Download the following [BERT_genre_classifier](https://drive.google.com/drive/folders/1lqVosgCPhRVH4A2m3bIaPdo5Ghggl9pQ?usp=sharing) Unzip it and place it in TryoutProject\Flask\model\genre_classifier_models\BERT_genre_classifier folder.
- Download the following [Science_Genre_classifier](https://drive.google.com/drive/folders/15cGe--BEXq3wnhEfV1dQSaDJ4P5jocjw?usp=sharing) Unzip it and place it in TryoutProject\Flask\model\genre_classifier_models\Science_Genre_classifier

### Vue.js ( 2.6.14 )

Try:

```
npm install vue
npm install -g @vue/cli
npm install -g vue@2.6.14

```

If this does not work check out the guide below to try and install another way.

- Follow [this](https://vuejs.org/v2/guide/installation.html) link to install vue.js we recoomend the produciton version as it has proper warnings for development.

### Python Packages

We recomend that use a seperate Conda envorinment or pipenv environment for installing packages, however this is only a recommendation.

- `cd Flask`
- `pip3 install -r requirements.txt`
- `python -m spacy download en_core_web_sm`

## Running the Code

Run the below commands in the terminal for running the code:

### Run the Flask App (Back End)

1. Navigate to the root directory
2. `cd Flask `
3. Download pre-trained **BERT_full_question** model from [here](https://drive.google.com/drive/folders/18dGwaxI7kx4Yx7gTMTiCbUv2YLxzNPmZ?usp=sharing) and move it to model/difficulty_models/ folder
4. If the model/difficulty_models/ does not exsist feel free to add the proper folders
5. ` python run.py`

### Run the Vue Framework (Front End)

6. (In a seperate terminal) Navigate to the root directory
7. `cd Vue`
8. `npm install`
9. `npm run dev`

## Examples

(Coming soon)

## Setup Error

- no module named cython” error
  - Try: https://pastebin.com/bB849hZ3
  - Second try: Updating pip and setuptools
  - Third try: https://pastebin.com/8BrK4W80
    - Cython is a prerequisite for numpy I think, but a simple pip3 install cython should work