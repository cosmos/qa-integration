import os, subprocess
from utils.commands import is_tool

HOME = os.getenv('HOME')
    
if is_tool('go'):
    print("Golang is already installed")
else:
    print(" ------ Installing dependencies ------")
    os.chdir(os.path.expanduser(HOME))
    subprocess.run(['sudo', 'apt', 'update'])
    subprocess.run(['sudo', 'apt', 'install', 'build-essential', 'jq', '-y'])
    subprocess.run(['wget', 'https://dl.google.com/go/go1.17.3.linux-amd64.tar.gz'])
    subprocess.run(['tar', '-xvf', 'go1.17.3.linux-amd64.tar.gz'])
    subprocess.run(['rm', 'go1.17.3.linux-amd64.tar.gz'])
    subprocess.run(['sudo', 'mv', 'go', '/usr/local'])

    print("------ Creating GOBIN, GOPATH directories") 
    os.environ['GOPATH'] = f"{HOME}/go"
    GOPATH = os.getenv('GOPATH')
    os.environ['GOROOT'] = '/usr/local/go'
    GOROOT = os.getenv('GOROOT')
    os.environ['GOBIN'] = f"{GOPATH}/bin"
    GOBIN = os.getenv('GOBIN')
    subprocess.run(['sudo', 'mkdir', '-p', f"{GOBIN}"])
    subprocess.run(['sudo', 'mkdir', '-p', f"{GOPATH}/src/github.com"])
    print("------ Updating ~/.bashrc file ------")
    bash_object = open(f"{HOME}/.bashrc", 'a')
    bash_object.write('')
    bash_object.write('export GOPATH=$HOME/go\n')
    bash_object.write('export GOROOT=/usr/local/go\n')
    bash_object.write('export GOBIN=$GOPATH/bin\n')
    bash_object.write('export PATH=$PATH:/usr/local/go/bin:$GOBIN\n')
    bash_object.close()
    print("------ Run source ~/.bashrc cmd to set the path ------")