#/bin/sh

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
  wget https://dl.google.com/go/go1.18.1.linux-amd64.tar.gz
  tar -xvf go1.18.1.linux-amd64.tar.gz
  sudo mv go /usr/local
  rm go1.18.1.linux-amd64.tar.gz
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

if command_exists python3-pip ; then
  echo "python3-pip is already installed"
else
  echo "Installing python3-pip"
  sudo apt install python3-pip
fi

if command_exits python3-venv ; then
  echo "python3-venv is already installed"
else
  echo "Installing python3-venv"
  sudo apt install python3-venv
fi

pip install --upgrade pip 
pip install python-dotenv
echo "" >> ~/.bashrc
echo 'export PYTHONPATH=$PYTHONPATH:$HOME/qa-integration:$HOME/qa-integration/python-qa-tools' >> ~/.bashrc
source ~/.bashrc
