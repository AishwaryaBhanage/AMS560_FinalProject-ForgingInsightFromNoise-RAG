import os
import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

PARQUET_FILE = "../spark_clean/pubmed_clean.parquet"
OUT_DIR = "../embeddings"
CHUNK_SIZE = 2000   # safe for CPU, increase if needed
MODEL_NAME = "intfloat/e5-small"

os.makedirs(OUT_DIR, exist_ok=True)

print("Loading model:", MODEL_NAME)
model = SentenceTransformer(MODEL_NAME, device="cpu")

print("Reading Parquet file metadata...")
pf = pq.ParquetFile(PARQUET_FILE)
num_rows = pf.metadata.num_rows
print("Total rows:", num_rows)

chunk_idx = 0

for batch in pf.iter_batches(batch_size=CHUNK_SIZE):
    df = batch.to_pandas()
    texts = df["abstract_clean"].fillna("").astype(str).tolist()

    print(f"Encoding chunk {chunk_idx} ...")
    embeddings = model.encode(
        texts,
        batch_size=64,
        show_progress_bar=False
    ).astype("float32")

    np.save(f"{OUT_DIR}/emb_{chunk_idx}.npy", embeddings)
    df[["pmid", "title"]].to_parquet(
        f"{OUT_DIR}/meta_{chunk_idx}.parquet",
        index=False
    )

    print("Saved emb_", chunk_idx)
    chunk_idx += 1

print("DONE! Total chunks:", chunk_idx)
