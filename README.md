Insight Data Engineering - Coding Challenge

This repository contains the code for Insight Data Engineering coding challange to clean and extract data from 
tweets, create a graph of hashtags in a tweet, and update the graph in a 60 seconds rolling window. 

This code was written and tested on CentOS with Python 3.5. It is assumed that python 3.5 executable is added to the path and is named as python3. If the python 3.5 executable is installed as python, please change run.sh to reflect that. This code will NOT work as is with python 2.x.

Dependencies:
The code uses networkx python graph library which can be installed using 'pip3 install networkx' command.

Running the code:
The top-level run.sh will execute two python programs -- tweets_cleaned.py and average_degree.py located in src directory.
These programs read tweets.txt from tweets-input directory and generate ft1.txt and ft2.txt output files in tweets-output directory.
