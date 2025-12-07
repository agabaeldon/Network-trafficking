"""
Flask Web Application for Network Traffic Prediction and Optimization Dashboard
"""
from flask import Flask, jsonify, render_template_string
from flask_cors import CORS
import threading
from monitor import NetworkMonitor
from config import API_CONFIG
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize monitor
monitor = NetworkMonitor()

# HTML Dashboard Template
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Network Traffic Prediction & Optimization</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        .header {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .header h1 {
            color: #667eea;
            margin-bottom: 10px;
        }
        .status {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            margin-left: 10px;
        }
        .status.running { background: #4caf50; color: white; }
        .status.stopped { background: #f44336; color: white; }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .card h2 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.2em;
        }
        .metric {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }
        .metric:last-child { border-bottom: none; }
        .metric-label { color: #666; }
        .metric-value {
            font-weight: bold;
            color: #333;
        }
        .chart-container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .controls {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        button {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin-right: 10px;
            font-size: 14px;
        }
        button:hover { background: #5568d3; }
        button.stop { background: #f44336; }
        button.stop:hover { background: #d32f2f; }
        .route-item {
            padding: 10px;
            margin: 5px 0;
            background: #f5f5f5;
            border-radius: 5px;
        }
        .progress-bar {
            height: 20px;
            background: #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 5px;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #4caf50, #8bc34a);
            transition: width 0.3s;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌐 Network Traffic Prediction & Optimization System
                <span class="status" id="status">●</span>
            </h1>
            <p>Real-time ML-based traffic prediction and bandwidth optimization</p>
        </div>

        <div class="controls">
            <button onclick="startMonitor()">Start Monitoring</button>
            <button class="stop" onclick="stopMonitor()">Stop Monitoring</button>
            <button onclick="trainModel()">Train Model</button>
            <button onclick="location.reload()">Refresh</button>
        </div>

        <div class="grid">
            <div class="card">
                <h2>📊 Current Traffic</h2>
                <div id="currentTraffic"></div>
            </div>
            <div class="card">
                <h2>🔮 Predicted Traffic</h2>
                <div id="predictedTraffic"></div>
            </div>
            <div class="card">
                <h2>⚡ System Metrics</h2>
                <div id="systemMetrics"></div>
            </div>
        </div>

        <div class="chart-container">
            <h2>📈 Traffic Trends</h2>
            <div id="trafficChart" style="height: 400px;"></div>
        </div>

        <div class="chart-container">
            <h2>🎯 Bandwidth Allocation</h2>
            <div id="allocationChart" style="height: 400px;"></div>
        </div>

        <div class="card">
            <h2>🛣️ Route Details</h2>
            <div id="routeDetails"></div>
        </div>
    </div>

    <script>
        let updateInterval;

        function updateStatus() {
            fetch('/api/status')
                .then(r => r.json())
                .then(data => {
                    // Update status indicator
                    const statusEl = document.getElementById('status');
                    statusEl.textContent = data.is_running ? '● Running' : '● Stopped';
                    statusEl.className = 'status ' + (data.is_running ? 'running' : 'stopped');

                    // Update current traffic
                    const currentDiv = document.getElementById('currentTraffic');
                    let html = '';
                    let totalCurrent = 0;
                    if (data.current_traffic) {
                        for (const [route, value] of Object.entries(data.current_traffic)) {
                            totalCurrent += value;
                            html += `<div class="metric">
                                <span class="metric-label">${route}:</span>
                                <span class="metric-value">${value.toFixed(2)} Mbps</span>
                            </div>`;
                        }
                    }
                    html += `<div class="metric" style="border-top: 2px solid #667eea; margin-top: 10px; padding-top: 10px;">
                        <span class="metric-label"><strong>Total:</strong></span>
                        <span class="metric-value"><strong>${totalCurrent.toFixed(2)} Mbps</strong></span>
                    </div>`;
                    currentDiv.innerHTML = html;

                    // Update predicted traffic
                    const predictedDiv = document.getElementById('predictedTraffic');
                    html = '';
                    let totalPredicted = 0;
                    if (data.predicted_traffic) {
                        for (const [route, value] of Object.entries(data.predicted_traffic)) {
                            totalPredicted += value;
                            html += `<div class="metric">
                                <span class="metric-label">${route}:</span>
                                <span class="metric-value">${value.toFixed(2)} Mbps</span>
                            </div>`;
                        }
                    }
                    html += `<div class="metric" style="border-top: 2px solid #667eea; margin-top: 10px; padding-top: 10px;">
                        <span class="metric-label"><strong>Total:</strong></span>
                        <span class="metric-value"><strong>${totalPredicted.toFixed(2)} Mbps</strong></span>
                    </div>`;
                    predictedDiv.innerHTML = html;

                    // Update system metrics
                    const metricsDiv = document.getElementById('systemMetrics');
                    html = '';
                    if (data.metrics && data.metrics.total) {
                        const total = data.metrics.total;
                        html += `<div class="metric">
                            <span class="metric-label">Total Utilization:</span>
                            <span class="metric-value">${total.utilization.toFixed(2)}%</span>
                        </div>`;
                        html += `<div class="metric">
                            <span class="metric-label">Available Bandwidth:</span>
                            <span class="metric-value">${total.available.toFixed(2)} Mbps</span>
                        </div>`;
                    }
                    if (data.optimization_metrics) {
                        html += `<div class="metric">
                            <span class="metric-label">Avg Utilization:</span>
                            <span class="metric-value">${data.optimization_metrics.average_utilization.toFixed(2)}%</span>
                        </div>`;
                    }
                    metricsDiv.innerHTML = html || '<p>No metrics available</p>';

                    // Update route details
                    const routeDiv = document.getElementById('routeDetails');
                    html = '';
                    if (data.metrics) {
                        for (const [route, stats] of Object.entries(data.metrics)) {
                            if (route !== 'total') {
                                html += `<div class="route-item">
                                    <strong>${route}</strong>
                                    <div class="metric">
                                        <span>Traffic: ${stats.traffic.toFixed(2)} Mbps</span>
                                        <span>Allocated: ${stats.allocated.toFixed(2)} Mbps</span>
                                        <span>Utilization: ${stats.utilization.toFixed(2)}%</span>
                                    </div>
                                    <div class="progress-bar">
                                        <div class="progress-fill" style="width: ${Math.min(100, stats.utilization)}%"></div>
                                    </div>
                                </div>`;
                            }
                        }
                    }
                    routeDiv.innerHTML = html || '<p>No route data available</p>';

                    // Update charts
                    updateCharts(data);
                })
                .catch(err => console.error('Error:', err));
        }

        function updateCharts(data) {
            // Get routes from current_traffic, allocation, or use defaults
            let routes = [];
            if (data.current_traffic && Object.keys(data.current_traffic).length > 0) {
                routes = Object.keys(data.current_traffic);
            } else if (data.allocation && Object.keys(data.allocation).length > 0) {
                routes = Object.keys(data.allocation);
            } else if (data.predicted_traffic && Object.keys(data.predicted_traffic).length > 0) {
                routes = Object.keys(data.predicted_traffic);
            } else {
                // Use default route names if no data
                routes = ['Route_1', 'Route_2', 'Route_3', 'Route_4', 'Route_5'];
            }

            const current = routes.map(r => data.current_traffic?.[r] || 0);
            const predicted = routes.map(r => data.predicted_traffic?.[r] || 0);
            const allocated = routes.map(r => data.allocation?.[r] || 0);

            // Only show charts if we have at least some data
            if (routes.length > 0 && (current.some(v => v > 0) || predicted.some(v => v > 0) || allocated.some(v => v > 0))) {
                // Traffic comparison chart
                const traces = [];
                
                if (current.some(v => v > 0)) {
                    traces.push({
                        x: routes,
                        y: current,
                        name: 'Current',
                        type: 'bar',
                        marker: { color: '#4caf50' }
                    });
                }
                
                if (predicted.some(v => v > 0)) {
                    traces.push({
                        x: routes,
                        y: predicted,
                        name: 'Predicted',
                        type: 'bar',
                        marker: { color: '#2196f3' }
                    });
                }

                if (traces.length > 0) {
                    Plotly.newPlot('trafficChart', traces, {
                        title: 'Current vs Predicted Traffic by Route',
                        xaxis: { title: 'Route' },
                        yaxis: { title: 'Traffic (Mbps)' },
                        barmode: traces.length > 1 ? 'group' : 'group'
                    });
                } else {
                    // Show empty chart with message
                    Plotly.newPlot('trafficChart', [{
                        x: routes,
                        y: new Array(routes.length).fill(0),
                        type: 'bar',
                        name: 'No Data',
                        marker: { color: '#cccccc' }
                    }], {
                        title: 'Current vs Predicted Traffic by Route (No Data Yet)',
                        xaxis: { title: 'Route' },
                        yaxis: { title: 'Traffic (Mbps)' }
                    });
                }

                // Allocation chart
                if (allocated.some(v => v > 0)) {
                    Plotly.newPlot('allocationChart', [{
                        x: routes,
                        y: allocated,
                        type: 'bar',
                        marker: { color: '#9c27b0' },
                        name: 'Allocated Bandwidth'
                    }], {
                        title: 'Bandwidth Allocation by Route',
                        xaxis: { title: 'Route' },
                        yaxis: { title: 'Bandwidth (Mbps)' }
                    });
                } else {
                    // Show empty chart with message
                    Plotly.newPlot('allocationChart', [{
                        x: routes,
                        y: new Array(routes.length).fill(0),
                        type: 'bar',
                        name: 'No Allocation Data',
                        marker: { color: '#cccccc' }
                    }], {
                        title: 'Bandwidth Allocation by Route (Start Monitoring to See Data)',
                        xaxis: { title: 'Route' },
                        yaxis: { title: 'Bandwidth (Mbps)' }
                    });
                }
            } else {
                // Show placeholder charts
                Plotly.newPlot('trafficChart', [{
                    x: routes,
                    y: new Array(routes.length).fill(0),
                    type: 'bar',
                    name: 'Waiting for Data',
                    marker: { color: '#cccccc' }
                }], {
                    title: 'Traffic Trends (Click "Start Monitoring" to see data)',
                    xaxis: { title: 'Route' },
                    yaxis: { title: 'Traffic (Mbps)' }
                });

                Plotly.newPlot('allocationChart', [{
                    x: routes,
                    y: new Array(routes.length).fill(0),
                    type: 'bar',
                    name: 'Waiting for Data',
                    marker: { color: '#cccccc' }
                }], {
                    title: 'Bandwidth Allocation (Click "Start Monitoring" to see data)',
                    xaxis: { title: 'Route' },
                    yaxis: { title: 'Bandwidth (Mbps)' }
                });
            }
        }

        function startMonitor() {
            fetch('/api/start', { method: 'POST' })
                .then(r => r.json())
                .then(data => {
                    alert(data.message || 'Monitoring started');
                    updateStatus();
                });
        }

        function stopMonitor() {
            fetch('/api/stop', { method: 'POST' })
                .then(r => r.json())
                .then(data => {
                    alert(data.message || 'Monitoring stopped');
                    updateStatus();
                });
        }

        function trainModel() {
            if (confirm('Train model on historical data? This may take several minutes.')) {
                fetch('/api/train', { method: 'POST' })
                    .then(r => r.json())
                    .then(data => {
                        alert(data.message || 'Training completed');
                    });
            }
        }

        // Initial load and periodic updates
        updateStatus();
        updateInterval = setInterval(updateStatus, 5000); // Update every 5 seconds
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    """Serve the main dashboard"""
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/status')
def get_status():
    """Get current system status"""
    return jsonify(monitor.get_status())

@app.route('/api/start', methods=['POST'])
def start_monitoring():
    """Start the monitoring service"""
    try:
        monitor.start()
        return jsonify({'message': 'Monitoring started successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stop', methods=['POST'])
def stop_monitoring():
    """Stop the monitoring service"""
    try:
        monitor.stop()
        return jsonify({'message': 'Monitoring stopped successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/train', methods=['POST'])
def train_model():
    """Train the prediction model"""
    try:
        success = monitor.train_model(hours=24)
        if success:
            return jsonify({'message': 'Model training completed successfully'})
        else:
            return jsonify({'error': 'Model training failed. Check logs for details.'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predictions')
def get_predictions():
    """Get prediction history"""
    return jsonify(monitor.get_prediction_history())

@app.route('/api/metrics')
def get_metrics():
    """Get detailed metrics"""
    return jsonify({
        'metrics': monitor.metrics,
        'optimization_metrics': monitor.optimizer.get_optimization_metrics()
    })

if __name__ == '__main__':
    logger.info("Starting Flask application...")
    logger.info(f"Dashboard available at http://{API_CONFIG['host']}:{API_CONFIG['port']}")
    app.run(
        host=API_CONFIG['host'],
        port=API_CONFIG['port'],
        debug=API_CONFIG['debug']
    )

