# Import files and packages
import pandas as pd
import numpy as np
import py_entitymatching as em
from Features import screen_ram_hd_equal, refurbished

def workflow(path_A, path_B, path_labeled):
    
    # Load csv files as dataframes and set the key attribute in the dataframe
    A = em.read_csv_metadata(path_A, key='ID')
    B = em.read_csv_metadata(path_B, key='ID')

    # Run attribute equivalence blocker on brand
    ab = em.AttrEquivalenceBlocker()
    C1 = ab.block_tables(A, B, 'Brand', 'Brand',
                   l_output_attrs=['Name', 'Price', 'Brand', 'Screen Size', 
                                   'RAM', 'Hard Drive Capacity', 'Processor Type',
                                   'Processor Speed', 'Operating System', 'Clean Name'],
                   r_output_attrs=['Name', 'Price', 'Brand', 'Screen Size', 
                                   'RAM', 'Hard Drive Capacity', 'Processor Type',
                                   'Processor Speed', 'Operating System', 'Clean Name'])


    # Get features for rule based blocking
    block_f = em.get_features_for_blocking(A, B, validate_inferred_attr_types=False)

    # Run rule based blocker with rule for jaccard score on Clean Name column
    rb = em.RuleBasedBlocker()
    rb.add_rule(['Clean_Name_Clean_Name_jac_qgm_3_qgm_3(ltuple, rtuple) < 0.2'], block_f)
    C2 = rb.block_candset(C1)

    # Run black box blocker to compare screen size, ram, and hard drive capacity
    bb_screen = em.BlackBoxBlocker()
    bb_screen.set_black_box_function((screen_ram_hd_equal))
    C = bb_screen.block_candset(C2)

    # Load the labeled data
    L = em.read_csv_metadata(path_labeled, key='_id', ltable=A, rtable=B, 
                             fk_ltable='ltable_ID', fk_rtable='rtable_ID')

    # Generate features
    feature_table = em.get_features_for_matching(A, B, validate_inferred_attr_types=False)
    feature_subset = feature_table.iloc[np.r_[4:10, 40:len(feature_table)], :]
    em.add_blackbox_feature(feature_subset, 'refurbished', refurbished)

    # Extract feature vectors
    feature_vectors_dev = em.extract_feature_vecs(L, 
                                                  feature_table=feature_subset, 
                                                  attrs_after='gold')

    # Impute feature vectors with the mean of the column values.
    feature_vectors_dev = em.impute_table(feature_vectors_dev, 
                                          exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'gold'],
                                          strategy='mean')

    # Train using feature vectors from the labeled data
    matcher = em.RFMatcher(name='RF')
    matcher.fit(table=feature_vectors_dev, 
                exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'gold'], 
                target_attr='gold')

    # Extract feature vectors for the rest of the data
    feature_vectors = em.extract_feature_vecs(C, feature_table=feature_subset)

    # Impute feature vectors with the mean of the column values.
    feature_vectors = em.impute_table(feature_vectors, 
                                      exclude_attrs=['_id', 'ltable_ID', 'rtable_ID'],
                                      strategy='mean')

    # Make predictions for the whole data set
    predictions = matcher.predict(table=feature_vectors, 
                                       exclude_attrs=['_id', 'ltable_ID', 'rtable_ID'], 
                                       append=True, 
                                       target_attr='predicted', 
                                       inplace=False)
    predictions = predictions.loc[:, ['_id', 'ltable_ID', 'rtable_ID', 'predicted']]

    return predictions[predictions['predicted'] == 1]

