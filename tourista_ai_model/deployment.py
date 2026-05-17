"""
Tourista AR AI Model - Cloud Deployment Configuration
Optimized for Beginner-Level Cloud Servers
Compatible with AWS, Azure, GCP, and Alibaba Cloud
"""

import os
from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class CloudConfig:
    server_type: str = "lightweight"
    memory_requirement_gb: int = 2
    cpu_cores: int = 2
    storage_gb: int = 20
    bandwidth_mbps: int = 100
    auto_scaling: bool = False
    max_concurrent_requests: int = 50

@dataclass
class PerformanceConfig:
    enable_caching: bool = True
    cache_ttl_seconds: int = 3600
    request_timeout_seconds: int = 30
    max_retries: int = 3
    connection_pool_size: int = 10
    enable_compression: bool = True
    batch_processing: bool = True
    max_batch_size: int = 100

@dataclass
class SecurityConfig:
    enable_ssl: bool = True
    require_api_key: bool = True
    rate_limiting: bool = True
    requests_per_minute: int = 60
    enable_cors: bool = True
    allowed_origins: list = None

    def __post_init__(self):
        if self.allowed_origins is None:
            self.allowed_origins = ["*"]

@dataclass
class MonitoringConfig:
    enable_logging: bool = True
    log_level: str = "INFO"
    enable_metrics: bool = True
    enable_health_check: bool = True
    health_check_interval_seconds: int = 60
    enable_alerting: bool = False

class DeploymentConfig:
    def __init__(self, environment: str = "production"):
        self.environment = environment
        self.cloud = CloudConfig()
        self.performance = PerformanceConfig()
        self.security = SecurityConfig()
        self.monitoring = MonitoringConfig()

        if environment == "development":
            self._configure_development()
        elif environment == "staging":
            self._configure_staging()
        elif environment == "production":
            self._configure_production()

    def _configure_development(self):
        self.cloud.memory_requirement_gb = 1
        self.cloud.cpu_cores = 1
        self.performance.max_concurrent_requests = 10
        self.security.rate_limiting = False
        self.monitoring.log_level = "DEBUG"

    def _configure_staging(self):
        self.cloud.memory_requirement_gb = 2
        self.cloud.cpu_cores = 2
        self.performance.max_concurrent_requests = 25
        self.monitoring.enable_alerting = True

    def _configure_production(self):
        self.cloud.memory_requirement_gb = 4
        self.cloud.cpu_cores = 4
        self.cloud.auto_scaling = True
        self.performance.max_concurrent_requests = 100
        self.security.rate_limiting = True
        self.security.requests_per_minute = 100
        self.monitoring.enable_alerting = True

    def get_docker_config(self) -> Dict:
        return {
            "base_image": "python:3.11-slim",
            "python_version": "3.11",
            "installed_packages": [
                "fastapi>=0.104.0",
                "uvicorn>=0.24.0",
                "pydantic>=2.4.0",
                "redis>=5.0.0",
                "aiofiles>=23.2.0",
                "python-multipart>=0.0.6"
            ],
            "exposed_ports": [8000],
            "environment_variables": {
                "ENVIRONMENT": self.environment,
                "PYTHONUNBUFFERED": "1",
                "UVICORN_WORKERS": str(self.cloud.cpu_cores)
            },
            "health_check": {
                "test": ["CMD", "curl", "-f", "http://localhost:8000/health"],
                "interval": "60s",
                "timeout": "10s",
                "retries": 3
            },
            "resources": {
                "limits": {
                    "cpus": str(self.cloud.cpu_cores),
                    "memory": f"{self.cloud.memory_requirement_gb}G"
                },
                "reservations": {
                    "cpus": "1",
                    "memory": "1G"
                }
            }
        }

    def get_kubernetes_config(self) -> Dict:
        return {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": "tourista-ai-model",
                "labels": {
                    "app": "tourista-ai",
                    "version": "v1"
                }
            },
            "spec": {
                "replicas": 2,
                "selector": {
                    "matchLabels": {
                        "app": "tourista-ai"
                    }
                },
                "template": {
                    "metadata": {
                        "labels": {
                            "app": "tourista-ai"
                        }
                    },
                    "spec": {
                        "containers": [{
                            "name": "tourista-ai",
                            "image": "tourista-ar/ai-model:latest",
                            "ports": [{
                                "containerPort": 8000
                            }],
                            "resources": {
                                "requests": {
                                    "memory": "1Gi",
                                    "cpu": "500m"
                                },
                                "limits": {
                                    "memory": f"{self.cloud.memory_requirement_gb}Gi",
                                    "cpu": f"{self.cloud.cpu_cores}"
                                }
                            },
                            "livenessProbe": {
                                "httpGet": {
                                    "path": "/health",
                                    "port": 8000
                                },
                                "initialDelaySeconds": 30,
                                "periodSeconds": 10
                            },
                            "readinessProbe": {
                                "httpGet": {
                                    "path": "/health",
                                    "port": 8000
                                },
                                "initialDelaySeconds": 5,
                                "periodSeconds": 5
                            }
                        }]
                    }
                }
            }
        }

    def get_nginx_config(self) -> str:
        return f"""
server {{
    listen 80;
    server_name api.tourista-ar.ai;
    client_max_body_size 10M;

    location / {{
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        # Caching
        proxy_cache_bypass $http_upgrade;
    }}

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate={self.security.requests_per_minute}r/m;

    location /api/ {{
        limit_req zone=api_limit burst=20 nodelay;
        proxy_pass http://localhost:8000;
    }}

    # Compression
    gzip on;
    gzip_types text/plain application/json application/javascript text/css;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}}
"""

    def get_system_requirements(self) -> Dict:
        return {
            "operating_system": "Ubuntu 22.04 LTS / Debian 12",
            "minimum": {
                "cpu": "2 cores",
                "ram": "2 GB",
                "storage": "20 GB SSD",
                "bandwidth": "100 Mbps"
            },
            "recommended": {
                "cpu": "4 cores",
                "ram": "4 GB",
                "storage": "50 GB SSD",
                "bandwidth": "1 Gbps"
            },
            "dependencies": [
                "Python 3.11+",
                "Redis 7.0+ (for caching)",
                "Nginx 1.18+ (for reverse proxy)",
                "Docker 24.0+ (for containerization)"
            ]
        }

    def get_startup_script(self) -> str:
        return """#!/bin/bash
set -e

echo "Starting Tourista AR AI Model..."

# Install dependencies
apt-get update
apt-get install -y python3.11 python3-pip redis-server nginx

# Install Python packages
pip3 install -r requirements.txt

# Start Redis
redis-server --daemonize yes

# Start the application
uvicorn api.endpoints:app --host 0.0.0.0 --port 8000 --workers 2

echo "Tourista AR AI Model started successfully"
"""

class ModelOptimizer:
    @staticmethod
    def optimize_for_latency() -> Dict:
        return {
            "enable_model_quantization": True,
            "use_fp16_inference": False,
            "batch_size": 1,
            "prefetch_requests": True,
            "async_processing": True,
            "connection_pooling": True,
            "aggressive_caching": True,
            "stream_responses": False
        }

    @staticmethod
    def optimize_for_throughput() -> Dict:
        return {
            "enable_model_quantization": True,
            "use_fp16_inference": True,
            "batch_size": 16,
            "prefetch_requests": True,
            "async_processing": True,
            "connection_pooling": True,
            "aggressive_caching": True,
            "stream_responses": False
        }

    @staticmethod
    def optimize_for_memory() -> Dict:
        return {
            "enable_model_quantization": True,
            "use_fp16_inference": True,
            "batch_size": 1,
            "prefetch_requests": False,
            "async_processing": True,
            "connection_pooling": False,
            "aggressive_caching": False,
            "lazy_loading": True,
            "unload_unused_models": True
        }

CONFIG = DeploymentConfig(environment=os.getenv("ENVIRONMENT", "production"))
