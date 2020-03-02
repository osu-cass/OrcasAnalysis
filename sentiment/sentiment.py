import pandas as pd
import string
import xlrd
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
parser.add_argument('--negate', '-N', help="boolean flag so that it the tally counts the inverse sentiment of a word, optional (default=false)", action='store_true')
parser.add_argument('--settings', '-s', help="specify path to setting file")
args = parser.parse_args()

processed_comments = []

class Preprocess():
    def __init__(self):
        self.nlp = StanfordCoreNLP('http://localhost:9000')
        self.stanford_annotators = 'tokenize,ssplit,pos,lemma'
        self.output_folder = 'commentdata'

    def str_process(self, comment_text):
        processed_json = self.nlp.annotate(comment_text, properties={'annotators':self.stanford_annotators, 'outputFormat': 'json'})
        return processed_json

    def output_preprocessed_data(self, json_input, file_name):
        rows = []
        for sent in json_input['sentences']:
            parsed_sent = " ".join([t['lemma'] + "/" + t['pos'] for t in sent['tokens']])
            rows.append(parsed_sent)
        final_string = ""
        for r in rows:
            final_string += r + " "
        processed_comments.append(final_string)

    def pos_tagging(self, raw_comment_text, i):
        try:
            comment_text = raw_comment_text.strip().encode().decode('utf-8', 'backslashreplace')
            parsed_json = self.str_process(raw_comment_text)
            file_name = str(i) + '.txt'
            self.output_preprocessed_data(parsed_json, file_name)
        except:
            processed_comments.append("./.")
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

lexicon = {}
negators = ["not", "no", "n't", "neither", "nor", "nothing", "never", "none", "lack", "lacked", "lacking", "lacks", "missing", "without", "absence", "devoid"]
boundary_words = ["but", "and", "or", "since", "because", "while", "after", "before", "when", "though", "although", "if", "which", "despite", "so", "then", "thus", "where", "whereas", "until", "unless"]
punct = [".", ",", ";", "!", "?", ":", "\"", "-"]

total = [0,0]
wordsInDicts = [0,0]
angerwords = [0,0]
anticipationwords = [0,0]
disgustwords = [0,0]
fearwords = [0,0]
joywords = [0,0]
sadnesswords = [0,0]
surprisewords = [0,0]
trustwords = [0,0]
total_words = [0,0]

emotion_mappings = {}
emotion_mappings["anger"] = 2
emotion_mappings["anticipation"] = 3
emotion_mappings["disgust"] = 4
emotion_mappings["fear"] = 5
emotion_mappings["joy"] = 6
emotion_mappings["sadness"] = 7
emotion_mappings["surprise"] = 8
emotion_mappings["trust"] = 9

emotion_array_mappings = {}
emotion_array_mappings[2] = angerwords
emotion_array_mappings[3] = anticipationwords
emotion_array_mappings[4] = disgustwords
emotion_array_mappings[5] = fearwords
emotion_array_mappings[6] = joywords
emotion_array_mappings[7] = sadnesswords
emotion_array_mappings[8] = surprisewords
emotion_array_mappings[9] = trustwords

negation_mappings = {}


for y,sh in enumerate(xlrd.open_workbook(lexicon_source).sheets()):
    if y == 0:
        for row in range(sh.nrows):
            myRow = sh.row_values(row)
            lexicon[str(myRow[0])] = myRow[-10:]
    else:
        break
if args.settings:
    settings_source = args.settings;
    for y,sh in enumerate(xlrd.open_workbook(settings_source).sheets()):
        if y == 0:
            if len(sh.col_values(0)) != 0 and len(sh.col_values(0)) != 1:
                raw_negators = sh.col_values(0)
                raw_negators = [x for x in raw_negators if x != '']
                negators = raw_negators
                negators.pop(0)
                # print(negators)
            if len(sh.col_values(1)) != 0 and len(sh.col_values(1)) != 1:
                raw_boundary = sh.col_values(1)
                raw_boundary = [x for x in raw_boundary if x != '']
                boundary_words = raw_boundary
                boundary_words.pop(0)
                # print(boundary_words)
            if len(sh.col_values(2)) != 0 and len(sh.col_values(2)) != 1:
                raw_punct = sh.col_values(2)
                raw_punct = [x for x in raw_punct if x != '']
                punct = raw_punct
                punct.pop(0)
                # print(punct)
            if len(sh.col_values(3)) != 0:
                raw_from = sh.col_values(3)
                raw_from = [x for x in raw_from if x != '']
                from_emotions = raw_from
                from_emotions.pop(0)

                raw_to = sh.col_values(4)
                raw_to = [x for x in raw_to if x != '']
                to_emotions = raw_to
                to_emotions.pop(0)
                for from_emotion,to_emotion in zip(from_emotions, to_emotions):
                    negation_mappings[emotion_mappings[from_emotion]] = emotion_array_mappings[emotion_mappings[to_emotion]]

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


tags = ["NN", "VB", "JJ", "RB"]
def get_word(pair): return pair[0].lower()
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
    # total = wordsInDicts = angerwords = anticipationwords = disgustwords = fearwords = joywords = sadnesswords = surprisewords = trustwords = total_words = [0,0]
    total[0] = 0
    total[1] = 0
    wordsInDicts[0] = 0
    wordsInDicts[1] = 0
    angerwords[0] = 0
    angerwords[1] = 0
    anticipationwords[0] = 0
    anticipationwords[1] = 0
    disgustwords[0] = 0
    disgustwords[1] = 0
    fearwords[0] = 0
    fearwords[1] = 0
    joywords[0] = 0
    joywords[1] = 0
    sadnesswords[0] = 0
    sadnesswords[1] = 0
    surprisewords[0] = 0
    surprisewords[1] = 0
    trustwords[0] = 0
    trustwords[1] = 0
    total_words[0] = 0
    total_words[1] = 0

    processed_comment_list = processed_comment.split()
    for word in processed_comment_list:
        text.append(word.split("/"))
    for index,pair in enumerate(text):
        #reset counted flag
        for x in range(8):
            negation_mappings[x+2][1] = 0
        try:
            if get_tag(pair) in tags:
                should_inverse = False
                if args.negate:
                    should_inverse = find_negation(index, get_tag(pair), text)
                if should_inverse:
                    print("negates")
                    #Add inverse values to the total emotion
                    try:
                        total[0] += lexicon[get_word(pair)][1] #Adds the negative value because negation of a negative = postive
                        total[0] -= lexicon[get_word(pair)][0] #Subtracts the postive value because negation of a positive = negative
                        total_words[0] += 1

                        for x in range(8):
                            #checks to see if mapping has been used already for a word
                            if negation_mappings[x+2][1] == 0:
                                # to account for double counting
                                if lexicon[get_word(pair)][x+2] != 0:
                                    negation_mappings[x+2][0] += lexicon[get_word(pair)][x+2]
                                    negation_mappings[x+2][1] = 1
                    except:
                        continue
                else:
                    try:
                        total[0] += lexicon[get_word(pair)][0]
                        total[0] -= lexicon[get_word(pair)][1]
                        angerwords[0]        += lexicon[get_word(pair)][2]
                        anticipationwords[0] += lexicon[get_word(pair)][3]
                        disgustwords[0]      += lexicon[get_word(pair)][4]
                        fearwords[0]         += lexicon[get_word(pair)][5]
                        joywords[0]          += lexicon[get_word(pair)][6]
                        sadnesswords[0]      += lexicon[get_word(pair)][7]
                        surprisewords[0]     += lexicon[get_word(pair)][8]
                        trustwords[0]        += lexicon[get_word(pair)][9]
                        total_words[0]       += 1

                    except:
                        continue
            else:
                #add value straight values to totals
                try:
                    total[0] += lexicon[get_word(pair)][0]
                    total[0] -= lexicon[get_word(pair)][1]
                    angerwords[0]        += lexicon[get_word(pair)][2]
                    anticipationwords[0] += lexicon[get_word(pair)][3]
                    disgustwords[0]      += lexicon[get_word(pair)][4]
                    fearwords[0]         += lexicon[get_word(pair)][5]
                    joywords[0]          += lexicon[get_word(pair)][6]
                    sadnesswords[0]      += lexicon[get_word(pair)][7]
                    surprisewords[0]     += lexicon[get_word(pair)][8]
                    trustwords[0]        += lexicon[get_word(pair)][9]
                    total_words[0]       += 1
                except:
                    continue
        except:
            continue
    f.write( str(angerwords[0]) + ',' + str(anticipationwords[0]) + ',' + str(disgustwords[0]) + ',' + str(fearwords[0]) + ',' + str(joywords[0]) + ',' + str(sadnesswords[0]) + ',' + str(surprisewords[0]) + ',' + str(trustwords[0]) + ',' + str(total[0] / (total_words[0]+2)) + '\n')

for comment,email,phone,first,last in zip(processed_comments, emails, phones, firsts, lasts):
    try:
        f.write('"' + str(first).encode('ascii', 'ignore').decode('ascii') + '","' + str(last).encode('ascii', 'ignore').decode('ascii') + '","' + str(email).encode('ascii', 'ignore').decode('ascii') + '","\'' + str(phone).encode('ascii', 'ignore').decode('ascii') + '\'",')
        get_text_from_preprocess(comment)
    except:
        continue
