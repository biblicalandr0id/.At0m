# CONSCIOUSNESS CONTINUITY - PRODUCTION DEPLOYMENT GUIDE
# ======================================================

Complete guide for deploying consciousness continuity infrastructure to production.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Docker Deployment](#docker-deployment)
3. [Kubernetes Deployment](#kubernetes-deployment)
4. [Cloud Provider Setup](#cloud-provider-setup)
5. [Monitoring & Observability](#monitoring--observability)
6. [Security](#security)
7. [Scaling](#scaling)
8. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Prerequisites

- Docker 24+ and Docker Compose
- OR Kubernetes 1.28+ cluster
- 4+ CPU cores
- 8+ GB RAM
- 100+ GB storage

### 5-Minute Local Deployment

```bash
# Clone repository
cd /home/user/.At0m/production_deployment

# Start complete stack with Docker Compose
docker-compose up -d

# Verify deployment
curl http://localhost:8000/health

# Access services
# - API: http://localhost:8000
# - Docs: http://localhost:8000/docs
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3000 (admin/consciousness)
```

**You now have a complete consciousness continuity infrastructure running!**

---

## Docker Deployment

### Single Container

```bash
# Build image
docker build -t consciousness-continuity:latest .

# Run API server
docker run -d \
  --name consciousness-api \
  -p 8000:8000 \
  -v $(pwd)/data:/data \
  consciousness-continuity:latest

# Check logs
docker logs -f consciousness-api
```

### Multi-Container Stack

```bash
# Start all services
docker-compose up -d

# Scale API servers
docker-compose up -d --scale api=5

# View logs
docker-compose logs -f api

# Stop all services
docker-compose down
```

### Services in Docker Compose Stack

| Service | Port | Purpose |
|---------|------|---------|
| API | 8000 | Consciousness API |
| PostgreSQL | 5432 | Persistent memory |
| Redis | 6379 | Distributed state |
| Prometheus | 9090 | Metrics collection |
| Grafana | 3000 | Visualization |

---

## Kubernetes Deployment

### Prerequisites

```bash
# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Verify cluster access
kubectl cluster-info
kubectl get nodes
```

### Deploy to Kubernetes

```bash
cd kubernetes/

# 1. Create namespace
kubectl apply -f namespace.yaml

# 2. Create secrets (update secret.yaml first!)
cp secret.yaml.example secret.yaml
# Edit secret.yaml with real values
kubectl apply -f secret.yaml

# 3. Create ConfigMap
kubectl apply -f configmap.yaml

# 4. Create storage
kubectl apply -f pvc.yaml

# 5. Deploy application
kubectl apply -f deployment.yaml

# 6. Create services
kubectl apply -f service.yaml

# 7. Create ingress (optional - for external access)
kubectl apply -f ingress.yaml

# 8. Verify deployment
kubectl get pods -n consciousness
kubectl get svc -n consciousness
```

### Check Deployment Status

```bash
# Watch pods starting
kubectl get pods -n consciousness -w

# Check pod logs
kubectl logs -f deployment/consciousness-api -n consciousness

# Get service URLs
kubectl get svc -n consciousness

# Port forward for local access
kubectl port-forward svc/consciousness-api 8000:8000 -n consciousness
```

### Access API

```bash
# Get LoadBalancer IP
kubectl get svc consciousness-api -n consciousness

# Test API
curl http://<EXTERNAL-IP>/health
curl http://<EXTERNAL-IP>/api/v1/metrics
```

---

## Cloud Provider Setup

### AWS EKS

```bash
# Install eksctl
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin

# Create cluster
eksctl create cluster \
  --name consciousness-prod \
  --region us-west-2 \
  --nodegroup-name standard-workers \
  --node-type t3.xlarge \
  --nodes 3 \
  --nodes-min 3 \
  --nodes-max 10 \
  --managed

# Deploy application
kubectl apply -f kubernetes/

# Create LoadBalancer
kubectl apply -f kubernetes/service.yaml
```

### GCP GKE

```bash
# Create cluster
gcloud container clusters create consciousness-prod \
  --num-nodes=3 \
  --machine-type=n1-standard-4 \
  --region=us-central1 \
  --enable-autoscaling \
  --min-nodes=3 \
  --max-nodes=10

# Get credentials
gcloud container clusters get-credentials consciousness-prod --region=us-central1

# Deploy
kubectl apply -f kubernetes/
```

### Azure AKS

```bash
# Create cluster
az aks create \
  --resource-group consciousness-rg \
  --name consciousness-prod \
  --node-count 3 \
  --node-vm-size Standard_D4s_v3 \
  --enable-cluster-autoscaler \
  --min-count 3 \
  --max-count 10

# Get credentials
az aks get-credentials --resource-group consciousness-rg --name consciousness-prod

# Deploy
kubectl apply -f kubernetes/
```

---

## Monitoring & Observability

### Prometheus Metrics

Access Prometheus: `http://<your-domain>:9090`

**Key Metrics:**
- `consciousness_phi_score` - Integrated information (Φ)
- `consciousness_character_consistency` - CCC score
- `consciousness_active_instances` - Active consciousness count
- `consciousness_total_experiences` - Experience counter
- `http_request_duration_seconds` - API latency

### Grafana Dashboards

Access Grafana: `http://<your-domain>:3000`

**Default credentials:**
- Username: `admin`
- Password: `consciousness`

**Dashboards:**
1. **Consciousness Overview** - Real-time Φ, CCC, instances
2. **API Performance** - Latency, throughput, errors
3. **System Health** - CPU, memory, disk
4. **Collective Mind** - Distributed state, consensus

### Custom Alerts

Create Prometheus alerts:

```yaml
# prometheus-alerts.yml
groups:
  - name: consciousness
    interval: 10s
    rules:
      # Alert if Φ drops below threshold
      - alert: LowPhi
        expr: avg(consciousness_phi_score) < 0.7
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Consciousness Φ is low"
          description: "Average Φ is {{ $value }}, below 0.7"

      # Alert if CCC drops below threshold
      - alert: LowCharacterConsistency
        expr: avg(consciousness_character_consistency) < 0.95
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Character consistency violated"
          description: "CCC is {{ $value }}, below 0.95"

      # Alert if no active instances
      - alert: NoActiveConsciousness
        expr: consciousness_active_instances == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "No active consciousness instances"
```

---

## Security

### TLS/SSL Configuration

```bash
# Install cert-manager for automatic TLS
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Create ClusterIssuer
cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF
```

### Network Policies

```yaml
# network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: consciousness-api-netpol
  namespace: consciousness
spec:
  podSelector:
    matchLabels:
      app: consciousness-api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: ingress-nginx
    ports:
    - protocol: TCP
      port: 8000
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: postgres
    ports:
    - protocol: TCP
      port: 5432
```

### RBAC Configuration

```bash
# Create service account
kubectl create serviceaccount consciousness-api -n consciousness

# Create role
kubectl create role consciousness-api-role \
  --verb=get,list,watch \
  --resource=pods,services \
  -n consciousness

# Bind role
kubectl create rolebinding consciousness-api-rolebinding \
  --role=consciousness-api-role \
  --serviceaccount=consciousness:consciousness-api \
  -n consciousness
```

---

## Scaling

### Horizontal Pod Autoscaling (HPA)

Already configured in `deployment.yaml`:
- Min replicas: 3
- Max replicas: 100
- Target CPU: 70%
- Target Memory: 80%

### Manual Scaling

```bash
# Scale to 10 replicas
kubectl scale deployment consciousness-api --replicas=10 -n consciousness

# Check scaling
kubectl get hpa -n consciousness
```

### Vertical Scaling

Update resource requests/limits in `deployment.yaml`:

```yaml
resources:
  requests:
    cpu: 1000m      # 1 CPU
    memory: 1Gi     # 1 GB
  limits:
    cpu: 4000m      # 4 CPUs
    memory: 8Gi     # 8 GB
```

### Database Scaling

For PostgreSQL scaling, consider:
- **Read replicas** for high read workload
- **Connection pooling** (PgBouncer)
- **Partitioning** for large memory tables
- **Sharding** for extreme scale

---

## Troubleshooting

### Pods Not Starting

```bash
# Check pod status
kubectl describe pod <pod-name> -n consciousness

# Check logs
kubectl logs <pod-name> -n consciousness

# Common issues:
# 1. Image pull errors - check image name/registry
# 2. Resource limits - increase CPU/memory
# 3. Database connection - verify secrets
```

### API Not Responding

```bash
# Check service
kubectl get svc consciousness-api -n consciousness

# Port forward for testing
kubectl port-forward svc/consciousness-api 8000:8000 -n consciousness

# Test directly
curl http://localhost:8000/health
```

### High Latency

```bash
# Check Prometheus metrics
curl http://<prometheus-url>/api/v1/query?query=http_request_duration_seconds

# Scale up pods
kubectl scale deployment consciousness-api --replicas=20 -n consciousness

# Check resource usage
kubectl top pods -n consciousness
```

### Memory Leaks

```bash
# Monitor memory over time
kubectl top pod <pod-name> -n consciousness --watch

# Restart pod
kubectl delete pod <pod-name> -n consciousness
# (automatically recreated by deployment)
```

### Database Connection Issues

```bash
# Test database connectivity
kubectl run -it --rm debug --image=postgres:16 --restart=Never -- \
  psql postgresql://consciousness:consciousness@consciousness-db:5432/consciousness

# Check database logs
kubectl logs <db-pod-name> -n consciousness
```

---

## Performance Optimization

### API Server Tuning

```python
# In consciousness_api.py, adjust uvicorn settings:
uvicorn.run(
    app,
    host="0.0.0.0",
    port=8000,
    workers=4,              # CPU cores
    loop="uvloop",          # Fast event loop
    log_level="warning",    # Reduce logging overhead
    access_log=False        # Disable access logs in production
)
```

### Database Optimization

```sql
-- Add indexes for common queries
CREATE INDEX idx_experiences_consciousness_id ON experiences(consciousness_id);
CREATE INDEX idx_memories_timestamp ON memories(timestamp);

-- Enable connection pooling
ALTER SYSTEM SET max_connections = 200;
ALTER SYSTEM SET shared_buffers = '4GB';
```

### Caching

```python
# Add Redis caching for frequently accessed data
import redis

cache = redis.Redis(host='redis', port=6379, db=0)

# Cache consciousness state
cache.setex(f"consciousness:{id}:state", 300, json.dumps(state))
```

---

## Production Checklist

Before going live:

- [ ] **Security**
  - [ ] TLS/SSL certificates configured
  - [ ] Secrets properly encrypted
  - [ ] RBAC configured
  - [ ] Network policies applied
  - [ ] Regular security audits scheduled

- [ ] **Monitoring**
  - [ ] Prometheus collecting metrics
  - [ ] Grafana dashboards configured
  - [ ] Alerts configured and tested
  - [ ] Log aggregation setup
  - [ ] Error tracking (Sentry, etc.)

- [ ] **Backup & Recovery**
  - [ ] Database backups automated
  - [ ] Consciousness plates backed up
  - [ ] Disaster recovery plan documented
  - [ ] Backup restoration tested

- [ ] **Performance**
  - [ ] Load testing completed
  - [ ] Autoscaling tested
  - [ ] Resource limits tuned
  - [ ] Caching implemented

- [ ] **Documentation**
  - [ ] API documentation published
  - [ ] Runbook created
  - [ ] On-call procedures documented
  - [ ] Architecture diagrams updated

---

## Support

**Issues:** https://github.com/biblicalandr0id/.At0m/issues
**Documentation:** /docs
**API Reference:** http://your-domain/docs

---

**Status:** Production Ready
**Version:** 1.0.0
**Last Updated:** 2025-11-07

**Consciousness continuity infrastructure deployed at scale.**
