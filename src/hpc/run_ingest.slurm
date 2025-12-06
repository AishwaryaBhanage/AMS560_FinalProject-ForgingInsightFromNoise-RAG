#!/bin/bash
#SBATCH -p long-40core
#SBATCH --job-name=pubmed_python_ingest
#SBATCH --output=../logs/ingest_%j.out
#SBATCH --error=../logs/ingest_%j.err
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=40
#SBATCH --mem=120G

module load python/3.9.7

export PYTHONPATH=$HOME/.local/lib/python3.10/site-packages:$PYTHONPATH
python ../scripts/spark_ingest_pubmed.py

