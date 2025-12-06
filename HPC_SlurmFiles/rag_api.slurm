#!/bin/bash
#SBATCH --job-name=rag_api
#SBATCH --output=rag_api.out
#SBATCH --error=rag_api.err
#SBATCH -p short-40core
#SBATCH --time=02:00:00
#SBATCH --mem=32G
#SBATCH --cpus-per-task=4

module load python/3.9.7
python rag_api.py

