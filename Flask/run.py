from flask import Flask
from app import app
import sys
import os
os.environ['TRANSFORMERS_CACHE'] = '/fs/clip-quiz/saptab1/AdvWrite/cache'
os.environ['HF_DATASETS_CACHE'] = '/fs/clip-quiz/saptab1/AdvWrite/cache'
os.environ["TOKENIZERS_PARALLELISM"] = "false"

if(len(sys.argv)==1):
    port_num = 7600
else:
    port_num = int(sys.argv[1])


@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin'] = '*'
    environ.headers['Access-Control-Allow-Method'] = '*'
    environ.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return environ


if __name__ == '__main__':
    app.run(debug=False, port = port_num)
