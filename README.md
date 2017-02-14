# Twitter Hashtag Graph

This repository contains the code to clean and extract data from tweets, create a graph of hashtags present in tweets, and update the graph in a 60 seconds rolling window. 

This code was written and tested on CentOS with Python 3.5. It is assumed that python 3.5 executable is added to the path and is named as python3. 

Dependencies:
The code uses networkx python graph library which can be installed using 'pip3 install networkx' command.

Running the code:
The top-level run.sh will execute two python programs -- tweets_cleaned.py and average_degree.py located in src directory.
These programs read tweets.txt from tweets-input directory and generate ft1.txt and ft2.txt output files in tweets-output directory.
