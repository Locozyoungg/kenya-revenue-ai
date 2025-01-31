"""
FILE: scripts/monitor.py
DESCRIPTION: System health monitoring and alerting
INTEGRATIONS: Prometheus, Grafana, Sentry
"""

from prometheus_client import start_http_server, Gauge
import psutil

class SystemMonitor:
    def __init__(self):
        self.metrics = {
            'cpu_usage': Gauge('system_cpu_percent', 'CPU utilization'),
            'memory_usage': Gauge('system_memory_usage', 'RAM used (MB)'),
            'api_errors': Gauge('kra_api_errors', 'Failed API calls')
        }
    
    def collect_system_metrics(self):
        """Update hardware metrics"""
        self.metrics['cpu_usage'].set(psutil.cpu_percent())
        self.metrics['memory_usage'].set(psutil.virtual_memory().used / 1024**2)

    def track_api_error(self):
        """Increment error counter"""
        self.metrics['api_errors'].inc()

# Initialize monitoring
monitor = SystemMonitor()
start_http_server(8001)

# Example usage in API code:
# try:
#     response = api_call()
# except APIError:
#     monitor.track_api_error()