'''
This file contains a function (gen_rule_data) to assist with creating blocking
rules and feature generation. The function returns two tables with information
about the number of times each word appears before/after a candidate word and
the number of times that candidate was labeled correct/false.

With this information, we might be able to find some words that never would
appear before/after an actual name to use as a blocking rule. Additionally,
we could find some works that commonly/rarely appear before/after
correct/incorrect names to create lists of words that can be used during
feature generation.
'''
import pandas as pd


def gen_rule_data(data, num):
    '''
    This function will generate two DataFrames from and input DataFrame. These
    can be used to help with blocking and feature generation.

    Args:
        data (DataFrame): This table is created using the gen_examples() funtion
                          found in ExampleGen.py. It contains a list of possible
                          candidates for names as well as the word previous to
                          and following the candidate in the original article.

        num (integer): This is the max number of words in a candidate name during
                       the example generation. This is necessary because if we
                       find a previous word that is before a correct name, it will
                       be previous to other incorrect longer/shorter names.

    Returns:
        prev_data (DataFrame): This table contains each word in the 'Previous'
                               column in the input table. It also shows the number
                               of times that word appeared before a correct name
                               and an incorrect name

        foll_data (DataFrame): Similar to prev_data, except this show the words
                               from the 'Following' column and their associated
                               counts from the input table.

    Usage:
        >>> # Generate examples from 10 articles ranging from 0 to 4 words long
        >>> examples = gen_examples(10, 4)
        >>>
        >>> prev, following = gen_rule_data(examples)
    '''

    # Create a list of two tables (one for previous and another for following words)
    rows = [[], []]

    # For each row in the table update our counts
    for row in data.itertuples():

        # We want to count for both previous and following words
        for j, table in enumerate(rows):

            tuple = {}

            # Get the previous and following words
            word = [getattr(row, 'Previous'), getattr(row, 'Following')]
            label = getattr(row, 'Label')

            # Add the new information to the table
            found = False
            for i, line in enumerate(table):

                # Change to lowercase
                if not type(word[j]) == float:
                    word[j] = word[j].lower()

                # If we find an entry for the word, increment values
                if line['Word'] == word[j]:
                    found = True
                    table[i]['Count'] += 1
                    if label == 1:
                        table[i]['Correct_Count'] += 1
                    else:
                        table[i]['False_Count'] += 1

            # If we don't find an entry for this word, create one
            if not found and not type(word[j]) == float:
                tuple['Word'] = word[j]
                tuple['Count'] = 1
                if label == 1:
                    tuple['Correct_Count'] = 1
                    tuple['False_Count'] = num - 1
                else:
                    tuple['Correct_Count'] = 0
                    tuple['False_Count'] = 1
                table.append(tuple)

    # Create two new data frames
    cols = ['Word', 'Count', 'Correct_Count', 'False_Count']
    prev_data = pd.DataFrame(rows[0], columns=cols)
    foll_data = pd.DataFrame(rows[1], columns=cols)

    return prev_data, foll_data
