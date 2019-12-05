import pandas as pd
import string
import xlrd
from spellchecker import SpellChecker
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
negators = ["not", "no", "n't", "neither", "nor", "nothing", "never", "none", "lack", "lacked", "lacking", "lacks", "missing", "without", "absence", "devoid"]
boundary_words = ["but", "and", "or", "since", "because", "while", "after", "before", "when", "though", "although", "if", "which", "despite", "so", "then", "thus", "where", "whereas", "until", "unless"]
punct = [".", ",", ";", "!", "?", ":", ")", "(", "\"", "'", "-"]


for y,sh in enumerate(xlrd.open_workbook(lexicon_source).sheets()):
    if y == 0:
        for row in range(sh.nrows):
            myRow = sh.row_values(row)
            lexicon[str(myRow[0])] = myRow[-10:]
    if y == 1:
        if len(sh.col_values(0)) != 0:
            negators = sh.col_values(0)
            negators.pop(0)
        if len(sh.col_values(1)) != 0:
            boundary_words = sh.col_values(1)
            boundary_words.pop(0)
        if len(sh.col_values(2)) != 0:
            punct = sh.col_values(2)
            punct.pop(0)

#this initializes the comments to be analyzed and parses the excel sheets for the comments column
comments = []
emails = []
phones = []
firsts = []
lasts = []

xls = pd.ExcelFile(data_source)


for sheet_name in xls.sheet_names:
    df = xls.parse(sheet_name)
    comments = comments + list(df['Comments'])
    emails = emails + list(df['email'])
    phones = phones + list(df['phone'])
    firsts = firsts + list(df['first'])
    lasts = lasts + list(df['last'])


p = Preprocess()

for index, comment in enumerate(comments):
    p.pos_tagging(comment, index)


# skipped = {"JJ": ["even", "to", "being", "be", "been", "is", "was", "'ve", "have", "had", "do", "did", "done", "of", "as", "DT", "PSP$"], "RB": ["VB", "VBZ", "VBP", "VBG"], "VB":["TO", "being", "been", "be"], "NN":["DT", "JJ", "NN", "of", "have", "has", "come", "with", "include"]}
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
    total = wordsInDicts = angerwords = anticipationwords = disgustwords = fearwords = joywords = sadnesswords = surprisewords = trustwords = total_words = 0
    processed_comment_list = processed_comment.split()
    for word in processed_comment_list:
        text.append(word.split("/"))
    for index,pair in enumerate(text):
        if get_tag(pair) in tags:
            should_inverse = find_negation(index, get_tag(pair), text)
            if should_inverse:
                #Add inverse values to the total emotion
                try:
                    total += lexicon[get_word(pair)][1] #Adds the negative value because negation of a negative = postive
                    total -= lexicon[get_word(pair)][0] #Subtracts the postive value because negation of a positive = negative
                    total_words += 1

                    # Anger += Anger
                    angerwords        += lexicon[get_word(pair)][2]
                    # anticipationwords += lexicon[get_word(pair)][3]
                    # Surprise += Anticipation
                    surprisewords     += lexicon[get_word(pair)][3]
                    # disgust += disgust
                    disgustwords      += lexicon[get_word(pair)][4]
                    # Fear += Fear
                    fearwords         += lexicon[get_word(pair)][5]
                    # joywords          += lexicon[get_word(pair)][6]
                    # Sadness += Joy
                    sadnesswords      += lexicon[get_word(pair)][6]
                    # Sadness += Sandness
                    sadnesswords      += lexicon[get_word(pair)][7]
                    # Surprise += Surprise
                    surprisewords     += lexicon[get_word(pair)][8]
                    # trustwords        += lexicon[get_word(pair)][9]
                    # Disgust += Trust
                    disgustwords      += lexicon[get_word(pair)][9]
                except:
                    # print("negation found for Word(s) but no values in dictionary:" + str(get_word(pair)))
                    continue
                # print("negation found for Word(s):" + str(get_word(pair)))
            else:
                #add given values to totals
                try:
                    total += lexicon[get_word(pair)][0]
                    total -= lexicon[get_word(pair)][1]
                    angerwords        += lexicon[get_word(pair)][2]
                    anticipationwords += lexicon[get_word(pair)][3]
                    disgustwords      += lexicon[get_word(pair)][4]
                    fearwords         += lexicon[get_word(pair)][5]
                    joywords          += lexicon[get_word(pair)][6]
                    sadnesswords      += lexicon[get_word(pair)][7]
                    surprisewords     += lexicon[get_word(pair)][8]
                    trustwords        += lexicon[get_word(pair)][9]
                    total_words += 1

                except:
                    # print("Do not negate for found for Word(s) but no values in dictionary:" + str(get_word(pair)))
                    continue
                # print("Do not negate for found for Word(s):" + str(get_word(pair)))
        else:
            #add value straight values to totals
            try:
                total += lexicon[get_word(pair)][0]
                total -= lexicon[get_word(pair)][1]
                angerwords        += lexicon[get_word(pair)][2]
                anticipationwords += lexicon[get_word(pair)][3]
                disgustwords      += lexicon[get_word(pair)][4]
                fearwords         += lexicon[get_word(pair)][5]
                joywords          += lexicon[get_word(pair)][6]
                sadnesswords      += lexicon[get_word(pair)][7]
                surprisewords     += lexicon[get_word(pair)][8]
                trustwords        += lexicon[get_word(pair)][9]
            except:
                # print("don't look for negation but no values in dictionary:" + str(get_word(pair)))
                continue
            # print("don't look for negation:" + str(get_word(pair)))
    f.write( str(angerwords) + ',' + str(anticipationwords) + ',' + str(disgustwords) + ',' + str(fearwords) + ',' + str(joywords) + ',' + str(sadnesswords) + ',' + str(surprisewords) + ',' + str(trustwords) + ',' + str(total / (total_words+2)) + '\r\n')

# print(processed_comments)
for comment,email,phone,first,last in zip(processed_comments, emails, phones, firsts, lasts):
    f.write('"' + str(first) + '","' + str(last) + '","' + str(email) + '","\'' + str(phone) + '\'",')
    get_text_from_preprocess(comment)
