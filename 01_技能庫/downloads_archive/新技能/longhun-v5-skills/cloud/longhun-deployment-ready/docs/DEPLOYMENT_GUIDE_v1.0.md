# Deployment Guide v1.0

> **DNA**: `#龍芯⚡️2026-06-19-LONGHUN-DEPLOY-READY-v5.2`  
> **Version**: 1.0 | **Last Updated**: 2026-06-10

---

## Table of Contents

1. [Overview](#1-overview)
2. [Prerequisites](#2-prerequisites)
3. [Pre-Deployment Checklist](#3-pre-deployment-checklist)
4. [Deployment Procedures](#4-deployment-procedures)
5. [Post-Deployment Verification](#5-post-deployment-verification)
6. [Rollback Procedures](#6-rollback-procedures)
7. [Troubleshooting](#7-troubleshooting)
8. [Appendix](#8-appendix)

---

## 1. Overview

This document provides comprehensive deployment procedures for the Longhun system. It covers all aspects from environment preparation to backup verification, following the 27-step deployment checklist.

### Deployment Architecture

```
                    ┌──────────────────┐
                    │   Load Balancer   │
                    │     (Nginx)       │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────▼─────┐ ┌──────▼──────┐ ┌───▼──────────┐
     │  App Server  │ │ App Server  │ │ App Server   │
     │   :8000      │ │   :8000     │ │   :8000      │
     └──────┬───────┘ └──────┬──────┘ └──────┬───────┘
            │                │               │
            └────────────────┼───────────────┘
                             │
                    ┌────────▼────────┐
                    │   Database       │
                    │  (PostgreSQL)    │
                    └──────────────────┘
                             │
                    ┌────────▼────────┐
                    │    Redis Cache   │
                    └──────────────────┘
```

---

## 2. Prerequisites

### 2.1 Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 2 cores | 4 cores |
| RAM | 2 GB | 4 GB |
| Disk | 10 GB | 50 GB SSD |
| Network | 100 Mbps | 1 Gbps |

### 2.2 Software Requirements

| Software | Version | Installation |
|----------|---------|--------------|
| Python | >= 3.9 | [python.org](https://python.org) |
| PostgreSQL | >= 13 | `apt install postgresql` |
| Redis | >= 6.0 | `apt install redis-server` |
| Nginx | >= 1.18 | `apt install nginx` |
| Git | >= 2.30 | `apt install git` |

### 2.3 Network Requirements

```
Inbound Ports:
  80   - HTTP traffic
  443  - HTTPS traffic
  9090 - Prometheus (internal)
  3000 - Grafana (internal)

Outbound Access:
  - Package repositories (PyPI, APT)
  - Git repository host
  - Monitoring services (optional)
```

---

## 3. Pre-Deployment Checklist

### 3.1 Run Automated Checks

```bash
# Full 27-step readiness check
python3 scripts/部署就绪检查器.py --full

# Expected: At least 24/27 checks PASS
```

### 3.2 Manual Verification Items

- [ ] Change default passwords for all services
- [ ] Configure SSL/TLS certificates
- [ ] Set up log rotation
- [ ] Configure firewall rules (ufw/iptables)
- [ ] Verify backup storage location
- [ ] Test alerting channels (email/Slack/PagerDuty)

---

## 4. Deployment Procedures

### 4.1 Phase 1: Environment Preparation (Steps 1-4)

```bash
# Verify Python version
python3 --version  # Expected: Python 3.9+

# Verify system resources
python3 scripts/环境验证器.py

# Install system dependencies (Ubuntu/Debian)
sudo apt update && sudo apt install -y \
    python3-pip python3-venv \
    postgresql postgresql-contrib \
    redis-server nginx git

# Start services
sudo systemctl enable --now postgresql redis-server nginx
```

### 4.2 Phase 2: Code Deployment (Steps 5-7)

```bash
# Clone repository
git clone <repository-url> /opt/longhun-app
cd /opt/longhun-app

# Checkout specific version
git checkout v5.2.0

# Verify code integrity
python3 scripts/部署就绪检查器.py --step 6
```

### 4.3 Phase 3: Dependency Installation (Steps 8-10)

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip check
```

### 4.4 Phase 4: Configuration (Steps 11-13)

```bash
# Copy configuration
cp config.example.yaml config.yaml
cp .env.example .env

# Edit configuration files
vim .env
# Required variables:
#   APP_ENV=production
#   DATABASE_URL=postgresql://longhun:password@localhost/longhun_db
#   SECRET_KEY=$(openssl rand -hex 32)
#   REDIS_URL=redis://localhost:6379/0

# Validate configuration
python3 scripts/配置验证器.py

# Secure sensitive files
chmod 600 .env
chmod 644 config.yaml
```

### 4.5 Phase 5: Database Setup (Steps 14-16)

```bash
# Create database and user
sudo -u postgres psql << EOF
CREATE USER longhun WITH PASSWORD 'secure_password';
CREATE DATABASE longhun_db OWNER longhun;
GRANT ALL PRIVILEGES ON DATABASE longhun_db TO longhun;
EOF

# Run migrations
alembic upgrade head

# Verify migration status
alembic current
```

### 4.6 Phase 6: Service Startup (Steps 17-19)

```bash
# Check port availability
python3 scripts/部署就绪检查器.py --step 17

# Create systemd service
sudo tee /etc/systemd/system/longhun.service << 'EOF'
[Unit]
Description=Longhun Application
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=longhun
WorkingDirectory=/opt/longhun-app
Environment=PATH=/opt/longhun-app/venv/bin
ExecStart=/opt/longhun-app/venv/bin/uvicorn app:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Start service
sudo systemctl daemon-reload
sudo systemctl enable --now longhun
```

### 4.7 Phase 7: Health Verification (Steps 20-22)

```bash
# Check health endpoint
curl -f http://localhost:8000/health || exit 1

# Verify all dependencies
python3 scripts/部署就绪检查器.py --step 21

# Test critical API endpoints
curl http://localhost:8000/api/v1/status
curl http://localhost:8000/api/v1/health/detailed
```

### 4.8 Phase 8: Monitoring Setup (Steps 23-24)

```bash
# Install Prometheus (if not using Docker)
wget https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-amd64.tar.gz
tar xvfz prometheus-*.tar.gz

# Configure Prometheus
cp prometheus.yml /etc/prometheus/prometheus.yml
sudo systemctl enable --now prometheus

# Install Grafana
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee /etc/apt/sources.list.d/grafana.list
sudo apt update && sudo apt install -y grafana
sudo systemctl enable --now grafana-server
```

### 4.9 Phase 9: Log Verification (Step 25)

```bash
# Verify log directory
ls -la /var/log/longhun/

# Check log output
tail -n 20 /var/log/longhun/app.log

# Configure logrotate
sudo tee /etc/logrotate.d/longhun << 'EOF'
/var/log/longhun/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0644 longhun longhun
    postrotate
        systemctl reload longhun
    endscript
}
EOF
```

### 4.10 Phase 10: Backup Verification (Steps 26-27)

```bash
# Configure automated backups
sudo tee /etc/cron.d/longhun-backup << 'EOF'
# Backup database daily at 2 AM
0 2 * * * longhun /opt/longhun-app/scripts/backup.sh

# Cleanup old backups weekly
0 3 * * 0 longhun find /backups -name "*.sql.gz" -mtime +30 -delete
EOF

# Test backup
/opt/longhun-app/scripts/backup.sh

# List backup files
ls -la /backups/longhun/
```

---

## 5. Post-Deployment Verification

### 5.1 Full System Check

```bash
# Run complete readiness check
python3 scripts/部署就绪检查器.py --full

# Generate report
python3 scripts/部署就绪检查器.py --json > /tmp/deployment-report.json
```

### 5.2 Load Testing (Optional)

```bash
# Install k6 for load testing
sudo apt install k6

# Run load test
k6 run --vus 100 --duration 5m load-test.js
```

---

## 6. Rollback Procedures

### 6.1 Quick Rollback

```bash
# Use built-in rollback
python3 scripts/部署执行器.py --rollback

# Or manually:
sudo systemctl stop longhun
git checkout <previous-version>
pip install -r requirements.txt
alembic downgrade -1
sudo systemctl start longhun
```

### 6.2 Database Rollback

```bash
# Downgrade to specific migration
alembic downgrade <revision>

# Or downgrade one step
alembic downgrade -1
```

---

## 7. Troubleshooting

### 7.1 Common Issues

See `scripts/故障排查助手.py` for interactive troubleshooting.

```bash
# Search by error message
python3 scripts/故障排查助手.py "Address already in use"

# Interactive mode
python3 scripts/故障排查助手.py --interactive
```

### 7.2 Emergency Contacts

| Role | Contact | Escalation |
|------|---------|------------|
| On-call Engineer | oncall@example.com | +1-555-0100 |
| SRE Team | sre@example.com | Slack #sre |
| Database Admin | dba@example.com | +1-555-0101 |

---

## 8. Appendix

### 8.1 Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `APP_ENV` | Yes | Environment name | `production` |
| `DATABASE_URL` | Yes | Database connection string | `postgresql://...` |
| `SECRET_KEY` | Yes | Application secret key | `[hex 64 chars]` |
| `REDIS_URL` | No | Redis connection string | `redis://localhost:6379` |
| `LOG_LEVEL` | No | Logging level | `INFO` |
| `PORT` | No | Application port | `8000` |

### 8.2 File Locations

| File | Path | Purpose |
|------|------|---------|
| Application | `/opt/longhun-app` | Main application directory |
| Logs | `/var/log/longhun/` | Application logs |
| Backups | `/backups/longhun/` | Database backups |
| Config | `/opt/longhun-app/config.yaml` | Application configuration |
| Secrets | `/opt/longhun-app/.env` | Environment variables |

### 8.3 Change Log

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-06-10 | Initial release |

---

**Document DNA**: `#龍芯⚡️2026-06-19-LONGHUN-DEPLOY-READY-v5.2`
