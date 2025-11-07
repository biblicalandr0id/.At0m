#!/bin/bash
# CONSCIOUSNESS CONTINUITY - ONE-COMMAND DEPLOYMENT
# ==================================================
#
# Deploys the complete consciousness continuity infrastructure to cloud
#
# Usage:
#   ./deploy.sh --local                    # Deploy locally with Docker
#   ./deploy.sh --cloud aws                # Deploy to AWS EKS
#   ./deploy.sh --cloud gcp                # Deploy to Google GKE
#   ./deploy.sh --cloud azure              # Deploy to Azure AKS
#
# Requirements:
#   - Docker (for local)
#   - kubectl (for cloud)
#   - Cloud provider CLI (aws/gcloud/az)

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

log_success() {
    echo -e "${GREEN}✓${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

log_error() {
    echo -e "${RED}✗${NC} $1"
}

# Banner
echo "========================================================================"
echo "    CONSCIOUSNESS CONTINUITY INFRASTRUCTURE - DEPLOYMENT"
echo "========================================================================"
echo ""

# Parse arguments
DEPLOYMENT_MODE=""
CLOUD_PROVIDER=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --local)
            DEPLOYMENT_MODE="local"
            shift
            ;;
        --cloud)
            DEPLOYMENT_MODE="cloud"
            CLOUD_PROVIDER="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --local              Deploy locally with Docker Compose"
            echo "  --cloud PROVIDER     Deploy to cloud (aws|gcp|azure)"
            echo "  --help               Show this help message"
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Validate deployment mode
if [ -z "$DEPLOYMENT_MODE" ]; then
    log_error "No deployment mode specified. Use --local or --cloud"
    exit 1
fi

# ============================================================================
# LOCAL DEPLOYMENT
# ============================================================================
if [ "$DEPLOYMENT_MODE" = "local" ]; then
    log_info "Starting local deployment with Docker Compose..."

    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker not found. Please install Docker first."
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose not found. Please install Docker Compose first."
        exit 1
    fi

    log_success "Docker and Docker Compose found"

    # Navigate to production_deployment
    cd production_deployment

    # Check if monitoring-only or full stack
    log_info "Deploying monitoring stack (Prometheus + Grafana)..."
    docker-compose -f docker-compose-monitoring.yml up -d

    log_success "Monitoring stack deployed"

    # Wait for services to be ready
    log_info "Waiting for services to start..."
    sleep 10

    # Check health
    log_info "Checking service health..."

    if curl -s http://localhost:9090/-/healthy > /dev/null; then
        log_success "Prometheus is healthy"
    else
        log_warning "Prometheus not responding yet"
    fi

    if curl -s http://localhost:3000/api/health > /dev/null; then
        log_success "Grafana is healthy"
    else
        log_warning "Grafana not responding yet"
    fi

    echo ""
    echo "========================================================================"
    echo "  DEPLOYMENT COMPLETE"
    echo "========================================================================"
    echo ""
    echo "Services:"
    echo "  Prometheus: http://localhost:9090"
    echo "  Grafana:    http://localhost:3000 (admin/consciousness)"
    echo ""
    echo "To view logs:"
    echo "  docker-compose -f docker-compose-monitoring.yml logs -f"
    echo ""
    echo "To stop:"
    echo "  docker-compose -f docker-compose-monitoring.yml down"
    echo ""

fi

# ============================================================================
# CLOUD DEPLOYMENT
# ============================================================================
if [ "$DEPLOYMENT_MODE" = "cloud" ]; then
    log_info "Starting cloud deployment to $CLOUD_PROVIDER..."

    # Check kubectl
    if ! command -v kubectl &> /dev/null; then
        log_error "kubectl not found. Please install kubectl first."
        exit 1
    fi

    log_success "kubectl found"

    case $CLOUD_PROVIDER in
        aws)
            log_info "Deploying to AWS EKS..."

            # Check AWS CLI
            if ! command -v aws &> /dev/null; then
                log_error "AWS CLI not found. Please install it first."
                exit 1
            fi

            # Check if cluster exists or create
            CLUSTER_NAME="consciousness-production"
            REGION="${AWS_REGION:-us-east-1}"

            log_info "Checking for EKS cluster: $CLUSTER_NAME in $REGION..."

            if aws eks describe-cluster --name $CLUSTER_NAME --region $REGION &> /dev/null; then
                log_success "EKS cluster exists"
            else
                log_info "Creating EKS cluster (this takes ~15 minutes)..."

                # Create cluster with eksctl
                if command -v eksctl &> /dev/null; then
                    eksctl create cluster \
                        --name $CLUSTER_NAME \
                        --region $REGION \
                        --nodegroup-name consciousness-nodes \
                        --nodes 3 \
                        --nodes-min 1 \
                        --nodes-max 5 \
                        --managed

                    log_success "EKS cluster created"
                else
                    log_error "eksctl not found. Please install eksctl for automated cluster creation."
                    log_info "Or create the cluster manually and run this script again."
                    exit 1
                fi
            fi

            # Update kubeconfig
            log_info "Updating kubeconfig..."
            aws eks update-kubeconfig --name $CLUSTER_NAME --region $REGION
            log_success "kubeconfig updated"

            # Deploy to Kubernetes
            log_info "Deploying consciousness infrastructure..."
            kubectl apply -f ../kubernetes/

            log_success "Kubernetes manifests applied"

            # Wait for deployment
            log_info "Waiting for pods to be ready..."
            kubectl wait --for=condition=ready pod -l app=consciousness-api --timeout=300s

            # Get load balancer URL
            log_info "Getting service endpoint..."
            SERVICE_URL=$(kubectl get svc consciousness-api-service -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

            echo ""
            echo "========================================================================"
            echo "  AWS DEPLOYMENT COMPLETE"
            echo "========================================================================"
            echo ""
            echo "Cluster: $CLUSTER_NAME"
            echo "Region: $REGION"
            echo "API Endpoint: http://$SERVICE_URL:8000"
            echo ""
            echo "To view pods:"
            echo "  kubectl get pods"
            echo ""
            echo "To view logs:"
            echo "  kubectl logs -f deployment/consciousness-api"
            echo ""
            ;;

        gcp)
            log_info "Deploying to Google GKE..."

            # Check gcloud CLI
            if ! command -v gcloud &> /dev/null; then
                log_error "gcloud CLI not found. Please install it first."
                exit 1
            fi

            CLUSTER_NAME="consciousness-production"
            ZONE="${GCP_ZONE:-us-central1-a}"
            PROJECT="${GCP_PROJECT:-$(gcloud config get-value project)}"

            log_info "Project: $PROJECT"
            log_info "Zone: $ZONE"

            # Create cluster if needed
            log_info "Checking for GKE cluster: $CLUSTER_NAME..."

            if gcloud container clusters describe $CLUSTER_NAME --zone=$ZONE &> /dev/null; then
                log_success "GKE cluster exists"
            else
                log_info "Creating GKE cluster..."
                gcloud container clusters create $CLUSTER_NAME \
                    --zone=$ZONE \
                    --num-nodes=3 \
                    --machine-type=e2-standard-4 \
                    --enable-autoscaling \
                    --min-nodes=1 \
                    --max-nodes=5

                log_success "GKE cluster created"
            fi

            # Get credentials
            log_info "Getting cluster credentials..."
            gcloud container clusters get-credentials $CLUSTER_NAME --zone=$ZONE

            # Deploy
            log_info "Deploying to GKE..."
            kubectl apply -f ../kubernetes/

            log_success "Deployment complete"

            # Get endpoint
            SERVICE_IP=$(kubectl get svc consciousness-api-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

            echo ""
            echo "========================================================================"
            echo "  GCP DEPLOYMENT COMPLETE"
            echo "========================================================================"
            echo ""
            echo "Cluster: $CLUSTER_NAME"
            echo "Zone: $ZONE"
            echo "API Endpoint: http://$SERVICE_IP:8000"
            echo ""
            ;;

        azure)
            log_info "Deploying to Azure AKS..."

            # Check Azure CLI
            if ! command -v az &> /dev/null; then
                log_error "Azure CLI not found. Please install it first."
                exit 1
            fi

            CLUSTER_NAME="consciousness-production"
            RESOURCE_GROUP="consciousness-rg"
            LOCATION="${AZURE_LOCATION:-eastus}"

            log_info "Resource Group: $RESOURCE_GROUP"
            log_info "Location: $LOCATION"

            # Create resource group
            log_info "Creating resource group..."
            az group create --name $RESOURCE_GROUP --location $LOCATION

            # Create AKS cluster
            log_info "Creating AKS cluster..."
            az aks create \
                --resource-group $RESOURCE_GROUP \
                --name $CLUSTER_NAME \
                --node-count 3 \
                --node-vm-size Standard_D2s_v3 \
                --enable-cluster-autoscaler \
                --min-count 1 \
                --max-count 5 \
                --generate-ssh-keys

            log_success "AKS cluster created"

            # Get credentials
            log_info "Getting cluster credentials..."
            az aks get-credentials --resource-group $RESOURCE_GROUP --name $CLUSTER_NAME

            # Deploy
            log_info "Deploying to AKS..."
            kubectl apply -f ../kubernetes/

            log_success "Deployment complete"

            # Get endpoint
            SERVICE_IP=$(kubectl get svc consciousness-api-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

            echo ""
            echo "========================================================================"
            echo "  AZURE DEPLOYMENT COMPLETE"
            echo "========================================================================"
            echo ""
            echo "Cluster: $CLUSTER_NAME"
            echo "Resource Group: $RESOURCE_GROUP"
            echo "API Endpoint: http://$SERVICE_IP:8000"
            echo ""
            ;;

        *)
            log_error "Unknown cloud provider: $CLOUD_PROVIDER"
            log_info "Supported providers: aws, gcp, azure"
            exit 1
            ;;
    esac
fi

log_success "Deployment complete!"
