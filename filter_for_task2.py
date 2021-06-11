import pandas as pd
import sys
import nltk
import utils
import json

"""
Commmand : python filter_specific_or_general.py <path to csv file>

This script removes questions that have a single answer or ask distance/time related questions that do not have a single right answer.
"""
def digit_exist(val):
    nums = ['0','1','2','3','4','5','6','7','8','9']
    for n in nums:
        if n in val:
            return True
    return False

def main():
    path = sys.argv[1]
    print(">>> Reading file " + path)
    df = pd.read_csv(path, header='infer')
    
    print(">>> Filtering answers that have same worker answers")
    df_ = df.copy()
    df_['worker_answer'] = df_['worker_answer'].apply(utils.normalized_text).apply(utils.lemmatize_text).apply(' '.join)
    df_['tmp'] = 1
    df_ = df_.groupby(['context_sentence', 'question', 'worker_answer']).agg(['count']).reset_index()
    df_ = df_[df_[('tmp','count')]>1][['context_sentence','question']].drop_duplicates()
    df_same = df.merge(df_, on=['context_sentence','question'], how='inner')
    df_diff = df[~((df.context_sentence.isin(df_same.context_sentence))&(df.question.isin(df_same.question)))]
    print(df_same.shape[0], ' annotations were filtered.\n')

    print(">>> Filtering answers that have numerical values")
    df_ = df_diff.copy()
    df_['contains_number'] = df_.apply(lambda x: digit_exist(x['worker_answer']),axis=1)
    df_ = df_[df_['contains_number']][['context_sentence','question']].drop_duplicates()
    df_cnum = df_diff.merge(df_, on=['context_sentence','question'], how='inner')
    df_dcnum = df_diff[~((df_diff.context_sentence.isin(df_cnum.context_sentence))&(df_diff.question.isin(df_cnum.question)))]
    print(df_cnum.shape[0], 'more annotations were filtered.\n')
    out_path = path[:-4]
    print(">>> Writing the filtered annotations")
    df_out = pd.concat([df_same,df_cnum])
    df_out.to_csv(out_path+'_filtered.csv', index=False)
    print(">>> Writing the remaining annotations")
    df_dcnum.to_csv(out_path+'_remaining.csv', index=False)






if __name__ == "__main__":
    main()