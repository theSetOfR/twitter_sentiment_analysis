
                          Twitter Sentiment Analysis

  What is it?
  -----------

  The Twitter Sentiment Analysis program is part of a Final Year project.
  The code is written in Python 2.7 and makes use of SemEval 2013 Data, and 
  the LIBSVM library. Both are supplied within the work. The aim of this
  work was to develope a simple program that can be the starting point for
  anyone whol would like to begin research in this field. A special thanks
  to Ravi Kiranj for his wonderful guide which was the starting block for
  this work. His work can be accessed here:
  http://ravikiranj.net/posts/2012/code/how-build-twitter-sentiment-analyzer/
  at time of writing, 15/4/2016.

  Files
  -----
  code
    + main.py Contains main script of program
    + functions.py Contains all the functions used in the program
    + preProcessing.py A script to prepare data for use in program
    + svm.py, svmutil.py All files from the LIBSVM package
    + .pyc files are made on first run of program
    + classifierDumpFile is where the SVM dumps all it's data
    
  data
    + other
      + hashtag lexicon
        + bigrams-pmilexicon.txt Contains a list of bigrams with their scores
        + unigrams-pmilexicon.txt Contains a list of unigrams with their scores
      + sentiment 140 lexicon
        + bigrams-pmilexicon.txt Contains a list of bigrams with their scores
        + unigrams-pmilexicon.txt Contains a list of unigrams with their scores
      + stopwords.txt a list of stopwords
    + tweets
      + finalTestingInput.txt SemEval data for testing in the correct format
      (contains DEV and TRAIN set)
      + finalTrainingInput.txt SemEval data for training in the correct format

  libsvm.so.2 A file to allow the SVM to run

  README.txt self explanitory


  Usage
  -----

  The Usage of this file is straight forward with no installations necessary.
  1. Using terminal cd to ~/B221319 FYP/code
  e.g on unix the command was '../../Volumes/B221319\ FYP/code'
  2. run the command python main.py
  3. the program will then begin to run.
  4. the output has been supressed, the visible output will be an accuracy on
  the training set, with all the predicted labels and am accuracy on the
  testing set with all the predicted labels.
  5. the run time will then be printed and is usually less than 6 minutes.

  Correct Data Format
  -------------------
  The correct data format for this program is the following:
  <tokenized tweet><\t><POS tags><\t><polarity>
  The tokenized data is retieved from using the CMU POS tagger. The script I used
  is supplied in this work as 'preProcessing.py', however it may need changing depending on your 
  input data. The POS tags are also taken from the CMU tagger. THe Polarity should 
  be changed to be the strings 'netural', 'negative' or 'positive'. 

  To use the CMU tagger wrapper please consult:
  https://github.com/ianozsvald/ark-tweet-nlp-python
  Please not that java must be installed and the original java implentation of the CMU tagger
  must be downloaded.

  Altering program
  ----------------
  As discussed in the accompanying report for this program, there are several different 
  features tried and tested. As default the best configuration is left for anyone to see 
  the results. However if changes were to be made, the file 'function.py' shoudl be
  consulted which contains information of what can be changed and how to change it.
  By default this program users the following features:
    - Unigrams and Bigrams
    - Negation
    - Hashtag Lexicon and Sentiment 140 Lexicon (both created by NRC and referenced in the 
    accompanying report)
    - POS count
    - Negation count
  For more imformation on all these features, please consult the accompanying report.



  Contacts
  --------

     o Ravi-Shyam Patel patelravishyam@gmail.com
