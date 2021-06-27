import pandas as pd
from ethnicolr import census_ln, pred_census_ln, pred_wiki_ln

def find_ethnicity(name): 
    names = [
    {'name': name}]
    df = pd.DataFrame(names)

    # print(census_ln(df, 'name'))
    return pred_wiki_ln(df, 'name')['race'][0] 