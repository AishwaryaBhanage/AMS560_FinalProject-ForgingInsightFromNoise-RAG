import os
import numpy as np
import pandas as pd
import faiss

EMB_DIR = "../embeddings"
OUT_INDEX = "faiss.index"
OUT_META = "metadata.parquet"

all_embeddings = []
all_meta = []

# Load chunked embeddings + metadata
for file in sorted(os.listdir(EMB_DIR)):
    if file.startswith("emb_") and file.endswith(".npy"):
        idx = file.split("_")[1].split(".")[0]
        emb = np.load(os.path.join(EMB_DIR, file))
        meta = pd.read_parquet(os.path.join(EMB_DIR, f"meta_{idx}.parquet"))
        
        all_embeddings.append(emb)
        all_meta.append(meta)

# Merge everything
all_embeddings = np.vstack(all_embeddings).astype("float32")
all_meta = pd.concat(all_meta, ignore_index=True)
print("Final embedding matrix shape:", all_embeddings.shape)

# Create FAISS index
dim = all_embeddings.shape[1]   # e.g., 384
index = faiss.IndexFlatL2(dim)
index.add(all_embeddings)
faiss.write_index(index, OUT_INDEX)

# Save metadata
all_meta.to_parquet(OUT_META)
print("Saved FAISS index + metadata")
