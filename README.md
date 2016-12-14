# rnnFaultFinder

Place a directory containing token (entropy) files in root dir with these scripts.

Execute:
tokenFileAppender.py dir_name

To get dictionary, stats, and filter rares:
preprocess.py *token_file*

To prep for network:
hundredLinesPerFile.py *token_file*
