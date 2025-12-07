"""
Machine Learning Models for Network Traffic Prediction
Implements LSTM and GRU models for time-series forecasting
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
import tensorflow as tf
try:
    from tensorflow import keras
    from tensorflow.keras.models import Sequential, load_model
    from tensorflow.keras.layers import LSTM, GRU, Dense, Dropout
    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
except ImportError:
    # Fallback for Keras 3.x standalone
    import keras
    from keras.models import Sequential
    from keras.layers import LSTM, GRU, Dense, Dropout
    from keras.callbacks import EarlyStopping, ModelCheckpoint
    from keras.saving import load_model
import joblib
import os
import logging
from config import MODEL_CONFIG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TrafficPredictor:
    """LSTM-based network traffic predictor"""
    
    def __init__(self):
        self.model = None
        self.scaler = MinMaxScaler()
        self.sequence_length = MODEL_CONFIG['sequence_length']
        self.prediction_horizon = MODEL_CONFIG['prediction_horizon']
        self.model_path = MODEL_CONFIG['model_path']
        self.scaler_path = MODEL_CONFIG['scaler_path']
        
        # Ensure models directory exists
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
    
    def prepare_data(self, df, feature_columns=None):
        """Prepare data for training"""
        if feature_columns is None:
            feature_columns = ['bandwidth_utilization', 'latency', 'packet_loss']
        
        # Select features
        data = df[feature_columns].values
        
        # Scale the data
        scaled_data = self.scaler.fit_transform(data)
        
        # Create sequences
        X, y = [], []
        for i in range(self.sequence_length, len(scaled_data) - self.prediction_horizon + 1):
            X.append(scaled_data[i - self.sequence_length:i])
            y.append(scaled_data[i:i + self.prediction_horizon, 0])  # Predict bandwidth
        
        return np.array(X), np.array(y)
    
    def build_lstm_model(self, input_shape):
        """Build LSTM model architecture"""
        model = Sequential([
            LSTM(MODEL_CONFIG['lstm_units'], return_sequences=True, input_shape=input_shape),
            Dropout(MODEL_CONFIG['dropout_rate']),
            LSTM(MODEL_CONFIG['lstm_units'], return_sequences=False),
            Dropout(MODEL_CONFIG['dropout_rate']),
            Dense(25),
            Dense(self.prediction_horizon)
        ])
        
        model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )
        
        return model
    
    def build_gru_model(self, input_shape):
        """Build GRU model architecture"""
        model = Sequential([
            GRU(MODEL_CONFIG['lstm_units'], return_sequences=True, input_shape=input_shape),
            Dropout(MODEL_CONFIG['dropout_rate']),
            GRU(MODEL_CONFIG['lstm_units'], return_sequences=False),
            Dropout(MODEL_CONFIG['dropout_rate']),
            Dense(25),
            Dense(self.prediction_horizon)
        ])
        
        model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )
        
        return model
    
    def train(self, df, model_type='lstm', feature_columns=None):
        """Train the prediction model"""
        logger.info("Preparing training data...")
        X, y = self.prepare_data(df, feature_columns)
        
        if len(X) == 0:
            logger.error("Insufficient data for training")
            return False
        
        logger.info(f"Training data shape: X={X.shape}, y={y.shape}")
        
        # Build model
        input_shape = (X.shape[1], X.shape[2])
        if model_type.lower() == 'gru':
            self.model = self.build_gru_model(input_shape)
        else:
            self.model = self.build_lstm_model(input_shape)
        
        logger.info(f"Built {model_type.upper()} model")
        
        # Callbacks
        early_stopping = EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        )
        
        model_checkpoint = ModelCheckpoint(
            self.model_path,
            monitor='val_loss',
            save_best_only=True,
            verbose=1
        )
        
        # Train model
        logger.info("Training model...")
        history = self.model.fit(
            X, y,
            batch_size=MODEL_CONFIG['batch_size'],
            epochs=MODEL_CONFIG['epochs'],
            validation_split=MODEL_CONFIG['validation_split'],
            callbacks=[early_stopping, model_checkpoint],
            verbose=1
        )
        
        # Save scaler
        joblib.dump(self.scaler, self.scaler_path)
        logger.info(f"Model saved to {self.model_path}")
        logger.info(f"Scaler saved to {self.scaler_path}")
        
        return True
    
    def load_model(self):
        """Load trained model and scaler"""
        try:
            if os.path.exists(self.model_path):
                self.model = load_model(self.model_path)
                logger.info(f"Model loaded from {self.model_path}")
            else:
                logger.warning("Model file not found")
                return False
            
            if os.path.exists(self.scaler_path):
                self.scaler = joblib.load(self.scaler_path)
                logger.info(f"Scaler loaded from {self.scaler_path}")
            else:
                logger.warning("Scaler file not found")
                return False
            
            return True
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False
    
    def predict(self, recent_data, feature_columns=None):
        """Make prediction based on recent data"""
        if self.model is None:
            if not self.load_model():
                logger.error("Model not available for prediction")
                return None
        
        if feature_columns is None:
            feature_columns = ['bandwidth_utilization', 'latency', 'packet_loss']
        
        # Prepare input
        if isinstance(recent_data, pd.DataFrame):
            data = recent_data[feature_columns].values
        else:
            data = recent_data
        
        # Scale data
        scaled_data = self.scaler.transform(data)
        
        # Ensure we have enough data points
        if len(scaled_data) < self.sequence_length:
            logger.warning(f"Insufficient data points. Need {self.sequence_length}, got {len(scaled_data)}")
            return None
        
        # Take last sequence_length points
        sequence = scaled_data[-self.sequence_length:]
        sequence = sequence.reshape(1, self.sequence_length, len(feature_columns))
        
        # Predict
        prediction = self.model.predict(sequence, verbose=0)
        
        # Inverse transform (only for bandwidth)
        # Create dummy array for inverse transform
        dummy = np.zeros((len(prediction[0]), len(feature_columns)))
        dummy[:, 0] = prediction[0]
        prediction_original = self.scaler.inverse_transform(dummy)[:, 0]
        
        return prediction_original
    
    def evaluate(self, df, feature_columns=None):
        """Evaluate model performance"""
        if self.model is None:
            if not self.load_model():
                return None
        
        X, y_true = self.prepare_data(df, feature_columns)
        
        if len(X) == 0:
            return None
        
        y_pred = self.model.predict(X, verbose=0)
        
        # Inverse transform predictions
        dummy_true = np.zeros((len(y_true), len(feature_columns) if feature_columns else 3))
        dummy_pred = np.zeros((len(y_pred), len(feature_columns) if feature_columns else 3))
        
        dummy_true[:, 0] = y_true[:, 0] if len(y_true.shape) > 1 else y_true
        dummy_pred[:, 0] = y_pred[:, 0] if len(y_pred.shape) > 1 else y_pred
        
        y_true_original = self.scaler.inverse_transform(dummy_true)[:, 0]
        y_pred_original = self.scaler.inverse_transform(dummy_pred)[:, 0]
        
        # Calculate metrics
        mae = mean_absolute_error(y_true_original, y_pred_original)
        rmse = np.sqrt(mean_squared_error(y_true_original, y_pred_original))
        
        return {
            'mae': mae,
            'rmse': rmse,
            'predictions': y_pred_original,
            'actual': y_true_original
        }

