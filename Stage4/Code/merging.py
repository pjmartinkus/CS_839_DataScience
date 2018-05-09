# Import files and packages
import pandas as pd


# Merge two tables
def merge_tables(A, B, matches):
    
   # First we will find all of the tuples that have not matches in each table
	data = []

	# Getting non-matches for A
	for tuple in A.itertuples(index=False):
		if not any(tuple.ID == matches.ltable_ID):
			data.append(tuple)

	# Getting non-matches for B
	for tuple in B.itertuples(index=False):
		if not any(tuple.ID == matches.rtable_ID):
			data.append(tuple)

	# Get all of the matches for each tuple in the walmart data
	A_matches = {}
	for tuple in matches.itertuples(index=False):

		 # If there is no entry for this id, start a list
		 if tuple.ltable_ID not in A_matches:
		     A_matches[tuple.ltable_ID] = [tuple.rtable_ID]

		 # Otherwise, append this value to the list
		 else:
		     A_matches[tuple.ltable_ID].append(tuple.rtable_ID)

	# Merge each set of matches
	for match in A_matches:	
		data.append(merge_tuple(match, A_matches[match], A, B))
	
	# Create a data frame from the merged tables
	merged_df = pd.DataFrame(data, columns=A.columns)
	return merged_df.drop('Clean Name', axis=1)

# Merge two tuples.
def merge_tuple(ltuple, rtuples, A, B):

    # Prefer Walmart data for most attributes
    feats = ['Name', 'Brand', 'Screen Size', 'RAM', 'Hard Drive Capacity', 'Processor Type',
                'Operating System', 'Operating System', 'Battery Life']
    for feat in feats:

        # If the value for this feature is null in ltuple, get most common value from rtuples
        if A.loc[ltuple][feat] == float('nan'):
            A.loc[ltuple][feat] = most_common(rtuples, feat, B)

    # Merge Processor Speed. Prefer Amazon data for this attribute
    A.loc[ltuple]['Processor Speed'] = most_common(rtuples, 'Processor Speed', B)

    # Merge Price using average
    total = 0
    num = 0

    # Only average non null values
    if A.loc[ltuple]['Price'] != float('nan'):
        total += A.loc[ltuple]['Price']
        num += 1

    for id in rtuples:
        if B.loc[id]['Price'] != float('nan'):
            total += B.loc[id]['Price']
            num += 1

    A.loc[ltuple]['Price'] = total / num

    # Return the merged tuple
    return A.loc[ltuple]
	

# Return the most common value in tuples for the given feature.
def most_common(tuples, feature, B):
    vals = {}

    # Count occurances of each value for this feature
    for id in tuples:
        if B.loc[id][feature] in vals:
            vals[feature] += 1
        else:
            vals[feature] = 1

    # Return most common value
    max_count = 0
    max_val = None
    for val in vals:
        if vals[val] > max_count:
            max_count = vals[val]
            max_val = val
    return val

