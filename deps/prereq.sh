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
  export GOPATH=$HOME/go
  echo "" >> ~/.bashrc
  echo 'export GOROOT=/usr/local/go' >> ~/.bashrc
fi

if [[ -z $GOPATH || -z $GOBIN || "$PATH" != *"$SGOBIN"* ]]; then
  echo "------ Update bashrc ---------------"
  export GOPATH=$HOME/go
  export GOBIN=$GOPATH/bin
  echo "" >> ~/.bashrc
  echo 'export GOPATH=$HOME/go' >> ~/.bashrc
  echo 'export GOBIN=$GOPATH/bin' >> ~/.bashrc
  echo 'export PATH=$PATH:/usr/local/go/bin:$GOROOT/bin:$GOBIN' >> ~/.bashrc
fi
source ~/.bashrc
mkdir -p "$GOBIN"
mkdir -p $GOPATH/src/github.com
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

echo "" >> ~/.bashrc
source ~/.bashrc
