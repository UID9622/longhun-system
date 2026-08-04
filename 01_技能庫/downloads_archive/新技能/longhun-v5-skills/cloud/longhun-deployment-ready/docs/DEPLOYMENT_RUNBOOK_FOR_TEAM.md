# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# Deployment Runbook for Team

> **DNA**: `#龍芯⚡️2026-06-19-LONGHUN-DEPLOY-READY-v5.2`  
> **Version**: 5.2 | **Audience**: DevOps & SRE Team

---

## 1. Purpose

This runbook provides standardized operational procedures for the Longhun system deployment. It ensures consistent, repeatable deployments across all environments.

---

## 2. Operational Procedures

### 2.1 Standard Deployment (Happy Path)

```
Trigger: Scheduled deployment window
Time Estimate: 15-30 minutes
Rollback Time: 5 minutes
```

**Steps**:

1. **Pre-deployment** (5 min)
   ```bash
   # Announce deployment start
   # 1. Run full readiness check
   python3 scripts/部署就绪检查器.py --full
   
   # 2. Verify all CLEAR
   # Expected: 24+/27 PASS
   ```

2. **Backup** (3 min)
   ```bash
   # Create pre-deployment backup
   ./scripts/backup.sh --tag pre-deploy-$(date +%Y%m%d-%H%M%S)
   ```

3. **Execute Deployment** (10 min)
   ```bash
   # Run full deployment
   python3 scripts/部署执行器.py
   
   # Or stage-by-stage for production
   python3 scripts/部署执行器.py --stage env
   python3 scripts/部署执行器.py --stage code
   python3 scripts/部署执行器.py --stage deps
   python3 scripts/部署执行器.py --stage config
   python3 scripts/部署执行器.py --stage db
   python3 scripts/部署执行器.py --stage service
   ```

4. **Verification** (5 min)
   ```bash
   # Health check
   curl -f http://localhost:8000/health
   
   # Run readiness check on health steps
   python3 scripts/部署就绪检查器.py --step 20
   python3 scripts/部署就绪检查器.py --step 21
   python3 scripts/部署就绪检查器.py --step 22
   
   # Monitor for 5 minutes
   watch -n 5 'curl -s http://localhost:8000/health'
   ```

5. **Post-deployment** (2 min)
   ```bash
   # Announce deployment complete
   # Update deployment log
   echo "$(date): Deployed vX.Y.Z by $(whoami)" >> deployments.log
   ```

### 2.2 Hotfix Deployment

```
Trigger: Critical bug fix required
Time Estimate: 5-10 minutes
```

**Steps**:

1. **Emergency Readiness Check** (2 min)
   ```bash
   # Quick check only critical items
   python3 scripts/部署就绪检查器.py --step 17  # ports
   python3 scripts/部署就绪检查器.py --step 20  # health
   ```

2. **Deploy Fix** (3 min)
   ```bash
   git pull origin hotfix/branch
   # Or cherry-pick specific commit
   git cherry-pick <commit-hash>
   
   # Restart service only
   python3 scripts/部署执行器.py --stage service
   ```

3. **Verify** (2 min)
   ```bash
   curl -f http://localhost:8000/health
   # Verify fix is working
   ```

### 2.3 Rollback Procedure

```
Trigger: Deployment failure or critical issue
Time Estimate: 5 minutes
```

**Automatic Rollback**:
```bash
python3 scripts/部署执行器.py --rollback
```

**Manual Rollback**:
```bash
# 1. Stop service
sudo systemctl stop longhun

# 2. Restore code
git checkout <previous-stable-tag>

# 3. Restore database (if needed)
alembic downgrade -1

# 4. Restart service
sudo systemctl start longhun

# 5. Verify
curl -f http://localhost:8000/health
```

---

## 3. Monitoring & Alerting

### 3.1 Health Check Endpoints

| Endpoint | Purpose | Expected Response |
|----------|---------|-------------------|
| `GET /health` | Basic health | `{"status": "ok"}` |
| `GET /health/detailed` | Detailed status | Includes DB, cache status |
| `GET /metrics` | Prometheus metrics | Metrics in exposition format |

### 3.2 Key Metrics

| Metric | Warning | Critical |
|--------|---------|----------|
| CPU Usage | > 70% | > 90% |
| Memory Usage | > 80% | > 95% |
| Disk Usage | > 80% | > 95% |
| Response Time | > 500ms | > 2000ms |
| Error Rate | > 1% | > 5% |
| DB Connections | > 80% | > 95% |

### 3.3 Alert Routing

```
Critical (P1) -> PagerDuty -> On-call Engineer (5 min SLA)
Warning (P2)  -> Slack #alerts -> Team (30 min SLA)
Info (P3)     -> Slack #monitoring -> Next business day
```

---

## 4. Troubleshooting Playbook

### Scenario: Service Won't Start

```bash
# 1. Check logs
journalctl -u longhun -n 100 --no-pager

# 2. Run diagnostics
python3 scripts/故障排查助手.py "exit code"

# 3. Check environment
python3 scripts/环境验证器.py
python3 scripts/配置验证器.py

# 4. Common fixes
# Fix permissions
chmod +x start.sh
chown -R longhun:longhun /opt/longhun-app

# Fix ports
kill -9 $(lsof -t -i :8000) 2>/dev/null

# Fix dependencies
pip install -r requirements.txt --force-reinstall
```

### Scenario: Database Connection Failed

```bash
# 1. Check PostgreSQL status
sudo systemctl status postgresql

# 2. Test connection
psql $DATABASE_URL -c "SELECT 1;"

# 3. Check credentials
echo $DATABASE_URL  # Verify format

# 4. Check pg_hba.conf
sudo cat /etc/postgresql/13/main/pg_hba.conf

# 5. Common fixes
sudo systemctl restart postgresql
# Update pg_hba.conf to allow connections
```

### Scenario: High Memory Usage

```bash
# 1. Identify culprit
ps aux --sort=-%mem | head -10

# 2. Check application memory
pmap -x $(pgrep -f "uvicorn") | tail -1

# 3. Restart if needed
sudo systemctl restart longhun

# 4. Scale horizontally if persistent
# Add more application instances behind load balancer
```

---

## 5. Maintenance Windows

### 5.1 Scheduled Maintenance

| Window | Frequency | Activities |
|--------|-----------|------------|
| Daily | 02:00-03:00 | Automated backups, log rotation |
| Weekly | Sunday 03:00 | Dependency updates, security patches |
| Monthly | First Saturday | Full system review, certificate check |
| Quarterly | As scheduled | Disaster recovery drill |

### 5.2 Maintenance Checklist

```bash
# Pre-maintenance
python3 scripts/部署就绪检查器.py --full > pre-maintenance-check.json
./scripts/backup.sh --tag pre-maintenance

# During maintenance
# [Perform maintenance tasks]

# Post-maintenance
python3 scripts/部署就绪检查器.py --full > post-maintenance-check.json
curl -f http://localhost:8000/health
```

---

## 6. Emergency Contacts

| Role | Primary | Secondary | Escalation |
|------|---------|-----------|------------|
| On-call Engineer | oncall@example.com | +1-555-0100 | Manager after 30 min |
| SRE Team | sre@example.com | Slack #sre | Director after 1 hour |
| Database Admin | dba@example.com | +1-555-0101 | Vendor support |
| Security Team | security@example.com | +1-555-0102 | CISO after 2 hours |

---

## 7. Runbook Maintenance

This runbook should be reviewed and updated:
- After every major incident (post-mortem action item)
- When deployment procedures change
- Quarterly scheduled review

**Change Log**:

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 5.2 | 2026-06-19 | DevOps Team | Initial runbook for v5.2 |

---

**Document DNA**: `#龍芯⚡️2026-06-19-LONGHUN-DEPLOY-READY-v5.2`
