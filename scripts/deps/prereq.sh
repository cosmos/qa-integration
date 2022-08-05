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

if command_exists go ; then
  echo "Golang is already installed"
else
  echo "Install dependencies"
  sudo apt update
  sudo apt install build-essential jq -y
  wget -q https://dl.google.com/go/go$goversion.linux-amd64.tar.gz
  tar -xf go$goversion.linux-amd64.tar.gz
  sudo cp -R go /usr/local
  go_path=`which go`
  if [ ! -z "$go_path" ]; then
    sudo cp go/bin/go $go_path
  fi
  rm -rf go$goversion.linux-amd64.tar.gz go
  export GOPATH=$HOME/go
  echo "" >> ~/.bashrc
  echo 'export GOROOT=/usr/local/go' >> ~/.bashrc
  source ~/.bashrc
fi
go version

if command_exists python3 ; then
  echo "python3-dev is already installed"
else
  echo "Installing python3-dev"
  sudo apt update
  sudo apt install python3-dev -y
fi

if command_exists pylint ; then
  echo "pylint is already installed"
else
  echo "Installing pylint"
  sudo apt update
  sudo apt install pylint -y
fi

if command_exists pip ; then
  echo "pip is already installed"
else
  echo "Installing pip"
  sudo apt update
  sudo apt install python3-pip -y
fi

pip install -r ../../internal/requirements.txt

if command_exists mongod ; then
  echo "mongo db is already installed"
else
  sudo apt-get install gnupg
  wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -
  echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list
  sudo apt-get update -y
  sudo apt-get install mongodb-org -y
fi
sudo systemctl start mongod
