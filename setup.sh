#!/bin/bash

_ALIAS="alias news='poetry --directory $PWD run $PWD/app.py'"

# "If the shell is NOT Bash"
if [ -n "$BASH_VERSION" ]; then
		echo "$_ALIAS" >> ~/.zshrc && echo "[+] Ok"
		echo '[i] Execute the following script to finish the setup:' 
		echo 'source ~/.zshrc'
		echo '[i] Then, just execute "news"'
# "If the shell is NOT Zsh"
elif [ -n "$ZSH_VERSION" ]; then
		echo "$_ALIAS" >> ~/.bashrc && echo "[+] Ok"
		echo '[i] Execute the following script to finish the setup:' 
		echo 'source ~/.bashrc'
		echo '[i] Then, just execute "news"'
fi


