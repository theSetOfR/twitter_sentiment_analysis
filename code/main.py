from functions import *
from svmutil import *
from datetime import datetime

# Begin timing script run time
startTime = datetime.now()

"""Call function to read in data files. These must be in the correct format
Consult README.txt for more information"""
# Read in training data
data = read_data("../data/tweets/finalTrainingInput.txt")
# Read in testing data
dataT = read_data("../data/tweets/finalTestingInput.txt")



"""Read in the three Lexicons/dictionaries. These should be imported into 
the dictionary type for quicker search. The key is the n-gram/word and the value
is the polarity score."""

# Read in sentiment 140 lexicon
dictionary={}
with open("../data/other/sentiment 140 lexicon/unigrams-pmilexicon copy.txt",'r') as f:
    for i in f:
        el = i.split("\t")
        dictionary[el[0]] = el[1]
with open("../data/other/sentiment 140 lexicon/bigrams-pmilexicon copy.txt",'r') as f:
    for i in f:
        el = i.split("\t")
        dictionary[el[0]] = el[1]

# Read in Hashtag lexicon
dictionary2={}
with open("../data/other/hashtag lexicon/unigrams-pmilexicon.txt",'r') as f:
    for i in f:
        el = i.split("\t")
        dictionary2[el[0]] = el[1]
with open("../data/other/hashtag lexicon/bigrams-pmilexicon.txt",'r') as f:
    for i in f:
        el = i.split("\t")
        dictionary2[el[0]] = el[1]

# Read in MPQA dictionary
dictionary3={}
with open("../data/other/MPQA/subjclueslen1-HLTEMNLP05.txt",'r') as f:
    for i in f:
        el = i.split("\t")
        dictionary3[el[0]] = el[1]

"""Build the Feature List and get the preprocessed tweets"""
featureList, train_tweets= get_features(data,1)
test_tweets = get_features(dataT,0)

"""Convert feature list into feature set to remove repitions of n-grams"""
featureList = list(set(featureList))


"""Pass the tweets, feature set and dictionaries to the function to create feature vector and labels.
The LibSVM package is then used to train an SVM on feature vector and labels"""
print 'Building feature vector'
training_fv = make_fv(train_tweets, featureList, dictionary, dictionary2, dictionary3)

print 'Begin training'
classifier = svm_train(training_fv['labels'], training_fv['feature_vector'], '-t 0 -c 10 -q')
svm_save_model('classifierDumpFile', classifier)

print 'Accuracy on training set'
t_labels, t_accs, t_vals = svm_predict(training_fv['labels'], training_fv['feature_vector'], classifier)
print t_labels

print 'Begin Testing'
# Test the classifier
test_fv = make_fv(test_tweets, featureList, dictionary, dictionary2, dictionary3)

print 'Accuracy on Testing'
p_labels, p_accs, p_vals = svm_predict(test_fv['labels'], test_fv['feature_vector'], classifier)
print p_labels


print 'Time taken', datetime.now() - startTime


