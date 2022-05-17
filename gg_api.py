'''Version 0.35'''

import pandas as pd

import import_ipynb
import preprocess_csv
from preprocess_csv import preprocess
from get_info import host_info, award_info, nominee_info

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
    entities_hosts = [ " host " , " hosting ", " hosted ", " hosts ", " cohost ", " cohosting ", " cohosts "]
    entities_nominated = [ " nominated ", " nominee ", " nominees ", " nominate ", " nominates ", " nomination "]
    entities_awards = [ " best ", " Best "]
    entities_winners = [ " win ", " won ", " winning ", " wins ", " winner ", " winners " , " goes "]
    entities_presenters = [ " presents ", " presenters ", " presenting ", " presenter ", " present ", " presented " ]
    df = pd.read_csv(f"datasets/dataset{year}.csv")
    
    hosts = host_info(df, entities_hosts)

    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    entities_hosts = [ " host " , " hosting ", " hosted ", " hosts ", " cohost ", " cohosting ", " cohosts "]
    entities_nominated = [ " nominated ", " nominee ", " nominees ", " nominate ", " nominates ", " nomination "]
    entities_awards = [ " best ", " Best "]
    entities_winners = [ " win ", " won ", " winning ", " wins ", " winner ", " winners " , " goes "]
    entities_presenters = [ " presents ", " presenters ", " presenting ", " presenter ", " present ", " presented " ]
    df = pd.read_csv(f"datasets/dataset{year}.csv")

    entities_winners += [entity.upper() for entity in entities_winners] + [entity.capitalize() for entity in entities_winners]

    awards = award_info(df, entities_winners, entities_presenters, entities_awards)
    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    entities_hosts = [ " host " , " hosting ", " hosted ", " hosts ", " cohost ", " cohosting ", " cohosts "]
    entities_nominated = [ " nominated ", " nominee ", " nominees ", " nominate ", " nominates ", " nomination "]
    entities_awards = [ " best ", " Best "]
    entities_winners = [ " win ", " won ", " winning ", " wins ", " winner ", " winners " , " goes "]
    entities_presenters = [ " presents ", " presenters ", " presenting ", " presenter ", " present ", " presented " ]
    df = pd.read_csv(f"datasets/dataset{year}.csv")
    
    nominees = nominee_info(df, entities_nominated)
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
    
    # preprocess(2013)
    # preprocess(2015)
    
    
    
   


def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your Code here

    # pre_ceremony()

    #hardcoding just for now 
    # hosts = get_hosts(year)

    return

if __name__ == '__main__':
    main()
