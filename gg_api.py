'''Version 0.35'''

import json
import pandas as pd
import config
from configparser import ConfigParser

import import_ipynb
import preprocess_csv
from preprocess_csv import preprocess

import nltk 
import nltk.data
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords as sw


import imdb
from imdb import Cinemagoer
from nltk.tokenize import word_tokenize
#from nltk.corpus import stopwords as sw
import nltk
nltk.download('punkt')
#from langdetect import detect
#from google_trans_new import google_translator

stopwords = ["to", "and", "I", "that", "this", "for", "the", "an", "at", "in", "a", "golden", "globe", "of", "or"]  #by in a an 

import ssl

##this made nltk.pos_tag and word_tokenize work for me
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']

stopwords = ["to", "and", "I", "that", "this", "for", "the", "an", "at", "in", "a", "golden", "globe", "of", "or"]  #by in a an 

movieDB = Cinemagoer()


aw = []
stopwords = list(sw.words("english"))[:100]

# host helper functions -----------------------------#

def get_text_with_entity(df, entities):
     text_with_entities = []
     for text in df["text"]:
          if any(entity in text.lower() for entity in entities):
               text_with_entities.append(text)
     return text_with_entities

def stem_ref(sent, ref, entities):
     sent = TweetTokenizer().tokenize(sent)
     sent_stemmed = []
     for word in sent: 
          if " " + word.lower() + " " in entities: sent_stemmed.append(ref)
          # for person name only
          elif nltk.pos_tag([word])[0][1] in ["NNP", "NN"]:
               sent_stemmed.append(word)
     return sent_stemmed

def get_right_bigrams(sent, i):
     return list(nltk.bigrams(sent[:i]))
def get_left_bigrams(sent, i):
     return list(nltk.bigrams(sent[i+1:]))

def get_candidates(sents, ref, entities):
     all_bigrams = []
     for sent in sents:
          sent = stem_ref(sent, ref, entities)
          i = sent.index(ref)
          right_bigrams = get_right_bigrams(sent, i)
          left_bigrams = get_left_bigrams(sent, i)
          if right_bigrams + left_bigrams != []:
               all_bigrams = all_bigrams + right_bigrams + left_bigrams
     return all_bigrams


# end -----------------------------------------------#

#helper funcs ----------------
def get_text_with_entity(df, entities):
        text_with_entities = []
        for text in df["text"]:
            if any(entity in text for entity in entities):
                text_with_entities.append(text)
        return text_with_entities


def sortCandidates(candidates):
    c = nltk.FreqDist([item for sublist in candidates for item in sublist])
    return c.max(1)
    # top_3 = = c.keys()[:3] - for ranked list

aw = []
stopwords = list(sw.words("english"))[:100]

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    df = pd.read_csv(f"datasets/dataset{year}.csv")
    hosts = [' host ', ' hosting ', ' hosted ', ' hosts ', ' cohost ', ' cohosting ', ' cohosts ']
    text_with_hosts = get_text_with_entity(df, hosts)
    all_bigrams = get_candidates(text_with_hosts, "host", hosts)
    freq_dic = nltk.FreqDist(all_bigrams)
    choices = []
    Max = freq_dic[freq_dic.max()] 
    for key, value in freq_dic.items():
        if value/Max > 0.9:
            key = " ".join(list(key))
            choices.append(key)

    return choices

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
    df = pd.read_csv(f"datasets/dataset{year}.csv")
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

        #helper funcs ----------------
    def sortCandidates(candidates, number, award):
        arrCombo = []
        for sublist in candidates:
            arrCombo = arrCombo + sublist

        c = nltk.FreqDist(arrCombo)
        topList = c.most_common(50)

        topList2 = [word[0] for word in topList if word[1]>1] #removes # frequency from list, just names
        print("test tops", topList)

        numFound = 0
        returnArr = []
        if "actor" in award or "actress" in award or "director" in award:
            for candidate in topList2:
                r = candidate.title() 
                if movieDB.search_person(r) and str(movieDB.search_person(r)[0].get("name")) == r:
                    numFound = numFound + 1
                    print("guess = ", r)
                    if number == 1: return r
                    returnArr.append(r)
                    if numFound == number: 
                        print(' -------------- ')
                        return returnArr

        elif "motion picture" in award or "film" in award:
            for candidate in topList2:
                r = candidate.title()
                q = movieDB.search_movie(r)
                if  q and str(q[0]) == r and q[0]["kind"] == "movie":
                    numFound = numFound + 1
                    print("guess = ", r)
                    if number == 1: return r
                    returnArr.append(r)
                    if numFound == number: 
                        print(' -------------- ')
                        return returnArr

        elif "television" in award or "series" in award:
            for candidate in topList2:
                r = candidate.title()
                q = movieDB.search_movie(r)
                if  q and str(q[0]) == r and q[0]["kind"] == "tv series":
                    numFound = numFound + 1
                    print("guess = ", r)
                    if number == 1: return r
                    returnArr.append(r)
                    if numFound == number: 
                        print(' -------------- ')
                        return returnArr
        
        if number == 1: 
            r = c.max().title()
            print("no IMDB match, guess = ", r)
            print(' -------------- ')
            return r
        else: 
            r = [c.title() for c in topList2[:number]]
            print("no IMDB match, guess = ", r)
            print(' -------------- ')
            return r

                
    def addRight(tweet, index):
        arr = []
        tArr = tweet.split()
        if index >= len(tArr)-1: return arr

        s = tArr[index+1] 
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
        tweet = tweet.replace(",", "")

        tweet = " ".join([word for word in tweet.split(" ") if word not in stopwords and len(word)>1])
        tweet = " ".join([word for word in tweet.split(" ") if word not in customSW and len(word)>1])

        return tweet
    # ----------------------------

    df = pd.read_csv(f"datasets/dataset{year}.csv")
    aw = []
    for list in OFFICIAL_AWARDS_1315:
       aw += [word for word in list.split()]


    def filterNoms(award):
        filtered = []
        
        for tweet in df["text"]:
            #removed golden and globes because they have been preprocessed from words in config file
            cTweet = cleanTweet(tweet, ['best', 'tv', 'motion', 'picture', 'film', 'picture', 'role', 'movie']) #golden globes needs to be added from config, not hardcoded here !

            if (bool(set(award.split()) & set(cTweet.split()))):
                cTweet = cleanTweet(cTweet, aw)
                if ' goes ' in cTweet: #goes to but to is cleaned out
                    filtered.append([cTweet, "goes"])
                if ' nominated ' in cTweet:
                    filtered.append([cTweet, "nominated"])
                if ' nominate ' in cTweet:
                    filtered.append([cTweet, "nominate"])
                if ' robbed ' in cTweet:
                    filtered.append([cTweet, "robbed"])
                if ' loses ' in cTweet: 
                    filtered.append([cTweet, "loses"])
                if ' lost ' in cTweet:
                    filtered.append([cTweet, "lost"])
                if ' snubbed ' in cTweet:
                    filtered.append([cTweet, "snubbed"])
                if ' beat ' in cTweet:
                    filtered.append([cTweet, "beat"])
                if ' falls short ' in cTweet:
                    filtered.append([cTweet, "falls"])
                
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
        nominees[award] = sortCandidates(candidates, 5, award)
    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here

        #helper funcs ----------------
    def sortCandidates(candidates, number, award):
        arrCombo = []
        for sublist in candidates:
            arrCombo = arrCombo + sublist

        c = nltk.FreqDist(arrCombo)
        topList = c.most_common(50)

        topList2 = [word[0] for word in topList if word[1]>1] #removes # frequency from list, just names
        print("test tops", topList)

        numFound = 0
        returnArr = []
        if "actor" in award or "actress" in award or "director" in award:
            for candidate in topList2:
                r = candidate.title() 
                if movieDB.search_person(r) and str(movieDB.search_person(r)[0].get("name")) == r:
                    numFound = numFound + 1
                    print("guess = ", r)
                    if number == 1: return r
                    returnArr.append(r)
                    if numFound == number: 
                        print(' -------------- ')
                        return returnArr

        elif "motion picture" in award or "film" in award:
            for candidate in topList2:
                r = candidate.title()
                q = movieDB.search_movie(r)
                if  q and str(q[0]) == r and q[0]["kind"] == "movie":
                    numFound = numFound + 1
                    print("guess = ", r)
                    if number == 1: return r
                    returnArr.append(r)
                    if numFound == number: 
                        print(' -------------- ')
                        return returnArr

        elif "television" in award or "series" in award:
            for candidate in topList2:
                r = candidate.title()
                q = movieDB.search_movie(r)
                if  q and str(q[0]) == r and q[0]["kind"] == "tv series":
                    numFound = numFound + 1
                    print("guess = ", r)
                    if number == 1: return r
                    returnArr.append(r)
                    if numFound == number: 
                        print(' -------------- ')
                        return returnArr
        
        if number == 1: 
            r = c.max().title()
            print("no IMDB match, guess = ", r)
            print(' -------------- ')
            return r
        else: 
            r = [c.title() for c in topList2[:number]]
            print("no IMDB match, guess = ", r)
            print(' -------------- ')
            return r

                
    def addRight(tweet, index):
        arr = []
        tArr = tweet.split()
        if index >= len(tArr)-1: return arr

        s = tArr[index+1] 
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
        tweet = tweet.replace(",", "")

        tweet = " ".join([word for word in tweet.split(" ") if word not in stopwords and len(word)>1])
        tweet = " ".join([word for word in tweet.split(" ") if word not in customSW and len(word)>1])

        return tweet
    # ----------------------------

    df = pd.read_csv(f"datasets/dataset{year}.csv")

    aw = []
    for list in OFFICIAL_AWARDS_1315:
       aw += [word for word in list.split()]


    def filterWinners(award):

        filtered = []
        
        for tweet in df["text"]:
            cTweet = cleanTweet(tweet, ['best', 'golden', 'globe', 'award', 'globes', 'tv', 'motion', 'picture', 'film', 'picture', 'role', 'performance', 'movie', 'miniseries']) #golden globes needs to be added from config, not hardcoded here !

            if (bool(set(award.split()) & set(cTweet.split()))):
                cTweet = cleanTweet(cTweet, aw)
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

    presenters={}

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
    config.run()
    pre_ceremony()

    return

if __name__ == '__main__':
    main()
