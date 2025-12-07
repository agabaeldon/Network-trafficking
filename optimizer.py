"""
Network Traffic Optimization Module
Implements bandwidth allocation and routing optimization algorithms
"""
import numpy as np
import pandas as pd
from config import OPTIMIZATION_CONFIG, NETWORK_CONFIG
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NetworkOptimizer:
    """Optimizes network bandwidth allocation based on predictions"""
    
    def __init__(self):
        self.total_bandwidth = NETWORK_CONFIG['total_bandwidth']
        self.num_routes = NETWORK_CONFIG['num_routes']
        self.route_names = NETWORK_CONFIG['route_names']
        self.algorithm = OPTIMIZATION_CONFIG['optimization_algorithm']
        self.current_allocation = self._initialize_allocation()
        self.allocation_history = []
    
    def _initialize_allocation(self):
        """Initialize equal bandwidth allocation"""
        bandwidth_per_route = self.total_bandwidth / self.num_routes
        return {route: bandwidth_per_route for route in self.route_names}
    
    def optimize_proportional(self, current_traffic, predicted_traffic):
        """Proportional allocation based on current and predicted traffic"""
        # Combine current and predicted traffic
        total_traffic = {}
        for route in self.route_names:
            current = current_traffic.get(route, 0)
            predicted = predicted_traffic.get(route, 0)
            total_traffic[route] = (current + predicted) / 2
        
        # Calculate total demand
        total_demand = sum(total_traffic.values())
        
        if total_demand == 0:
            return self._initialize_allocation()
        
        # Allocate proportionally
        allocation = {}
        for route in self.route_names:
            proportion = total_traffic[route] / total_demand
            allocation[route] = max(
                OPTIMIZATION_CONFIG['min_bandwidth'],
                min(
                    OPTIMIZATION_CONFIG['max_bandwidth'],
                    self.total_bandwidth * proportion
                )
            )
        
        # Normalize to ensure total doesn't exceed available bandwidth
        total_allocated = sum(allocation.values())
        if total_allocated > self.total_bandwidth:
            scale_factor = self.total_bandwidth / total_allocated
            allocation = {k: v * scale_factor for k, v in allocation.items()}
        
        return allocation
    
    def optimize_adaptive(self, current_traffic, predicted_traffic, utilization_history=None):
        """Adaptive allocation with load balancing"""
        allocation = {}
        threshold_low = OPTIMIZATION_CONFIG['bandwidth_threshold_low']
        threshold_high = OPTIMIZATION_CONFIG['bandwidth_threshold_high']
        
        # Calculate utilization for each route
        route_utilization = {}
        for route in self.route_names:
            current = current_traffic.get(route, 0)
            predicted = predicted_traffic.get(route, 0)
            avg_traffic = (current + predicted) / 2
            current_alloc = self.current_allocation.get(route, self.total_bandwidth / self.num_routes)
            
            if current_alloc > 0:
                utilization = avg_traffic / current_alloc
            else:
                utilization = 1.0
            
            route_utilization[route] = utilization
        
        # Identify overloaded and underloaded routes
        overloaded = [r for r, u in route_utilization.items() if u > threshold_high]
        underloaded = [r for r, u in route_utilization.items() if u < threshold_low]
        
        # Start with current allocation
        allocation = self.current_allocation.copy()
        
        # Redistribute bandwidth from underloaded to overloaded routes
        if overloaded and underloaded:
            total_underutilized = sum(
                allocation[r] * (threshold_low - route_utilization[r])
                for r in underloaded
                if route_utilization[r] < threshold_low
            )
            
            total_overload = sum(
                (current_traffic.get(r, 0) + predicted_traffic.get(r, 0)) / 2 - allocation[r] * threshold_high
                for r in overloaded
            )
            
            # Redistribute
            if total_underutilized > 0 and total_overload > 0:
                redistribution = min(total_underutilized, total_overload)
                
                # Reduce from underloaded
                for route in underloaded:
                    if route_utilization[route] < threshold_low:
                        reduction = allocation[route] * (threshold_low - route_utilization[route]) * 0.5
                        allocation[route] = max(OPTIMIZATION_CONFIG['min_bandwidth'], allocation[route] - reduction)
                
                # Add to overloaded
                for route in overloaded:
                    needed = ((current_traffic.get(route, 0) + predicted_traffic.get(route, 0)) / 2) / threshold_high - allocation[route]
                    if needed > 0:
                        allocation[route] = min(
                            OPTIMIZATION_CONFIG['max_bandwidth'],
                            allocation[route] + min(needed, redistribution / len(overloaded))
                        )
        
        # Ensure constraints
        for route in self.route_names:
            allocation[route] = max(
                OPTIMIZATION_CONFIG['min_bandwidth'],
                min(OPTIMIZATION_CONFIG['max_bandwidth'], allocation[route])
            )
        
        # Normalize
        total_allocated = sum(allocation.values())
        if total_allocated > self.total_bandwidth:
            scale_factor = self.total_bandwidth / total_allocated
            allocation = {k: v * scale_factor for k, v in allocation.items()}
        elif total_allocated < self.total_bandwidth:
            # Distribute remaining bandwidth
            remaining = self.total_bandwidth - total_allocated
            per_route = remaining / self.num_routes
            allocation = {k: v + per_route for k, v in allocation.items()}
        
        return allocation
    
    def optimize_ml_based(self, current_traffic, predicted_traffic, ml_model=None):
        """ML-based optimization (placeholder for reinforcement learning)"""
        # For now, use adaptive with ML predictions
        # In full implementation, this would use RL to learn optimal allocations
        return self.optimize_adaptive(current_traffic, predicted_traffic)
    
    def optimize(self, current_traffic, predicted_traffic, **kwargs):
        """Main optimization function"""
        if self.algorithm == 'proportional':
            allocation = self.optimize_proportional(current_traffic, predicted_traffic)
        elif self.algorithm == 'ml_based':
            allocation = self.optimize_ml_based(
                current_traffic, 
                predicted_traffic, 
                kwargs.get('ml_model')
            )
        else:  # adaptive
            allocation = self.optimize_adaptive(
                current_traffic, 
                predicted_traffic,
                kwargs.get('utilization_history')
            )
        
        # Update current allocation
        self.current_allocation = allocation
        
        # Record history
        self.allocation_history.append({
            'allocation': allocation.copy(),
            'current_traffic': current_traffic.copy(),
            'predicted_traffic': predicted_traffic.copy()
        })
        
        # Keep only recent history
        if len(self.allocation_history) > 1000:
            self.allocation_history = self.allocation_history[-1000:]
        
        return allocation
    
    def get_utilization_stats(self, current_traffic):
        """Calculate utilization statistics"""
        stats = {}
        total_utilized = 0
        
        for route in self.route_names:
            traffic = current_traffic.get(route, 0)
            allocated = self.current_allocation.get(route, 0)
            
            if allocated > 0:
                utilization = (traffic / allocated) * 100
            else:
                utilization = 0
            
            stats[route] = {
                'traffic': traffic,
                'allocated': allocated,
                'utilization': utilization,
                'available': max(0, allocated - traffic)
            }
            
            total_utilized += traffic
        
        stats['total'] = {
            'traffic': total_utilized,
            'allocated': self.total_bandwidth,
            'utilization': (total_utilized / self.total_bandwidth) * 100 if self.total_bandwidth > 0 else 0,
            'available': max(0, self.total_bandwidth - total_utilized)
        }
        
        return stats
    
    def get_optimization_metrics(self):
        """Calculate optimization performance metrics"""
        if len(self.allocation_history) < 2:
            return None
        
        recent = self.allocation_history[-10:]  # Last 10 optimizations
        
        # Calculate average utilization
        avg_utilizations = []
        for entry in recent:
            stats = self.get_utilization_stats(entry['current_traffic'])
            avg_utilizations.append(stats['total']['utilization'])
        
        avg_utilization = np.mean(avg_utilizations) if avg_utilizations else 0
        
        # Calculate allocation changes (stability)
        allocation_changes = []
        for i in range(1, len(recent)):
            prev = recent[i-1]['allocation']
            curr = recent[i]['allocation']
            change = sum(abs(curr.get(r, 0) - prev.get(r, 0)) for r in self.route_names)
            allocation_changes.append(change)
        
        avg_change = np.mean(allocation_changes) if allocation_changes else 0
        
        return {
            'average_utilization': avg_utilization,
            'allocation_stability': 1 / (1 + avg_change),  # Higher is more stable
            'total_bandwidth_used': avg_utilization * self.total_bandwidth / 100
        }

