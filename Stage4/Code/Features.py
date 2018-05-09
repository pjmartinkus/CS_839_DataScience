import pandas as pd
import re


def add_numeric_features(data):
    # Keep track of update data
    result = []

    # For each tuple, add the new features
    cols = list(data.columns)
    for row in data.itertuples():
        row = list(row)[1:len(row)]
    
        # Add an additioanl column with each of the following features changed to a numeric value
        features = ['Screen Size', 'RAM', 'Hard Drive Capacity', 'Processor Speed', 'Battery Life']
        for feat in features:
            
            # Check for null values for this feature
            if pd.isnull(row[cols.index(feat)]) or pd.isnull(row[cols.index(feat)]):
                val = float('nan')
            
            # Otherwise change to a numeric value
            else:
                val = float(re.sub('[^0-9.]', '', row[cols.index(feat)]))
            
            # Change TB to GB for hard drive capacity
            if feat == 'Hard Drive Capacity' and val == 1:
                val = 1000
                
            # Add new value to this row
            row.append(val)
        
        # Add the new row to the results
        result.append(row)

    # Create a DataFrame
    cols = ['ID', 'Name', 'Price', 'Brand', 'Screen Size', 'RAM', 'Hard Drive Capacity',
            'Processor Type', 'Processor Speed', 'Operating System', 'Battery Life',
            'Screen Size (Numeric)', 'RAM (Numeric)', 'Hard Drive Capacity (Numeric)',
            'Processor Speed (Numeric)', 'Battery Life (Numeric)']
    return pd.DataFrame(result, columns=cols)


def impute_features(data):

    # Find the mean of each feature
    features = ['Price', 'Screen Size (Numeric)', 'RAM (Numeric)', 'Hard Drive Capacity (Numeric)',
                'Processor Speed (Numeric)', 'Battery Life (Numeric)']
    averages = {}
    for feat in features:
        averages[feat] = data[feat].mean()

    # impute missing values with the average value
    result = []
    cols = list(data.columns)
    for row in data.itertuples():
        row = list(row)[1:len(row)]
            
        # check each feature
        for feat in features:
            if pd.isnull(row[cols.index(feat)]):
                row[cols.index(feat)] = averages[feat]
    
        # Add the updated row to result
        result.append(row)

    # Return a dataframe
    cols = ['ID', 'Name', 'Price', 'Brand', 'Screen Size', 'RAM', 'Hard Drive Capacity',
            'Processor Type', 'Processor Speed', 'Operating System', 'Battery Life',
            'Screen Size (Numeric)', 'RAM (Numeric)', 'Hard Drive Capacity (Numeric)',
            'Processor Speed (Numeric)', 'Battery Life (Numeric)']
    return pd.DataFrame(result, columns=cols)        


'''
This function returns 1.0 if both laptops are refurbished or neither laptop is 
refurbished. It return 0.5 if the Name feature is missing for either laptop. It
returns 0.0 if one laptop is refurbished and the other isn't.
'''
def refurbished(x, y):
	 # Check for null values
    if pd.isnull(x['Name']) or pd.isnull(y['Name']):
        return 0.5

    # Get the laptop names
    x_name = x['Name'].lower()
    y_name = y['Name'].lower()

    if ('refurbished' in x_name) == ('refurbished' in y_name):
        return 1.0
    return 0.0


'''
This function checks that the screen size, RAM, and hard drive capacity are all equal
for the two given tuples. However, whenever there is a missing value for a feature,
the pair of tuples are considered to have equal values for that feature. This prevents
candidates from being killed off from the blocking stage due to missing values. 
Additionally, we allow for a small margin of error (5 percent of the larger value) to
account for minor differences.
'''
def screen_ram_hd_equal(x, y):

    screen = compare_feats(x, y, 'Screen Size')
    ram = compare_feats(x, y, 'RAM')
    drive = compare_feats(x, y, 'Hard Drive Capacity')

    if screen or ram or drive:
        return True
    return False


# This function completes the actual comparison of tuples for screen_ram_hd_equal
def compare_feats(x, y, feat_name):
    # Check for null values
    if pd.isnull(x[feat_name]) or pd.isnull(y[feat_name]):
        return False

    # Set each string to the screen size. Remove non-numeric components
    x_val = float(re.sub('[^0-9.]', '', x[feat_name]))
    y_val = float(re.sub('[^0-9.]', '', y[feat_name]))

    # Get the difference and margin for error for these values
    diff = x_val - y_val
    error = max(x_val, y_val) * 0.05

    # Don't block if the values are close
    if -error < diff < error:
        return False
    # Block otherwise
    return True
