import pandas as pd
import string
import xlrd
from spellchecker import SpellChecker
from autocorrect import spell
import time
import argparse
start = time.time()

parser = argparse.ArgumentParser()
parser.add_argument('--lexicon', '-l', help="specify path to file that should be used as sentiment lexicon")
parser.add_argument('--data', '-d', help="specify path to data that should be analyzed")
parser.add_argument('--file', '-f', help="specify path to output file")
args = parser.parse_args()


if not(args.lexicon) or not(args.data):
    print('not enough specified arguments')
    exit()

lexicon_source = args.lexicon
data_source = args.data

output_file = "results.txt"
if args.file:
    output_file = args.file
f = open(output_file, "a+")

#initializes the lexicon dictionary, with the word as the key and the set of values as the value
lexicon = {}
for sh in xlrd.open_workbook(lexicon_source).sheets():
    for row in range(sh.nrows):
        myRow = sh.row_values(row)
        lexicon[str(myRow[0])] = myRow[-10:]

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
    [x for x in processedcomment if x not in misspelled]
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

    for i,word in enumerate(a):
        try:
            f.write(word)
            if (i+1) % 160 == 0:
                f.write('\r\n')
        except:
            f.write(' ')
    f.write('\r\n')
    f.write('\r\n')

    try:
        f.write('Posted by:' + str(d) + ' ' + str(e) + ' email:' + str(b) + ' / phone:' + str(c) +'\r\n')
    except:
        f.write('Error printing User contact information')
    f.write('net total:' + str(total) + '\r\n')
    f.write('percentage of total / (unique words found in lexicon):' + str(total / (wordsInDicts + 2)) + '\r\n')
    f.write('percentage of total / (unique words found in comment):' + str(total / (len(commentdict) + 2)) + '\r\n')
    f.write('[Anger:' + str(angerwords) + ', Anticipation:' + str(anticipationwords) + ', Disgust:' + str(disgustwords) + ', Fear:' + str(fearwords) + ', Joy:' + str(joywords) + ', Sadness:' + str(sadnesswords) + ', Surprise:' + str(surprisewords) + ', Trust:' + str(trustwords) + ']\r\n\r\n\r\n')
    del processedcomment
    del misspelled
end = time.time()
f.write(str(end - start) + '\r\n')
