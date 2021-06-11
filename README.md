# Interface-TryoutProject

- This project tries to create a Vue/Flask app which is able to answer the given input question on the quanta QA dataset(https://s3-us-west-2.amazonaws.com/pinafore-us-west-2/qanta-jmlr-datasets/qanta.train.2018.04.18.json).
- The framework used on the front end is Vue.
- The framework used on the back end is Flask.
- The method I used is tf-idf, because it is easy to implement and achieves relatively good results. After the model has been called, it pre-process the real question, filter part of the questions using the inverted table, use the tf_idf vectors of the real question and the filtered question list for cosine similarity calculation, and then use the priority queue to find the most similar answer to the question.

## Steps to run the code

Run the below commands in the terminal for running the code:
Run the Flask app:

1. **cd Flask**
2. **python run.py**
   Run the Vue framework:
3. **cd Vue**
4. **npm install**
5. **npm run dev**

## Results

- I have recorded the test results in the form and attached it to the attachment, which contains questions, correct answers, and answers given by the app. And there are some patterns in the test results of answering questions.
  - Shorter text input is more likely to lead to incorrect answers
  - The lack of key information is more likely to lead to wrong answers. For example, in line 20 of the table file, the part about Engels was deleted from the question about Karl Marx, causing the model to give the wrong answer

## Conclusion

- I am planing to add more interactive content to guide people to use the interface.
- Although tf-idf is not perfect at the moment, the amount of calculations it take is small, making the computation time short. As a result, it is easy to implement and works relatively well.
- I am considering using the attention mechanism, the transformer framework and BertForQuestionAnswering to implement the Q&A system.
- The reason why I haven't used bert yet is that I'm worried that the amount of calculations and the length of time that bert takes will make the user experience worse
