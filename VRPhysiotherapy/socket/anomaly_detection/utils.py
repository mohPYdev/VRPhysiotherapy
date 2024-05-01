# utils.py

import pandas as pd

def merge_loss_dataframes(test_loss_df, lstm_loss_df):
    padding_df = pd.DataFrame({'batch': range(-5, 0), 'LSTM_loss': [0] * 5})
    lstm_loss_df = pd.concat([padding_df, lstm_loss_df], ignore_index=True)
    lstm_loss_df['batch'] = range(len(lstm_loss_df))
    result_df = pd.merge(test_loss_df, lstm_loss_df, on='batch', how='outer')
    result_df.fillna(0, inplace=True)
    result_df = result_df[['batch', 'ELBO_loss', 'reconstruction_loss', 'KLD_loss', 'LSTM_loss']]
    return result_df