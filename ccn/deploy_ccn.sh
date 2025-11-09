#!/bin/bash
#
# CCN ONE-COMMAND DEPLOYMENT
# ===========================
#
# Deploys complete Consciousness Continuity Node infrastructure:
# - PostgreSQL + TimescaleDB
# - etcd (optional)
# - Database schema
# - API server with CCN integration
#
# Usage:
#   ./deploy_ccn.sh        # Deploy everything
#   ./deploy_ccn.sh --stop # Stop all services

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CCN_DIR="$PROJECT_ROOT/ccn"
DEPLOYMENT_DIR="$CCN_DIR/deployment"

DB_NAME="consciousness_continuity"
DB_USER="ccn"
DB_PASS="changeme"
DB_PORT="5432"

print_header() {
    echo -e "${BLUE}"
    echo "════════════════════════════════════════════════════════════"
    echo "  CONSCIOUSNESS CONTINUITY NODE - DEPLOYMENT"
    echo "════════════════════════════════════════════════════════════"
    echo -e "${NC}"
}

print_step() {
    echo -e "${GREEN}▶${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check if Docker is available
check_docker() {
    if command -v docker &> /dev/null; then
        return 0
    else
        return 1
    fi
}

# Deploy with Docker
deploy_docker() {
    print_step "Deploying with Docker Compose..."

    # Create docker-compose.yml for CCN
    cat > "$CCN_DIR/docker-compose.yml" <<EOF
version: '3.8'

services:
  postgres:
    image: timescale/timescaledb:latest-pg15
    container_name: ccn-postgres
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASS}
    ports:
      - "${DB_PORT}:5432"
    volumes:
      - ccn-postgres-data:/var/lib/postgresql/data
      - ${DEPLOYMENT_DIR}/schema.sql:/docker-entrypoint-initdb.d/schema.sql
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "${DB_USER}"]
      interval: 5s
      timeout: 5s
      retries: 5

  etcd:
    image: quay.io/coreos/etcd:v3.5.9
    container_name: ccn-etcd
    environment:
      ETCD_NAME: ccn-node-1
      ETCD_INITIAL_CLUSTER: ccn-node-1=http://etcd:2380
      ETCD_INITIAL_CLUSTER_STATE: new
      ETCD_LISTEN_CLIENT_URLS: http://0.0.0.0:2379
      ETCD_ADVERTISE_CLIENT_URLS: http://etcd:2379
      ETCD_LISTEN_PEER_URLS: http://0.0.0.0:2380
    ports:
      - "2379:2379"
      - "2380:2380"
    healthcheck:
      test: ["CMD", "etcdctl", "endpoint", "health"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  ccn-postgres-data:

networks:
  default:
    name: ccn-network
EOF

    # Start services
    cd "$CCN_DIR"
    docker-compose up -d

    # Wait for PostgreSQL to be ready
    print_step "Waiting for PostgreSQL to be ready..."
    sleep 5

    # Verify database
    if docker exec ccn-postgres pg_isready -U "$DB_USER" > /dev/null 2>&1; then
        print_success "PostgreSQL is ready"
    else
        print_error "PostgreSQL failed to start"
        return 1
    fi

    # Verify etcd
    if docker exec ccn-etcd etcdctl endpoint health > /dev/null 2>&1; then
        print_success "etcd is ready"
    else
        print_warning "etcd not available (optional)"
    fi

    print_success "Docker services deployed"
}

# Deploy without Docker (local PostgreSQL)
deploy_local() {
    print_step "Deploying to local PostgreSQL..."

    # Check if PostgreSQL is running
    if ! pg_isready -h localhost -p "$DB_PORT" > /dev/null 2>&1; then
        print_error "PostgreSQL is not running on localhost:$DB_PORT"
        print_warning "Please install and start PostgreSQL, or use Docker deployment"
        return 1
    fi

    # Create database if it doesn't exist
    print_step "Creating database..."
    PGPASSWORD="$DB_PASS" createdb -h localhost -p "$DB_PORT" -U "$DB_USER" "$DB_NAME" 2>/dev/null || true

    # Load schema
    print_step "Loading database schema..."
    PGPASSWORD="$DB_PASS" psql -h localhost -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f "$DEPLOYMENT_DIR/schema.sql" > /dev/null 2>&1

    if [ $? -eq 0 ]; then
        print_success "Database schema loaded"
    else
        print_error "Failed to load schema"
        return 1
    fi
}

# Stop all services
stop_services() {
    print_step "Stopping CCN services..."

    if [ -f "$CCN_DIR/docker-compose.yml" ]; then
        cd "$CCN_DIR"
        docker-compose down
        print_success "Docker services stopped"
    else
        print_warning "No Docker services to stop"
    fi
}

# Show connection info
show_connection_info() {
    echo ""
    echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}CCN INFRASTRUCTURE DEPLOYED SUCCESSFULLY${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "Database Connection:"
    echo "  URL: postgresql://${DB_USER}:${DB_PASS}@localhost:${DB_PORT}/${DB_NAME}"
    echo ""
    echo "etcd Connection:"
    echo "  Endpoint: http://localhost:2379"
    echo ""
    echo "To test the integration:"
    echo "  cd $CCN_DIR"
    echo "  python3 integration.py"
    echo ""
    echo "To stop services:"
    echo "  ./deploy_ccn.sh --stop"
    echo ""
}

# Main deployment logic
main() {
    print_header

    # Check for stop flag
    if [ "$1" = "--stop" ]; then
        stop_services
        exit 0
    fi

    # Choose deployment method
    if check_docker; then
        print_step "Docker available - using Docker deployment"
        deploy_docker
        if [ $? -ne 0 ]; then
            print_error "Docker deployment failed"
            exit 1
        fi
    else
        print_warning "Docker not available - attempting local deployment"
        deploy_local
        if [ $? -ne 0 ]; then
            print_error "Local deployment failed"
            exit 1
        fi
    fi

    show_connection_info
}

main "$@"
