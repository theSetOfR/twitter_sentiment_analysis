"""THis file contains the majority of functions used in the project"""
import re

"""This function creates n-grams. The tweets are passed to it along with
the number of n-grams required. A list of n-grams are returned"""


def ngrams(tweet, n):
    tweet = tweet.split(' ')
    output = []
    for i in range(len(tweet) - n + 1):
        output.append(tweet[i:i + n])
    return output


"""Pre-processes tweet"""


def preprocess(tweet):
    # Convert to lower case
    tweet = tweet.lower()
    # Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)
    # Convert @username to AT_USER
    tweet = re.sub('@[^\s]+', 'AT_USER', tweet)
    # Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    # Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    # trim
    tweet = tweet.strip('\'"')
    return tweet


"""Finds the number furthest to 0"""


def biggestscore(a, b):
    if abs(a) > abs(b):
        return a
    elif abs(a) < abs(b):
        return b
    else:
        return 0


"""Get lexicon scores"""


def scorelexicon(tweet, dictionary):
    count = 0
    score = 0.0
    maxscore = []
    lastscore = 0.0
    for i in range(len(tweet)):
        if tweet[i] in dictionary:
            sent = float(dictionary[tweet[i]])
            count += 1
            score += sent
            maxscore.append(sent)
            lastscore = sent
    if maxscore != []:
        # return [count, score, biggestscore(max(maxscore), min(maxscore)), lastscore]
        return [count, biggestscore(max(maxscore), min(maxscore)), lastscore]
    else:
        #return [count, score, 0.0, lastscore]
        return [count, 0.0, lastscore]


"""Replace with letter reptitions from more than 2 to 2"""


def totwo(s):
    # look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)


"""add negation to tweetss"""


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


"""Count the POS tags"""


def countPOS(pos):
    PUNCT = N = V = PN = P = A = O = R = NUM = C = MEN = D = L = U = HASH = 0
    for i in range(len(pos)):
        if pos[i] == ',':
            PUNCT += 1
        elif pos[i] == 'N':
            N += 1
        elif pos[i] == 'V':
            V += 1
        elif pos[i] == '^':
            PN += 1
        elif pos[i] == 'P':
            P += 1
        elif pos[i] == 'A':
            A += 1
        elif pos[i] == 'O':
            O += 1
        elif pos[i] == 'R':
            R += 1
        elif pos[i] == '$':
            NUM += 1
        elif pos[i] == '&':
            C += 1
        elif pos[i] == '@':
            MEN += 1
        elif pos[i] == 'D':
            D += 1
        elif pos[i] == 'L':
            L += 1
        elif pos[i] == 'U':
            U += 1
        elif pos[i] == '#':
            HASH += 1
    return [PUNCT, N, V, PN, P, A, O, R, NUM, C, MEN, D, L, U, HASH]


"""Feature extractors"""


# start getfeatureVector
def get_unigrams(tweet, stopWords, process):
    if process ==1:
        tweetP = preprocess(tweet)
    else:
        tweetP = tweet
    featureVector = []
    # split tweet into words
    words = tweetP.split()
    for w in words:
        if process ==1:
            # replace two or more with two occurrences
            w = totwo(w)
            # strip punctuation
            w = w.strip('\'"?,.:;')
            # check if the word starts with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
            # ignore if it is a stop word
        if (w in stopWords or val is None and process==1):
            continue
        else:
            featureVector.append(w.lower())
            # replace negation
    # replaceNegationUni(featureVector)
    return featureVector


def getBigrams(tweet, stopWords, process):
    if process == 1:
        tweetP = preprocess(tweet)
    else:
        tweetP = tweet
    tweetB = ngrams(tweetP, 2)
    bigrams = []
    for i in range(len(tweetB)):
        w = tweetB[i][0]
        if process == 1:
            w = totwo(w)
            w = w.strip('\'"?,.')
        w = w.lower()
        tweetB[i][0] = w

        w2 = tweetB[i][1]
        if process == 1:
            w2 = totwo(w2)
            w2 = w2.strip('\'"?,.:;')
        w2 = w2.lower()
        tweetB[i][1] = w2
        # ignore if stop word
        if tweetB[i][0] in stopWords and tweetB[i][1] in stopWords and process == 1:
            continue
        else:
            bigrams.append(' '.join(tweetB[i]))
    # replaceNegationBi(bigrams)
    return bigrams


def getTrigrams(tweet, stopWords):
    tweetP = preprocess(tweet)
    tweetB = ngrams(tweetP, 3)
    trigrams = []
    for i in range(len(tweetB)):
        w = tweetB[i][0]
        w = totwo(w)
        w = w.strip('\'"?,.')
        w = w.lower()
        tweetB[i][0] = w

        w2 = tweetB[i][1]
        w2 = totwo(w2)
        w2 = w2.strip('\'"?,.:;')
        w2 = w2.lower()
        tweetB[i][1] = w2

        w3 = tweetB[i][2]
        w3 = totwo(w3)
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
    # replaceNegationBi(bigrams)
    return trigrams


"""Get stop words"""


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


"""read in data from file"""


def read_data(filename):
    f = open(filename, 'r')
    data = []
    for i in f:
        if i:
            i = i.split('\t')
            tweet = i[1]
            token = i[2]
            label = i[3].strip('\n')
            data.append([tweet, token, label])
    return data


"""build feature list"""


def make_feature_vector(data, T):
    featureList = []
    vector = []
    stopWords = getStopWordList('../data/other/stopwords.txt')
    for i in range(len(data)):
        sentiment = data[i][2]
        token = data[i][1]
        featureVector1 = getBigrams(data[i][0], stopWords, 1)
        featureList.extend(featureVector1)
        featureVector2 = get_unigrams(data[i][0], stopWords, 1)
        featureList.extend(featureVector2)
        featureVector3 = getTrigrams(data[i][0], stopWords)
        featureList.extend(featureVector3)
        n_grams = get_unigrams(data[i][0], stopWords, 0)+getBigrams(data[i][0], stopWords, 0)
        # remember to add +feature vector 3 below
        vector.append((featureVector1 + featureVector2 + featureVector3, token, sentiment, n_grams))
    if T == 1:
        return (featureList, vector)
    else:
        return vector


"""Extract features"""


def getSVMFeatureVectorAndLabels(tweets, featureList, dictionary1, dictionary2):
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
        tweet_n_grams = t[3]
        # Fill the map
        for word in tweet_words:
            # process the word (remove repetitions and punctuations)
            # word = replaceTwoOrMore(word)
            # word = word.strip('\'"?,.')
            # set map[word] to 1 if word exists
            if word in map:
                map[word] = 1
        # end for loop
        values = map.values()

        # Get the lexicon values
        # print scorelexicon(tweet_words)
        values.extend(scorelexicon(tweet_words, dictionary1))
        values.extend(scorelexicon(tweet_n_grams, dictionary2))
        values.extend(countPOS(tweet_token))

        feature_vector.append(values)
        # need to add more things here
        # if (tweet_opinion == 'neutral'):
        #     label = 0
        if tweet_opinion == 'negative':
            label = -1
            labels.append(label)
        elif tweet_opinion == 'positive':
            label = 1
            labels.append(label)
        elif tweet_opinion == 'neutral':
            label = 0
            labels.append(label)

    # return the list of feature_vector and labels
    return {'feature_vector': feature_vector, 'labels': labels}
