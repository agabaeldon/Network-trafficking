"""
Network Traffic Data Collection Module
Collects real-time network traffic data or simulates traffic patterns
"""
import time
import psutil
import pandas as pd
import numpy as np
from datetime import datetime
import os
from config import DATA_CONFIG, NETWORK_CONFIG
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NetworkDataCollector:
    """Collects network traffic data from system or simulation"""
    
    def __init__(self):
        self.data_file = DATA_CONFIG['data_file']
        self.collection_interval = DATA_CONFIG['collection_interval']
        self.simulation_mode = DATA_CONFIG['simulation_mode']
        self.history = []
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        
        # Initialize data file if it doesn't exist
        if not os.path.exists(self.data_file):
            self._initialize_data_file()
    
    def _initialize_data_file(self):
        """Initialize CSV file with headers"""
        df = pd.DataFrame(columns=[
            'timestamp', 'bytes_sent', 'bytes_recv', 'packets_sent', 
            'packets_recv', 'bandwidth_utilization', 'latency', 
            'packet_loss', 'route_1', 'route_2', 'route_3', 'route_4', 'route_5'
        ])
        df.to_csv(self.data_file, index=False)
        logger.info(f"Initialized data file: {self.data_file}")
    
    def get_real_network_stats(self):
        """Collect real network statistics from system"""
        try:
            net_io = psutil.net_io_counters()
            
            # Calculate bandwidth utilization (simplified)
            total_bytes = net_io.bytes_sent + net_io.bytes_recv
            bandwidth_mbps = (total_bytes * 8) / (1024 * 1024) / self.collection_interval
            
            # Simulate latency and packet loss (in real implementation, use actual measurements)
            latency = np.random.normal(50, 10)  # ms
            packet_loss = np.random.uniform(0, 0.01)  # 0-1%
            
            # Distribute traffic across routes (simplified)
            route_traffic = self._distribute_traffic(bandwidth_mbps)
            
            return {
                'timestamp': datetime.now().isoformat(),
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv,
                'bandwidth_utilization': bandwidth_mbps,
                'latency': latency,
                'packet_loss': packet_loss,
                **route_traffic
            }
        except Exception as e:
            logger.error(f"Error collecting real network stats: {e}")
            return self.get_simulated_stats()
    
    def get_simulated_stats(self):
        """Generate simulated network traffic data"""
        base_traffic = DATA_CONFIG['simulation_traffic_base']
        variance = DATA_CONFIG['simulation_variance']
        
        # Add time-based patterns (morning rush, evening peak, etc.)
        hour = datetime.now().hour
        time_factor = 1.0
        if 8 <= hour <= 10 or 17 <= hour <= 20:
            time_factor = 1.5  # Peak hours
        elif 0 <= hour <= 6:
            time_factor = 0.5  # Off-peak hours
        
        # Add random variation
        traffic_variation = np.random.uniform(
            1 - variance, 
            1 + variance
        )
        
        bandwidth_mbps = base_traffic * time_factor * traffic_variation
        
        # Add some spikes occasionally
        if np.random.random() < 0.1:  # 10% chance of spike
            bandwidth_mbps *= np.random.uniform(1.5, 2.5)
        
        # Simulate latency (higher with more traffic)
        latency = 30 + (bandwidth_mbps / base_traffic) * 40 + np.random.normal(0, 5)
        latency = max(10, min(200, latency))  # Clamp between 10-200ms
        
        # Packet loss increases with traffic
        packet_loss = min(0.05, (bandwidth_mbps / (base_traffic * 2)) * 0.02)
        packet_loss += np.random.uniform(0, 0.005)
        
        # Distribute traffic across routes
        route_traffic = self._distribute_traffic(bandwidth_mbps)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'bytes_sent': int(bandwidth_mbps * 1024 * 1024 / 8 * self.collection_interval * 0.6),
            'bytes_recv': int(bandwidth_mbps * 1024 * 1024 / 8 * self.collection_interval * 0.4),
            'packets_sent': int(bandwidth_mbps * 1000),
            'packets_recv': int(bandwidth_mbps * 1200),
            'bandwidth_utilization': bandwidth_mbps,
            'latency': latency,
            'packet_loss': packet_loss,
            **route_traffic
        }
    
    def _distribute_traffic(self, total_bandwidth):
        """Distribute total bandwidth across multiple routes"""
        num_routes = NETWORK_CONFIG['num_routes']
        
        # Generate random distribution weights
        weights = np.random.dirichlet(np.ones(num_routes))
        weights = weights / weights.sum()  # Normalize
        
        route_traffic = {}
        for i, route_name in enumerate(NETWORK_CONFIG['route_names']):
            route_traffic[route_name.lower()] = total_bandwidth * weights[i]
        
        return route_traffic
    
    def collect_sample(self):
        """Collect a single sample of network data"""
        if self.simulation_mode:
            data = self.get_simulated_stats()
        else:
            data = self.get_real_network_stats()
        
        self.history.append(data)
        
        # Keep only recent history
        max_history = DATA_CONFIG['history_window'] // self.collection_interval
        if len(self.history) > max_history:
            self.history = self.history[-max_history:]
        
        return data
    
    def save_to_file(self, data):
        """Save collected data to CSV file"""
        try:
            df = pd.DataFrame([data])
            df.to_csv(self.data_file, mode='a', header=False, index=False)
        except Exception as e:
            logger.error(f"Error saving data to file: {e}")
    
    def load_historical_data(self, hours=24):
        """Load historical data from file"""
        try:
            if not os.path.exists(self.data_file):
                return pd.DataFrame()
            
            df = pd.read_csv(self.data_file)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Filter by time range
            cutoff_time = datetime.now().timestamp() - (hours * 3600)
            df = df[df['timestamp'].apply(lambda x: x.timestamp() > cutoff_time)]
            
            return df
        except Exception as e:
            logger.error(f"Error loading historical data: {e}")
            return pd.DataFrame()
    
    def start_collection(self):
        """Start continuous data collection"""
        logger.info("Starting network data collection...")
        while True:
            try:
                data = self.collect_sample()
                self.save_to_file(data)
                logger.debug(f"Collected data: {data['bandwidth_utilization']:.2f} Mbps")
                time.sleep(self.collection_interval)
            except KeyboardInterrupt:
                logger.info("Data collection stopped")
                break
            except Exception as e:
                logger.error(f"Error in data collection loop: {e}")
                time.sleep(self.collection_interval)

