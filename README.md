## Requirements:
>Python 3 (64 bit) <br />  
>the package dependencies are in the requirements.txt file

## Instructions on how to run the sentiment analysis.

### Format for how the execution should be ran
`python sentiment.py -lexicon PATH_TO_LEXICON_SOURCE -data PATH_TO_DATA_SOURCE -file PATH_TO_OUTPUT_FILE -H`

### Example:
`python sentiment.py -lexicon sampledata/lexicon.xlsx -data sampledata/data.xlsx -file output.csv`


### This is shorthand for the flags and also works

`python sentiment.py -l PATH_TO_LEXICON_SOURCE -d PATH_TO_DATA_SOURCE -f PATH_TO_OUTPUT_FILE`

### Example:
`python sentiment.py -l sampledata/lexicon.xlsx -d sampledata/data.xlsx -f output.csv`

### If the output flag is not specified the program will default to put the results into a file named results.csv

### Example:
`python sentiment.py -l sampledata/lexicon.xlsx -d sampledata/data.xlsx`

### There is an optional parameter that prints out the row of headers for each column. For this flag to be set all that is needed is just to put -H in the command line

### Example with header
`python sentiment.py -l sampledata/lexicon.xlsx -d sampledata/data.xlsx -f output.csv -H`


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

## Initial Set Up Windows
### 1 Go to Python.org
- Click Downloads tab
- Click Download Windows x86-64 executable installer
### 2 Open/run the downloaded executable
- Click the checkbox to add Python 3.7 to path
- click install now
- After completing the installation the window can now be closed
### 3 Locate where the sentiment.py file is located
### 4 Move the lexicon file and data file to be in the same directory (aka folder) as the sentiment.py file
### 5 Open the cmd prompt
- in the windows search bar type in cmd and it should be clickable
### 6 In the command prompt navigate to where the sentiment.py, lexicon, and data files are located
- if the file was located in Downloads
`cd Downloads`
### 7 There is a provided requirements.txt file that comes with the sentiment.py package to make it easier to install required dependencies
- This should be done only once before you can run the sentiment analysis
- In the command prompt you should enter
`pip install -r requirements.txt`
### 8 with all the dependencies install you are now able to run the sentiment analysis with the semantics above


## Initial Setup MacOS
### Install Brew
Follow the instructions here[https://brew.sh/] to install brew.
Check that brew is installed by running ``` brew -v``` in the terminal. you should get something similar to the below.
```
10-249-96-112:OrcasAnalysis engineeringuser$ brew -v
Homebrew 2.1.13
Homebrew/homebrew-core (git revision 3658; last commit 2019-10-09)
Homebrew/homebrew-cask (git revision 4ac53; last commit 2019-10-09)
```

### Install Python 3
Before trying to install python check which version of python you are running by running ```python -V``` in the terminal. You should get the following out put:
```
Python 2.7.15
```
If you get a version 3.x.x you should be good to go and shouldn't need to install python3.

If you get 2.x.x you will need to install python3.

To install python3 run the following command in the terminal
```
brew install python3
```

To ensure python3 is installed type ```python3 -V``` into the terminal.
You should get ```Python 3.x.x``` as output from this command.

### Running the project
Follow the same usage instructions above for windows only replace python with python3 in all the commands. You will also need to replace pip with pip3 in the instructions above as well.
