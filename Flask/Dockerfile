# use python container image
FROM python:3.7-stretch

LABEL author="damianrene@cs.umd.edu"

COPY . /Flask
WORKDIR /Flask
RUN pip3 install nltk
RUN python3 -m nltk.downloader stopwords
RUN python3 -m nltk.downloader punkt
RUN pip3 install -r requirements.txt
EXPOSE 5000
EXPOSE 3306
CMD ["python3", "run.py"]
