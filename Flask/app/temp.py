# <<<_____ASK ATITH______>>>
import json
f = open('qanta.json')
data = json.load(f)

genre = {}
for i in range(0, len(data['questions'])):
  if data['questions'][i]['category'] in genre.keys():
    genre[data['questions'][i]['category']] = genre[data['questions'][i]['category']] + 1
  else:
    genre[data['questions'][i]['category'] ] = 1

with open('genre.json', 'w') as fp:
    json.dump(genre, fp)


