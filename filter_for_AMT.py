import pandas as pd
import sys
import nltk
import utils
import json

"""
Commmand : python filter.py <path to csv file>
"""

def get_dataframe(path_with_filename):
    df = pd.read_csv(path_with_filename, header='infer')
    df['answer_json'] = df['Answer.taskAnswers'].str[1:-1]
    df['answer_json'] = df['answer_json'].apply(lambda x: json.loads(x))
    df['worker_answer'] = df['answer_json'].apply(lambda x: x['worker_answer'] if 'worker_answer' in x.keys() else "")
    df['worker_question'] = df['answer_json'].apply(
        lambda x: x['worker_question'] if 'worker_question' in x.keys() else "")
    df = df.drop(columns=['answer_json'])
    return df


def check_in_context(df):
    df['Input.context_sentence'] = df['Input.context_sentence'].str.lower()
    df['worker_answer'] = df['worker_answer'].str.lower()
    df['context_sentence_'] = df['Input.context_sentence'].apply(utils.lemmatize_text).apply(' '.join)
    df['worker_answer_'] = df['worker_answer'].apply(utils.lemmatize_text)
    df['Reject_indicator'] = df.apply(lambda x: utils.reject(x['worker_answer_'], x['context_sentence_']), axis=1)
    df['Reject'] = df['Reject_indicator'].apply(lambda x: "Some words of the answer text are in the context sentence or instructions. Please create a question whose answer is not in the context sentence. See examples of the task." if x else None)
    df = df.drop(columns=['context_sentence_', 'worker_answer_'])
    return df


def main():
    path = sys.argv[1]
    print(">>> Reading file " + path)
    df = get_dataframe(path)
    print(">>> Checking if the answer is in context sentence")
    df = check_in_context(df)
    df['Reject'] = df.apply(
        lambda x: "Answer is too long. Please keep it under 150 characters" if len(x['worker_answer']) > 150 else x[
            'Reject'], axis=1)
    df['Reject'] = df.apply(
        lambda x: "Answer field is empty" if len(x['worker_answer']) == 0 else x['Reject'], axis=1)
    df['Reject'] = df.apply(
        lambda x: "Answer field can not be unknow" if (x['worker_answer'].strip() == 'unknown' or x['worker_answer'].strip() == 'no idea') else x['Reject'], axis=1)
    df['Reject'] = df.apply(
        lambda x: "The question should be a w-word question or a how question." if ((len(
            x['worker_question']) > 0 and not (
            (x['worker_question'].lower().startswith('wh') or x['worker_question'].lower().startswith('how'))))) else x[
            'Reject'], axis=1)
    out_path = path[:-4] + "_rejected.csv"
    print(">>> Generating output file " + out_path)
    df.drop(columns=['worker_answer', 'worker_question']).to_csv(out_path, index=False)


if __name__ == "__main__":
    main()