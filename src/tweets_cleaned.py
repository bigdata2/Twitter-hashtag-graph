# Program that calculates the number of tweets cleaned
# Submitted by Anurag Tiwari
import json
import sys
import re

input_filename = sys.argv[1]
output_filename = sys.argv[2]

# Top-level function to read, clean, and extract data from tweets
# file. It then writes the extracted data into another file.
def cleandata():
   cnt_unicode = 0 
   outputfile = open(output_filename, 'w')
   with open(input_filename) as inputfile:
      for line in inputfile:
         line = replaceEscapeChar(line)
         jsonline = (json.loads(line))
         if 'text' in jsonline:
            check_ascii, ascii_str = is_ascii(jsonline['text'])
            timestamp = jsonline['created_at']
            out_line = ascii_str + " (timestamp: " + timestamp + " )\n" 
            outputfile.write(out_line)
            if(not check_ascii):
               cnt_unicode += 1
   out_line = "\n%s tweets contained unicode" %cnt_unicode
   outputfile.write(out_line)

# Replace the escape characters specified in the FAQ.
def replaceEscapeChar(str):
    str = str.replace("\\'", "'");
    re.sub( '\s+', ' ', str) 
    return str
   
# Check if the string contains Unicode characters and 
# remove them from the string.
def is_ascii(str):
    ascii_str = ""
    check_ascii = True
    for s in str:
       if ((ord(s) > 127) | (ord(s) < 32)):
          check_ascii = False
       else:
          ascii_str+=s
    return check_ascii, ascii_str

if __name__ == '__main__':
   cleandata()
