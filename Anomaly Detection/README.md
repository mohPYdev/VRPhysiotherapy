# Anomaly Detection in Sensor Data

This project performs anomaly detection on sensor data using a combination of Variational Autoencoder (VAE) and Long Short-Term Memory (LSTM) models.

## Requirements

- Python 3.x
- PyTorch
- pandas
- numpy
- scipy

## Project Structure

- `data_preprocessing.py`: Contains functions for data preprocessing and loading.
- `model_loading.py`: Includes functions for loading the LSTM and VAE models.
- `anomaly_detection.py`: Implements the anomaly detection logic and generates the output.
- `utils.py`: Contains utility functions used across different modules.
- `main.py`: Serves as the entry point of the program, orchestrating the flow of the anomaly detection process.

## Usage

1. Place the sensor data files in the `test_data` folder.
2. Ensure that the LSTM weights (`lstm_model_weights.pth`) and VAE weights (`vae_model_weights.pth`) are available in the project directory.
3. Run the `main.py` script to perform anomaly detection:
4. The script will output a dictionary containing the anomalous batch indices for different threshold values.

## Output Format

The output is a dictionary in the following format:
{
0.25: [list of anomalous batch indices],
0.5: [list of anomalous batch indices],
0.75: [list of anomalous batch indices]
}

Each key in the output dictionary corresponds to a specific threshold value, and the value is a list of anomalous batch indices.