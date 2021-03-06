 
import sys
import os
import os.path

import pandas as pd
import numpy as np

from scipy.special import erf

def pval(n_test, r, classes):
    """
    return the p_value for the null hypothesis
    """
    # Pi = np.array( classes * [1/classes] )
    # Pi = 0.5 + n_test * (1 - classes/2)/np.sum(n_test)
    # std = np.sqrt( np.sum( Pi * (1 -Pi)/n_test ) )/classes
    std = np.sqrt (np.sum(1/n_test) - (classes-2)**2/np.sum(n_test) ) /( 2 * classes )
    
    return 1 - erf( abs( r - 1/classes)/ (np.sqrt(2) * std ) ) 

def sign(p)
    '''
    return the sign according of the p_value
    '''
    sign = '***' if p < .001 else '**' if p < .01 else '*' if p < .05 else 0
    return(sign)

### PATH
base_path = 
raw_path = 

### SESSION and DECODERS       
session = 
#session = os.listdir(raw_path)
#session.remove('unique_recordings.mat')

decoders = ['stim', 'resp'] # ['stim']


for decode_for in decoders :
    if decode_for == 'stim':
        classes = 5
    else:
        classes = 2
    
    
    ## merge files
    df_session = len(session) * [0]
    
    for count, sess_no in enumerate(session):
        file_name = base_path + 'results/training/'+ sess_no + '_training_'+decode_for+'.csv'
        df_session[count] = pd.read_csv(file_name)
        
    result = pd.concat(df_session, ignore_index=True)
    
    
    # select columns
    #result = result
                               #'renorm',
                           #'n_layers','patch_dim', 'pool_dim',
                           #'channels_in', 'channels_out',
                           #'nonlin','fc_units',
                           #'n_iterations', 'size_of_batches', 'learning_rate',
                           #'weights_dist', 'normalized_weights',
                           #'batch_norm',
                           #'keep_prob_train',
                           #'l2_regularization_penalty',
                           #'time']
     
    # keep only these columns
    result = result[ ['session', 'decode_for', 'only_correct_trials',
                      'areas', 'cortex', 'elec_type',
                      'frequency_band',
                      'interval',
                      'recall_macro', 'error_bar_th', 'error_bar_emp',
                      'seed', 'n_splits',
                      'data_size', 'n_chans', 'window_size'] ]
    
    ## ADD pval and sign
    
    result['pval'] = result.apply(lambda row: pval(row.n_test_per_class, row.recall_macro, classes), axis=1)
    result['sign'] = result.apply(lambda row : sign(row.pval), axis=1)
    
    # Save file
    file_name = base_path + 'results/pval/'
            + 'pval_all_sess_'+decode_for+'.csv'
    file_exists = os.path.isfile(file_name)
    # if file already exist, just append the data.
    if file_exists :
        with open(file_name, 'a') as f:
            df.to_csv(f, mode ='a', index=False, header=False)
    else:
        with open(file_name, 'w') as f:
            df.to_csv(f, mode ='w', index=False, header=True)
            
            

        
