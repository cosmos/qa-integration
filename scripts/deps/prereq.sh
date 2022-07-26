#/bin/bash

## This script installs the basic apt packages and also checks if go is installed on the system or
## not. If go is not installed on the system then go1.17.3 is installed by the script. Env variables
## related to go are also exported to bashrc. 

command_exists () {
    type "$1" &> /dev/null ;
}

CURPATH=`dirname $(realpath "$0")`
cd $CURPATH
source ../../env

if command_exists docker ; then
  echo "[+] docker is already installed"
else
  echo "[!] Please check https://docs.docker.com/desktop/install/linux-install/ , how to install docker"
  exit 
fi

if command_exists docker-compose ; then
  echo "[+] docker-compose is already installed"
else
  echo "[!] Installing docker-compose  > Check (https://docs.docker.com/compose/install/compose-plugin/#install-the-plugin-manually)"
  curl -SL https://github.com/docker/compose/releases/download/v2.7.0/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
  sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
fi

if command_exists python3 ; then
  echo "[+] python3-dev is already installed"
else
  echo "[!] Installing python3-dev"
  sudo apt update
  sudo apt install python3-dev -y
fi

if command_exists pylint ; then
  echo "[+] pylint is already installed"
else
  echo "[!] Installing pylint"
  sudo apt update
  sudo apt install pylint -y
fi

if command_exists pip ; then
  echo "[+] pip is already installed"
else
  echo "[!] Installing pip"
  sudo apt update
  sudo apt install python3-pip -y
fi

pip install -r ../../internal/requirements.txt
