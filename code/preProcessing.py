import subprocess
import shlex
import sys
import csv

"""This script can be used to prepare and reformat data to work with the program
    - It contains the CMU tagger script which will tokenise and tag the tweets,
    more information on this is availbale in the README
    - A data file is read in and each tweet is run through the tagger, and then
    returned to the format that will work with the program. 
    - In order for this to work, the file paths need to be changed to match your 
    data.
    - Please note that the data should be a txt file that only contains sentiment 
    and the tweet text."""

reload(sys)
sys.setdefaultencoding('ISO-8859-1')

#####Wrapper for CMU tokenizer############
#Call using the runtagger_parse([data[0][1]])

# The only relavent source I've found is here:
# http://m1ked.com/post/12304626776/pos-tagger-for-twitter-successfully-implemented-in
# which is a very simple implementation, my implementation is a bit more
# useful (but not much).

# NOTE this command is directly lifted from runTagger.sh
RUN_TAGGER_CMD = "java -XX:ParallelGCThreads=2 -Xmx500m -jar ark-tweet-nlp-0.3.2.jar"


def _split_results(rows):
    """Parse the tab-delimited returned lines, modified from: https://github.com/brendano/ark-tweet-nlp/blob/master/scripts/show.py"""
    for line in rows:
        line = line.strip()  # remove '\n'
        if len(line) > 0:
            if line.count('\t') == 2:
                parts = line.split('\t')
                tokens = parts[0]
                tags = parts[1]
                confidence = float(parts[2])
                yield tokens, tags, confidence


def _call_runtagger(tweets, run_tagger_cmd=RUN_TAGGER_CMD):
    """Call runTagger.sh using a named input file"""

    # remove carriage returns as they are tweet separators for the stdin
    # interface
    tweets_cleaned = [tw.replace('\n', ' ') for tw in tweets]
    message = "\n".join(tweets_cleaned)

    # force UTF-8 encoding (from internal unicode type) to avoid .communicate encoding error as per:
    # http://stackoverflow.com/questions/3040101/python-encoding-for-pipe-communicate
    message = message.encode('utf-8')

    # build a list of args
    args = shlex.split(run_tagger_cmd)
    args.append('--output-format')
    args.append('conll')
    po = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # old call - made a direct call to runTagger.sh (not Windows friendly)
    #po = subprocess.Popen([run_tagger_cmd, '--output-format', 'conll'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = po.communicate(message)
    # expect a tuple of 2 items like:
    # ('hello\t!\t0.9858\nthere\tR\t0.4168\n\n',
    # 'Listening on stdin for input.  (-h for help)\nDetected text input format\nTokenized and tagged 1 tweets (2 tokens) in 7.5 seconds: 0.1 tweets/sec, 0.3 tokens/sec\n')

    pos_result = result[0].strip('\n\n')  # get first line, remove final double carriage return
    pos_result = pos_result.split('\n\n')  # split messages by double carriage returns
    pos_results = [pr.split('\n') for pr in pos_result]  # split parts of message by each carriage return
    return pos_results


def runtagger_parse(tweets, run_tagger_cmd=RUN_TAGGER_CMD):
    """Call runTagger.sh on a list of tweets, parse the result, return lists of tuples of (term, type, confidence)"""
    pos_raw_results = _call_runtagger(tweets, run_tagger_cmd)
    pos_result = []
    for pos_raw_result in pos_raw_results:
        pos_result.append([x for x in _split_results(pos_raw_result)])
    return pos_result


def check_script_is_present(run_tagger_cmd=RUN_TAGGER_CMD):
    """Simple test to make sure we can see the script"""
    success = False
    try:
        args = shlex.split(run_tagger_cmd)
        args.append("--help")
        po = subprocess.Popen(args, stdout=subprocess.PIPE)
        # old call - made a direct call to runTagger.sh (not Windows friendly)
        #po = subprocess.Popen([run_tagger_cmd, '--help'], stdout=subprocess.PIPE)
        while not po.poll():
            lines = [l for l in po.stdout]
        # we expected the first line of --help to look like the following:
        assert "RunTagger [options]" in lines[0]
        success = True
    except OSError as err:
        print "Caught an OSError, have you specified the correct path to runTagger.sh? We are using \"%s\". Exception: %r" % (run_tagger_cmd, repr(err))
    return success


# Change the file name to the data. 
with open('positive.txt', 'r') as f:
    reader = csv.reader(f, dialect='excel', delimiter='\t')
    data=list(reader)

# This is the file name of the output file 
l =open('output.txt',"w")

for i in range(len(data)):
    #this pointer can be altered to the column where the polarity is
    sentiment = data[i][0]
    
    # Change the values of 4, 0 and neutral to the relevant polarities of your data
    if sentiment =='4':
        sentiment = 'positive'
    elif sentiment =='0':
        sentiment = 'negative'
    elif sentiment =='netural':
        sentiment = 'neutral'

    # THis pointer can be changed to point to the column of your data that contains the tweet
    tweet = data[i][1]
    POS = runtagger_parse([tweet])
    token = ''
    tag =''
    for j in range(len(POS[0])):
        #get CMU token
        token += POS[0][j][0]+ ' '
        #get CMU pos tag
        tag += POS[0][j][1]+ ' '
    # Write data to file.
    l.write(token +'\t'+ tag + '\t' + sentiment + '\n')