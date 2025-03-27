# 1. Basis-Image mit Python
FROM python:3.10-slim

# 2. Systemabhängigkeiten installieren
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 3. Arbeitsverzeichnis setzen
WORKDIR /app

# 4. Requirements kopieren und installieren
COPY requirements.txt .

# 5. Installiere alle Packages OHNE Build-Isolation (für detectron2)
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir --no-build-isolation 'git+https://github.com/facebookresearch/detectron2.git'

# 6. App-Code kopieren (Backend Ordner mit Leerzeichen)
COPY ["CNN/Backend Vercel/", "/app"]

# 7. Port-Variable (für Railway, aber lokal läuft 5000)
ENV PORT=5000

# 8. App starten
CMD ["python", "app.py"]
