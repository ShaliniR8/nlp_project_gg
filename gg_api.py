'''Version 0.35'''

import pandas as pd

import import_ipynb
import preprocess_csv
from preprocess_csv import preprocess
import nltk
import nltk.data
from nltk.corpus import stopwords as sw



OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']

aw = []
#stopwords = ["to", "and", "I", "that", "this", "for", "the", "an", "at"]
stopwords = list(sw.words("english"))[:100]

#helper funcs ----------------
def sortCandidates(candidates, number, award):
    arrCombo = []
    for sublist in candidates:
        arrCombo = arrCombo + sublist

    c = nltk.FreqDist(arrCombo)
    topList = c.most_common(20)

    #print("RANKING === ", topList)

    topList2 = [word[0] for word in topList]
    print("test tops", topList2)
    print(' -------------- ')
    #tags = nltk.pos_tag(topList2) only look for names for categories with actor/actress/director/etc
    if number == 1: return c.max()
    else: return topList2[:number]

    # top_3 = c.keys()[:3] - for ranked list

            
def addRight(tweet, index):
    arr = []
    tArr = tweet.split()
    if index >= len(tArr)-1: return arr

    s = tArr[index+1] #range could be oob
    if s not in stopwords:
        arr.append(s)

    for i in range(index+2, len(tArr)): 
        s = s + " " + tArr[i]
        arr.append(s)
    return arr


def addLeft(tweet, index):
    arr = []
    tArr = tweet.split() 

    if index == 0: return arr
    if index == 1:
        if tArr[0] not in stopwords:
            arr.append(tArr[0])
        return arr

    s = tArr[index-1]
    if s not in stopwords:
        arr.append(s)

    for i in range(index-2, -1, -1):
        s = tArr[i] + " " + s
        arr.append(s)
    return arr


def cleanTweet(tweet, customSW):
    
    tweet = tweet.lower()
    tweet = tweet.replace(".", "")

    tweet = " ".join([word for word in tweet.split(" ") if word not in stopwords and len(word)>1])
    tweet = " ".join([word for word in tweet.split(" ") if word not in customSW and len(word)>1])

    return tweet


# ----------------------------


def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    hosts = ()
    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here

    df = pd.read_csv("datasets/dataset2.csv")

    def filterWinners(award):
        filtered = []
        for tweet in df["text"]:
            cTweet = cleanTweet(tweet, [])

            if award in cTweet: 
                filtered.append([cTweet, award.split()[0]])
            if ' wins ' in cTweet:
                filtered.append([cTweet, "wins"])
            if ' won ' in cTweet:
                filtered.append([cTweet, "won"])
            if ' goes to ' in cTweet:
                filtered.append([cTweet, "goes"])
            if ' winner ' in cTweet:
                filtered.append([cTweet, "winner"])
        return filtered

    awards = {}

    candidates = []
    for tweet in filterWinners(" "):
        c = addRight(tweet[0], tweet[0].split().index(tweet[1]))
        candidates.append(c)
    awards = sortCandidates(candidates) #should pull top 15-20 though


 
    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    df = pd.read_csv("datasets/dataset2.csv")

    aw = []
    for list in OFFICIAL_AWARDS_1315:
       aw += [word for word in list.split()]

    def filterNoms(award):
        filtered = []
        for tweet in df["text"]:

            cTweet = cleanTweet(tweet, ['best', 'golden', 'globe', 'award', 'globes', 'tv', 'motion', 'picture', 'film', 'picture', 'role', 'performance']) #golden globes needs to be added from config, not hardcoded here !!

            if (bool(set(award.split()) & set(cTweet.split()))): ##figure out better factors
                cTweet = cleanTweet(cTweet, aw)
                if ' nominated ' in cTweet:
                    filtered.append([cTweet, "nominated"])
                if ' nominate ' in cTweet:
                    filtered.append([cTweet, "nominate"])
                if ' nominee ' in cTweet:
                    filtered.append([cTweet, "nominee"])
                if ' loses ' in cTweet: #goes to but to is cleaned out
                    filtered.append([cTweet, "loses"])
                if ' lost ' in cTweet:
                    filtered.append([cTweet, "lost"])
                if ' snub ' in cTweet:
                    filtered.append([cTweet, 'snub'])
                if ' snubbed ' in cTweet:
                    filtered.append([cTweet, "snubbed"])
        return filtered

    nominees = {}
    for award in OFFICIAL_AWARDS_1315:
        print("Award Name: ", award)
        candidates = []
        for tweet in filterNoms(award):
            c = addRight(tweet[0], tweet[0].split().index(tweet[1]))
            c2 = addLeft(tweet[0], tweet[0].split().index(tweet[1]))
            candidates.append(c)
            candidates.append(c2)
        nominees[award] = sortCandidates(candidates, 5, award) #needs to return 5-6? dynamically add # based on number of freq/avg?
    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    df = pd.read_csv("datasets/dataset2.csv")

    aw = []
    for list in OFFICIAL_AWARDS_1315:
       aw += [word for word in list.split()]

    def filterWinners(award):
        filtered = []
        
        for tweet in df["text"]:
            cTweet = cleanTweet(tweet, ['best', 'golden', 'globe', 'award', 'globes', 'tv', 'motion', 'picture', 'film', 'picture', 'role', 'performance']) #golden globes needs to be added from config, not hardcoded here !!
##should remove words common to all awards
            if (bool(set(award.split()) & set(cTweet.split()))):
                
                cTweet = cleanTweet(cTweet, aw)
                #print("cleantweet = ", cTweet)
                if ' wins ' in cTweet:
                    filtered.append([cTweet, "wins"])
                if ' won ' in cTweet:
                    filtered.append([cTweet, "won"])
                if ' goes ' in cTweet: #goes to but to is cleaned out
                    filtered.append([cTweet, "goes"])
                if ' winner ' in cTweet:
                    filtered.append([cTweet, "winner"])
        return filtered

    winners = {}
    for award in OFFICIAL_AWARDS_1315:
        print("Award Name = ", award)
        candidates = []
        for tweet in filterWinners(award):
            c = addRight(tweet[0], tweet[0].split().index(tweet[1]))
            c2 = addLeft(tweet[0], tweet[0].split().index(tweet[1]))
            candidates.append(c)
            candidates.append(c2)
        winners[award] = sortCandidates(candidates, 1, award)
    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    df = pd.read_csv("datasets/dataset2.csv")
    
    def filterPresenters(award):
        filtered = []
        for tweet in df["text"]:
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
    df = pd.read_csv("datasets/dataset2.csv")
    #print(df["text"])
    
   


def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your Code here
  
    

    pre_ceremony()
    n = get_nominees(2013)
    print("NOMS =", n)

    a1 = ["i", "i love", "i love this", "i love this movie"]
    a2 = ["this", "this is", "this is my", "this is my favorite"]
    a3 = ["i", "i am", "i am another", "i am another list"]
    aAll = [a1, a2, a3]


    return

if __name__ == '__main__':
    main()
