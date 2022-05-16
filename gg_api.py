'''Version 0.35'''

import pandas as pd

import import_ipynb
import nltk
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords as sw
from nltk import word_tokenize, pos_tag
import preprocess_csv
from preprocess_csv import preprocess
from hosts import get_text_with_hosts, stem_ref_word, get_candidates, get_all_choices
import imdb

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']
stopwords = list(sw.words("english"))[:100]

movieDB = imdb.IMDb()

#helper funcs ----------------
def sortCandidates(candidates, number, award):
    arrCombo = []
    for sublist in candidates:
        arrCombo = arrCombo + sublist

    c = nltk.FreqDist(arrCombo)
    topList = c.most_common(40)
    print("top list", topList)

    topList2 = [word[0] for word in topList] #removes # frequency from list, just names
    print("test tops", topList2)
    print(' -------------- ')

    #tags = nltk.pos_tag(topList2) <<POS tagging
    #print("TAGS!", tags) 

    #awardArr = award.split()
    for candidate in topList2:
        r = candidate.title()
        if len(r.split()) > 1:
            if movieDB.name2imdbID(r): 
                print("guess = ", r)
                return r
    # numFound = 0
    # returnArr = []
    # for candidate in topList2:
    #     r = candidate.title()
    #     if movieDB.name2imdbID(r):
    #         if len(r.split()) > 1:
    #     #if movieDB.search_person(r)[0].get(“name”) == r:
    #             numFound = numFound + 1
    #             print("guess = ", r)
    #             if number == 1: return r
    #             returnArr.append(r)
    #             if numFound == number:
    #                 print(' -------------- ')
    #                 return returnArr
    
    if number == 1: 
        r = c.max().title()
        print("no IMDB match, guess = ", r)
        return r
    else: 
        r = [c.title() for c in topList2[:number]]
        print("no IMDB match, guess = ", r)
        return r


            
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
# ----------------------------


# def get_hosts(year):
#     '''Hosts is a list of one or more strings. Do NOT change the name
#     of this function or what it returns.'''
#     # Your code here
#     df = pd.read_csv("datasets/dataset2.csv")

#     text_with_hosts = get_text_with_hosts(df)
#     sents_stemmed = stem_ref_word(text_with_hosts)
#     all_bigrams = get_candidates(sents_stemmed)
#     hosts = get_all_choices(all_bigrams)

#     return hosts

# def get_awards(year):
#     '''Awards is a list of strings. Do NOT change the name
#     of this function or what it returns.'''
#     # Your code here
#     awards = ()
#     return awards

# def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here


#     def filterNoms(award):
#         filtered = []
#         for tweet in df:
#             if award in tweet and ('nominated' in tweet or 'nominate' in tweet or 'loses' in tweet or 'lost' in tweet):
#                 filtered.append(tweet)
#         return filtered

#     nominees = {}
#     for award in OFFICIAL_AWARDS_1315:
#         candidates = []
#         for tweet in filterNoms(award):
#             c = addRight(tweet)
#             candidates.append(c)
#         nominees[award] = sortCandidates(candidates) #needs to return 5-6? dynamically add # based on number of freq/avg?
#     return nominees

# def get_winner(year):
#     '''Winners is a dictionary with the hard coded award
#     names as keys, and each entry containing a single string.
#     Do NOT change the name of this function or what it returns.'''
#     # Your code here

#     def filterWinners(award):
#         filtered = []
#         for tweet in df:
#             if award in tweet and ('wins' in tweet or 'won' in tweet or 'goes to' in tweet or 'winner' in tweet):
#                 filtered.append(tweet)
#         return filtered

#     winners = {}
#     for award in OFFICIAL_AWARDS_1315:
#         candidates = []
#         for tweet in filterWinners(award):
#             c = addRight(tweet)
#             candidates.append(c)
#         winners[award] = sortCandidates(candidates)
#     return winners

def cleanTweet(tweet, customSW):
    
    tweet = tweet.lower()
    tweet = tweet.replace(".", "")
    tweet = tweet.replace("@", "")

    tweet = " ".join([word for word in tweet.split(" ") if word not in stopwords and len(word)>1])
    tweet = " ".join([word for word in tweet.split(" ") if word not in customSW and len(word)>1])

    return tweet

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    df = pd.read_csv("datasets/dataset2.csv")
    aw = []
    for list in OFFICIAL_AWARDS_1315:
       aw += [word for word in list.split()]

    def filterPresenters(award):
    #     filtered = []
    #     for tweet in df:
    #         if award in tweet and ('presenting' in tweet or 'present' in tweet or 'announce' in tweet or 'announcing' in tweet):
    #             filtered.append(tweet)
    #     return filtered

    # presenters = {}
    # for award in OFFICIAL_AWARDS_1315:
    #     candidates = []
    #     for tweet in filterPresenters(award):
    #         c = addRight(tweet)
    #         candidates.append(c)
    #     presenters[award] = sortCandidates(candidates) #only returns 1 rn, will need multiple (set 2-3?)
    # return presenters
        filtered = []
        for tweet in df["text"]:
            cTweet = cleanTweet(tweet, ['best', 'golden', 'globe', 'award', 'globes', 'tv', 'motion', 'picture', 'film', 'picture', 'role', 'performance']) #golden globes needs to be added from config, not hardcoded here !!
            exclude_nom_and_win = ['nominated', 'nominates', 'nominee', 'win', 'wins', 'won']
            if (bool(set(award.split()) & set(cTweet.split()))): ##figure out better factors
                cTweet = cleanTweet(cTweet, aw)
                if ('nominated' not in cTweet or
                    'nominates' not in cTweet or
                    'nominee' not in cTweet or
                    'win' not in cTweet or
                    'wins' not in cTweet or
                    'won' not in cTweet or
                    'beat' not in cTweet or
                    'triumph' not in cTweet or
                    'upset' not in cTweet or
                    'victory' not in cTweet or
                    'victorious' not in cTweet):
                    if ' present ' in cTweet:
                        filtered.append([cTweet, "present"])
                    elif ' presented ' in cTweet:
                        filtered.append([cTweet, "presented"])
                    elif ' presents ' in cTweet:
                        filtered.append([cTweet, "presents"])
                    elif ' presenter ' in cTweet:
                        filtered.append([cTweet, "presenter"])
                    elif ' presenters ' in cTweet:
                        filtered.append([cTweet, "presenters"])
                    elif ' presenting ' in cTweet:
                        filtered.append([cTweet, "presenting"])
                    elif ' presentadora ' in cTweet:
                        filtered.append([cTweet, 'presentadora'])
                    elif ' presento ' in cTweet:
                        filtered.append([cTweet, 'presento'])
                    elif ' apresentando ' in cTweet:
                        filtered.append([cTweet, 'apresentando'])
                    elif ' presentar ' in cTweet:
                        filtered.append([cTweet, 'presentar'])
                    elif ' apresentao ' in cTweet:
                        filtered.append([cTweet, 'apresentao'])
                    elif ' announce ' in cTweet: 
                        filtered.append([cTweet, "announce"])
                    elif ' announced ' in cTweet:
                        filtered.append([cTweet, "announced"])
                    elif ' announces ' in cTweet:
                        filtered.append([cTweet, 'announces'])
                    elif ' announcer ' in cTweet:
                        filtered.append([cTweet, 'announcer'])
                    elif ' stage ' in cTweet:
                        filtered.append([cTweet, 'stage'])
                    elif ' stages ' in cTweet:
                        filtered.append([cTweet, 'stages'])
                    elif ' staged ' in cTweet:
                        filtered.append([cTweet, 'staged'])
                    elif ' introduce ' in cTweet:
                        filtered.append([cTweet, 'introduce'])
                    elif ' introduces ' in cTweet:
                        filtered.append([cTweet, 'introduces'])
                    elif ' introduced ' in cTweet:
                        filtered.append([cTweet, 'introduced'])
                    elif ' declare ' in cTweet:
                        filtered.append([cTweet, 'declare'])
                    elif ' declared ' in cTweet:
                        filtered.append([cTweet, 'declared'])
                
                
        return filtered
    presenters = {}
    for award in OFFICIAL_AWARDS_1315:
        print("Award Name: ", award)
        candidates = []
        for tweet in filterPresenters(award):
            c = addRight(tweet[0], tweet[0].split().index(tweet[1]))
            c2 = addLeft(tweet[0], tweet[0].split().index(tweet[1]))
            candidates.append(c)
            candidates.append(c2)
        presenters[award] = sortCandidates(candidates, 2, award) #needs to return 5-6? dynamically add # based on number of freq/avg?
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

    #hardcoding just for now 
    year = None
    hosts = get_presenters(year)

    return

if __name__ == '__main__':
    main()
