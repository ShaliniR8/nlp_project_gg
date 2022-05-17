'''Version 0.35'''

import pandas as pd

import import_ipynb
import preprocess_csv
from preprocess_csv import preprocess
from hosts import get_text_with_hosts, stem_ref_word, get_candidates, get_all_choices
from nltk.tokenize import word_tokenize
#from nltk.corpus import stopwords as sw
import nltk
nltk.download('punkt')
#from langdetect import detect
#from google_trans_new import google_translator


OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']

stopwords = ["to", "and", "I", "that", "this", "for", "the", "an", "at", "in", "a", "golden", "globe", "of", "or"]  #by in a an 

#helper funcs ----------------
def sortCandidates(candidates):
    c = nltk.FreqDist([item for sublist in candidates for item in sublist])
    return c.max(1)
    # top_3 = = c.keys()[:3] - for ranked list

            
def addRight(tweet, index):
    arr = []
    tArr = word_tokenize(tweet) #NLTK func
    if index == len(tArr) - 1: return

    s = tArr[index+1] #range could be oob
    arr.append(s)

    for i in range(index+2, len(tArr)):
        if tArr[i] in stopwords:  continue
        s = s + " " + tArr[i]
        arr.append(s)
    return arr


def addLeft(tweet, index):
    arr = []
    tArr = word_tokenize(tweet) #NLTK func
    if index == 0: return

    s = tArr[index-1]
    arr.append(s)

    for i in range(index-2, 0, -1): #check if range will get skipped if oob
        if tArr[i] in stopwords:  continue
        s = tArr[i] + " " + s
        arr.append(s)
    return arr
# ----------------------------


def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    df = pd.read_csv("datasets/dataset2.csv")

    text_with_hosts = get_text_with_hosts(df)
    sents_stemmed = stem_ref_word(text_with_hosts)
    all_bigrams = get_candidates(sents_stemmed)
    hosts = get_all_choices(all_bigrams)

    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    # Helper function in awards
    def Right(tweet, index):
        arr = []
        tweet = tweet.lower()
        tArr = word_tokenize(tweet) #NLTK func
        index += 1                  # start adding from index + 1
        if index == len(tArr) - 1: return

        while tArr[index] in stopwords:
            index += 1
            if index == len(tArr):  return 

        s = tArr[index] #range could be oob
        arr.append(s)

        for i in range(index+1, len(tArr)):
            if tArr[i] in stopwords:  continue
            s = s + " " + tArr[i]
            arr.append(s)
        return arr
    def Left(tweet, index):
        arr = []
        tArr = word_tokenize(tweet) #NLTK func
        index -= 1
        if index == 0: return

        while tArr[index] in stopwords:
            index -= 1
            if index == 0:  return
        s = tArr[index]
        arr.append(s)

        for i in range(index-1, 0, -1): #check if range will get skipped if oob
            if tArr[i] in stopwords:  continue
            s = tArr[i] + " " + s
            arr.append(s)
        return arr
    
    #main processing in awards
    df = pd.read_csv("datasets/dataset2.csv")
    awards = []
    size = 0
    if year == 2013 or year == 2015:
        size = len(OFFICIAL_AWARDS_1315)
    else:
        size = len(OFFICIAL_AWARDS_1819)
    #translator = google_translator()

    candidates = []
    for tweet in df["text"]:
        #if detect(tweet) != 'en':
        #tweet = translator.translate(tweet, lang_tgt='en')
        temp = word_tokenize(tweet)
        
        if "best" in temp:
            index = 0
            while temp[index] != "best":
                index += 1
            index -= 1  # find the position of "best" and change it to the left 
            if index > 0 and index < len(temp):
                c = Right(tweet, index)
                candidates.append(c)
        if "win" in temp or "wins" in temp or "won" in temp:
            index = 0
            while temp[index] != "win" and temp[index] != "wins" and temp[index] != "won":
                index += 1
            if index != (len(temp) - 1):  
                c = Right(tweet, index)
                candidates.append(c)
        if "lost" in temp or "lose" in temp or "loses" in temp:
            index = 0
            while temp[index] != "lost" and temp[index] != "lose" and temp[index] != "loses":
                index += 1
            if index != (len(temp) - 1):  
                c = Right(tweet, index)
                candidates.append(c)
        if "goes" in temp or "go" in temp:
            index = 0
            while temp[index] != "goes" and temp[index] != "go":
                index += 1
            if index != (0):  
                c = Left(tweet, index)
                candidates.append(c)
        
    intoOneLis = []
    for sub in candidates:
        if sub == None:     continue
        intoOneLis = intoOneLis + sub
    c = nltk.FreqDist(intoOneLis)
    TopList = c.most_common()
    
    counter = 0
    ind = 0
    while counter < size:
        if len(word_tokenize(TopList[ind][0])) > 2:  
            counter += 1
            awards.append(TopList[ind][0])
        ind += 1
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
            if award in tweet and ('presenting' in tweet or 'present' in tweet or 'announce' in tweet or 'announcing' in tweet):
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
    
    preprocess()
    
    
    
   


def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your Code here

    pre_ceremony()
    df = pd.read_csv("datasets/dataset2.csv")
    awards = get_awards(2013)
    print(awards)
    #hardcoding just for now 
    #year = None
    #hosts = get_hosts(year)

    return

if __name__ == '__main__':
    main()
