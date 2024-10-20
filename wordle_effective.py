import pandas as pd
from itertools import product
import math
import time

df = pd.read_csv('wordle_words.csv')
N = len(df)
# Create a list of all possible outcomes: 0. Green, 1. Yellow, 2. White
outcomes = list(product([0, 1, 2], repeat=5)) # len = 3^5 = 243
words = df['Word'].values

def eva(outcome, df, word):
    for pos, color in enumerate(outcome):
        if len(df)==0: return df
        if color == 0: #Green
            df = df.query(f"Letter{pos+1}=='{word[pos]}'")
        elif color == 1: #Yellow
            df = df.query(f"Letter{pos+1}!='{word[pos]}'") #Not at same pos
            if len(df)==0: return df
            df = df[df.apply(lambda row: word[pos] in row.values, axis=1)] #char still in answer
        else: df = df[df.apply(lambda row: word[pos] not in row.values, axis=1)] #White
    return df

def get_score(word):
    scores = []
    for outcome in outcomes:
        remaining = len(eva(outcome, df, word))
        if remaining>0: scores.append(remaining)
    return scores

def get_entropy(scores, n = N):
    return -sum([score/n * math.log2(score/n) for score in scores])

entropy_list = []
k=0
for word in words:
    start_time = time.time()
    print(f'Processing: {word}', end='...')
    scores = get_score(word)
    entropy = get_entropy(scores)
    entropy_list.append([word, entropy])
    time_spent = round(time.time()-start_time, 2)
    k+=1
    print(f'time spent: {time_spent}s', end = " ")
    print(f'Remaining words: {N-k}', end = " ")
    print(f'Remaining time: {round(time_spent*(N-k)/60, 2)}m')

df_entropy = pd.DataFrame(entropy_list, columns=['Word', 'Entropy'])
df_entropy.sort_values('Entropy', ascending=False, inplace=True)
print(df_entropy.head(10))
df_entropy.to_csv('wordle_effective.csv', index=False)
print('-------------Done!-------------')
