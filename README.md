# QAML
![GitHub repo size](https://img.shields.io/github/repo-size/JustBluce/TryoutProject?logo=Files&logoColor=white&style=for-the-badge)
![Lines of code](https://img.shields.io/tokei/lines/github/JustBluce/TryoutProject?color=royalblue&logo=Visual%20Studio%20Code&style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/JustBluce/TryoutProject?color=lightgreen&style=for-the-badge)
![GitHub contributors](https://img.shields.io/github/contributors/JustBluce/TryoutProject?color=lightgreen&style=for-the-badge)

QAML (*/ˈkæməl/*, **Q**uestion-writing **A**ided by **M**achine **L**earning) is an interface for adversarial question-writing enhanced by the [QANTA QA dataset](https://s3-us-west-2.amazonaws.com/pinafore-us-west-2/qanta-jmlr-datasets/qanta.train.2018.04.18.json).

Front end: Vue.js

Back end: Flask

Database: MySQL


## Preparations

1. Clone the Repo
2. cd into the repo in your terminal

### Model Files

Please try our new model download script first! If there are any problems, you can revert to installing them manually. 

With Script: 
```
cd Flask
pip install -r requirements.txt
python3 download.py
```
- Optional: use the `-t` or `--target` flag when running `pip` to specify path to directory where you want to install packages, and the `--cache-dir` flag to specify the package cache location

Without Script: 
- Download the following [model.pickle](https://drive.google.com/file/d/1k1akEuLpW02tfZ-ApValJwlcxJji-riO/view?usp=sharing) Place it in `QAML\Flask\model `
- Download the following [difficulty_classifier](https://drive.google.com/drive/folders/1-Le-JF5e9fPPnZT3VuukxHSNnnqqGPu4?usp=sharing) Unzip it and place it in `QAML\Flask\model\difficulty_models`
- Download the following and place ALL of them in `QAML\Flask\model\pronunciation_models\`
  -   [Pronunciation Regression.pickle](https://drive.google.com/file/d/16fb-dRHVRxK0JgUW8cT6zOSepIaikbEL/view?usp=sharing)
  -   [Pronunciation_tf-idf.pickle](https://drive.google.com/file/d/1hV9WO4Md5Ht_5HuzKtZu0fswnh--1ean/view?usp=sharing)
  -   [word_freq.pickle](https://drive.google.com/file/d/1PzZMWm_jcJdz22TDvKI5MbBr9RBJKgLa/view?usp=sharing)

Optional: to set the path for the model cache, define the `TRANSFORMERS_CACHE` environment variable

### Vue.js ( 2.6.14 )

```
npm install
```
- Optional: use the `--prefix` flag when running `npm install` to specify path to directory where you want to install packages, and use `npm config set cache` to specify the cache location

If this does not work check out the guide below to try and install another way.

- Follow [this](https://vuejs.org/v2/guide/installation.html) link to install vue.js we recommend the production version as it has proper warnings for development.

### Python Packages

We recomend that use a seperate Conda envorinment or pipenv environment for installing packages, however this is only a recommendation. 

(2.5 Gb needed)

If Conda:
- To install conda visit [this](https://www.anaconda.com/products/individual) link. 
- `conda create --name QAML python=3.9`
- `conda activate QAML`
- `cd Flask`
- `python3 -m spacy download en_core_web_sm`
- `pip3 install -r requirements.txt`

If no Conda: 
- `cd Flask`
- `python3 -m spacy download en_core_web_sm`
- `pip3 install -r requirements.txt`


## Running the Code

### Run the Flask App (Back End)

1. Navigate to the root directory
2. `cd Flask `
3. `python3 run.py`

### Run the Vue Framework (Front End)

4. (In a seperate terminal) Navigate to the root directory
5. `cd Vue`
6. `npm install`
7. `npm run dev`


## Setup Error

- no module named cython” error
  - Try: https://pastebin.com/bB849hZ3
  - Second try: Updating pip and setuptools
  - Third try: https://pastebin.com/8BrK4W80
    - Cython is a prerequisite for numpy I think, but a simple pip3 install cython should work
