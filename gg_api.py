'''Version 0.35'''

import pandas as pd
import json 
import re
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
import spacy

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']


#helper funcs ----------------
def sortCandidates(candidates):
    c = nltk.FreqDist([item for sublist in candidates for item in sublist])
    return c.max(1)
    # top_3 = = c.keys()[:3] - for ranked list

            
def addRight(tweet, index):
    arr = []
    tArr = tokenize_word(tweet) #NLTK func
    if index == tArr.size(): return

    s = tArr[index+1] #range could be oob
    arr.append(s)

    for i in range(index+2, tArr.size()): 
        s = s + " " + tArr[i]
        arr.append(s)
    return arr


def addLeft(tweet, index):
    arr = []
    tArr = tokenize_word(tweet) #NLTK func
    if index == 0: return

    s = tArr[index-1]
    arr.append(s)

    for i in range(index-2, 0, -1): #check if range will get skipped if oob
        s = tArr[i] + " " + s
        arr.append(s)
    return arr
# ----------------------------


def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here

    def filterNoms(award):
        filtered = []
        for tweet in df:
            if award in tweet and ('nominated' in tweet or 'nominate' in tweet or 'loses' in tweet or 'lost' in tweet):
                filtered.append(tweet)
        return filtered

    nominees = {}
    for award in OFFICIAL_AWARDS_1315:
        candidates = []
        for tweet in filterNoms(award):
            c = addRight(tweet)
            candidates.append(c)
        nominees[award] = sortCandidates(candidates) #needs to return 5-6? dynamically add # based on number of freq/avg?
    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    def filterWinners(award):
        filtered = []
        for tweet in df:
            if award in tweet and ('wins' in tweet or 'won' in tweet or 'goes to' in tweet or 'winner' in tweet):
                filtered.append(tweet)
        return filtered

    winners = {}
    for award in OFFICIAL_AWARDS_1315:
        candidates = []
        for tweet in filterWinners(award):
            c = addRight(tweet)
            candidates.append(c)
        winners[award] = sortCandidates(candidates)

    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    def filterPresenters(award):
        filtered = []
        for tweet in df:
            if award in tweet and ('presented' in tweet or 'presenting' in tweet or 'present' in tweet or 'announce' in tweet or 'announcing' in tweet):
                filtered.append(tweet)
        return filtered

    presenters = {}
    for award in OFFICIAL_AWARDS_1315:
        candidates = []
        for tweet in filterPresenters(award):
            c = addRight(tweet)
            candidates.append(c)
        presenters[award] = sortCandidates(candidates) #only returns 1 rn, will need multiple (set 2-3?)

    return presenters

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''

    #load dataset
    df = pd.read_csv("datasets/dataset1.csv")
    
    #initial cleaning of the tweets/sentences in three steps -- 
    # 1)Extract the sentences if it's a normal tweet. If it's not a simple tweet, i.e, it's a retweet of a 
    # tweet, then extract the tweet within that retweet.
    # 2)Remove links 
    # 3)Remove emojis
    # 4)Remove unicode characters
    # 5)Remove Apostrophe s ('s)
    def clean_sentences(x):
        def fetch_rt(x):
            pattern = re.compile("(RT @\w+:)(?P<rt>.+)")
            retweet = re.match(pattern, x)
            if retweet is None: return x 
            else: 
                return retweet.group("rt")

        def remove_links(x):
            pattern = re.compile('((http:|https:)[a-zA-Z0-9\._\\/]+)')
            links = re.findall(pattern, x)
            for link in links:
                x = re.sub(link[0], " ", x)
            return x

        def remove_emojis(x):
            x = re.sub("[;:<>^/\|?*\)\(]+", "", x)
            return x

        def remove_unicode(x):
            x = x.encode("ascii", "ignore").decode()
            return x

        def remove_apostrophe(x):
            x = re.sub("('s)", "", x)
            return x

        
                
        

        x = fetch_rt(x)
        x = remove_links(x)
        x = remove_emojis(x)
        x = remove_unicode(x)
        x = remove_apostrophe(x)

        return x

    df["text"] = df["text"].apply(lambda x: clean_sentences(x))
  
    


def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your Code here
    

    return

if __name__ == '__main__':
    main()
