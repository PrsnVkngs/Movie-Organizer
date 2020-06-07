@echo off
python -m pip install --upgrade pip
title Installing Dependencies
echo Now Executing Pip command
pip install git+https://github.com/alberanid/imdbpy
pip install tk
pip install pymediainfo

timeout 3