# Interface For Improving the Writing of Adversarial Quesitons

## Overview 

![GitHub language count](https://img.shields.io/github/languages/count/JustBluce/TryoutProject) 
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/JustBluce/TryoutProject?include_prereleases)

This project tries to create a Vue/Flask app which is able to answer the given input question on the quanta QA dataset(https://s3-us-west-2.amazonaws.com/pinafore-us-west-2/qanta-jmlr-datasets/qanta.train.2018.04.18.json).This project also tries to help question writers write more Adversarial quesitons.

Front end: Vue.js

Back end: Flask

Databased: mysql

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
```
- Edit the following file: `Flask/config.py` to use your mysql settings, change 'YOURPASSWORD' to the password you set up earlier

```
mysql+pymysql://root:YOURPASSWORD@localhost:3306/QA?charset=utf8
```

### Model Files
- Run https://github.com/Pinafore/qanta-codalab locally and you will get `qanta-codalab/src/tfidf.pickle`
- Remove and rename `qanta-codalab/src/tfidf.pickle` to `TRYOUT-PROJECT/Flask/model/model.pickle`

### Vue.js ( 2.6.14 )
- Follow [this]https://vuejs.org/v2/guide/installation.html link to install vue.js
- We recommend using `npm install` as your instalation method

### Python Packages
- `cd Flask`
- `pip3 install -r requirements.txt`



## Running the Code

Run the below commands in the terminal for running the code:

### Run the Flask App (Back End)

1. Navigate to the root directory
2. ``cd Flask ``
3. `` python run.py``
4. Download pre-trained BERT_full_question model from [here](https://drive.google.com/drive/folders/18dGwaxI7kx4Yx7gTMTiCbUv2YLxzNPmZ?usp=sharing) and move it to model/difficulty_models/ folder
5. If the model/difficulty_models/ does not exsist feel free to add the proper folders


### Run the Vue Framework (Front End)

6. Navigate to the root directory
7. ``cd Vue``
8. ``npm install``
9. ``npm run dev``



