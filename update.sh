#!/bin/bash

update_dot_sh_version=2.0.0

# TODO: download svn here, cache and set in path, then delete when finished
#       https://www.visualsvn.com/files/Apache-Subversion-1.14.3.zip

python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
python update.py
deactivate
