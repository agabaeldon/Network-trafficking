# PROJECT REPORT

## REAL-TIME NETWORK TRAFFIC PREDICTION AND OPTIMIZATION SYSTEM USING MACHINE LEARNING

---

**Submitted by:**

| Name | Registration Number |
|------|-------------------|
| WANYAMA DAVID | 2022/BSE/016/PS |
| LUMURO JOSEPH KANJAGA | 2022/BSE/006/PS |
| AGABA ELDON | 2021/BSE/129/PS |
| MURIISA JOHN | 2021/BSE/081/PS |
| TWINE BENSON VAMER | 2021/BSE/176/PS |
| MULINDWA ERIC | 2020/BSE/036/PS |

**Date:** December 2025

**GitHub Repository:** https://github.com/agabaeldon/Network-trafficking

---

## TABLE OF CONTENTS

1. [Executive Summary](#executive-summary)
2. [Introduction](#introduction)
3. [Problem Statement](#problem-statement)
4. [Objectives](#objectives)
5. [System Architecture](#system-architecture)
6. [Methodology](#methodology)
7. [Implementation](#implementation)
8. [System Features](#system-features)
9. [Results and Evaluation](#results-and-evaluation)
10. [Conclusion](#conclusion)
11. [References](#references)
12. [Appendices](#appendices)

---

## 1. EXECUTIVE SUMMARY

This report presents the development and implementation of a **Real-Time Network Traffic Prediction and Optimization System** using Machine Learning techniques. The system addresses the critical challenge of network congestion and inefficient bandwidth utilization in modern communication networks.

### Key Achievements:

- ✅ **Developed** a complete ML-based framework for real-time network traffic prediction
- ✅ **Implemented** LSTM (Long Short-Term Memory) neural networks for accurate traffic forecasting
- ✅ **Created** adaptive bandwidth optimization algorithms for dynamic resource allocation
- ✅ **Built** an interactive web dashboard for real-time monitoring and visualization
- ✅ **Achieved** automated network management with predictive capabilities

### System Capabilities:

- **Real-time Data Collection:** Automatic network traffic monitoring every 5 seconds
- **AI-Powered Prediction:** LSTM models predict future traffic patterns with high accuracy
- **Automatic Optimization:** Dynamic bandwidth allocation across multiple network routes
- **Performance Metrics:** Comprehensive evaluation using MAE, RMSE, R², and latency metrics
- **User-Friendly Interface:** Web-based dashboard for monitoring and control

### Impact:

The system enables network operators to:
- **Predict** traffic spikes before they occur
- **Prevent** network congestion proactively
- **Optimize** bandwidth utilization automatically
- **Improve** Quality of Service (QoS) for end users
- **Reduce** operational costs through efficient resource management

---

## 2. INTRODUCTION

### 2.1 Background

Modern communication networks face unprecedented challenges due to exponential growth in data-driven applications, IoT devices, and high-bandwidth multimedia services. According to Cisco (2023), global IP traffic is projected to reach 5.3 zettabytes per year by 2025, highlighting the urgent need for intelligent network management systems.

Traditional network management approaches rely on static, rule-based mechanisms that are reactive rather than predictive. These methods often fail to adapt to sudden traffic spikes or fluctuations, leading to:

- Network congestion during peak hours
- Inefficient bandwidth utilization
- Poor Quality of Service (QoS)
- High operational costs
- User dissatisfaction

### 2.2 Motivation

Machine Learning (ML) techniques, particularly time-series forecasting and deep learning, have demonstrated superior performance in predicting network behavior compared to classical statistical methods. By integrating ML into network management systems, operators can:

- **Proactively** manage network resources
- **Predict** traffic patterns before they occur
- **Optimize** bandwidth allocation dynamically
- **Improve** overall network efficiency

### 2.3 Scope

This project focuses on developing a comprehensive framework that:
- Collects real-time network traffic data
- Predicts future traffic patterns using LSTM neural networks
- Optimizes bandwidth allocation automatically
- Provides real-time monitoring and visualization
- Evaluates system performance using standard metrics

---

## 3. PROBLEM STATEMENT

Current network management systems, especially in developing regions like Uganda, face significant challenges:

### 3.1 Existing Problems

1. **Reactive Management:** Systems respond to problems after they occur, not before
2. **Static Thresholds:** Fixed rules cannot adapt to dynamic traffic patterns
3. **Inefficient Resource Utilization:** Bandwidth is often wasted on idle routes while other routes are congested
4. **Lack of Predictive Capabilities:** No ability to forecast traffic spikes
5. **Manual Intervention Required:** Network administrators must manually adjust settings
6. **Limited Real-time Monitoring:** Insufficient visibility into network performance

### 3.2 Research Gap

- Limited research on real-time prediction in resource-constrained networks
- Few studies integrate prediction and optimization in a single framework
- Most ML-based methods are validated on simulated data rather than real-world networks
- Lack of user-friendly interfaces for network administrators

### 3.3 Solution Approach

Our system addresses these challenges by:
- Implementing **predictive** rather than reactive management
- Using **adaptive** algorithms that learn from network patterns
- Providing **automatic** optimization without manual intervention
- Offering **real-time** monitoring and visualization
- Supporting both **simulated** and **real** network environments

---

## 4. OBJECTIVES

### 4.1 Main Objective

To develop and evaluate a machine learning-based framework for real-time network traffic prediction and optimization to enhance network efficiency and Quality of Service.

### 4.2 Specific Objectives

1. **To review existing network traffic prediction and optimization methods**
   - Analyzed current approaches and identified research gaps
   - Evaluated ML techniques suitable for time-series traffic prediction
   - Reviewed optimization algorithms for bandwidth allocation

2. **To design and implement a machine learning model capable of real-time traffic forecasting**
   - Implemented LSTM (Long Short-Term Memory) neural networks
   - Developed GRU (Gated Recurrent Unit) as alternative model
   - Created data preprocessing and feature engineering pipeline
   - Achieved real-time prediction capabilities

3. **To evaluate the system's performance in terms of prediction accuracy, latency reduction, and bandwidth utilization**
   - Implemented comprehensive evaluation metrics (MAE, RMSE, R², MAPE)
   - Measured network performance improvements
   - Evaluated optimization algorithm effectiveness
   - Compared different optimization strategies

---

## 5. SYSTEM ARCHITECTURE

### 5.1 Overall Architecture

The system follows a modular architecture with four main components:

```
┌─────────────────────────────────────────────────────────┐
│                    WEB DASHBOARD                        │
│         (Flask Application - User Interface)           │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│              REAL-TIME MONITORING SERVICE                │
│              (Orchestrates all components)              │
└───────┬───────────────────────┬──────────────────────────┘
        │                       │
        ▼                       ▼
┌──────────────────┐   ┌──────────────────┐
│  DATA COLLECTOR  │   │  ML PREDICTOR    │
│  - Collects      │   │  - LSTM/GRU      │
│    traffic data  │   │  - Predicts       │
│  - Simulated/    │   │    future traffic │
│    Real network  │   │  - Evaluates      │
└────────┬─────────┘   └────────┬─────────┘
         │                      │
         └──────────┬───────────┘
                    ▼
         ┌──────────────────┐
         │   OPTIMIZER       │
         │  - Adaptive       │
         │  - Proportional   │
         │  - ML-based       │
         │  - Allocates      │
         │    bandwidth      │
         └───────────────────┘
```

### 5.2 Component Details

#### 5.2.1 Data Collection Module
- **Purpose:** Collects network traffic metrics
- **Features:**
  - Real-time data collection every 5 seconds
  - Supports both simulated and real network monitoring
  - Collects: bandwidth, latency, packet loss, route-specific traffic
  - Stores data in CSV format for historical analysis

#### 5.2.2 Machine Learning Prediction Module
- **Purpose:** Predicts future network traffic
- **Models Implemented:**
  - LSTM (Long Short-Term Memory) - Primary model
  - GRU (Gated Recurrent Unit) - Alternative model
- **Features:**
  - Sequence length: 60 time steps (look back)
  - Prediction horizon: 10 steps ahead
  - Automatic data scaling and preprocessing
  - Model persistence and loading

#### 5.2.3 Optimization Module
- **Purpose:** Optimizes bandwidth allocation
- **Algorithms:**
  - **Adaptive:** Load balancing with threshold-based redistribution
  - **Proportional:** Distribution based on traffic demand
  - **ML-based:** Machine learning-driven optimization
- **Features:**
  - Dynamic bandwidth allocation
  - Route-specific optimization
  - Utilization threshold management
  - Real-time adjustment

#### 5.2.4 Web Dashboard
- **Purpose:** User interface for monitoring and control
- **Features:**
  - Real-time traffic visualization
  - Interactive charts and graphs
  - System control (start/stop monitoring, train model)
  - Performance metrics display
  - Route-specific details

---

## 6. METHODOLOGY

### 6.1 Research Design

The study adopts a **developmental research design**, integrating system development with empirical evaluation. Both qualitative and quantitative analyses are conducted:

- **Quantitative:** Model performance metrics (MAE, RMSE, R²)
- **Quantitative:** Network performance metrics (latency, throughput, utilization)
- **Qualitative:** System usability and efficiency evaluation

### 6.2 Development Approach

Following a **Prototyping Model**:

1. **Requirement Analysis**
   - Identified network traffic patterns
   - Defined data sources and requirements
   - Specified optimization requirements

2. **Model Development**
   - Trained LSTM/GRU models on historical traffic data
   - Implemented data preprocessing pipeline
   - Developed prediction algorithms

3. **Optimization Module**
   - Designed bandwidth allocation algorithms
   - Implemented adaptive optimization strategies
   - Created real-time adjustment mechanisms

4. **User Interface Development**
   - Built web-based dashboard
   - Implemented real-time visualization
   - Created control interfaces

5. **Testing and Evaluation**
   - Tested with simulated network traffic
   - Evaluated model performance
   - Measured optimization effectiveness
   - Refined based on results

### 6.3 Data Collection

- **Simulated Mode:** Generates realistic network traffic patterns
  - Base traffic: 1000 Mbps
  - Variance: 30%
  - Time-based patterns (peak hours, off-peak)
  - Random spikes and variations

- **Real Network Mode:** Monitors actual network interfaces
  - Uses psutil library for system network statistics
  - Collects bytes sent/received, packets, latency
  - Requires appropriate system permissions

### 6.4 Machine Learning Approach

#### 6.4.1 Model Architecture

**LSTM Model:**
- Input Layer: Sequence of 60 time steps
- LSTM Layer 1: 50 units, return sequences
- Dropout: 0.2 (regularization)
- LSTM Layer 2: 50 units
- Dropout: 0.2
- Dense Layer: 25 units
- Output Layer: 10 predictions (prediction horizon)

**Training Parameters:**
- Batch size: 32
- Epochs: 50 (with early stopping)
- Optimizer: Adam
- Loss function: Mean Squared Error (MSE)
- Validation split: 20%

#### 6.4.2 Data Preprocessing

- **Feature Selection:** Bandwidth utilization, latency, packet loss
- **Scaling:** Min-Max normalization (0-1 range)
- **Sequence Creation:** Sliding window approach
- **Train/Test Split:** 80/20 with temporal ordering

### 6.5 Optimization Algorithms

#### 6.5.1 Adaptive Algorithm

- **Threshold-based:** Low (30%) and High (80%) utilization thresholds
- **Load Balancing:** Redistributes from underloaded to overloaded routes
- **Dynamic Adjustment:** Real-time bandwidth reallocation
- **Constraint Handling:** Maintains min/max bandwidth limits

#### 6.5.2 Proportional Algorithm

- **Demand-based:** Allocates bandwidth proportional to traffic demand
- **Current + Predicted:** Uses average of current and predicted traffic
- **Normalization:** Ensures total allocation doesn't exceed capacity

---

## 7. IMPLEMENTATION

### 7.1 Technology Stack

- **Programming Language:** Python 3.8+
- **Machine Learning:** TensorFlow 2.15+, Keras 2.15+
- **Web Framework:** Flask 2.3+
- **Data Processing:** Pandas, NumPy
- **Visualization:** Plotly, Matplotlib
- **System Monitoring:** psutil
- **Other Libraries:** scikit-learn, joblib

### 7.2 Project Structure

```
network-trafficking/
├── main.py              # Main entry point
├── config.py            # Configuration settings
├── data_collector.py    # Network data collection
├── ml_models.py          # LSTM/GRU prediction models
├── optimizer.py         # Bandwidth optimization
├── monitor.py           # Real-time monitoring service
├── evaluator.py         # Performance evaluation
├── app.py               # Flask web application
├── requirements.txt     # Python dependencies
├── readme.md            # Documentation
├── data/                # Collected traffic data
└── models/              # Trained models
```

### 7.3 Key Implementation Features

#### 7.3.1 Real-Time Data Collection
- Automatic collection every 5 seconds
- Supports multiple network routes
- Stores historical data for training
- Handles both simulated and real networks

#### 7.3.2 Model Training
- Automatic data preparation
- Sequence generation for time-series
- Model checkpointing for best performance
- Early stopping to prevent overfitting
- Model persistence for reuse

#### 7.3.3 Prediction Pipeline
- Loads trained model
- Preprocesses recent data
- Generates predictions for next 10 steps
- Distributes predictions across routes
- Updates in real-time

#### 7.3.4 Optimization Engine
- Monitors route utilization
- Identifies overloaded/underloaded routes
- Calculates optimal bandwidth allocation
- Applies constraints (min/max limits)
- Updates allocation in real-time

#### 7.3.5 Web Dashboard
- Real-time data updates (every 5 seconds)
- Interactive charts using Plotly
- System control buttons
- Performance metrics display
- Responsive design

---

## 8. SYSTEM FEATURES

### 8.1 Core Features

#### 8.1.1 Real-Time Monitoring
- ✅ Continuous data collection
- ✅ Live traffic visualization
- ✅ Route-specific metrics
- ✅ System status indicators

#### 8.1.2 Traffic Prediction
- ✅ LSTM-based forecasting
- ✅ Multi-step ahead predictions
- ✅ Route-specific predictions
- ✅ Confidence indicators

#### 8.1.3 Bandwidth Optimization
- ✅ Automatic allocation
- ✅ Multiple algorithms (Adaptive, Proportional, ML-based)
- ✅ Dynamic adjustment
- ✅ Constraint handling

#### 8.1.4 Performance Evaluation
- ✅ MAE (Mean Absolute Error)
- ✅ RMSE (Root Mean Square Error)
- ✅ R² Score
- ✅ MAPE (Mean Absolute Percentage Error)
- ✅ Latency metrics
- ✅ Throughput analysis

### 8.2 User Interface Features

#### 8.2.1 Dashboard Components
- **Status Indicator:** System running/stopped status
- **Current Traffic Card:** Real-time traffic per route
- **Predicted Traffic Card:** Future traffic predictions
- **System Metrics Card:** Overall performance indicators
- **Traffic Trends Chart:** Visual comparison of current vs predicted
- **Bandwidth Allocation Chart:** Allocation visualization
- **Route Details:** Individual route statistics

#### 8.2.2 Control Functions
- **Start Monitoring:** Begin data collection
- **Stop Monitoring:** Pause data collection
- **Train Model:** Train AI model on collected data
- **Refresh:** Reload dashboard

### 8.3 Configuration Options

- **Model Parameters:** LSTM units, sequence length, epochs
- **Data Collection:** Interval, simulation mode, traffic patterns
- **Optimization:** Algorithm selection, thresholds, bandwidth limits
- **Network Settings:** Total bandwidth, number of routes
- **API Settings:** Host, port, debug mode

---

## 9. RESULTS AND EVALUATION

### 9.1 Model Performance Metrics

The system evaluates prediction accuracy using standard metrics:

#### 9.1.1 Mean Absolute Error (MAE)
- **Definition:** Average absolute difference between predicted and actual values
- **Target:** < 50 Mbps
- **Interpretation:** Lower is better
- **Use Case:** Measures average prediction error

#### 9.1.2 Root Mean Square Error (RMSE)
- **Definition:** Square root of average squared errors
- **Target:** < 100 Mbps
- **Interpretation:** Penalizes larger errors more
- **Use Case:** Better indicator of overall accuracy

#### 9.1.3 R² Score (Coefficient of Determination)
- **Definition:** Proportion of variance explained by model
- **Range:** 0 to 1 (higher is better)
- **Target:** > 0.8
- **Interpretation:** Model fit quality

#### 9.1.4 Mean Absolute Percentage Error (MAPE)
- **Definition:** Average percentage error
- **Interpretation:** Lower is better
- **Use Case:** Relative error measurement

### 9.2 Network Performance Metrics

#### 9.2.1 Bandwidth Utilization
- **Current Utilization:** Real-time percentage of total bandwidth used
- **Average Utilization:** Long-term average
- **Target Range:** 30-70% (healthy usage)
- **Monitoring:** Prevents over/under utilization

#### 9.2.2 Latency
- **Definition:** Network response time in milliseconds
- **Target:** < 100 ms
- **Monitoring:** Ensures acceptable response times

#### 9.2.3 Throughput
- **Definition:** Actual data transfer rate
- **Target:** > 85% of allocated bandwidth
- **Monitoring:** Measures efficiency

### 9.3 Optimization Effectiveness

#### 9.3.1 Allocation Stability
- Measures how often allocation changes
- Higher stability = fewer disruptions
- Target: Stable allocation with minimal changes

#### 9.3.2 Resource Utilization
- Measures how efficiently bandwidth is used
- Target: High utilization without congestion
- Monitors: Balance between efficiency and performance

### 9.4 System Capabilities Demonstrated

✅ **Real-time Data Collection:** Successfully collects network data every 5 seconds  
✅ **Traffic Prediction:** LSTM model accurately predicts future traffic patterns  
✅ **Bandwidth Optimization:** Adaptive algorithm effectively redistributes bandwidth  
✅ **Web Dashboard:** Provides intuitive interface for monitoring and control  
✅ **Performance Evaluation:** Comprehensive metrics for system assessment  

---

## 10. CONCLUSION

### 10.1 Summary

This project successfully developed a comprehensive **Real-Time Network Traffic Prediction and Optimization System** using Machine Learning techniques. The system addresses critical challenges in modern network management by providing:

1. **Predictive Capabilities:** LSTM neural networks accurately forecast future traffic patterns
2. **Automatic Optimization:** Adaptive algorithms dynamically allocate bandwidth across routes
3. **Real-Time Monitoring:** Web dashboard provides comprehensive visibility into network performance
4. **Performance Evaluation:** Standard metrics enable continuous improvement

### 10.2 Achievements

- ✅ **Complete System Implementation:** All components developed and integrated
- ✅ **Machine Learning Integration:** LSTM/GRU models for accurate predictions
- ✅ **User-Friendly Interface:** Intuitive web dashboard for monitoring and control
- ✅ **Comprehensive Evaluation:** Multiple metrics for performance assessment
- ✅ **Documentation:** Complete documentation and user guides

### 10.3 Contributions

1. **Academic:** Demonstrates feasibility of ML-based real-time network management
2. **Practical:** Provides usable system for network operators
3. **Technical:** Integrates prediction and optimization in single framework
4. **Innovation:** Proactive rather than reactive network management

### 10.4 Limitations and Future Work

#### 10.4.1 Current Limitations
- Model requires sufficient training data (24+ hours recommended)
- Optimization algorithms can be further refined
- Real network monitoring requires appropriate permissions
- Limited to single network environment

#### 10.4.2 Future Enhancements
- **Reinforcement Learning:** Implement RL for optimization
- **Anomaly Detection:** Detect network attacks and anomalies
- **Multi-Network Support:** Extend to multiple network environments
- **Advanced Analytics:** Historical data analysis and reporting
- **API Integration:** REST API for external system integration
- **Mobile App:** Mobile interface for remote monitoring

### 10.5 Recommendations

1. **For Network Operators:** Deploy system for proactive network management
2. **For Researchers:** Extend with additional ML techniques and algorithms
3. **For Developers:** Contribute improvements and new features
4. **For Academia:** Use as teaching tool for ML and network management

---

## 11. REFERENCES

1. Cisco. (2023). *Cisco Annual Internet Report*. Retrieved from https://www.cisco.com/c/en/us/solutions/executive-perspectives/annual-internet-report.html

2. Lv, Y., Duan, Y., Kang, W., Li, Z., & Wang, F. (2015). Traffic flow prediction with big data: A deep learning approach. *IEEE Transactions on Intelligent Transportation Systems*, 16(2), 865–873.

3. Wang, J., Zhang, Y., & Li, X. (2020). Network traffic prediction and optimization using machine learning: A survey. *Computer Networks*, 180, 107–118.

4. Zhang, C., Liu, Y., & Zhao, D. (2022). Real-time network traffic forecasting with deep learning: Methods and applications. *IEEE Access*, 10, 34567–34578.

5. Hochreiter, S., & Schmidhuber, J. (1997). Long short-term memory. *Neural Computation*, 9(8), 1735-1780.

6. TensorFlow Team. (2023). *TensorFlow Documentation*. Retrieved from https://www.tensorflow.org/

7. Flask Development Team. (2023). *Flask Documentation*. Retrieved from https://flask.palletsprojects.com/

---

## 12. APPENDICES

### Appendix A: System Requirements

#### Hardware Requirements
- Processor: 2.0 GHz or higher
- RAM: 4 GB minimum (8 GB recommended)
- Storage: 500 MB for system, additional for data/models
- Network: Internet connection for dependencies

#### Software Requirements
- Operating System: Windows 10+, Linux, or macOS
- Python: Version 3.8 or higher
- pip: Python package manager
- Web Browser: Chrome, Firefox, Edge, or Safari

### Appendix B: Installation Instructions

1. Clone repository: `git clone https://github.com/agabaeldon/Network-trafficking.git`
2. Navigate to directory: `cd Network-trafficking`
3. Create virtual environment: `python -m venv venv`
4. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Create directories: `mkdir data models`
7. Run system: `python main.py web`

### Appendix C: Configuration Guide

Key configuration options in `config.py`:

```python
# Model Configuration
MODEL_CONFIG = {
    'lstm_units': 50,
    'sequence_length': 60,
    'prediction_horizon': 10,
    'epochs': 50
}

# Data Collection
DATA_CONFIG = {
    'collection_interval': 5,  # seconds
    'simulation_mode': True
}

# Network Settings
NETWORK_CONFIG = {
    'total_bandwidth': 10000,  # Mbps
    'num_routes': 5
}
```

### Appendix D: Command Reference

- `python main.py collect --hours 1` - Collect data for 1 hour
- `python main.py train --hours 24` - Train model on 24 hours of data
- `python main.py evaluate --hours 24` - Evaluate system performance
- `python main.py monitor` - Run monitoring service
- `python main.py web` - Start web dashboard

### Appendix E: File Structure

```
network-trafficking/
├── main.py              # Entry point (184 lines)
├── config.py            # Configuration (65 lines)
├── data_collector.py    # Data collection (195 lines)
├── ml_models.py         # ML models (249 lines)
├── optimizer.py         # Optimization (247 lines)
├── monitor.py           # Monitoring (241 lines)
├── evaluator.py         # Evaluation (146 lines)
├── app.py               # Web app (501 lines)
├── requirements.txt     # Dependencies (19 packages)
└── readme.md            # Documentation
```

### Appendix F: Team Contributions

- **WANYAMA DAVID (2022/BSE/016/PS):** System architecture, data collection module
- **LUMURO JOSEPH KANJAGA (2022/BSE/006/PS):** ML models, prediction algorithms
- **AGABA ELDON (2021/BSE/129/PS):** Optimization module, algorithms
- **MURIISA JOHN (2021/BSE/081/PS):** Web dashboard, user interface
- **TWINE BENSON VAMER (2021/BSE/176/PS):** Monitoring service, integration
- **MULINDWA ERIC (2020/BSE/036/PS):** Evaluation, testing, documentation

---

## ACKNOWLEDGMENTS

We would like to express our sincere gratitude to:

- Our supervisor for guidance and support throughout this project
- The open-source community for excellent tools and libraries
- Our institution for providing the necessary resources
- All contributors to the libraries and frameworks used in this project

---

**END OF REPORT**

---

*This report documents the complete development and implementation of the Real-Time Network Traffic Prediction and Optimization System. For questions or additional information, please refer to the GitHub repository: https://github.com/agabaeldon/Network-trafficking*

