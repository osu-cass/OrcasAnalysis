import pandas as pd
import string
import xlrd
from spellchecker import SpellChecker
from autocorrect import spell
import time
import argparse
import os
import unidecode
from pycorenlp import StanfordCoreNLP

parser = argparse.ArgumentParser()
parser.add_argument('--lexicon', '-l', help="specify path to file that should be used as sentiment lexicon")
parser.add_argument('--data', '-d', help="specify path to data that should be analyzed")
parser.add_argument('--file', '-f', help="specify path to output file")
parser.add_argument('--header', '-H', help="boolean flag so that output produces the header, optional (default=false)", action='store_true')
args = parser.parse_args()

processed_comments = []

class Preprocess():
    def __init__(self):
        self.nlp = StanfordCoreNLP('http://localhost:9000')
        self.stanford_annotators = 'tokenize,ssplit,pos'
        self.output_folder = 'commentdata'

    def str_process(self, comment_text):
        processed_json = self.nlp.annotate(comment_text, properties={'annotators':self.stanford_annotators, 'outputFormat': 'json'})
        return processed_json

    def output_preprocessed_data(self, json_input, file_name):
        rows = []
        for sent in json_input['sentences']:
            parsed_sent = " ".join([t['originalText'] + "/" + t['pos'] for t in sent['tokens']])
            rows.append(parsed_sent)
        final_string = ""
        for r in rows:
            final_string += r
        processed_comments.append(final_string)
        # output_file_path = self.output_folder + '/' + file_name
        # if os.path.exists(output_file_path):
        #     open(output_file_path, 'w').close()
        # with open(output_file_path, 'a') as preprocessed_out:
        #     for r in rows:
        #         preprocessed_out.write(unidecode.unidecode(r) + "\n")

    def pos_tagging(self, raw_comment_text, i):
        try:
            comment_text = raw_comment_text.strip().encode().decode('utf-8', 'backslashreplace')
            parsed_json = self.str_process(raw_comment_text)
            file_name = str(i) + '.txt'
            self.output_preprocessed_data(parsed_json, file_name)
        except:
            return


if not(args.lexicon) or not(args.data):
    print('not enough specified arguments')
    print('try python sentiment.py -h for more help')
    exit()

lexicon_source = args.lexicon
data_source = args.data

output_file = "results.csv"
if args.file:
    output_file = args.file
f = open(output_file, "a+")

if args.header:
    f.write('first name,last name,email,phone,# of anger words,# of anticipation words,# of disgust words,# of fear words,# of joy words,# of sadness words,# of surprise words,# of trust words,sentiment\r\n')
#initializes the lexicon dictionary, with the word as the key and the set of values as the value
lexicon = {}
#COULBY UNCOMMENT OUT BELOW AFTER YOU IMPLEMENT PRE-PROCESS
# for sh in xlrd.open_workbook(lexicon_source).sheets():
#     for row in range(sh.nrows):
#         myRow = sh.row_values(row)
#         lexicon[str(myRow[0])] = myRow[-10:]

#this initializes the comments to be analyzed and parses the excel sheets for the comments column
comments = []
email = []
phone = []
first = []
last = []

xls = pd.ExcelFile(data_source)

for sheet_name in xls.sheet_names:
    df = xls.parse(sheet_name)
    comments = comments + list(df['Comments'])
    email = email + list(df['email'])
    phone = phone + list(df['phone'])
    first = first + list(df['first'])
    last = last + list(df['last'])

p = Preprocess()

for index, comment in enumerate(comments):
    p.pos_tagging(comment, index)

negators = ["not", "no", "n't", "neither", "nor", "nothing", "never", "none", "lack", "lacked", "lacking", "lacks", "missing", "without", "absence", "devoid"]
boundary_words = ["but", "and", "or", "since", "because", "while", "after", "before", "when", "though", "although", "if", "which", "despite", "so", "then", "thus", "where", "whereas", "until", "unless"]
punct = [".", ",", ";", "!", "?", ":", ")", "(", "\"", "'", "-"]
skipped = {"JJ": ["even", "to", "being", "be", "been", "is", "was", "'ve", "have", "had", "do", "did", "done", "of", "as", "DT", "PSP$"], "RB": ["VB", "VBZ", "VBP", "VBG"], "VB":["TO", "being", "been", "be"], "NN":["DT", "JJ", "NN", "of", "have", "has", "come", "with", "include"]}
tags = ["NN", "VB", "JJ", "RB"]
def get_word(pair): return pair[0]
def get_tag(pair): return pair[1]

def at_boundary(index, text):
    if get_word(text[index]) in punct:
        return True
    elif get_word(text[index]) in boundary_words:
        return True
    else:
        return False

def find_negation(index, word_type, text):
    search = True
    while search and not at_boundary(index, text) and index != -1:
        current = get_word(text[index]).lower()
        if current in negators:
            search = False
        index -= 1
    return not search

def get_text_from_preprocess(processed_comment):
    text = []
    processed_comment_list = processed_comment.split()
    for word in processed_comment_list:
        text.append(word.split("/"))
    for index,pair in enumerate(text):
        if get_tag(pair) in tags:
            should_inverse = find_negation(index, get_tag(pair), text)
            if should_inverse:
                #Add inverse values to the total emotion
                print("negation found for word:" + str(get_word(pair)))
            else:
                #add given values to totals
                print("no negation found for word:" + str(get_word(pair)))
        else:
            #add value straight values to totals
            print("don't look for negation")
    exit()


# print(processed_comments)
for x in processed_comments:
    get_text_from_preprocess(x)





exit()




#this iterates through each comment, removes the punctuation, splits the comment by white space and
#sets the words to lowercase
#Then the words are checked to see if they are misspelled, misspelled words are then corrected and
#appended to the list words
#The Hash table is then created to account for unique words
#Lastly the unique words are checked to see if they are in the lexicon, if they are found in the lexicon
#the tallies are added to the comments running totals
#after each word in the comment is analyzed an overall sentiment is determined by summing the positive emotions
#and subtracting the negative emotions
#This total is then divided by the number of unique words in the comment that were found in the dictionary
#This total is then divided by the number of unique words in the comment
#The totals of the other emotions are also tallied and displayed
for a,b,c,d,e in zip(comments,email,phone,first,last):
    spellcheck = SpellChecker()
    processedcomment = []
    try:
        processedcomment = a.translate(str.maketrans('', '', string.punctuation))
    except:
        continue
    processedcomment = processedcomment.lower().split()
    misspelled = []
    misspelled = spellcheck.unknown(processedcomment)
    processedcomment = [x for x in processedcomment if x not in misspelled]
    for y in misspelled:
        processedcomment.append(spell(y))

    commentdict = {}
    for x in processedcomment:
        try:
            commentdict[x] += 1
        except:
            commentdict[x] = 1

    total = wordsInDicts = angerwords = anticipationwords = disgustwords = fearwords = joywords = sadnesswords = surprisewords = trustwords = 0

    for word in commentdict:
        try:
            total += lexicon[word][0]
            total -= lexicon[word][1]
            wordsInDicts += 1

            angerwords        += lexicon[word][2]
            anticipationwords += lexicon[word][3]
            disgustwords      += lexicon[word][4]
            fearwords         += lexicon[word][5]
            joywords          += lexicon[word][6]
            sadnesswords      += lexicon[word][7]
            surprisewords     += lexicon[word][8]
            trustwords        += lexicon[word][9]
        except:
            continue
    c = str(c)
    c = c.translate(str.maketrans('', '', string.punctuation))
    c = c.translate(str.maketrans('', '', ' '))
    f.write(str(d) + ',' + str(e) + ',' + str(b) + ',' + str(c) +',')
    f.write( str(angerwords) + ',' + str(anticipationwords) + ',' + str(disgustwords) + ',' + str(fearwords) + ',' + str(joywords) + ',' + str(sadnesswords) + ',' + str(surprisewords) + ',' + str(trustwords) + ',' + str(total / (len(commentdict)+2)) + '\r\n')


    del processedcomment
    del misspelled
