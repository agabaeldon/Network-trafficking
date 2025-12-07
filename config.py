"""
Configuration file for Network Traffic Prediction and Optimization System
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Model Configuration
MODEL_CONFIG = {
    'lstm_units': 50,
    'dropout_rate': 0.2,
    'sequence_length': 60,  # Time steps to look back
    'prediction_horizon': 10,  # Steps ahead to predict
    'batch_size': 32,
    'epochs': 50,
    'validation_split': 0.2,
    'model_path': 'models/traffic_predictor.h5',
    'scaler_path': 'models/scaler.pkl'
}

# Data Collection Configuration
DATA_CONFIG = {
    'collection_interval': 5,  # seconds
    'history_window': 3600,  # 1 hour of history
    'data_file': 'data/network_traffic.csv',
    'simulation_mode': True,  # Set to False for real network monitoring
    'simulation_traffic_base': 1000,  # Base traffic in Mbps
    'simulation_variance': 0.3  # 30% variance
}

# Optimization Configuration
OPTIMIZATION_CONFIG = {
    'bandwidth_threshold_low': 0.3,  # 30% utilization
    'bandwidth_threshold_high': 0.8,  # 80% utilization
    'reallocation_interval': 30,  # seconds
    'min_bandwidth': 100,  # Minimum Mbps per route
    'max_bandwidth': 10000,  # Maximum Mbps per route
    'optimization_algorithm': 'adaptive'  # 'adaptive', 'proportional', 'ml_based'
}

# Network Configuration
NETWORK_CONFIG = {
    'total_bandwidth': 10000,  # Total available bandwidth in Mbps
    'num_routes': 5,
    'route_names': ['Route_1', 'Route_2', 'Route_3', 'Route_4', 'Route_5'],
    'monitoring_interfaces': []  # Add network interfaces to monitor
}

# API Configuration
API_CONFIG = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': True
}

# Evaluation Metrics
METRICS_CONFIG = {
    'mae_threshold': 50,  # Mbps
    'rmse_threshold': 100,  # Mbps
    'latency_threshold': 100,  # ms
    'throughput_target': 0.85  # 85% of total bandwidth
}

