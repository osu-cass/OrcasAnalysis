## Requirements:
>Python 3 (64 bit) <br />  
>the package dependencies are in the requirements.txt file

## Instructions on how to run the sentiment analysis.

### Format for how the execution should be ran
`python sentiment.py -lexicon PATH_TO_LEXICON_SOURCE -data PATH_TO_DATA_SOURCE -file PATH_TO_OUTPUT_FILE`

### Example:
`python sentiment.py -lexicon lexicon.xlsx -data comments.xlsx -file output.txt`


### This is shorthand for the flags and also works

`python sentiment.py -l PATH_TO_LEXICON_SOURCE -d PATH_TO_DATA_SOURCE -f PATH_TO_OUTPUT_FILE`

### Example:
`python sentiment.py -l lexicon.xlsx -d comments.xlsx -f output.txt`

### If the output flag is not specified the program will default to put the results into a file named results.txt

### Example:
`python sentiment.py -l lexicon.xlsx -d comments.xlsx`


## List of Features
- Using command line arguments knows where to read data from <br />
- Reads input from excel file for lexicon <br />
- Creates hashtables from lexicon data to make searching words O(1) operation <br />
- Reads input from excel file for data <br />
- Grabs all comments from all sheets <br />
- Only counts unique words into the sentiment <br />
- Spell Checks Words <br />
- Removes all punctuation from a comment <br />
- Edge Cases (divide by 0 or empty comment or weird punctuation) <br />
- Calculates sentiment based on positive and negative words in the comment <br />
- Tallies up all emotions in a comment <br />
- Outputs the corresponding data to specified file or default file <br />
