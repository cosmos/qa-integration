#/bin/sh

## This script installs the basic apt packages and also checks if go is installed on the system or
## not. If go is not installed on the system then go1.17.3 is installed by the script. Env variables
## related to go are also exported to bashrc. 

command_exists () {
    type "$1" &> /dev/null ;
}

cd $HOME

if command_exists go ; then
  echo "Golang is already installed"
else
  echo "Install dependencies"
  sudo apt update
  sudo apt-get -y upgrade
  sudo apt install build-essential jq -y
  source ../env
  wget https://dl.google.com/go/go$goversion.linux-amd64.tar.gz
  tar -xvf go$goversion.linux-amd64.tar.gz
  sudo mv go /usr/local
  rm go$goversion.linux-amd64.tar.gz
  echo "------ Update bashrc ---------------"
  export GOPATH=$HOME/go
  export GOROOT=/usr/local/go
  export GOBIN=$GOPATH/bin
  export PATH=$PATH:/usr/local/go/bin:$GOBIN
  echo "" >> ~/.bashrc
  echo 'export GOPATH=$HOME/go' >> ~/.bashrc
  echo 'export GOROOT=/usr/local/go' >> ~/.bashrc
  echo 'export GOBIN=$GOPATH/bin' >> ~/.bashrc
  echo 'export PATH=$PATH:/usr/local/go/bin:$GOBIN' >> ~/.bashrc
  source ~/.bashrc
  mkdir -p "$GOBIN"
  mkdir -p $GOPATH/src/github.com
  go version
fi

if command_exists python3-dev ; then
  echo "python3-dev is already installed"
else
  echo "Installing python3-dev"
  sudo apt install python3-dev
fi

echo "" >> ~/.bashrc
source ~/.bashrc
