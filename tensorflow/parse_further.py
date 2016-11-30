#!/usr/bin/python
#
# This script will be used to produce a file with 100 tokens on each line.

def main():

	fp = open("tokenLines.txt", "r")
	data = fp.readlines()

	#fp = open("tokensLines_25.txt")
	buf = [ ]
	one_big_line = ' '.join(data)
	data = one_big_line.split(' ')
	total_tokens = len(data)

	fp2 = open("tokenlines_100.txt", "w")
	count = 0
	while count < total_tokens-100:
		for i in range(0, 101):
			if data[count+i].find("\n") != -1:
				buf.append(data[count+i][:-1])
			else:
				buf.append(data[count+i])
		count = count + 100
		string_to_write = ' '.join(buf)
		fp2.write(string_to_write+'\n')
		#print(count)
		buf=[ ]
	fp2.close()
	fp.close()

if __name__ == "__main__":
    main()