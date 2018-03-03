'''
This file contains the function gen_examples(), which creates a DataFrame
that contains all possible candidate names along with some additional data
about each candidate.
'''

import pandas as pd
import re, random
from shutil import copyfile

def gen_examples(length):
    '''
    Extracts candidate names from articles. The function extracts names ranging
    from one to num words long. It will extract names from text documents in a
    folder called Data that have the names article0.txt to article<num>.txt. In
    the text files, a word is indicated with '<n>' before it and '</n>' after.

    Args:
        num (integer): The number of available articles to extract candidate
                       names from.

        length (integer): The maximum length of each candidate name in number
                          of words.

    Returns:
        train (DataFrame): A table containing candidate name, position of the
                          word within the original article, the number of the
                          article, the previous word, the following word, and
                          a label indicating if the candidate is actually a name.
                          Contains examples generated for 200 random articles and
                          is used as the training set.

        test (DataFrame): A table containing the same information as the table
                          above, but only contains the other 100 articles and
                          is used as the test set.

    '''

    regex = re.compile('[^a-zA-Z(<n>)(</n>)]')
    regex_final = re.compile('[a-zA-Z]')

    # Sample articles to be used in training and test sets
    random.seed(0)
    training_articles = random.sample(range(300), 200)

    train = []
    test = []

    # Repeat num times for each article
    for article in range(300):

        # Open the file
        path = './Data/All_Articles/article' + str(article) + '.txt'
        input = open(path, 'r')

        # Create a list of all words in this article
        words = []
        for line in input:
            # Remove any newlines from the line
            line = line.strip()

            for word in line.split(' '):
                if not word == '':
                    words.append(word)

        # Go through entire list of words to generate examples
        for i in range(len(words)):

            # Generate examples with 0 to lenth number of words
            for j in range(length):

                # If there enough words left
                if (i + j) < len(words):

                    # Find the correct label
                    name = ' '.join(words[i:i+j+1])
                    label = 1
                    for k in range(i, i+j+1):
                        # Remove unnecessary characters
                        name_test = regex.sub('', words[k])

                        # Test for a correct name
                        if k == i and name_test[:3] != '<n>':
                            label = 0
                        elif k != i and '<n>' in name_test:
                            label = 0
                        elif k == i+j and name_test.replace("</n>s", '</n>')[-4:] != '</n>':
                            label = 0

                    # Check if there is punctuation in the name
                    row = {}
                    # Look for non-letter and non period
                    regex_punct = re.compile('[^a-zA-Z (<n>)(</n>)]')
                    row['Punctuation'] = False
                    if regex_punct.search(name) is not None:
                        row['Punctuation'] = True

                    # Remove unnecessary characters
                    name = name.replace('<n>', '').replace('</n>', '')
                    start = 0
                    while regex_final.match(name[start]) is None and start < len(name) - 1:
                        start += 1
                    end = len(name) - 1
                    while regex_final.match(name[end]) is None and \
                            name.lower().find('jr.') != end - 2 and \
                            name.lower().find('sr.') != end - 2 and \
                            end > 0:
                        end -= 1
                    name = name[start:end+1].strip()

                    # Create the row dictionary
                    if "'s" in words[i+j]:
                        name = name.replace("'s", '')
                        name = name.replace("’s", '')
                        row['Possessive'] = True
                    else:
                        row['Possessive'] = False
                    row['String'] = name
                    row['Position'] = i
                    row['Article'] = article
                    if i > 0:
                        row['Previous'] = words[i - 1].replace('<n>', '').replace('</n>', '')
                    if i > 1:
                        row['Previous_2'] = words[i - 2].replace('<n>', '').replace('</n>', '')
                    if i + j + 1 < len(words):
                        row['Following'] = words[i + j + 1].replace('<n>', '').replace('</n>', '')
                    row['Label'] = label

                    # Add dictionary to the list
                    if len(name) > 0:
                        if article in training_articles:
                            train.append(row)
                        else:
                            test.append(row)

    # Create the pandas dataframe
    train_df = pd.DataFrame(train, columns = ['String', 'Position', 'Article', 'Previous', 'Previous_2', 'Following',
                                              'Possessive', 'Punctuation', 'Label'])
    test_df = pd.DataFrame(test, columns = ['String', 'Position', 'Article', 'Previous', 'Previous_2', 'Following',
                                            'Possessive', 'Punctuation', 'Label'])

    return train_df, test_df

def copy_articles():

    train = [197, 215, 20, 132, 261, 248, 207, 155, 244, 183, 111, 258, 71, 144, 287, 48, 128, 272, 75, 158, 50, 37,
             169, 241, 51, 181, 222, 161, 104, 291, 226, 266, 133, 31, 7, 47, 204, 0, 252, 170, 124, 166, 32, 97,
             113, 61, 205, 247, 36, 253, 139, 114, 23, 297, 81, 224, 130, 238, 125, 27, 77, 141, 74, 180, 268, 140,
             85, 208, 138, 52, 263, 154, 234, 150, 73, 255, 295, 152, 229, 98, 245, 147, 254, 237, 264, 284, 210,
             298, 8, 156, 168, 66, 121, 17, 22, 173, 193, 33, 38, 9, 246, 179, 231, 174, 100, 236, 134, 70, 267, 60,
             55, 221, 269, 107, 148, 192, 115, 126, 277, 164, 198, 91, 21, 83, 213, 29, 259, 187, 282, 233, 214, 62,
             4, 69, 196, 56, 95, 43, 260, 109, 15, 25, 278, 194, 11, 146, 136, 18, 6, 235, 274, 218, 30, 195, 223,
             94, 165, 200, 5, 49, 212, 172, 122, 53, 159, 242, 108, 280, 232, 206, 175, 273, 239, 44, 189, 145, 265,
             64, 59, 203, 76, 12, 89, 279, 296, 202, 45, 93, 190, 186, 72, 177, 117, 86, 26, 220, 123, 228, 106, 199]

    for i in range(300):
        if i in train:
            copyfile('./Data/All_Articles/article' + str(i) + '.txt', './Data/Train/article' + str(i) + '.txt')
        else:
            copyfile('./Data/All_Articles/article' + str(i) + '.txt', './Data/Test/article' + str(i) + '.txt')
