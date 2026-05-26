# Imagen base oficial de Jenkins
FROM jenkins/jenkins:lts

# Cambiar a root para instalar dependencias del sistema
USER root

# Instalar Python, Chrome y dependencias necesarias
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    chromium \
    chromium-driver \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    wget \
    curl \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Crear symlinks para que 'python3' y 'chromedriver' sean encontrados fácilmente
RUN ln -sf /usr/bin/python3 /usr/local/bin/python3
RUN ln -sf /usr/bin/chromium /usr/local/bin/chromium
RUN ln -sf /usr/bin/chromedriver /usr/local/bin/chromedriver

# Volver al usuario jenkins para que el daemon corra sin privilegios
USER jenkins

# Instalar plugins de Jenkins automáticamente
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt
