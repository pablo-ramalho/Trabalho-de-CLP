#!/bin/bash
# Script para executar interface.py com virtual environment

cd "$(dirname "$0")"

# Ativa virtual environment
source venv/bin/activate

# Executa o programa com os argumentos passados
python3 interface.py "$@"
