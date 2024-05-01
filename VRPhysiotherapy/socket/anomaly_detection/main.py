# main.py (continued)
import torch
from data_preprocessing import MyDataset, create_dataloader
from model_loading import load_vae_model, load_lstm_model
from anomaly_detection import get_encodings_with_loss, create_encodings_dataframe, LSTMTrainingDataset, get_lstm_loss, detect_outliers, identify_anomalous_batches
from utils import merge_loss_dataframes


def main():
    data_folder_path = 'test_data'
    window_size = 5
    batch_size = 4
    shuffle = False
    num_workers = 1

    # Load the dataset
    dataset = MyDataset(data_folder_path, window_size)
    data_loader = create_dataloader(dataset, batch_size, shuffle, num_workers)

    # Load the VAE model
    vae_weights_path = 'vae_model_weights.pth'
    window_length = 5
    num_features = 24
    embedding_size = 32
    vae_model = load_vae_model(vae_weights_path, window_length, num_features, embedding_size)

    # Get the encodings and losses from the VAE model
    test_encodings, test_loss_df = get_encodings_with_loss(dataset, vae_model, batch_size=1)
    num_features = len(test_encodings[0])
    test_df_encodings = create_encodings_dataframe(test_encodings, num_features)

    # Load the LSTM model
    lstm_weights_path = 'lstm_model_weights.pth'
    input_size = 32
    hidden_size = 128
    num_layers = 2
    output_size = 32
    use_gpu = False
    device = torch.device("cuda:0" if use_gpu and torch.cuda.is_available() else "cpu")
    lstm_model = load_lstm_model(lstm_weights_path, input_size, hidden_size, num_layers, output_size, device)

    # Create the LSTM dataset and get the losses
    seq_length = 5
    lstm_dataset = LSTMTrainingDataset(test_df_encodings, seq_length)
    lstm_loss_df = get_lstm_loss(lstm_dataset, lstm_model, batch_size=1)

    # Merge the loss dataframes
    result_df = merge_loss_dataframes(test_loss_df, lstm_loss_df)

    # Detect outliers and identify anomalous batches
    result = detect_outliers(result_df)
    smoothed_trend = result['smoothed_trend']
    outliers = result['outliers']
    anomalous_batches = identify_anomalous_batches(result_df, outliers)

    # Print the final result
    print(anomalous_batches)

if __name__ == '__main__':
    main()