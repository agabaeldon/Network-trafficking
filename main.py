"""
Main Entry Point for Network Traffic Prediction and Optimization System
"""
import argparse
import sys
import os
from data_collector import NetworkDataCollector
from ml_models import TrafficPredictor
from evaluator import SystemEvaluator
from monitor import NetworkMonitor
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def collect_data(hours=1):
    """Run data collection for specified hours"""
    logger.info(f"Starting data collection for {hours} hours...")
    collector = NetworkDataCollector()
    
    import time
    end_time = time.time() + (hours * 3600)
    
    try:
        while time.time() < end_time:
            data = collector.collect_sample()
            collector.save_to_file(data)
            logger.info(f"Collected: {data['bandwidth_utilization']:.2f} Mbps")
            time.sleep(collector.collection_interval)
    except KeyboardInterrupt:
        logger.info("Data collection interrupted by user")
    finally:
        logger.info("Data collection completed")


def train_model(hours=24):
    """Train the prediction model"""
    logger.info(f"Training model on {hours} hours of data...")
    
    collector = NetworkDataCollector()
    predictor = TrafficPredictor()
    
    df = collector.load_historical_data(hours=hours)
    
    if len(df) == 0:
        logger.error("No historical data found. Please collect data first.")
        return False
    
    logger.info(f"Loaded {len(df)} data points")
    
    success = predictor.train(df, model_type='lstm')
    
    if success:
        logger.info("Model training completed successfully!")
    else:
        logger.error("Model training failed")
    
    return success


def evaluate_system(hours=24):
    """Evaluate system performance"""
    logger.info("Evaluating system performance...")
    
    evaluator = SystemEvaluator()
    
    # Evaluate model
    model_eval = evaluator.evaluate_model(hours=hours)
    
    # Generate report
    report = evaluator.generate_report(model_eval=model_eval)
    
    logger.info("\n" + "="*50)
    logger.info("EVALUATION REPORT")
    logger.info("="*50)
    
    if model_eval:
        logger.info(f"\nModel Performance:")
        logger.info(f"  MAE: {model_eval['mae']:.2f} Mbps")
        logger.info(f"  RMSE: {model_eval['rmse']:.2f} Mbps")
        logger.info(f"  R² Score: {model_eval['r2_score']:.4f}")
        logger.info(f"  MAPE: {model_eval['mape']:.2f}%")
        logger.info(f"  Status: {'PASS' if model_eval['overall_pass'] else 'FAIL'}")
    
    logger.info("="*50)
    
    return report


def run_monitor():
    """Run the monitoring service"""
    logger.info("Starting network monitoring service...")
    
    monitor = NetworkMonitor()
    
    # Try to load existing model
    if not monitor.predictor.load_model():
        logger.warning("No trained model found. Training on available data...")
        monitor.train_model(hours=24)
    
    # Start monitoring
    monitor.start()
    
    try:
        # Keep running
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping monitoring service...")
        monitor.stop()
        logger.info("Monitoring service stopped")


def run_web_app():
    """Run the web dashboard"""
    logger.info("Starting web application...")
    from app import app, monitor, API_CONFIG
    
    # Try to load existing model
    if not monitor.predictor.load_model():
        logger.warning("No trained model found. The system will collect data first.")
    
    logger.info(f"Web dashboard available at http://{API_CONFIG['host']}:{API_CONFIG['port']}")
    app.run(
        host=API_CONFIG['host'],
        port=API_CONFIG['port'],
        debug=API_CONFIG['debug']
    )


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Network Traffic Prediction and Optimization System'
    )
    
    parser.add_argument(
        'command',
        choices=['collect', 'train', 'evaluate', 'monitor', 'web'],
        help='Command to execute'
    )
    
    parser.add_argument(
        '--hours',
        type=int,
        default=24,
        help='Number of hours of data to use (default: 24)'
    )
    
    args = parser.parse_args()
    
    # Ensure necessary directories exist
    os.makedirs('data', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    
    if args.command == 'collect':
        collect_data(hours=args.hours)
    
    elif args.command == 'train':
        train_model(hours=args.hours)
    
    elif args.command == 'evaluate':
        evaluate_system(hours=args.hours)
    
    elif args.command == 'monitor':
        run_monitor()
    
    elif args.command == 'web':
        run_web_app()
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()

