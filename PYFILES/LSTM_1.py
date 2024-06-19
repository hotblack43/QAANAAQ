import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam

# Parameters
intercept = 10
slope = 2
noise_level = 0.5
timesteps = 100

# Generate synthetic time series data
np.random.seed(0)
time_series = intercept + slope * np.arange(timesteps) + np.random.normal(scale=noise_level, size=timesteps)

# Normalize data
scaler = MinMaxScaler(feature_range=(0, 1))
time_series_scaled = scaler.fit_transform(time_series.reshape(-1, 1))

# Prepare data for LSTM
def create_dataset(data, look_back=1):
    X, Y = [], []
    for i in range(len(data) - look_back):
        X.append(data[i:(i + look_back), 0])
        Y.append(data[i + look_back, 0])
    return np.array(X), np.array(Y)

look_back = 1
X, Y = create_dataset(time_series_scaled, look_back)

# Reshape input to be [samples, time steps, features]
X = np.reshape(X, (X.shape[0], look_back, 1))

# Build LSTM model
model = Sequential()
model.add(LSTM(50, input_shape=(look_back, 1)))
model.add(Dense(1))
model.compile(optimizer=Adam(learning_rate=0.01), loss='mean_squared_error')

# Train the model
model.fit(X, Y, epochs=100, batch_size=1, verbose=2)

# Make predictions
predictions = model.predict(X)
predictions = scaler.inverse_transform(predictions)
actual = scaler.inverse_transform(Y.reshape(-1, 1))

# Calculate error series
errors = actual - predictions

# Plot results
plt.figure(figsize=(15, 5))
plt.plot(time_series, label='Actual Time Series')
plt.plot(np.arange(look_back, len(predictions) + look_back), predictions, label='Predicted Time Series')
plt.legend()
plt.title('Actual vs Predicted Time Series')
plt.xlabel('Time')
plt.ylabel('Value')
plt.show()

# Plot error series
plt.figure(figsize=(15, 5))
plt.plot(errors, label='Error Series')
plt.legend()
plt.title('Error Series')
plt.xlabel('Time')
plt.ylabel('Error')
plt.show()

