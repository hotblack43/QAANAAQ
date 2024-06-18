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
offset_point = 70
offset_value = 4

# Generate synthetic time series data with offset
np.random.seed(0)
time_series = intercept + slope * np.arange(timesteps) + np.random.normal(scale=noise_level, size=timesteps)
time_series[offset_point:] += offset_value

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

# Train on data before the offset
train_data = time_series_scaled[:offset_point]
X_train, Y_train = create_dataset(train_data, look_back)

# Reshape input to be [samples, time steps, features]
X_train = np.reshape(X_train, (X_train.shape[0], look_back, 1))

# Build LSTM model
model = Sequential()
model.add(LSTM(50, input_shape=(look_back, 1)))
model.add(Dense(1))
model.compile(optimizer=Adam(learning_rate=0.01), loss='mean_squared_error')

# Train the model
model.fit(X_train, Y_train, epochs=100, batch_size=1, verbose=2)

# Make predictions on entire series including the offset piece
X_all, Y_all = create_dataset(time_series_scaled, look_back)
X_all = np.reshape(X_all, (X_all.shape[0], look_back, 1))
predictions = model.predict(X_all)
predictions = scaler.inverse_transform(predictions)
actual = scaler.inverse_transform(Y_all.reshape(-1, 1))

# Calculate error series
errors = actual - predictions

# Plot results
plt.figure(figsize=(15, 5))
plt.plot(time_series, label='Actual Time Series')
plt.plot(np.arange(look_back, len(predictions) + look_back), predictions, label='Predicted Time Series')
plt.axvline(x=offset_point, color='r', linestyle='--', label='Offset Point')
plt.legend()
plt.title('Actual vs Predicted Time Series')
plt.xlabel('Time')
plt.ylabel('Value')
plt.show()

# Plot error series
plt.figure(figsize=(15, 5))
plt.plot(errors, label='Error Series')
plt.axvline(x=offset_point - look_back, color='r', linestyle='--', label='Offset Point')
plt.legend()
plt.title('Error Series')
plt.xlabel('Time')
plt.ylabel('Error')
plt.show()

