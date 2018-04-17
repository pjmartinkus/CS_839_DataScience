# Stage 3 Data

### Table A: Walmart Data
The Walmart Data contains product information about laptops and was retrieved from Walmart's website in stage 2. More information on the orgin of this table can be found in stage 2.

The original Walmart data from stage 2 can be found in the Walmart.csv file. This is data is taken directly from the results of stage 2. For entity matching, we found that we needed to clean this table up. Specifically, we have made three important changes:

    1. The RAM and hard-drive capacities are often listed in KB when in reality they should be GB. Sometimes the hard drive capicity is listed as 1000 Gb and other times as 1 TB so we set all occurances to 1 TB.
    2. The names are very long and contain plenty of additional information such as the hard drive capacity or the processor type. We added an extra column called 'Clean Name' that has some of this additional information removed.
    3. We updated to format to conform to py_entitymatching. Specifically, we added an id column and changed the quotes used for strings from a single quote to double quotes.

The resulting table for the walmart data after making these changes can be found in Walmart_clean.csv.

Length of the Walmart table: 3034 tuples

### Table B: Amazon Data
Similarly, the data for table B was retrieved from Amazon.com for stage 2 and can be found in the Amazon.csv file. We also had to make some changes to clean the amazon data:

    1. The RAM of many laptops is listed as 6GB when in reality it should be 8GB. Just like the walmart data we changed all occurances of 1000 GB to 1 TB.
    2. Sometimes the brand Lenovo is listed as Lenovo_320. We changed all occurances of Lenovo_320 to just Lenovo.
    3. Just like in the Walmart data we cleaned up the Name column and created a new Clean Name column.
    4. Again, like the Walmart data, we needed to change the format of our table to match the requirments for py_entitymatching.

The resulting table for the Amazon data can be found in Amazon_clean.csv.

Length of the Amazon table: 3102 tuples

### Table C: Final Candidate Set after Blocking

After blocking, we ended up with the candidate C. This data table can be found in the Candidate_Set.csv file. This data table contains all of the tuple pairs that survived the blocking step.

### Table G: Labeled Data

After sampling and labeling, we ended up with the set G which can be found in the Labeled_Data.csv file.

### Sets I and J: Development and Evaluation Set

The development set I can be found in the Development.csv file and the evaluation set J can be found in the Evaluation.csv file.
