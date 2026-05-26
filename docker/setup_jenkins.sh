#!/bin/bash
# =============================================================================
# setup_jenkins.sh
# Construye la imagen personalizada de Jenkins y levanta el contenedor.
# Uso: bash setup_jenkins.sh
# =============================================================================

IMAGE_NAME="jenkins-qa"
CONTAINER_NAME="jenkins-qa"
JENKINS_PORT="8080"
JENKINS_VOLUME="jenkins_qa_home"

echo ""
echo "========================================"
echo "  🚀 Jenkins QA Automation Setup"
echo "========================================"
echo ""

# ── 1. Detener y eliminar contenedor anterior si existe ───────────────────────
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "🛑 Deteniendo contenedor anterior..."
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
    echo "✅ Contenedor eliminado"
fi

# ── 2. Construir la imagen personalizada ──────────────────────────────────────
echo ""
echo "🔨 Construyendo imagen Docker personalizada..."
docker build -t $IMAGE_NAME ./docker/

if [ $? -ne 0 ]; then
    echo "❌ Error al construir la imagen. Revisa el Dockerfile."
    exit 1
fi
echo "✅ Imagen '$IMAGE_NAME' construida correctamente"

# ── 3. Levantar el contenedor ─────────────────────────────────────────────────
echo ""
echo "🐳 Levantando contenedor Jenkins..."
docker run -d \
    -p $JENKINS_PORT:8080 \
    -u root \
    -v $JENKINS_VOLUME:/var/jenkins_home \
    -v //var/run/docker.sock:/var/run/docker.sock \
    --name $CONTAINER_NAME \
    --restart unless-stopped \
    $IMAGE_NAME

if [ $? -ne 0 ]; then
    echo "❌ Error al levantar el contenedor."
    exit 1
fi

# ── 4. Esperar a que Jenkins arranque ─────────────────────────────────────────
echo ""
echo "⏳ Esperando que Jenkins inicie (esto puede tomar 1-2 minutos)..."
sleep 15

# ── 5. Mostrar la contraseña inicial ─────────────────────────────────────────
echo ""
echo "========================================"
echo "  ✅ Jenkins listo!"
echo "========================================"
echo ""
echo "  URL:      http://localhost:$JENKINS_PORT"
echo ""
echo "  🔑 Contraseña inicial de admin:"
docker exec $CONTAINER_NAME cat /var/jenkins_home/secrets/initialAdminPassword 2>/dev/null || echo "  (El contenedor aún está iniciando, espera unos segundos y corre:)"
echo "  docker exec $CONTAINER_NAME cat /var/jenkins_home/secrets/initialAdminPassword"
echo ""
echo "  📌 Versiones instaladas:"
docker exec $CONTAINER_NAME python3 --version 2>/dev/null
docker exec $CONTAINER_NAME chromium --version 2>/dev/null
echo ""
