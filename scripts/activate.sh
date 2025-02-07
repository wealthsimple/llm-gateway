#!/bin/bash
. .venv/bin/activate
export PYTHONPATH=/usr/src/app
export $(cat .envrc | xargs)
