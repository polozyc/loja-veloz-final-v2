# Loja Veloz – Plataforma de Pedidos

Plataforma de e-commerce baseada em microserviços com observabilidade, CI/CD automatizado e infraestrutura como código.

##  Arquitetura

```
┌─────────────────────────────────────────────────┐
│                   CLIENTES                        │
└───────────────────────┬─────────────────────────┘
                        │
                        ▼
              ┌───────────────┐
              │  API Gateway  │ :8080
              └───────┬───────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
┌───────────┐ ┌───────────┐ ┌───────────┐
│  Pedidos  │ │Pagamentos │ │  Estoque  │
└─────┬─────┘ └───────────┘ └───────────┘
        │
        ▼
┌───────────┐
│ PostgreSQL│
└───────────┘
```

### Serviços

| Serviço | Descrição | Porta |
|---------|-----------|-------|
| api-gateway | Gateway de entrada, roteamento | 8080 |
| pedidos | Gestão de pedidos | 8080 (interno) |
| pagamentos | Processamento de pagamentos | 8080 (interno) |
| estoque | Controle de estoque | 8080 (interno) |
| postgres | Banco de dados | 5432 |
| jaeger | Tracing distribuído | 16686 (UI) |
| prometheus | Métricas | 9090 |

##  Execução Local

### Pré-requisitos
- Docker >= 20.10
- Docker Compose >= 2.0

### Subir todos os serviços

```bash
docker compose up -d
```

### Verificar status

```bash
docker compose ps
```

### Parar serviços

```bash
docker compose down
```

##  Endpoints

| Endpoint | URL | Descrição |
|----------|-----|----------|
| Health Check | http://localhost:8080/health | Status do serviço |
| Métricas | http://localhost:8080/metrics | Métricas Prometheus |
| Jaeger UI | http://localhost:16686 | Tracing distribuído |
| Prometheus | http://localhost:9090 | Dashboard de métricas |

##  Estrutura do Projeto

```
├── .github/workflows/     # CI/CD pipelines
│   └── ci-cd.yml
├── k8s/                   # Manifests Kubernetes
│   ├── deployments/       # Deployments dos serviços
│   ├── services/          # Services (ClusterIP, NodePort)
│   ├── configmaps/        # Configurações
│   ├── secrets/           # Secrets (senhas, tokens)
│   └── hpa/               # Horizontal Pod Autoscalers
├── services/              # Código dos microserviços
│   ├── api-gateway/
│   ├── pedidos/
│   ├── pagamentos/
│   └── estoque/
├── observability/         # Configurações de observabilidade
│   └── prometheus.yml
├── terraform/             # Infraestrutura como código
├── tests/                 # Testes unitários
└── docker-compose.yml     # Orquestração local
```

##  Kubernetes

### Deploy no cluster

```bash
# Aplicar todos os manifests
kubectl apply -f k8s/configmaps/
kubectl apply -f k8s/secrets/
kubectl apply -f k8s/deployments/
kubectl apply -f k8s/services/
kubectl apply -f k8s/hpa/
```

### Verificar recursos

```bash
kubectl get pods
kubectl get services
kubectl get hpa
```

### Acessar via NodePort

```bash
curl http://localhost:30080/health
```

##  Segurança

### Containers
- **Usuário não-root**: Todos os containers rodam com `appuser`
- **Multi-stage build**: Imagens mínimas sem ferramentas de build
- **Read-only filesystem**: Containers com filesystem somente leitura

### Kubernetes
- **SecurityContext**: Pods configurados com:
  - `runAsNonRoot: true`
  - `allowPrivilegeEscalation: false`
  - `readOnlyRootFilesystem: true`
  - `capabilities.drop: ALL`

##  Observabilidade

### Métricas (Prometheus)
Todos os serviços expõem métricas no endpoint `/metrics`:
- `http_requests_total` - Total de requisições HTTP por serviço/método/endpoint

### Logs
Logs estruturados no formato:
```
2024-01-01 12:00:00 | INFO | api-gateway | GET /health
```

### Tracing (Jaeger)
Tracing distribuído com OpenTelemetry:
- UI disponível em http://localhost:16686
- Protocolo OTLP (gRPC: 4317, HTTP: 4318)

##  CI/CD

Pipeline automatizado com GitHub Actions:

1. **Lint & Testes**: flake8 + pytest
2. **Security Scan**: Trivy vulnerability scanner
3. **Build**: Construção das imagens Docker
4. **Testes de integração**: Health check dos containers
5. **Push**: Publicação no Docker Hub

### Secrets necessários
- `DOCKERHUB_USERNAME`: Usuário do Docker Hub
- `DOCKERHUB_TOKEN`: Token de acesso do Docker Hub

##  Escalabilidade

### Horizontal Pod Autoscaler (HPA)
Cada serviço possui HPA configurado:
- **CPU threshold**: 70%
- **Memory threshold**: 80%
- **Min replicas**: 2
- **Max replicas**: 6-10 (varia por serviço)

### Estratégia de Deploy: Rolling Update
- `maxSurge: 1` - Máximo 1 pod extra durante update
- `maxUnavailable: 0` - Zero downtime

##  Tecnologias

- **Linguagem**: Python 3.11
- **Framework**: Flask
- **Banco de dados**: PostgreSQL 15
- **Containerização**: Docker
- **Orquestração**: Kubernetes
- **CI/CD**: GitHub Actions
- **Observabilidade**: Prometheus + Jaeger
- **IaC**: Terraform

##  Licença

MIT License
