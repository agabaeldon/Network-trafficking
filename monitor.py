"""
Real-time Network Traffic Monitoring and Prediction Service
"""
import time
import threading
import pandas as pd
from datetime import datetime, timedelta
from data_collector import NetworkDataCollector
from ml_models import TrafficPredictor
from optimizer import NetworkOptimizer
from config import DATA_CONFIG, OPTIMIZATION_CONFIG
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NetworkMonitor:
    """Real-time network monitoring and prediction service"""
    
    def __init__(self):
        self.data_collector = NetworkDataCollector()
        self.predictor = TrafficPredictor()
        self.optimizer = NetworkOptimizer()
        self.is_running = False
        self.monitoring_thread = None
        
        # Current state
        self.current_traffic = {}
        self.predicted_traffic = {}
        self.current_allocation = {}
        self.metrics = {}
        self.prediction_history = []
        
        # Load model if available
        self.predictor.load_model()
    
    def get_current_traffic_by_route(self):
        """Get current traffic distribution across routes"""
        try:
            # Load recent data
            df = self.data_collector.load_historical_data(hours=1)
            
            if len(df) == 0:
                return {}
            
            # Get latest data
            latest = df.iloc[-1]
            
            traffic = {}
            for route in self.optimizer.route_names:
                route_key = route.lower()
                traffic[route] = latest.get(route_key, 0)
            
            return traffic
        except Exception as e:
            logger.error(f"Error getting current traffic: {e}")
            return {}
    
    def predict_traffic(self):
        """Make traffic prediction"""
        try:
            # Load recent data
            df = self.data_collector.load_historical_data(hours=2)
            
            if len(df) < self.predictor.sequence_length:
                logger.warning("Insufficient data for prediction")
                return None
            
            # Make prediction
            prediction = self.predictor.predict(df)
            
            if prediction is None:
                return None
            
            # Distribute predicted bandwidth across routes
            # Use current distribution pattern
            current_traffic = self.get_current_traffic_by_route()
            total_current = sum(current_traffic.values())
            
            predicted_by_route = {}
            if total_current > 0:
                for route in self.optimizer.route_names:
                    proportion = current_traffic.get(route, 0) / total_current
                    predicted_by_route[route] = prediction[0] * proportion
            else:
                # Equal distribution
                per_route = prediction[0] / len(self.optimizer.route_names)
                predicted_by_route = {route: per_route for route in self.optimizer.route_names}
            
            return predicted_by_route
        except Exception as e:
            logger.error(f"Error in traffic prediction: {e}")
            return None
    
    def update_optimization(self):
        """Update bandwidth allocation based on predictions"""
        try:
            current_traffic = self.get_current_traffic_by_route()
            predicted_traffic = self.predicted_traffic
            
            # If no current traffic, use empty dict
            if not current_traffic:
                current_traffic = {}
            
            # If no predictions, use current traffic as prediction
            if not predicted_traffic:
                predicted_traffic = current_traffic.copy() if current_traffic else {}
            
            # If we have current traffic, optimize
            if current_traffic:
                # Optimize
                allocation = self.optimizer.optimize(
                    current_traffic,
                    predicted_traffic
                )
                
                self.current_allocation = allocation
                
                # Calculate metrics
                stats = self.optimizer.get_utilization_stats(current_traffic)
                self.metrics = stats
            else:
                # Use default allocation if no traffic data yet
                if not self.current_allocation:
                    self.current_allocation = self.optimizer._initialize_allocation()
            
        except Exception as e:
            logger.error(f"Error in optimization: {e}")
            # Set default allocation on error
            if not self.current_allocation:
                self.current_allocation = self.optimizer._initialize_allocation()
    
    def monitoring_loop(self):
        """Main monitoring loop"""
        logger.info("Starting monitoring loop...")
        
        while self.is_running:
            try:
                # Collect current data
                sample = self.data_collector.collect_sample()
                self.data_collector.save_to_file(sample)
                
                # Update current traffic
                self.current_traffic = self.get_current_traffic_by_route()
                
                # Make prediction
                predicted = self.predict_traffic()
                if predicted:
                    self.predicted_traffic = predicted
                    
                    # Store prediction history
                    self.prediction_history.append({
                        'timestamp': datetime.now().isoformat(),
                        'prediction': predicted.copy()
                    })
                    
                    # Keep only recent history
                    if len(self.prediction_history) > 100:
                        self.prediction_history = self.prediction_history[-100:]
                
                # Update optimization (always try, even without predictions)
                self.update_optimization()
                
                # Ensure we always have allocation data for display
                if not self.current_allocation:
                    self.current_allocation = self.optimizer._initialize_allocation()
                
                # Log status
                if self.current_traffic and self.predicted_traffic:
                    total_current = sum(self.current_traffic.values())
                    total_predicted = sum(self.predicted_traffic.values())
                    logger.info(
                        f"Current: {total_current:.2f} Mbps, "
                        f"Predicted: {total_predicted:.2f} Mbps"
                    )
                
                # Sleep
                time.sleep(DATA_CONFIG['collection_interval'])
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(DATA_CONFIG['collection_interval'])
    
    def start(self):
        """Start monitoring service"""
        if self.is_running:
            logger.warning("Monitoring already running")
            return
        
        self.is_running = True
        self.monitoring_thread = threading.Thread(target=self.monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        logger.info("Monitoring service started")
    
    def stop(self):
        """Stop monitoring service"""
        self.is_running = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        logger.info("Monitoring service stopped")
    
    def get_status(self):
        """Get current system status"""
        # Ensure allocation exists for display
        if not self.current_allocation:
            self.current_allocation = self.optimizer._initialize_allocation()
        
        return {
            'is_running': self.is_running,
            'current_traffic': self.current_traffic,
            'predicted_traffic': self.predicted_traffic,
            'allocation': self.current_allocation,
            'metrics': self.metrics,
            'optimization_metrics': self.optimizer.get_optimization_metrics()
        }
    
    def get_prediction_history(self, limit=50):
        """Get recent prediction history"""
        return self.prediction_history[-limit:]
    
    def train_model(self, hours=24):
        """Train the prediction model on historical data"""
        logger.info("Training model on historical data...")
        
        df = self.data_collector.load_historical_data(hours=hours)
        
        if len(df) < self.predictor.sequence_length * 2:
            logger.error("Insufficient historical data for training")
            return False
        
        success = self.predictor.train(df, model_type='lstm')
        
        if success:
            logger.info("Model training completed successfully")
            # Reload the model
            self.predictor.load_model()
        
        return success

