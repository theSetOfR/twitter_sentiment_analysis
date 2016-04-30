"""This file contains the all of functions used in the project"""
import re
from datetime import datetime


"""This function creates n-grams. The tweets are passed to it along with
the number of n-grams required. A list of n-grams are returned
    -Adapted from http://stackoverflow.com/a/13424002 
    Accessed:10/02/16"""


def ngrams(tweet, n):
    tweet = tweet.split(' ')
    output = []
    for i in range(len(tweet) - n + 1):
        output.append(tweet[i:i + n])
    return output


"""Pre-processes tweet
    -Replace URLs and user mentions with URL and AT_USER repectively
    -Remove the Hastag from a '#word' and return just the word
    -Replace repetitions of letters in a word with double occurence
    -strip words of unnesecary punctuation
    -Adapted from http://ravikiranj.net/posts/2012/code/how-build-twitter-sentiment-analyzer/
    Acessed:20/02/16"""


def preprocess(word):

    word = word.lower()
    # Convert a url to URL
    word = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', word)
    # Convert a username to AT_USER
    word = re.sub('@[^\s]+', 'AT_USER', word)
    # Replace the hashtag without the hasthag
    word = re.sub(r'#([^\s]+)', r'\1', word)
    # used to replace 'coooooooool' to 'cool'
    word = totwo(word)
    # strip punctuation
    word = word.strip('\'"?,.:;')
    # Remove additional white spaces
    word = re.sub('[\s]+', ' ', word)
    return word


"""Finds which of two numbers is furthest from 0
    -This function is used to get one of the lexicon scores"""


def biggestscore(a, b):
    if abs(a) > abs(b):
        return a
    elif abs(a) < abs(b):
        return b
    else:
        return 0


"""Get lexicon scores
    -4 scores are calculated and returned as a list"""


def scorelexicon(tweet, dictionary, n):
    count = 0
    score = 0.0
    maxscore = []
    b_score = 0
    lastscore = 0.0
    for i in range(len(tweet)):
        if tweet[i] in dictionary:
            sent = float(dictionary[tweet[i]])
            count += 1
            score += sent
            maxscore.append(sent)
            lastscore = sent

    if maxscore != []:
        b_score = biggestscore(max(maxscore), min(maxscore))
    else:
        b_score = 0.0

    return [count, score, b_score, lastscore]


"""Replace with letter reptitions from more than 2 to 2, makes use of 
regular expression
    -From: http://ravikiranj.net/posts/2012/code/how-build-twitter-sentiment-analyzer/
    Accessed: 20/02/16"""


def totwo(s):
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)


"""Negation
    - Tweet is passed to function and words are marked with _NEG from the rules given in section
    2.2.4 of the report.
    - A count of how many words are negated is also calculated."""


def negation(tweets):
    neg_list = ['never', 'no', 'nothing', 'nowhere', 'noone', 'none', 'not', 'havent', 'hasnt', 'hadnt', 'cant',
                'couldnt', 'shouldnt', 'wont', 'wouldnt', 'dont', 'doesnt', 'didnt', 'isnt', 'arent', 'aint']
    punct = [',', '.', ':', ';', '!', '?']
    neg_count = 0.0
    tweet = tweets.split()
    for i in range(len(tweet)):
        # print tweet[i]
        word = tweet[i]
        # if word == "no" or word == "not":
        if word in neg_list or "n't" in word:
            # print 'fired'
            for j in range(i, len(tweet)):
                # print j
                if tweet[j] in punct:
                    # print 'break'
                    break
                else:
                    tweet[j] += '_NEG'
                    neg_count += 1.0
    return tweet, neg_count

"""Count the POS tags
    - The number of each POS tag is counted from a tweet."""


def countPOS(pos):
    PUNCT = N = V = PN = P = A = O = R = NUM = C = MEN = D = L = U = HASH = INT = DIS = VER = EMO = PRO = F = EX = NOM = 0
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
        elif pos[i] == '!':
            INT += 1
        elif pos[i] == '~':
            DIS += 1
        elif pos[i] == 'T':
            VER += 1
        elif pos[i] == 'E':
            EMO += 1
        elif pos[i] == 'Z':
            PRO += 1
        elif pos[i] == 'G':
            F += 1
        elif pos[i] == 'X':
            EX += 1
        elif pos[i] == 'S':
            NOM += 1

    count = [PUNCT, N, V, PN, P, A, O, R, NUM, C, MEN, D, L, U, HASH]
    return count


"""Feature extractors:
    -The following 3 functions are used to pr-process different length n-grams
    and build the feature list.
    -Tweets are passed to the functions and split into n-grams.
    -N-grams are processed if processing is required. Some lexicons require unprocessed
    n-grams, this is why the option 'process' is a parameter in the function.
    -If the n-gram is made of stop words, begins with a non-alphabetic character, then the
     word is not added to the feature list. 
    -Adapted from http://ravikiranj.net/posts/2012/code/how-build-twitter-sentiment-analyzer/
    Accessed: 02/03/16"""


# start getfeatureVector
def get_unigrams(tweet, stopWords, process):
    unigrams = []
    # split tweet into words
    #   - if negation is not being used in the get_features function, then use 'words = tweet.split()'
    #   - It negation is used, use 'words = tweet'.

    #words = tweet.split()
    words = tweet

    for i in range(len(words)):
        if process == 1:
            words[i] = preprocess(words[i])
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", words[i])

        # ignore if it is a stop word, not alphabetic, or only processed not
        # for use in lexicon
        if (words[i] in stopWords or val is None and process == 1):
            continue
        else:
            unigrams.append(words[i].lower())

    return unigrams


def get_bigrams(tweet, stopWords, process):
    tweetB = ngrams(tweet, 2)
    bigrams = []
    # split bigram into two and process each word
    for i in range(len(tweetB)):
        w = tweetB[i][0]
        if process == 1:
            w = preprocess(w)
        w = w.lower()
        tweetB[i][0] = w

        w2 = tweetB[i][1]
        if process == 1:
            w2 = preprocess(w2)
        w2 = w2.lower()
        tweetB[i][1] = w2

        # ignore if stop word and not for use in lexicon
        if tweetB[i][0] in stopWords and tweetB[i][1] in stopWords and process == 1:
            continue
        else:
            bigrams.append(' '.join(tweetB[i]))
    return bigrams


def get_trigrams(tweet, stopWords):
    tweetB = ngrams(tweet, 3)
    trigrams = []
    for i in range(len(tweetB)):
        w = tweetB[i][0]
        w = preprocess(w)
        tweetB[i][0] = w

        w2 = tweetB[i][1]
        w2 = preprocess(w2)
        tweetB[i][1] = w2

        w3 = tweetB[i][2]
        w3 = preprocess(w3)
        tweetB[i][2] = w3
        # ignore if stop word
        if tweetB[i][0] in stopWords and tweetB[i][1] in stopWords:
            continue
        elif tweetB[i][1] in stopWords and tweetB[i][2] in stopWords:
            continue
        else:
            trigrams.append(' '.join(tweetB[i]))
    return trigrams


"""Get stop words
    -Reads in stopwords from a given file name
    -Appends 'AT_USER and URL from preprocessing stage
    -From http://ravikiranj.net/posts/2012/code/how-build-twitter-sentiment-analyzer/
    Accessed: 02/03/16 """


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


"""read in data from file
    -used to read in training/testing data.
    -Index of tweet, token and label can be altered depending on format of
    input file
    -By default, the classifier only runs on two polarities. If three are required
    then replace 'neutral' string in the last if with an empty string. i.e '' """


def read_data(filename):
    f = open(filename, 'r')
    data = []
    for i in f:
        if i:
            i = i.split('\t')
            tweet = i[0]
            token = i[1]
            label = i[2].strip('\n')
            if label != 'neutral':
                data.append([tweet, token, label])
    return data


"""Build feature list
    -Code uses earlier functions and extracts the different n-grams while building the 
    feature list. See section 2.2.1 of report for more information of implementation.
    -As default the trigrams are commented out as they cause a drop in performance, to use
    them, the 2 lines under 'Extract trigrams' need to be uncommented and 'feature_list_tri'
    must be added to the last line of the for loop.
    -The if statement is used to seperate out the training and testing data. Only the training
    data's feature list is used, not the testing.
    -Adapted from http://ravikiranj.net/posts/2012/code/how-build-twitter-sentiment-analyzer/
    Accessed: 02/03/16"""


def get_features(data, T):
    feature_list = []
    vector = []
    stopWords = getStopWordList('../data/other/stopwords.txt')
    for i in range(len(data)):
        sentiment = data[i][2]
        token = data[i][1]

        # Used to get negated version of tweet
        negated, neg_count = negation(data[i][0])

        # Extract uni-grams
        #   - If negation is used, use the first line
        #   - If negation is not used, use the second line
        #   - Please consult function 'get_unigrams' for more changes
        feature_list_uni = get_unigrams(negated, stopWords, 1)
        #feature_list_uni = get_unigrams(data[i][0], stopWords, 1)
        feature_list.extend(feature_list_uni)

        # Extract bigrams
        feature_list_bi = get_bigrams(data[i][0], stopWords, 1)
        feature_list.extend(feature_list_bi)

        # Extract trigrams
        #feature_list_tri = get_trigrams(data[i][0], stopWords)
        # feature_list.extend(feature_list_tri)

        # Extract unigrams and bigrams for use with certain lexicons
        unigrams = get_unigrams(data[i][0], stopWords, 0)
        bigrams = get_bigrams(data[i][0], stopWords, 0)
        n_grams = unigrams + bigrams
        # remember to add +feature vector 3 below
        vector.append((feature_list_uni + feature_list_bi,
                       token, sentiment, n_grams, neg_count))
    if T == 1:
        return (feature_list, vector)
    else:
        return vector


"""Extract features:
    - Extracts the features from the text and stores them in a format ready for to be passed
    to the support vector machine. For more information on correct format for LibSVM, please
    consult the LibSVM README.txt.
    - Build the feature vectors as discussed in the report section 2.2.
    - Dictionary 3 is commented out by default as it reduces the performance.
    - Adapted from http://ravikiranj.net/posts/2012/code/how-build-twitter-sentiment-analyzer/
    Accessed: 02/03/16"""""


def make_fv(tweets, featureList, dictionary1, dictionary2, dictionary3):
    sortedFeatures = sorted(featureList)

    feature_vector = []
    labels = []
    label = 0
    counter = 0

    for t in tweets:

        # Initialize empty map to store all n-grams
        map = {}
        for w in sortedFeatures:
            map[w] = 0

        tweet_words = t[0]
        tweet_token = t[1]
        tweet_opinion = t[2]
        tweet_n_grams = t[3]
        tweet_neg_count = int(t[4])

        # Add 1 to map if an n-gram in tweet is in the map of n-grams
        for word in tweet_words:
            if word in map:
                map[word] = 1

        values = map.values()

        # Get the lexicon values
        # Setiment140 lexicon
        values.extend(scorelexicon(tweet_words, dictionary1, 1))

        # Hashtag lexicon
        #   -Makes use of unprocessed unigrams and bigrams
        values.extend(scorelexicon(tweet_n_grams, dictionary2, 2))

        # MPQA lexicon, commented out as it reduces the performance
        #values.extend(scorelexicon(tweet_words, dictionary3,3))

        # Count POS tags
        values.extend(countPOS(tweet_token))

        # Count Negation
        values.extend([tweet_neg_count])

        # Add all values to the feature vector
        feature_vector.append(values)

        # Add the label of the tweet to the labels
        if tweet_opinion == 'negative':
            label = -1
            labels.append(label)
        elif tweet_opinion == 'positive':
            label = 1
            labels.append(label)
        elif tweet_opinion == 'neutral':
            label = 0
            labels.append(label)

    # return a dictionary of lists of feature_vector and labels
    return {'feature_vector': feature_vector, 'labels': labels}
