# rnnFaultFinder

Place a directory containing token (entropy) files and projects in root dir with these scripts.

---- PREPROCESSING

-- To get training and testing sets with bug status flags:
python tokenFileAppenderBugLineVersion.py dir_name

-- To get training and testing sets with entropies (as calculated by Ray et al's work):
python tokenFileAppenderEntropies.py dir_name

-- To get dictionary, stats, and filter out rares:
arg1 = Threshold of token occurences needed to classify a token as non-rare. This argument can be ignored to filter no tokens.
preprocess.py *training_file.txt* arg1


---- TRAINING AND TESTING

1. test_rnn.py

    USAGE: python test_rnn.py <TRAINFILE.txt> <TESTFILE.txt> <No_Of_Epochs>

    TRAINFILE.txt: The file that has token sequences for training
    TESTFILE.txt: The file that has token sequences for testing, i.e. lines for which entropy is to generated

    No_Of_Epochs: an integer indicating the number of training epochs

    Description: This python script builds and trains the LSTM model. It creates a 'my_model.h5' trained model, which can be used for testing at anytime without having to train again.

2. model_test.py

    USAGE: python model_test.py <TRAINFILE.txt> <TESTFILE.txt> <No_Of_Epochs>

    Description: This file reads in the 'my_model.h5' created by earlier script (name should not be changed, as this script is hard coded to read that file). It generates entropies for lines in the TESTFILE.txt. These entropies are reflected in the 'final_entropies.txt' file that this script generates.

    In final_entropies.txt, each line has following information.

    {token sequence} {bug_flag} {generated entropy} {probability of occurrence of last token given previous tokens}

3. classifier_data_gen.py

    USAGE: python classifier_data_gen.py


    Description: This file reads in the final_entropies.txt created by earlier file. It trains a binary classifier on 80% of data in final_entropies.txt. This classifier tries to classify a given entropy value into two categories: bug and not bug. This file outputs the trained classifier and saves in under the name 'classifier.h5'

4. prediction.py

    USAGE: python prediction.py

    Description: This script prints the predictions from the classifier on bug status to stdout, but these values doesn't many sense. Ideally, the values should be close to 1 or close to 0, but all of them are close to 0, indicating none of the lines are buggy.

