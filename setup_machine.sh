#!/usr/bin/env bash

# This script installs a set of common tools that I use on each machine.  For
# example, you could run this script in a docker container and end up with a
# setup very similar to one of my local development machines

set -e

if [[ ! -f $HOME/.ssh/id_ed25519 ]]
    echo "Error: you need to have an ssh key setup with Github for this to work"
    exit 1
fi

# make some common files
mkdir -p $HOME/dev/personal

# install common packages required to build everything else...
sudo apt update

sudo apt-get install make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm zsh \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

# install python & nodejs environments
curl https://pyenv.run | bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash

pyenv install 3.9.6
pip install pipenv

nvm install --lts

# install local dotfiles
cd $HOME/dev/personal
git clone https://github.com/michaelhelvey/dotfiles-manager
cd dotfiles-manager
pipenv run python source/main.py sync

# install antigen
mkdir -p $HOME/.config/antigen
curl -L git.io/antigen > $HOME/.config/antigen/antigen.zsh

# set shell to be zsh
chsh -s $(which zsh)

# install nvim, with nodejs and python support
sudo apt install neovim # should be automatically aliased by our zshrc

pip install neovim
npm i -g neovim

# install Rust and Go toolchains
cd $HOME/Downloads
wget https://go.dev/dl/go1.18.2.linux-amd64.tar.gz
rm -rf /usr/local/go && tar -C /usr/local -xzf go1.18.2.linux-amd64.tar.gz

curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
rustup update
