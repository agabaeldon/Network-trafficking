"""
Evaluation Module for Model Performance and System Metrics
"""
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from ml_models import TrafficPredictor
from data_collector import NetworkDataCollector
from config import METRICS_CONFIG
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SystemEvaluator:
    """Evaluates system performance and model accuracy"""
    
    def __init__(self):
        self.predictor = TrafficPredictor()
        self.data_collector = NetworkDataCollector()
    
    def evaluate_model(self, hours=24):
        """Evaluate model performance on historical data"""
        logger.info(f"Evaluating model on {hours} hours of data...")
        
        # Load data
        df = self.data_collector.load_historical_data(hours=hours)
        
        if len(df) < self.predictor.sequence_length * 2:
            logger.error("Insufficient data for evaluation")
            return None
        
        # Evaluate
        results = self.predictor.evaluate(df)
        
        if results is None:
            return None
        
        # Calculate additional metrics
        mae = results['mae']
        rmse = results['rmse']
        
        # Calculate R² score
        r2 = r2_score(results['actual'], results['predictions'])
        
        # Calculate Mean Absolute Percentage Error (MAPE)
        mape = np.mean(np.abs((results['actual'] - results['predictions']) / 
                              (results['actual'] + 1e-10))) * 100
        
        # Check thresholds
        mae_pass = mae <= METRICS_CONFIG['mae_threshold']
        rmse_pass = rmse <= METRICS_CONFIG['rmse_threshold']
        
        evaluation = {
            'mae': mae,
            'rmse': rmse,
            'r2_score': r2,
            'mape': mape,
            'mae_threshold': METRICS_CONFIG['mae_threshold'],
            'rmse_threshold': METRICS_CONFIG['rmse_threshold'],
            'mae_pass': mae_pass,
            'rmse_pass': rmse_pass,
            'overall_pass': mae_pass and rmse_pass,
            'num_samples': len(results['actual'])
        }
        
        logger.info(f"Evaluation Results:")
        logger.info(f"  MAE: {mae:.2f} Mbps (Threshold: {METRICS_CONFIG['mae_threshold']} Mbps)")
        logger.info(f"  RMSE: {rmse:.2f} Mbps (Threshold: {METRICS_CONFIG['rmse_threshold']} Mbps)")
        logger.info(f"  R² Score: {r2:.4f}")
        logger.info(f"  MAPE: {mape:.2f}%")
        
        return evaluation
    
    def evaluate_network_performance(self, metrics_history):
        """Evaluate network performance improvements"""
        if not metrics_history or len(metrics_history) < 2:
            return None
        
        # Calculate average latency
        latencies = [m.get('latency', 0) for m in metrics_history if 'latency' in m]
        avg_latency = np.mean(latencies) if latencies else 0
        
        # Calculate average packet loss
        packet_losses = [m.get('packet_loss', 0) for m in metrics_history if 'packet_loss' in m]
        avg_packet_loss = np.mean(packet_losses) if packet_losses else 0
        
        # Calculate throughput
        throughputs = [m.get('bandwidth_utilization', 0) for m in metrics_history if 'bandwidth_utilization' in m]
        avg_throughput = np.mean(throughputs) if throughputs else 0
        
        # Check thresholds
        latency_pass = avg_latency <= METRICS_CONFIG['latency_threshold']
        throughput_pass = avg_throughput >= (METRICS_CONFIG['throughput_target'] * 10000)  # Assuming 10Gbps total
        
        evaluation = {
            'average_latency': avg_latency,
            'average_packet_loss': avg_packet_loss,
            'average_throughput': avg_throughput,
            'latency_threshold': METRICS_CONFIG['latency_threshold'],
            'throughput_target': METRICS_CONFIG['throughput_target'],
            'latency_pass': latency_pass,
            'throughput_pass': throughput_pass,
            'overall_pass': latency_pass and throughput_pass
        }
        
        return evaluation
    
    def generate_report(self, model_eval=None, network_eval=None):
        """Generate comprehensive evaluation report"""
        report = {
            'timestamp': pd.Timestamp.now().isoformat(),
            'model_evaluation': model_eval,
            'network_evaluation': network_eval,
            'summary': {}
        }
        
        if model_eval:
            report['summary']['model_accuracy'] = {
                'mae': f"{model_eval['mae']:.2f} Mbps",
                'rmse': f"{model_eval['rmse']:.2f} Mbps",
                'r2_score': f"{model_eval['r2_score']:.4f}",
                'status': 'PASS' if model_eval['overall_pass'] else 'FAIL'
            }
        
        if network_eval:
            report['summary']['network_performance'] = {
                'average_latency': f"{network_eval['average_latency']:.2f} ms",
                'average_throughput': f"{network_eval['average_throughput']:.2f} Mbps",
                'status': 'PASS' if network_eval['overall_pass'] else 'FAIL'
            }
        
        return report
    
    def compare_algorithms(self, hours=24):
        """Compare different optimization algorithms"""
        # This would require running the system with different algorithms
        # For now, return placeholder
        return {
            'adaptive': {'avg_utilization': 75.5, 'stability': 0.85},
            'proportional': {'avg_utilization': 72.3, 'stability': 0.78},
            'ml_based': {'avg_utilization': 77.1, 'stability': 0.88}
        }

