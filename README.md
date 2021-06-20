# Interface-TryoutProject

- This project tries to create a Vue/Flask app which is able to answer the given input question on the quanta QA dataset(https://s3-us-west-2.amazonaws.com/pinafore-us-west-2/qanta-jmlr-datasets/qanta.train.2018.04.18.json).
- The framework used on the front end is Vue.
- The framework used on the back end is Flask.
- The databased used is mysql.

## Preparations

- Install mysql in your computer
- Use the sql file `QA_QA.sql` to set up your database
- Write `Flask/config.py` to use your mysql settings
- Run https://github.com/Pinafore/qanta-codalab locally and you will get `qanta-codalab/src/tfidf.pickle`
- Remove and rename `qanta-codalab/src/tfidf.pickle` to `TRYOUT-PROJECT/Flask/model/model.pickle`

## Steps to run the code

Run the below commands in the terminal for running the code:

### Run the Flask app

1. **cd Flask**
2. **python run.py**
3. **pip install -r requirements.txt**
4. **Download pre-trained BERT_full_question model from [here](https://drive.google.com/drive/folders/18dGwaxI7kx4Yx7gTMTiCbUv2YLxzNPmZ?usp=sharing) and move it to model/difficulty_models/  folder**
### Run the Vue framework
5. **cd Vue**
6. **npm install**
7. **npm run dev**

## Tips

- The Vue code for interface is `Vue/src/views/friends/test6/index.vue`
- We can create new interface in `Vue/src/views` and register this interface in the navigation bar in `Vue/router/index.js`
- The Flask code for answering questions, storing data and calling the model is `Flask/app/func.py`
- If you want to connect the Vue to Flask, youneed to ensure that the web request method is set correctly.
- Vue file

```javascript
this.axios({
        url: "http://127.0.0.1:5000/func/act",
        method: "POST",
        data: formData,
        // header:{
        //   'Content-Type':'application/json'  //如果写成contentType会报错
        // }
      }).then((response) => {
        this.returndata = response.data;
        this.answer = response.data["guess"];
        console.log(response);
        console.log(this.text);
        console.log(this.answer);
      });
```

- Flask file

```Python
@func.route('/act', methods=['POST'])
def act():
    if request.method == 'POST':
        question = request.form.get('text')
    answer = guess(question=[question])

    sql = "insert into QA (Question, Answer) VALUES ('"+question+"', '"+answer +"'); "
    result_sql=db.session.execute(sql)

    return jsonify({'guess': answer})
```

## Results

- I have recorded the test results in the form and attached it to the attachment, which contains questions, correct answers, and answers given by the app. And there are some patterns in the test results of answering questions.
  - Shorter text input is more likely to lead to incorrect answers
  - The lack of key information is more likely to lead to wrong answers. For example, in line 20 of the table file, the part about Engels was deleted from the question about Karl Marx, causing the model to give the wrong answer

## Conclusion

- I am planing to add more interactive content to guide people to use the interface.
- Although tf-idf is not perfect at the moment, the amount of calculations it take is small, making the computation time short. As a result, it is easy to implement and works relatively well.
- I am considering using the attention mechanism, the transformer framework and BertForQuestionAnswering to implement the Q&A system.
- The reason why I haven't used bert yet is that I'm worried that the amount of calculations and the length of time that bert takes will make the user experience worse
