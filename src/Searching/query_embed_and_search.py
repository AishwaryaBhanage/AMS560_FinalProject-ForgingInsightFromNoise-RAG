import os, sys

# Disable transformers optional integrations
os.environ["TRANSFORMERS_NO_TORCHVISION"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
os.environ["AWS_EC2_METADATA_DISABLED"] = "true"
os.environ["BOTO_CONFIG"] = "/dev/null"

# Prevent boto3/botocore import attempts
sys.modules["boto3"] = None
sys.modules["botocore"] = None
sys.modules["botocore.client"] = None
sys.modules["botocore.session"] = None
sys.modules["botocore.utils"] = None
sys.modules["botocore.httpsession"] = None

import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer


FAISS_INDEX_PATH = "faiss.index"
META_FILE = "metadata.parquet"
FULL_DATASET = "../spark_clean/pubmed_clean.parquet"
MODEL_NAME = "intfloat/e5-small"

# Load model
print("Loading model...")
model = SentenceTransformer(MODEL_NAME, device="cpu")

# Load FAISS index
print("Loading index...")
index = faiss.read_index(FAISS_INDEX_PATH)

# Load minimal metadata (pmid + title)
meta = pd.read_parquet(META_FILE)   # only pmid, title

# Load full dataset containing abstracts
full_df = pd.read_parquet(FULL_DATASET)  # pmid, title, abstract, journal, year
full_df = full_df.set_index("pmid")      # fast lookup

# Search function
def search_pubmed(query, top_k=5):
    qvec = model.encode([query]).astype("float32")
    faiss.normalize_L2(qvec)

    distances, idxs = index.search(qvec, top_k)

    results = []
    for rank, (dist, midx) in enumerate(zip(distances[0], idxs[0]), start=1):
        pmid = meta.iloc[midx]["pmid"]
        title = meta.iloc[midx]["title"]

        # Now retrieve abstract from full dataset
        abstract = full_df.loc[pmid]["abstract_clean"]

        results.append({
            "rank": rank,
            "pmid": pmid,
            "title": title,
            "abstract": abstract,
            "score": float(dist)
        })

    return results

# Run example
if __name__ == "__main__":
    q = "genetic biomarkers for breast cancer"
    res = search_pubmed(q)

    for r in res:
        print(f"{r['rank']}. PMID {r['pmid']} – {r['title']}")
        print(f"   Score: {r['score']}")
        print(f"   Abstract: {r['abstract'][:200]}...\n")
