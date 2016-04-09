from functions import *
from svmutil import *
from datetime import datetime

# read in testing and training data
data = read_data("../data/tweets/finalTrainingInput.txt")
dataT = read_data("../data/tweets/finalTestingInput.txt")



#Build dictionaries
dictionary={}
with open("../data/other/sentiment 140 lexicon/unigrams-pmilexicon copy.txt",'r') as f:
    for i in f:
        el = i.split("\t")
        dictionary[el[0]] = el[1]
with open("../data/other/sentiment 140 lexicon/bigrams-pmilexicon copy.txt",'r') as f:
    for i in f:
        el = i.split("\t")
        dictionary[el[0]] = el[1]
dictionary2={}
with open("../data/other/hashtag lexicon/unigrams-pmilexicon.txt",'r') as f:
    for i in f:
        el = i.split("\t")
        dictionary2[el[0]] = el[1]
with open("../data/other/hashtag lexicon/bigrams-pmilexicon.txt",'r') as f:
    for i in f:
        el = i.split("\t")
        dictionary2[el[0]] = el[1]

# dictionary3={}
# with open("../data/other/hashtag lexicon/bigrams-pmilexicon.txt",'r') as f:
#     for i in f:
#         el = i.split("\t")
#         dictionary2[el[0]] = el[1]

featureList, train_tweets= make_feature_vector(data,1)
test_tweets = make_feature_vector(dataT,0)

featureList = list(set(featureList))


startTime = datetime.now()

print 'getting result'
result = getSVMFeatureVectorAndLabels(train_tweets, featureList, dictionary, dictionary2)

problem = svm_problem(result['labels'], result['feature_vector'])
# '-q' option suppress console output
param = svm_parameter('-q -c 0.1 -b 1')
param.kernel_type = LINEAR

print 'begin training'
classifier = svm_train(problem, param)
svm_save_model('classifierDumpFile', classifier)

print 'accuracy on training set'
t_labels, t_accs, t_vals = svm_predict(result['labels'], result['feature_vector'], classifier,'-b 1')
print t_labels

print 'begin Testing'
# Test the classifier
test_feature_vector = getSVMFeatureVectorAndLabels(test_tweets, featureList, dictionary, dictionary2)
p_labels, p_accs, p_vals = svm_predict(test_feature_vector['labels'], test_feature_vector['feature_vector'], classifier,'-b 1')
print p_labels

print datetime.now() - startTime

#previous @0.1 56.586, 50.3221

