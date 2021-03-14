#!/bin/env sh

# Comandos para instalar python y virtualenv
mkdir ~/.virtualenv;
sudo apt update;
sudo apt -y install python3-pip;
pip3 install virtualenvwrapper;
echo "PATH=\$PATH:\$HOME/.local/bin" >>  ~/.bashrc;
echo "export WORKON_HOME=\$HOME/.virtualenvs" >>  ~/.bashrc;
echo "VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >>  ~/.bashrc;
echo ". \$HOME/.local/bin/virtualenvwrapper.sh" >>  ~/.bashrc;
source ~/.bashrc;

# Comandos para instalar Docker
sudo apt -y install apt-transport-https ca-certificates curl software-properties-common;
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -;
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable";
sudo apt update;
sudo apt -y install docker-ce;
sudo usermod -aG docker ${USER}; # Este comando necesita de un logout/login para hacer efecto

# Comando para instalar Splash
sudo docker pull scrapinghub/splash;

# Comandos para crear y configurar el virtualenv del Crawler
cd;
git clone https://github.com/josed1608/CrawlEncuentra24.git;
cd ~/CrawlEncuentra24;
mkvirtualenv crawler;
pip install scrapy;
pip install scrapy-splash;