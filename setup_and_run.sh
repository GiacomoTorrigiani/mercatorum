#!/bin/bash

# === 1. Aggiorna pacchetti
sudo apt update && sudo apt upgrade -y

# === 2. Installa dipendenze
sudo apt install -y wget unzip curl gnupg python3 python3-pip xvfb libxi6 libgconf-2-4 libnss3 libxss1 libappindicator1 libindicator7 fonts-liberation libatk-bridge2.0-0 libgtk-3-0

# === 3. Installa Google Chrome (Stable)
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb

# === 4. Installa ChromeDriver compatibile
CHROME_VERSION=$(google-chrome --version | grep -oP "\d+\.\d+\.\d+" | head -1)
CHROMEDRIVER_VERSION=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_$CHROME_VERSION")
wget -O chromedriver.zip "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip"
unzip chromedriver.zip
sudo mv chromedriver-linux64/chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
rm -rf chromedriver.zip chromedriver-linux64*

# === 5. Installa pacchetti Python richiesti
pip3 install selenium

# === 6. Salva ed esegui lo script Python
cat <<EOF > autoplay_mercatorum.py
# Incolla qui tutto il tuo script Python (esattamente come nel tuo messaggio precedente)
# Per comodità puoi anche fare: nano autoplay_mercatorum.py e incollarlo manualmente
EOF

# === 7. Esegui con X virtuale (headless reale)
xvfb-run -a python3 autoplay_mercatorum.py
