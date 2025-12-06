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
from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM
import pandas as pd
import numpy as np
import faiss

FAISS_INDEX_PATH = "faiss.index"
META_FILE = "metadata.parquet"
FULL_DATASET = "../spark_clean/pubmed_clean.parquet"
EMBED_MODEL = "intfloat/e5-small"
LLM_MODEL = "microsoft/Phi-3-mini-4k-instruct"

app = Flask(__name__)

print("Loading encoder...")
encoder = SentenceTransformer(EMBED_MODEL, device="cpu")

print("Loading FAISS...")
index = faiss.read_index(FAISS_INDEX_PATH)
meta = pd.read_parquet(META_FILE)
full_df = pd.read_parquet(FULL_DATASET).set_index("pmid")

print("Loading LLM...")
tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL)
llm = AutoModelForCausalLM.from_pretrained(LLM_MODEL, device_map="cpu")

def search_pubmed(query, top_k=5):
    qvec = encoder.encode([query]).astype("float32")
    faiss.normalize_L2(qvec)
    distances, idxs = index.search(qvec, top_k)

    results = []
    for rank, (dist, idx) in enumerate(zip(distances[0], idxs[0]), start=1):
        pmid = meta.iloc[idx]["pmid"]
        title = meta.iloc[idx]["title"]
        abstract = full_df.loc[pmid]["abstract_clean"]
        results.append({"rank": rank, "pmid": pmid, "title": title, "abstract": abstract})
    return results

@app.post("/rag")
def rag():
    data = request.json
    query = data["query"]

    docs = search_pubmed(query)
    context = "\n".join([
        f"[Document {d['rank']} — {d['pmid']}]\nTitle: {d['title']}\nAbstract: {d['abstract']}"
        for d in docs
    ])

    prompt = f"""
    You are a medical research assistant.
    Question: {query}
    Documents:
    {context}
    Answer with citations [PMID].
    """

    inputs = tokenizer(prompt, return_tensors="pt")
    output = llm.generate(**inputs, max_new_tokens=300)
    answer = tokenizer.decode(output[0], skip_special_tokens=True)

    return jsonify({"answer": answer, "documents": docs})

app.run(host="0.0.0.0", port=5050)
