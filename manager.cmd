@echo off
@setlocal
cd %~dp0
pipenv run python manager.py %*

