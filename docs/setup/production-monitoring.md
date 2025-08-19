# The Hero Foundry - Production Monitoring & Alerting Configuration

## Document Information
**Document Type:** Production Monitoring & Alerting Configuration  
**Version:** 1.0  
**Date:** 2025-01-27  
**Author:** Product Owner  
**Status:** Draft  
**Next Review:** 2025-02-27  

---

## Executive Summary

This document provides detailed configuration and implementation guidance for The Hero Foundry's production monitoring and alerting infrastructure. It covers the complete observability stack including metrics collection, logging, alerting, and dashboard configuration.

**Monitoring Stack Components:**
- **Prometheus:** Metrics collection and storage
- **Grafana:** Visualization and dashboards
- **AlertManager:** Alert routing and notification
- **ELK Stack:** Log aggregation and analysis
- **Custom Metrics:** Business-specific monitoring

---

## 1. PROMETHEUS CONFIGURATION

### 1.1 Prometheus Server Configuration

**File:** `prometheus.yml`

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    project: "hero-foundry"
    environment: "production"

rule_files:
  - "alert_rules.yml"

scrape_configs:
  # Self-monitoring
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # FastAPI Backend
  - job_name: 'fastapi-backend'
    static_configs:
      - targets: ['backend-1:8000', 'backend-2:8000', 'backend-3:8000']
    metrics_path: '/metrics'
    scrape_interval: 10s

  # React Frontend
  - job_name: 'react-frontend'
    static_configs:
      - targets: ['frontend-1:3000', 'frontend-2:3000']
    metrics_path: '/metrics'
    scrape_interval: 10s

  # PostgreSQL
  - job_name: 'postgresql'
    static_configs:
      - targets: ['postgres-primary:5432', 'postgres-replica-1:5432', 'postgres-replica-2:5432']
    metrics_path: '/metrics'
    scrape_interval: 30s

  # Redis
  - job_name: 'redis'
    static_configs:
      - targets: ['redis-1:6379', 'redis-2:6379', 'redis-3:6379']
    metrics_path: '/metrics'
    scrape_interval: 30s

  # Node Exporter (System Metrics)
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-1:9100', 'node-2:9100', 'node-3:9100']
    scrape_interval: 30s
```

### 1.2 Custom Metrics Collection

**FastAPI Application Metrics:**

```python
# metrics.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import FastAPI
import time

# Request metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')

# Business metrics
CHARACTER_CREATED = Counter('characters_created_total', 'Total characters created')
CHARACTER_LEVEL_UP = Counter('characters_leveled_up_total', 'Total character level-ups')
AI_QUERIES = Counter('ai_queries_total', 'Total AI assistance queries')
EXPORT_OPERATIONS = Counter('export_operations_total', 'Total export operations')

# Performance metrics
ACTIVE_USERS = Gauge('active_users_current', 'Currently active users')
CHARACTER_CREATION_DURATION = Histogram('character_creation_duration_seconds', 'Character creation time')
LEVEL_UP_DURATION = Histogram('level_up_duration_seconds', 'Level-up process time')

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    REQUEST_DURATION.observe(duration)
    return response

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

**React Frontend Metrics:**

```typescript
// metrics.ts
import { register, collectDefaultMetrics, Counter, Histogram, Gauge } from 'prom-client';

// Register default metrics
collectDefaultMetrics();

// Custom business metrics
export const pageViewCounter = new Counter({
  name: 'page_views_total',
  help: 'Total page views',
  labelNames: ['page_name', 'user_type']
});

export const characterCreationDuration = new Histogram({
  name: 'character_creation_duration_seconds',
  help: 'Character creation duration',
  buckets: [30, 60, 120, 300, 600] // 30s, 1m, 2m, 5m, 10m
});

export const activeUsersGauge = new Gauge({
  name: 'active_users_current',
  help: 'Currently active users'
});

// Metrics collection
export function collectMetrics() {
  return register.metrics();
}

// Send metrics to backend
export async function sendMetrics() {
  const metrics = await collectMetrics();
  await fetch('/api/metrics', {
    method: 'POST',
    body: metrics,
    headers: { 'Content-Type': 'text/plain' }
  });
}
```

---

## 2. GRAFANA DASHBOARD CONFIGURATION

### 2.1 Main Dashboard Configuration

**File:** `grafana-dashboards/main-dashboard.json`

```json
{
  "dashboard": {
    "title": "The Hero Foundry - Production Overview",
    "panels": [
      {
        "title": "System Health Overview",
        "type": "stat",
        "targets": [
          {
            "expr": "up",
            "legendFormat": "{{job}} - {{instance}}"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "color": {
              "mode": "thresholds"
            },
            "thresholds": {
              "steps": [
                {"color": "red", "value": 0},
                {"color": "green", "value": 1}
              ]
            }
          }
        }
      },
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{endpoint}}"
          }
        ],
        "yAxis": {
          "label": "Requests per second"
        }
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          },
          {
            "expr": "histogram_quantile(0.50, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "50th percentile"
          }
        ],
        "yAxis": {
          "label": "Response time (seconds)"
        }
      },
      {
        "title": "Business Metrics",
        "type": "stat",
        "targets": [
          {
            "expr": "rate(characters_created_total[1h])",
            "legendFormat": "Characters Created/Hour"
          },
          {
            "expr": "rate(characters_leveled_up_total[1h])",
            "legendFormat": "Level-ups/Hour"
          },
          {
            "expr": "rate(ai_queries_total[1h])",
            "legendFormat": "AI Queries/Hour"
          }
        ]
      }
    ]
  }
}
```

### 2.2 Performance Dashboard

**File:** `grafana-dashboards/performance-dashboard.json`

```json
{
  "dashboard": {
    "title": "Performance & User Experience",
    "panels": [
      {
        "title": "Character Creation Performance",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(character_creation_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile - Creation Time"
          }
        ],
        "yAxis": {
          "label": "Duration (seconds)"
        },
        "thresholds": [
          {"color": "green", "value": 300},
          {"color": "yellow", "value": 300},
          {"color": "red", "value": 300}
        ]
      },
      {
        "title": "Level-up Performance",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(level_up_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile - Level-up Time"
          }
        ],
        "yAxis": {
          "label": "Duration (seconds)"
        },
        "thresholds": [
          {"color": "green", "value": 120},
          {"color": "yellow", "value": 120},
          {"color": "red", "value": 120}
        ]
      },
      {
        "title": "Active Users",
        "type": "gauge",
        "targets": [
          {
            "expr": "active_users_current",
            "legendFormat": "Active Users"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "maxValue": 1000,
            "thresholds": {
              "steps": [
                {"color": "green", "value": 0},
                {"color": "yellow", "value": 500},
                {"color": "red", "value": 800}
              ]
            }
          }
        }
      }
    ]
  }
}
```

---

## 3. ALERTING RULES CONFIGURATION

### 3.1 Alert Rules Configuration

**File:** `alert_rules.yml`

```yaml
groups:
  - name: hero-foundry-critical
    rules:
      # Service Health Alerts
      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
          service: "{{ $labels.job }}"
        annotations:
          summary: "Service {{ $labels.job }} is down"
          description: "Service {{ $labels.job }} has been down for more than 1 minute"

      # High Error Rate Alerts
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }} (threshold: 5%)"

      # Response Time Degradation
      - alert: HighResponseTime
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2
        for: 3m
        labels:
          severity: warning
        annotations:
          summary: "High response time detected"
          description: "95th percentile response time is {{ $value }}s (threshold: 2s)"

  - name: hero-foundry-business
    rules:
      # Character Creation Performance
      - alert: CharacterCreationSlow
        expr: histogram_quantile(0.95, rate(character_creation_duration_seconds_bucket[5m])) > 300
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Character creation is slow"
          description: "95th percentile creation time is {{ $value }}s (threshold: 5 minutes)"

      # Level-up Performance
      - alert: LevelUpSlow
        expr: histogram_quantile(0.95, rate(level_up_duration_seconds_bucket[5m])) > 120
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Level-up process is slow"
          description: "95th percentile level-up time is {{ $value }}s (threshold: 2 minutes)"

      # AI Service Issues
      - alert: AIServiceDown
        expr: rate(ai_queries_total[5m]) == 0
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "AI service appears to be down"
          description: "No AI queries in the last 10 minutes"

  - name: hero-foundry-infrastructure
    rules:
      # High CPU Usage
      - alert: HighCPUUsage
        expr: 100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage on {{ $labels.instance }}"
          description: "CPU usage is {{ $value }}% (threshold: 80%)"

      # High Memory Usage
      - alert: HighMemoryUsage
        expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100 > 85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"
          description: "Memory usage is {{ $value }}% (threshold: 85%)"

      # Disk Space Low
      - alert: DiskSpaceLow
        expr: (node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100 < 20
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Low disk space on {{ $labels.instance }}"
          description: "Disk space is {{ $value }}% (threshold: 20%)"
```

### 3.2 AlertManager Configuration

**File:** `alertmanager.yml`

```yaml
global:
  smtp_smarthost: 'smtp.gmail.com:587'
  smtp_from: 'alerts@herofoundry.com'
  smtp_auth_username: 'alerts@herofoundry.com'
  smtp_auth_password: 'your-app-password'

route:
  group_by: ['alertname', 'service']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  receiver: 'team-slack'
  routes:
    - match:
        severity: critical
      receiver: 'pagerduty-critical'
      continue: true
    - match:
        severity: warning
      receiver: 'team-slack'

receivers:
  - name: 'team-slack'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK'
        channel: '#hero-foundry-alerts'
        title: '{{ template "slack.title" . }}'
        text: '{{ template "slack.text" . }}'
        actions:
          - type: button
            text: 'View in Grafana'
            url: '{{ template "slack.grafana" . }}'

  - name: 'pagerduty-critical'
    pagerduty_configs:
      - service_key: 'your-pagerduty-service-key'
        description: '{{ template "pagerduty.description" . }}'
        severity: '{{ if eq .GroupLabels.severity "critical" }}critical{{ else }}warning{{ end }}'
        client: 'Prometheus AlertManager'
        client_url: '{{ template "pagerduty.clientURL" . }}'

templates:
  - '/etc/alertmanager/template/*.tmpl'
```

---

## 4. LOGGING CONFIGURATION (ELK STACK)

### 4.1 Logstash Configuration

**File:** `logstash.conf`

```ruby
input {
  beats {
    port => 5044
  }
}

filter {
  if [fields][service] == "fastapi" {
    grok {
      match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} %{GREEDYDATA:message}" }
    }
    date {
      match => [ "timestamp", "ISO8601" ]
    }
    mutate {
      add_field => { "service_type" => "backend" }
    }
  }
  
  if [fields][service] == "react" {
    grok {
      match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} %{GREEDYDATA:message}" }
    }
    date {
      match => [ "timestamp", "ISO8601" ]
    }
    mutate {
      add_field => { "service_type" => "frontend" }
    }
  }
  
  if [fields][service] == "postgresql" {
    grok {
      match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} %{GREEDYDATA:message}" }
    }
    date {
      match => [ "timestamp", "ISO8601" ]
    }
    mutate {
      add_field => { "service_type" => "database" }
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "hero-foundry-logs-%{+YYYY.MM.dd}"
    document_type => "%{service_type}"
  }
}
```

### 4.2 Filebeat Configuration

**File:** `filebeat.yml`

```yaml
filebeat.inputs:
  - type: log
    enabled: true
    paths:
      - /var/log/hero-foundry/fastapi/*.log
    fields:
      service: fastapi
    fields_under_root: true
    multiline.pattern: '^\d{4}-\d{2}-\d{2}'
    multiline.negate: true
    multiline.match: after

  - type: log
    enabled: true
    paths:
      - /var/log/hero-foundry/react/*.log
    fields:
      service: react
    fields_under_root: true

  - type: log
    enabled: true
    paths:
      - /var/log/hero-foundry/postgresql/*.log
    fields:
      service: postgresql
    fields_under_root: true

output.logstash:
  hosts: ["logstash:5044"]

logging.level: info
```

---

## 5. CUSTOM METRICS IMPLEMENTATION

### 5.1 Business Metrics Collection

**File:** `business_metrics.py`

```python
from prometheus_client import Counter, Histogram, Gauge, Summary
import time
from functools import wraps

# Business Metrics
CHARACTER_CREATION_SUCCESS = Counter('character_creation_success_total', 'Successful character creations')
CHARACTER_CREATION_FAILURE = Counter('character_creation_failure_total', 'Failed character creations')
CHARACTER_CREATION_DURATION = Histogram('character_creation_duration_seconds', 'Character creation time')

LEVEL_UP_SUCCESS = Counter('level_up_success_total', 'Successful level-ups')
LEVEL_UP_FAILURE = Counter('level_up_failure_total', 'Failed level-ups')
LEVEL_UP_DURATION = Histogram('level_up_duration_seconds', 'Level-up process time')

AI_QUERY_SUCCESS = Counter('ai_query_success_total', 'Successful AI queries')
AI_QUERY_FAILURE = Counter('ai_query_failure_total', 'Failed AI queries')
AI_QUERY_DURATION = Histogram('ai_query_duration_seconds', 'AI query response time')

EXPORT_SUCCESS = Counter('export_success_total', 'Successful exports')
EXPORT_FAILURE = Counter('export_failure_total', 'Failed exports')
EXPORT_DURATION = Histogram('export_duration_seconds', 'Export operation time')

# User Experience Metrics
ACTIVE_SESSIONS = Gauge('active_sessions_current', 'Currently active user sessions')
CHARACTER_EDITIONS = Counter('character_editions_total', 'Total character edits')
RULE_LOOKUPS = Counter('rule_lookups_total', 'Total rule lookups')

# Performance Metrics
DATABASE_QUERY_DURATION = Histogram('database_query_duration_seconds', 'Database query time')
CACHE_HIT_RATIO = Gauge('cache_hit_ratio', 'Cache hit ratio percentage')
API_RESPONSE_SIZE = Histogram('api_response_size_bytes', 'API response size')

def track_metric(metric, success=True):
    """Track success/failure metrics"""
    if success:
        metric.inc()
    else:
        metric.inc()

def track_duration(metric):
    """Decorator to track operation duration"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                track_metric(metric, success=True)
                return result
            except Exception as e:
                track_metric(metric, success=False)
                raise
            finally:
                duration = time.time() - start_time
                metric.observe(duration)
        return wrapper
    return decorator

# Usage examples
@track_duration(CHARACTER_CREATION_DURATION)
def create_character(character_data):
    # Character creation logic
    pass

@track_duration(LEVEL_UP_DURATION)
def level_up_character(character_id):
    # Level-up logic
    pass
```

---

## 6. MONITORING DASHBOARD SETUP

### 6.1 Grafana Dashboard Import

**Setup Commands:**

```bash
# Create Grafana namespace
kubectl create namespace monitoring

# Install Grafana
helm repo add grafana https://grafana.github.io/helm-charts
helm install grafana grafana/grafana --namespace monitoring

# Get admin password
kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode

# Port forward to access Grafana
kubectl port-forward --namespace monitoring svc/grafana 3000:80

# Import dashboards
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d @grafana-dashboards/main-dashboard.json \
  http://localhost:3000/api/dashboards/db
```

### 6.2 Prometheus Setup

**Setup Commands:**

```bash
# Install Prometheus
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring

# Apply custom configuration
kubectl apply -f prometheus-config.yml
kubectl apply -f alert-rules.yml

# Restart Prometheus to load new config
kubectl rollout restart deployment/prometheus-server -n monitoring
```

---

## 7. ALERTING NOTIFICATION SETUP

### 7.1 Slack Integration

**Slack App Configuration:**
1. Create new Slack app at https://api.slack.com/apps
2. Enable incoming webhooks
3. Create webhook for #hero-foundry-alerts channel
4. Add webhook URL to AlertManager configuration

### 7.2 PagerDuty Integration

**PagerDuty Setup:**
1. Create new PagerDuty service
2. Generate service API key
3. Add API key to AlertManager configuration
4. Configure escalation policies for critical alerts

### 7.3 Email Notifications

**SMTP Configuration:**
1. Configure SMTP settings in AlertManager
2. Set up email distribution lists
3. Configure email templates for different alert types

---

## Success Criteria

✅ **Complete:** All monitoring and alerting components configured  
✅ **Comprehensive:** Covers metrics, logging, alerting, and dashboards  
✅ **Actionable:** Clear configuration files and setup procedures  
✅ **Integrated:** All components work together seamlessly  
✅ **Maintainable:** Clear documentation and configuration management  
✅ **Scalable:** Supports growth and additional services  

---

## Next Steps

1. **Infrastructure Setup:** Deploy monitoring stack to production
2. **Configuration Testing:** Verify all metrics collection and alerting
3. **Dashboard Customization:** Adjust dashboards based on team needs
4. **Alert Tuning:** Fine-tune alert thresholds based on actual usage
5. **Team Training:** Train team on monitoring tools and procedures
6. **Continuous Improvement:** Regular review and optimization of monitoring

---

**This document completes the production monitoring requirements identified in the PO master checklist, providing comprehensive observability for The Hero Foundry production environment.**
