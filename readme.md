# Real-Time Network Traffic Prediction and Optimization System

A complete machine learning-based framework for real-time network traffic prediction and bandwidth optimization using LSTM neural networks.

## Authors
- WANYAMA DAVID 2022/BSE/016/PS
- LUMURO JOSEPH KANJAGA 2022/BSE/006/PS
- AGABA ELDON 2021/BSE/129/PS
- MURIISA JOHN 2021/BSE/081/PS
- TWINE BENSON VAMER 2021/BSE/176/PS
- MULINDWA ERIC 2020/BSE/036/PS

## 📚 Documentation


## Features

- **Real-time Traffic Prediction**: LSTM/GRU models for accurate traffic forecasting
- **Bandwidth Optimization**: Adaptive algorithms for dynamic bandwidth allocation
- **Web Dashboard**: Interactive visualization and monitoring interface
- **Data Collection**: Automatic network traffic data collection (simulated or real)
- **Performance Evaluation**: Comprehensive metrics (MAE, RMSE, R², latency, throughput)
- **Multiple Optimization Algorithms**: Adaptive, Proportional, and ML-based approaches

## System Architecture

```
┌─────────────────┐
│  Data Collector │ → Collects network traffic data
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   ML Models     │ → LSTM/GRU for traffic prediction
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Optimizer     │ → Bandwidth allocation optimization
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Web Dashboard  │ → Real-time visualization & control
└─────────────────┘
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Clone or navigate to the project directory**
```bash
cd "network trafficing"
```

2. **Create a virtual environment (recommended)**
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Linux/Mac:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create necessary directories**
```bash
mkdir data models
```

## Usage

### Quick Start

1. **Start the web dashboard** (recommended for first-time users):
```bash
python main.py web
```

Then open your browser and navigate to: `http://localhost:5000`

2. **Collect data first** (if starting fresh):
```bash
python main.py collect --hours 1
```

3. **Train the model**:
```bash
python main.py train --hours 24
```

4. **Start monitoring** (standalone):
```bash
python main.py monitor
```

### Command-Line Options

- `collect`: Collect network traffic data
  - `--hours N`: Collect data for N hours (default: 1)

- `train`: Train the prediction model
  - `--hours N`: Use N hours of historical data (default: 24)

- `evaluate`: Evaluate system performance
  - `--hours N`: Evaluate on N hours of data (default: 24)

- `monitor`: Run monitoring service (standalone)

- `web`: Start web dashboard (recommended)

### Web Dashboard Features

The web dashboard provides:
- Real-time traffic monitoring
- Traffic prediction visualization
- Bandwidth allocation charts
- Route-specific metrics
- System control (start/stop monitoring, train model)
- Performance metrics display

Access at: `http://localhost:5000`

## Configuration

Edit `config.py` to customize:

- **Model Configuration**: LSTM units, sequence length, epochs
- **Data Collection**: Collection interval, simulation mode
- **Optimization**: Algorithm type, thresholds, bandwidth limits
- **Network Settings**: Total bandwidth, number of routes
- **API Settings**: Host, port, debug mode

### Key Configuration Options

```python
# Enable real network monitoring (requires admin privileges)
DATA_CONFIG['simulation_mode'] = False

# Change optimization algorithm
OPTIMIZATION_CONFIG['optimization_algorithm'] = 'adaptive'  # or 'proportional', 'ml_based'

# Adjust total bandwidth
NETWORK_CONFIG['total_bandwidth'] = 10000  # Mbps
```

## Project Structure

```
network trafficing/
├── main.py              # Main entry point
├── config.py            # Configuration settings
├── data_collector.py    # Network data collection
├── ml_models.py         # LSTM/GRU prediction models
├── optimizer.py         # Bandwidth optimization algorithms
├── monitor.py           # Real-time monitoring service
├── evaluator.py         # Performance evaluation
├── app.py              # Flask web application
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── data/               # Collected traffic data (CSV)
└── models/             # Trained models and scalers
```

## How It Works

1. **Data Collection**: System collects network traffic metrics (bandwidth, latency, packet loss) at regular intervals
2. **Prediction**: LSTM model analyzes historical patterns to predict future traffic
3. **Optimization**: Optimization algorithms allocate bandwidth across routes based on predictions
4. **Monitoring**: Real-time dashboard displays current state, predictions, and optimizations
5. **Evaluation**: System tracks performance metrics (MAE, RMSE, utilization, latency)

## Evaluation Metrics

The system evaluates performance using:

- **MAE (Mean Absolute Error)**: Average prediction error in Mbps
- **RMSE (Root Mean Square Error)**: Penalizes larger errors
- **R² Score**: Model fit quality (0-1, higher is better)
- **MAPE (Mean Absolute Percentage Error)**: Percentage prediction error
- **Latency**: Network response time in milliseconds
- **Throughput**: Bandwidth utilization percentage

## Troubleshooting

### Model Not Found Error
If you see "Model file not found":
1. Collect data: `python main.py collect --hours 1`
2. Train model: `python main.py train --hours 24`

### Port Already in Use
If port 5000 is busy, edit `config.py`:
```python
API_CONFIG['port'] = 5001  # or another port
```

### Insufficient Data
The model needs at least 60 data points. Collect more data:
```bash
python main.py collect --hours 2
```

### TensorFlow/Keras Issues
If you encounter TensorFlow errors:
```bash
pip install --upgrade tensorflow keras
```

## Performance Tips

1. **Training**: More data = better predictions. Collect at least 24 hours of data
2. **Sequence Length**: Longer sequences (60+) capture more patterns but require more data
3. **Optimization**: 'adaptive' algorithm works best for dynamic traffic
4. **Collection Interval**: 5 seconds is optimal balance between accuracy and overhead

## Future Enhancements

- Reinforcement learning for optimization
- Anomaly detection for network attacks
- Multi-network support
- Historical data analysis dashboard
- Export reports (PDF, CSV)
- REST API for integration

## License

This project is developed for academic research purposes.

## References

1. Cisco. (2023). Cisco Annual Internet Report
2. Lv, Y., et al. (2015). Traffic flow prediction with big data: A deep learning approach
3. Wang, J., et al. (2020). Network traffic prediction and optimization using machine learning
4. Zhang, C., et al. (2022). Real-time network traffic forecasting with deep learning

## Support

For issues or questions, please check:
- Configuration in `config.py`
- Logs in console output
- Data files in `data/` directory
- Model files in `models/` directory

---

**Note**: This system can operate in simulation mode (default) or real network monitoring mode. For production use with real networks, ensure proper permissions and network access.
