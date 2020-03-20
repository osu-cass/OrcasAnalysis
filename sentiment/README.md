
## Additional Set Up Required
### 1. Follow the instructions in the Project readme to install the CoreNPL Package.

### 2. Install Sentiment Specific Python Packages
- in the sentiment folder run the following command: <br/>
`pip install -r requirements.txt`

### 3a. Before you can run the sentiment program, the Stanford Server must be started
- Open a second instance of CMD prompt or bash
- Change into the extracted folder of the Stanford CoreNLP Package
- Run the following command: <br/>
`java -mx5g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer`
- If there is an error that states that port is in use: <br/>
`netstat -ano | findstr :9000` <br/>
`taskkill /PID [THE NUMBER AFTER LISTENING] /F` <br/>
- Re run the command:
`java -mx5g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer`
![Execution](./img/execution.png)

### 3b. Runing the server if you used script to install CoreNPL Package.
From the Sentiment Directory run the following command:
```.\runserver.ps1```

## 4 Instructions on how to run the sentiment analysis.

### Format for how the execution should be ran
`python sentiment.py --lexicon PATH_TO_LEXICON_SOURCE --data PATH_TO_DATA_SOURCE --settings PATH_TO_SETTINGS_FILE --file PATH_TO_OUTPUT_FILE -H -N`

### Example:
`python sentiment.py --lexicon sampledata/lexicon.xlsx --data sampledata/data.xlsx --settings sampledata/settings.xlsx --file output.csv -H -N`


### This is shorthand for the flags and also works

`python sentiment.py -l PATH_TO_LEXICON_SOURCE -d PATH_TO_DATA_SOURCE -s PATH_TO_SETTINGS_FILE -f PATH_TO_OUTPUT_FILE -H -N`

### Example:
`python sentiment.py -l sampledata/lexicon.xlsx -d sampledata/data.xlsx -s sampledata/settings.xlsx -f output.csv -H -N`

### If the output flag is not specified the program will default to put the results into a file named results.csv
![Settings File](./img/Config.png)

### Example:
`python sentiment.py -l sampledata/lexicon.xlsx -d sampledata/data.xlsx`

### There is an optional parameter that prints out the row of headers for each column. For this flag to be set all that is needed is just to put -H in the command line

### Example with header
`python sentiment.py -l sampledata/lexicon.xlsx -d sampledata/data.xlsx -f output.csv -H`

### There is an optional parameter that allows for tallies of the opposite sentiment, if a negation should be applied. For this flag to be set all that is needed is just to put -N in the command line. If a settings file is not specified it will use the default mapping.

> If you specify the negation flag, without providing a settings file, it will use a default negation mapping where the sentiment tally will be the same, but the positive/negative sentiment for words will be correctly negated.

### Example with negation
`python sentiment.py -l sampledata/lexicon.xlsx -d sampledata/data.xlsx -s sampledata/settings.xlsx -f output.csv -N`

### Setting up config [OPTIONAL]
- Below are the default negator, boundary, and punctuation terms.
- They will be used if the sheet, or columns do not exist or have size 0
- Negators = ["not", "no", "n't", "neither", "nor", "nothing", "never", "none", "lack", "lacked", "lacking", "lacks", "missing", "without", "absence", "devoid"]
- Boundary Words = ["but", "and", "or", "since", "because", "while", "after", "before", "when", "though", "although", "if", "which", "despite", "so", "then", "thus", "where", "whereas", "until", "unless"]
- Punctuation = [".", ",", ";", "!", "?", ":", ")", "(", "\"", "'", "-"]
- To create a custom config: In the Lexicon, Create a second sheet
- The First Column is designated for Negator Terms
- The Second Column is designated for Boundary Words
- The Third Column is designated for Punctuation  
- The names of the columns can be anything as it will be removed when read in, therefore the terms of use need to start at line 2 in each column.
![Config](./img/sheet2lex.PNG)

## List of Features
- Using command line arguments knows where to read data from <br />
- Reads input from excel file for lexicon <br />
- Creates hashtables from lexicon data to make searching words O(1) operation <br />
- Reads input from excel file for data <br />
- Grabs all comments from all sheets <br />
- Only counts unique words into the sentiment <br />
- Edge Cases (divide by 0 or empty comment or weird punctuation) <br />
- Calculates sentiment based on positive and negative words in the comment <br />
- Tallies up all emotions in a comment <br />
- Outputs the corresponding data to specified file or default file <br />
- Able to negate terms based on boundary words and negatory terms
- Able to change configuration based on user demands
