FROM python:3.9-slim

# Install Chrome and dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg2 \
    apt-transport-https \
    ca-certificates \
    curl \
    unzip \
    chromium \
    chromium-driver \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Chrome
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMIUM_PATH=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver
ENV DISPLAY=:99
ENV PYTHONUNBUFFERED=1
ENV WDM_LOG_LEVEL=0
ENV WDM_LOCAL=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create a wrapper script for Xvfb
RUN echo '#!/bin/bash\nXvfb :99 -screen 0 1024x768x16 &\nexec "$@"' > /entrypoint.sh \
    && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["flask", "run", "--host=0.0.0.0"]