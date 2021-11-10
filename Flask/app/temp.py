# <<<_____ASK ATITH______>>>
# import json
# f = open('qanta.json')
# data = json.load(f)

# genre = {}
# for i in range(0, len(data['questions'])):
#   if data['questions'][i]['category'] in genre.keys():
#     genre[data['questions'][i]['category']] = genre[data['questions'][i]['category']] + 1
#   else:
#     genre[data['questions'][i]['category'] ] = 1

# with open('genre.json', 'w') as fp:
#     json.dump(genre, fp)
import json

f_pop = open('app/entity.json')
wiki_population = json.load(f_pop)

print(wiki_population)
# import json 
# import pickle
# with open('C:\\Users\\User\\Downloads\\people_freq.pickle', 'rb') as f:
#   x = pickle.load(f)

# with open("app\\entity.json", "w") as outfile:
#     json.dump(x, outfile)


