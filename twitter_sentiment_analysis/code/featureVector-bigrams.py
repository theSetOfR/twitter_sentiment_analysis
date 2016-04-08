import csv
import re
from itertools import *
import svm
from svmutil import *
from datetime import datetime


# ########function to make n-grams###########
def ngrams(input, n):
    input = input.split(' ')
    output = []
    for i in range(len(input) - n + 1):
        output.append(input[i:i + n])
    return output

def processTweet(tweet):
    # process the tweets

    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    return tweet
#end

def biggestNum(a,b):
    if abs(a)>abs(b):
        return a
    elif abs(a)<abs(b):
        return b
    else:
        return 0

def lexiconScores(tweet):
    count = 0
    score = 0.0
    maxS = []
    lastS = 0.0
    for i in range(len(tweet)):
        if tweet[i] in dictionary:
            sent = float(dictionary[tweet[i]])
            count += 1
            score += sent
            maxS.append(sent)
            lastS = sent
    if maxS!=[]:
        return [count, score, biggestNum(max(maxS), min(maxS)), lastS]
    else:
        return [count, score, 0.0, lastS]

# initialize stopWords
stopWords = []


# flatten arrays
def flatten(listOfLists):
    "Flatten one level of nesting"
    return chain.from_iterable(listOfLists)


# start replaceTwoOrMore
def replaceTwoOrMore(s):
    # look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)


def replaceNegationBi(tweet):
    for i in range(len(tweet)):
        word = tweet[i]
        if "no " in word or "not " in word or "n't" in word:
            tweet[i] += '_NEG'


def replaceNegationUni(tweet):
    for i in range(len(tweet)):
        word = tweet[i]
        if word == "no" or word == "not":
            if i < len(tweet) - 1:
                tweet[i + 1] += '_NEG'
            else:
                continue
        elif "n't" in word:
            tweet[i] += '_NEG'

#Count POS tags
def countPOS(pos):
    PUNCT=N=V=PN=P=A=O=R=NUM=C=MEN=D=L=U=HASH=0
    for i in range(len(pos)):
        if pos[i]==',':
            PUNCT +=1
        elif pos[i]=='N':
            N+=1
        elif pos[i]=='V':
            V+=1
        elif pos[i]=='^':
            PN+=1
        elif pos[i]=='P':
            P+=1
        elif pos[i]=='A':
            A+=1
        elif pos[i]=='O':
            O+=1
        elif pos[i]=='R':
            R+=1
        elif pos[i]=='$':
            NUM+=1
        elif pos[i]=='&':
            C+=1
        elif pos[i]=='@':
            MEN+=1
        elif pos[i]=='D':
            D+=1
        elif pos[i]=='L':
            L+=1
        elif pos[i]=='U':
            U+=1
        elif pos[i]=='#':
            HASH+=1
    return [PUNCT,N,V,PN,P,A,O,R,NUM,C,MEN,D,L,U,HASH]

# start getStopWordList
def getStopWordList(stopWordListFileName):
    # read the stopwords file and build a list
    stopWords = []
    stopWords.append('AT_USER')
    stopWords.append('URL')

    fp = open(stopWordListFileName, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    return stopWords


# start getfeatureVector
def getFeatureVector(tweet):
    tweetP = processTweet(tweet)
    featureVector = []
    # split tweet into words
    words = tweetP.split()
    for w in words:
        # replace two or more with two occurrences
        w = replaceTwoOrMore(w)
        # strip punctuation
        w = w.strip('\'"?,.:;')
        # check if the word starts with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        # ignore if it is a stop word
        if (w in stopWords or val is None):
            continue
        else:
            featureVector.append(w.lower())
         #replace negation
    #replaceNegationUni(featureVector)
    return featureVector


# end

def getBigrams(tweet):
    tweetP = processTweet(tweet)
    tweetB = ngrams(tweetP, 2)
    bigrams = []
    for i in range(len(tweetB)):
        w = tweetB[i][0]
        w = replaceTwoOrMore(w)
        w = w.strip('\'"?,.')
        w = w.lower()
        tweetB[i][0] = w

        w2 = tweetB[i][1]
        w2 = replaceTwoOrMore(w2)
        w2 = w2.strip('\'"?,.:;')
        w2 = w2.lower()
        tweetB[i][1] = w2
        # ignore if stop word
        if tweetB[i][0] in stopWords and tweetB[i][1] in stopWords:
            continue
        else:
            bigrams.append(' '.join(tweetB[i]))
    #replaceNegationBi(bigrams)
    return bigrams

def getTrigrams(tweet):
    tweetP = processTweet(tweet)
    tweetB = ngrams(tweetP, 3)
    trigrams = []
    for i in range(len(tweetB)):
        w = tweetB[i][0]
        w = replaceTwoOrMore(w)
        w = w.strip('\'"?,.')
        w = w.lower()
        tweetB[i][0] = w

        w2 = tweetB[i][1]
        w2 = replaceTwoOrMore(w2)
        w2 = w2.strip('\'"?,.:;')
        w2 = w2.lower()
        tweetB[i][1] = w2

        w3 = tweetB[i][2]
        w3 = replaceTwoOrMore(w3)
        w3 = w3.strip('\'"?,.:;')
        w3 = w3.lower()
        tweetB[i][2] = w3
        # ignore if stop word
        if tweetB[i][0] in stopWords and tweetB[i][1] in stopWords:
            continue
        elif tweetB[i][1] in stopWords and tweetB[i][2] in stopWords:
            continue
        else:
            trigrams.append(' '.join(tweetB[i]))
    #replaceNegationBi(bigrams)
    return trigrams

#Build dictionaries
dictionary={}
with open("../data/other/NRC-Hashtag Lexicon/unigrams-pmilexicon copy.txt",'r') as f:
    for i in f:
        el = i.split("\t")
        dictionary[el[0]] = el[1]
with open("../data/other/NRC-Hashtag Lexicon/bigrams-pmilexicon copy.txt",'r') as f:
    for i in f:
        el = i.split("\t")
        dictionary[el[0]] = el[1]

# store feature vector with sentiment
train_tweets = []
# featureVector = []
featureList = []
# Read the tweets one by

data=[]
f=open("../data/tweets/finalTrainingInput.txt",'r')
for i in f:
    if i:
        i=i.split('\t')
        tweet=i[1]
        token=i[2]
        label=i[3].strip('\n')
        #this added to remove neutral classs
        if label == 'blah':
            continue
        else:
            data.append([tweet,token,label])

st = open("../data/other/stopwords.txt", 'r')
stopWords = getStopWordList('../data/other/stopwords.txt')

for i in range(len(data)):
    sentiment = data[i][2]
    token = data[i][1]
    featureVector1 = getBigrams(data[i][0])
    featureList.extend(featureVector1)
    featureVector2 = getFeatureVector(data[i][0])
    featureList.extend(featureVector2)
    featureVector3 = getTrigrams(data[i][0])
    featureList.extend(featureVector3)
    #remember to add +feature vector 3 below
    train_tweets.append((featureVector1 + featureVector2 + featureVector3, token, sentiment))


dataT=[]
f=open("../data/tweets/finalTestingInput.txt",'r')
for i in f:
    if i:
        i=i.split('\t')
        tweet=i[1]
        token=i[2]
        label=i[3].strip('\n')
        #added to remove neutral class
        if label == 'blah':
            continue
        else:
            dataT.append([tweet, token, label])

test_tweets = []

for i in range(len(dataT)):
    sentiment = dataT[i][2]
    token = dataT[i][1]
    featureVector1 = getBigrams(dataT[i][0])
    featureVector2 = getFeatureVector(dataT[i][0])
    featureVector3 = getTrigrams(dataT[i][0])
    test_tweets.append((featureVector1 + featureVector2+ featureVector3, token, sentiment))

featureList = list(set(featureList))


def getSVMFeatureVectorAndLabels(tweets, featureList):
    sortedFeatures = sorted(featureList)

    feature_vector = []
    labels = []
    for t in tweets:
        label = 0
        map = {}
        # Initialize empty map
        for w in sortedFeatures:
            map[w] = 0

        # print map
        tweet_words = t[0]
        tweet_token = t[1]
        tweet_opinion = t[2]
        #Fill the map
        # for word in tweet_words:
        #     # process the word (remove repetitions and punctuations)
        #     # word = replaceTwoOrMore(word)
        #     # word = word.strip('\'"?,.')
        #     # set map[word] to 1 if word exists
        #     if word in map:
        #         map[word] = 1
        # # end for loop
        # values = map.values()

        #Get the lexicon values
        #print lexiconScores(tweet_words)
        values=lexiconScores(tweet_words)
        #values.extend(countPOS(tweet_token))

        feature_vector.append(values)
        #need to add more things here
        # if (tweet_opinion == 'neutral'):
        #     label = 0
        if (tweet_opinion == 'negative'):
            label = -1
            labels.append(label)
        elif (tweet_opinion == 'positive'):
            label = 1
            labels.append(label)
        elif (tweet_opinion == 'neutral'):
            label = 0
            labels.append(label)

    # return the list of feature_vector and labels
    return {'feature_vector': feature_vector, 'labels': labels}


startTime = datetime.now()

print 'getting result'
result = getSVMFeatureVectorAndLabels(train_tweets, featureList)

problem = svm_problem(result['labels'], result['feature_vector'])
# '-q' option suppress console output
param = svm_parameter('-q -c 100 -b 1')
param.kernel_type = LINEAR

print 'begin training'
classifier = svm_train(problem, param)
svm_save_model('classifierDumpFile', classifier)

print 'accuracy on training set'
t_labels, t_accs, t_vals = svm_predict(result['labels'], result['feature_vector'], classifier,'-b 1')
print t_labels

print 'begin Testing'
# Test the classifier
test_feature_vector = getSVMFeatureVectorAndLabels(test_tweets, featureList)
p_labels, p_accs, p_vals = svm_predict(test_feature_vector['labels'], test_feature_vector['feature_vector'], classifier,'-b 1')
print p_labels

print datetime.now() - startTime