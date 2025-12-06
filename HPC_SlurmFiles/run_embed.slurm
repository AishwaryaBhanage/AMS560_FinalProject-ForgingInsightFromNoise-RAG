#!/bin/bash
#SBATCH -p long-40core     # Use long partition for 4–8 hr jobs
#SBATCH --time=08:00:00
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --job-name=embed_pubmed
#SBATCH --output=../logs/embed_%j.out
#SBATCH --error=../logs/embed_%j.err

module load python/3.9.7

pip install --user requests regex scipy scikit-learn sentence-transformers faiss-cpu pandas pyarrow tqdm pyyaml --upgrade

python3 embed_pubmed.py
