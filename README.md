# 🚀 System Architecture & Full Pipeline Documentation

> This repository documents the complete architecture of the system:
>
> - Inference Pipeline (Push & Forget)
> - CI/CD Pipeline (Build & Deployment)
> - Observability Pipeline (Monitoring, Logging, Tracing)
>
> Use this as the reference for development, deployment, and maintenance.

---

# 🧭 Table of Contents

- [1. Inference Pipeline – Push & Forget](#1-inference-pipeline--push--forget)
  - [1.1 Flow Overview](#11-flow-overview)
  - [1.2 Detailed Steps](#12-detailed-steps)
- [2. CI/CD Pipeline](#2-cicd-pipeline)
  - [2.1 Build Flow](#21-build-flow)
  - [2.2 Deploy Flow](#22-deploy-flow)
- [3. Observability Pipeline](#3-observability-pipeline)
  - [3.1 Metrics](#31-metrics)
  - [3.2 Logging](#32-logging)
  - [3.3 Tracing](#33-tracing)
- [4. Full Architecture Diagram](#4-full-architecture-diagram)
- [5. Implementation Roadmap](#5-implementation-roadmap)
- [6. Why This Architecture?](#6-why-this-architecture)

---

# 🔥 1. Inference Pipeline – Push & Forget

This is the core asynchronous processing pipeline.

## 1.1 Flow Overview
```arduino
1. Client → 2. NGINX Ingress → 3. API Gateway → 4. Redis → 5. RabbitMQ 
→ 6. Worker GPU → 7. GCS → 8. API Gateway → 9. Client
```

---

## 1.2 Detailed Steps
### Step 0 — Client → NGINX
NGINX Ingress will:

- handle HTTPS termination
- perform basic rate limiting
- forward traffic to API Gateway
- allow multiple replicas behind load balancer
### Step 1 — NGINX → API Gateway (FastAPI Service)

POST /generate


API Gateway:
- Generates `task_id`
- Writes `{status: "PENDING"}` into Redis
- Generates signed URL for client to upload image directly into GCS
- Publishes a job into RabbitMQ:
```json
{
  "task_id": "...",
  "prompt": "...",
  "model_version": "...",
  "input_url": "gs://..."
}
```

Response:
```json
{
  "task_id": "...",
  "upload_url": "..."
}
```

### Step 2 — Worker (GPU VM)

1. Sequential processing:

2. Download input file from GCS

3. Run Stable Diffusion inference

Upload output to GCS:
```
gs://bucket/output/{task_id}.png
```

4. Update Redis:
```json
{
  "status": "SUCCEEDED",
  "image_url": "gs://...",
  "worker_version": "...",
  "model_version": "..."
}
```

Worker updates Redis only AFTER successful upload → prevents race-conditions.

### Step 3 — Client polls result
```bash
GET /tasks/{task_id}
```
API Gateway reads Redis:

* If PENDING → return {status: "PENDING"}

* If SUCCEEDED → return GCS signed URL or base64 image

* If FAILED → return error
# 🛠 2. CI/CD Pipeline
Automated build + deployment for API Gateway and Worker.
## 2.1 Build Flow
```bash
Developer → GitHub (push code)
                 │
                 └──► Jenkins CI/CD Pipeline
                        │
                        ├── Git clone
                        ├── Run tests
                        ├── Build Docker images (API + Worker)
                        ├── Tag version
                        └── Push images → Docker Hub

```

## 2.2 Deploy Flow
### API Deploy:
```bash
Jenkins → kubectl/helm → GKE
```

### Worker Deploy (GPU VM):
```pgsql
Jenkins → SSH → GPU VM
        → docker pull worker:<version>
        → restart container
```
Terraform provisions:

* GKE cluster
* GPU VM
* RabbitMQ
* Redis
* VPC, IAM, buckets

# 📡 3. Observability Pipeline
Complete monitoring, logging, & tracing.
## 3.1 Metrics Pipeline
Components:
* Prometheus
* Grafana
* AlertManager
* Node Exporter
* Discord Webhook
Flow:
```bash
API/Worker/NodeExporter → Prometheus
Prometheus → AlertManager → Discord
Grafana → Query Prometheus
```
## 3.2 Logging Pipeline
Components:
* Filebeat
* ElasticSearch
* Kibana
Flow:
```bash
App Logs → Filebeat → ElasticSearch → Kibana
```

## 3.3 Tracing Pipeline
Components:

* Jaeger Agent
* Jaeger Collector
* Jaeger UI
Flow:
```bash
API/Worker → Jaeger Agent → Jaeger Collector → Jaeger UI
```

# 🧩 4. Full Architecture Diagram (ASCII)
```yaml
                              ┌────────────────────────────────┐
                              │          CI/CD PIPELINE        │
Developer ─► GitHub ─► Jenkins ─► Docker Hub ─► Deploy API/Worker
Terraform ─► Provision Infrastructure
                              └────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│                     INFERENCE PIPELINE                                     │
│ Client → NGINX Ingress → API Gateway → Redis → RabbitMQ → Worker GPU → GCS → API → Client        │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│                 OBSERVABILITY PIPELINE                                     │
│ Metrics: Prometheus → AlertManager → Discord, Grafana                       │
│ Logs: Filebeat → ElasticSearch → Kibana                                     │
│ Traces: Jaeger Agent → Collector → Jaeger UI                                │
└────────────────────────────────────────────────────────────────────────────┘
```

# 🚀 5. Implementation Roadmap
## Phase 1 — Local (Minikube + Local Worker)

* Deploy Redis + RabbitMQ (Helm)

* Implement API Gateway

* Mock Worker output

* End-to-end test locally

## Phase 2 — GPU Worker

* Integrate Stable Diffusion

* Add versioning

* Upload inference results to GCS

## Phase 3 — CI/CD

* Jenkins pipeline for API + Worker

* Push Docker images

* Deploy API → GKE

* Deploy Worker → GPU VM

## Phase 4 — Observability

* Deploy Prometheus + Grafana

* Deploy Jaeger

* Deploy Filebeat + ElasticSearch + Kibana

* Configure Discord alerts

## Phase 5 — Production Hardening

* Autoscaling worker pool

* Redis TTL policies

* IAM least-privilege

* Firewall + Signed URLs