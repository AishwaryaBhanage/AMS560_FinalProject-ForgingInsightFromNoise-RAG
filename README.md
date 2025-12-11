# PubMed Semantic Search System 🔍

A powerful AI-driven semantic search engine for finding relevant medical research papers from PubMed database. Instead of simple keyword matching, this system understands the **meaning** behind your queries and returns the most relevant scientific papers with AI-generated summaries.

---

## 📋 Table of Contents

- [What Does This Project Do?](#what-does-this-project-do)
- [Problem Statement](#problem-statement)
- [How It Works](#how-it-works)
- [System Requirements](#system-requirements)
- [Installation Guide](#installation-guide)
- [Step-by-Step Execution](#step-by-step-execution)
- [Usage Examples](#usage-examples)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Technical Details](#technical-details)

---

## 🎯 What Does This Project Do?

This system allows researchers, doctors, and students to:

1. **Search millions of medical research papers** using natural language questions
2. **Get the top 5 most relevant papers** based on semantic similarity (meaning), not just keywords
3. **Receive AI-generated answers** that synthesize information from multiple papers with proper citations

### Example Use Case:

**Your Question:** *"What are the latest treatments for ovarian cancer?"*

**What You Get:**
- 5 most relevant research papers with full abstracts
- An AI-generated summary combining insights from all papers
- Proper citations (PMID numbers) for each claim

**Why This Is Better Than Google Scholar:**
- Understands **semantic meaning** (e.g., "cancer treatment" = "chemotherapy" = "therapeutic interventions")
- Works **completely offline** (no internet needed after setup)
- Generates **synthesized answers** instead of just listing papers
- **Fast** - Results in under 1 second

---

## 🚨 Problem Statement

### The Challenge

Medical researchers face several problems when searching for scientific literature:

1. **Information Overload**: PubMed contains over 35 million research articles
2. **Keyword Limitations**: Traditional search engines only find exact keyword matches
   - Searching "genetic biomarkers" misses papers about "tumor markers" or "hereditary cancer"
3. **Time-Consuming**: Researchers spend hours reading abstracts to find relevant papers
4. **Context Missing**: Hard to synthesize information across multiple papers

### Our Solution

We built an AI-powered semantic search system that:
- ✅ Converts research papers into mathematical vectors (embeddings) that capture meaning
- ✅ Uses FAISS (Facebook AI Similarity Search) to find similar papers in milliseconds
- ✅ Employs a Large Language Model (LLM) to generate coherent answers with citations
- ✅ Works entirely offline with no API costs

---

## 🛠️ How It Works

### 4-Stage Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  STAGE 1: DATA INGESTION                                       │
│  ├─ Input: Raw XML files from PubMed                          │
│  ├─ Process: Parse, clean, extract metadata                   │
│  └─ Output: Clean Parquet file (pubmed_clean.parquet)         │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  STAGE 2: EMBEDDINGS GENERATION                                │
│  ├─ Input: Clean Parquet file                                 │
│  ├─ Process: Convert abstracts → 384-dim vectors              │
│  └─ Output: Embedding files (.npy) + metadata                 │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  STAGE 3: INDEXING                                             │
│  ├─ Input: All embedding files                                │
│  ├─ Process: Create searchable FAISS index                    │
│  └─ Output: faiss.index + metadata.parquet                    │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  STAGE 4: SEARCH & ANSWER                                      │
│  ├─ Input: User query                                         │
│  ├─ Process: Find top 5 papers + generate LLM answer          │
│  └─ Output: Ranked results with AI summary                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Simple Explanation:

1. **Ingestion**: We read XML files containing research papers and clean the data
2. **Embeddings**: We convert each paper's abstract into a list of 384 numbers that represent its meaning
3. **Indexing**: We organize all these number lists for super-fast searching
4. **Search**: When you ask a question, we convert it to numbers, find the closest matching papers, and generate an answer

---

## 💻 System Requirements

### Minimum Requirements:
- **Operating System**: Windows, macOS, or Linux
- **RAM**: 16 GB (32 GB recommended for large datasets)
- **Storage**: 100+ GB free space
- **CPU**: Multi-core processor (4+ cores recommended)
- **Internet**: Required only for initial setup (downloading models)

### Optional:
- **GPU**: Not required but can speed up processing

---

## 📦 Installation Guide

### Step 1: Install Python

Download and install Python 3.8 or higher from [python.org](https://www.python.org/downloads/)

**Verify installation:**
```bash
python --version
```

You should see something like: `Python 3.10.x`

---

### Step 2: Create Project Directory

Create a folder for your project:

**Windows (PowerShell):**
```powershell
mkdir "C:\PubMed_Search"
cd "C:\PubMed_Search"
```

**macOS/Linux:**
```bash
mkdir ~/PubMed_Search
cd ~/PubMed_Search
```

---

### Step 3: Create Virtual Environment (Recommended)

This keeps your project dependencies isolated.

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` before your command prompt.

---

### Step 4: Install Required Packages

Copy and paste this command:

```bash
pip install pandas numpy pyarrow lxml sentence-transformers faiss-cpu transformers torch tqdm
```

**What each package does:**
- `pandas`: Data manipulation
- `numpy`: Numerical operations
- `pyarrow`: Fast Parquet file reading/writing
- `lxml`: XML parsing
- `sentence-transformers`: Text → Vector conversion
- `faiss-cpu`: Fast similarity search
- `transformers`: LLM support
- `torch`: Deep learning framework
- `tqdm`: Progress bars

**Installation time:** 5-10 minutes (downloads ~2-3 GB)

---

### Step 5: Download Project Files

Copy these 5 Python files into your project directory:

1. `ingestion.py` - Parses XML files
2. `embeddings.py` - Generates embeddings
3. `indexing.py` - Creates searchable index
4. `searching.py` - Search functionality
5. `answer.py` - Answer generation

**Your directory should look like:**
```
PubMed_Search/
├── venv/
├── ingestion.py
├── embeddings.py
├── indexing.py
├── searching.py
└── answer.py
```

---

### Step 6: Prepare Data Directory Structure

Create these folders:

**Windows:**
```powershell
mkdir raw
mkdir spark_clean
mkdir embeddings
```

**macOS/Linux:**
```bash
mkdir raw spark_clean embeddings
```

**Final structure:**
```
PubMed_Search/
├── venv/
├── raw/                    ← Put XML files here
├── spark_clean/            ← Cleaned data goes here
├── embeddings/             ← Embedding files go here
├── ingestion.py
├── embeddings.py
├── indexing.py
├── searching.py
└── answer.py
```

---

### Step 7: Download PubMed Data

You need PubMed XML files. You can:

**Option A: Download from NCBI FTP** (Full dataset - Large!)
```
ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/
```

**Option B: Download Sample Data** (Recommended for testing)
- Download a few XML files (~100 MB each) for testing
- Place them in the `raw/` folder

**Example:** Download files like `pubmed24n0001.xml.gz`, extract them, and place in `raw/`

---

## 🚀 Step-by-Step Execution

Now that everything is installed, follow these steps **in order**.

---

### STAGE 1: Data Ingestion 📥

**What this does:** Extracts data from XML files and cleans it.

**Command:**
```bash
python ingestion.py
```

**What you'll see:**
```
Found 10 XML files
100%|████████████████████████████████| 10/10 [05:23<00:00, 32.35s/it]
Total parsed rows: 500000
Saved cleaned data to: ../spark_clean/pubmed_clean.parquet
```

**Time:** 10-60 minutes (depends on file count and CPU)

**Output:** `spark_clean/pubmed_clean.parquet` file

**Troubleshooting:**
- If you get "File not found", make sure XML files are in `raw/` folder
- If you get memory errors, you have too many large files - start with fewer files

---

### STAGE 2: Generate Embeddings 🧮

**What this does:** Converts paper abstracts into numerical vectors.

**Command:**
```bash
python embeddings.py
```

**What you'll see:**
```
Loading model: intfloat/e5-small
Reading Parquet file metadata...
Total rows: 500000
Encoding chunk 0 ...
Saved emb_ 0
Encoding chunk 1 ...
Saved emb_ 1
...
DONE! Total chunks: 250
```

**Time:** 1-3 hours (depends on number of papers and CPU speed)

**Output:** 
- Multiple `embeddings/emb_*.npy` files
- Multiple `embeddings/meta_*.parquet` files

**What happens:**
1. Downloads the e5-small model (~33 MB) on first run
2. Processes papers in chunks of 2000
3. Creates one embedding file per chunk

**Troubleshooting:**
- If download fails, check internet connection
- If too slow, reduce `CHUNK_SIZE` in `embeddings.py` to 1000

---

### STAGE 3: Create Search Index 📚

**What this does:** Creates a fast searchable index from all embeddings.

**Command:**
```bash
python indexing.py
```

**What you'll see:**
```
Final embedding matrix shape: (500000, 384)
Saved FAISS index + metadata
```

**Time:** 5-10 minutes

**Output:**
- `faiss.index` - The searchable index (~2 GB for 1M papers)
- `metadata.parquet` - Mapping file

**Troubleshooting:**
- If "Out of memory" error, close other applications
- Requires ~10+ GB RAM for 1M papers

---

### STAGE 4: Search and Get Answers 🎯

**What this does:** Lets you search and get AI-generated answers!

#### Option A: Quick Search Test

**Command:**
```bash
python searching.py
```

**Default query:** "genetic biomarkers for breast cancer"

**What you'll see:**
```
Loading model...
Loading index...
1. PMID 12345678 – "Genetic markers in breast cancer"
   Score: 0.234
   Abstract: genetic biomarkers have shown promise in...

2. PMID 87654321 – "BRCA1 and BRCA2 mutations"
   Score: 0.341
   Abstract: hereditary breast cancer is associated with...

[... 3 more results]
```

#### Option B: Search with Custom Query

Edit `searching.py` and change the query at the bottom:

```python
if __name__ == "__main__":
    q = "YOUR QUESTION HERE"  # ← Change this
    res = search_pubmed(q)
```

Then run:
```bash
python searching.py
```

#### Option C: Get AI-Generated Answer

**Command:**
```bash
python answer.py
```

**Default query:** "latest treatments for ovarian cancer"

**What you'll see:**
```
Loading local LLM: microsoft/Phi-3-mini-4k-instruct
Loading model...
Loading index...

=== ANSWER ===

You are a scientific research assistant.
Use ONLY the documents below. Provide a concise answer with citations [PMID].

User question:
latest treatments for ovarian cancer

Documents:
[Document 1 — PMID 1393742]
Title: Advances in the screening and treatment of ovarian cancer.
Abstract: ovarian cancer is the leading cause of death...
-----
[... 4 more documents]

Answer:
The latest treatments for ovarian cancer include advancements in 
chemotherapy, such as platinum-based chemotherapy [PMID 1500391], 
which has improved response rates and prolonged survival. Taxol in 
combination with platinum drugs shows promise for even further 
improvements in survival [PMID 1500391]...
```

**Time:** 
- First run: 2-3 minutes (downloads Phi-3 model ~2.3 GB)
- Subsequent runs: 2-5 seconds per query

**To customize the question:**

Edit `answer.py` at the bottom:

```python
if __name__ == "__main__":
    answer_query("YOUR QUESTION HERE")  # ← Change this
```

---

## 📝 Usage Examples

### Example 1: Cancer Research

**Query:** *"What are the side effects of chemotherapy?"*

**Expected Results:**
- Papers about chemotherapy toxicity
- Papers about adverse drug reactions
- Papers about patient management during treatment

### Example 2: Drug Discovery

**Query:** *"compounds that inhibit tumor growth"*

**Expected Results:**
- Papers on anti-cancer agents
- Papers on molecular mechanisms
- Papers on drug screening studies

### Example 3: Clinical Practice

**Query:** *"diagnosis methods for diabetes"*

**Expected Results:**
- Papers on blood glucose testing
- Papers on HbA1c measurements
- Papers on diagnostic criteria

---

## 📁 Project Structure

After complete execution, your directory will look like:

```
PubMed_Search/
│
├── raw/                          # Input XML files
│   ├── pubmed24n0001.xml
│   ├── pubmed24n0002.xml
│   └── ...
│
├── spark_clean/                  # Cleaned data
│   └── pubmed_clean.parquet      # All papers in clean format
│
├── embeddings/                   # Vector embeddings
│   ├── emb_0.npy                # Embedding chunk 0
│   ├── meta_0.parquet           # Metadata chunk 0
│   ├── emb_1.npy
│   ├── meta_1.parquet
│   └── ...
│
├── faiss.index                   # FAISS search index
├── metadata.parquet              # Index → PMID mapping
│
├── ingestion.py                  # Stage 1 script
├── embeddings.py                 # Stage 2 script
├── indexing.py                   # Stage 3 script
├── searching.py                  # Stage 4 script (search only)
├── answer.py                     # Stage 4 script (search + LLM)
│
└── venv/                         # Python virtual environment
```

---

## 🐛 Troubleshooting

### Issue 1: "ModuleNotFoundError: No module named 'X'"

**Solution:**
```bash
pip install X
```

Make sure your virtual environment is activated.

---

### Issue 2: "Out of Memory" during indexing

**Solutions:**
1. Close other applications
2. Process fewer papers at a time
3. Upgrade RAM (16 GB minimum, 32 GB recommended)

---

### Issue 3: XML parsing errors

**Solution:**
The code uses `recover=True` to handle malformed XML. If files are corrupt:
1. Re-download the XML file
2. Check file integrity
3. Remove corrupt files from `raw/` folder

---

### Issue 4: Embeddings too slow

**Solutions:**
1. Reduce `CHUNK_SIZE` in `embeddings.py` from 2000 to 1000
2. Reduce batch size from 64 to 32
3. Use a faster CPU or enable GPU support

---

### Issue 5: Search returns irrelevant results

**Possible causes:**
1. Query is too vague - be more specific
2. Not enough papers indexed - add more data
3. Papers indexed don't cover your topic - get domain-specific data

---

### Issue 6: LLM download fails

**Solution:**
```bash
# Manually download model
python -c "from transformers import AutoModel; AutoModel.from_pretrained('microsoft/Phi-3-mini-4k-instruct')"
```

If internet is slow, this downloads the ~2.3 GB model separately.

---

### Issue 7: FAISS index file is huge

**This is normal!**
- 1 million papers ≈ 1.5 GB index
- 10 million papers ≈ 15 GB index

If space is limited:
1. Index fewer papers
2. Use compressed index types (advanced)

---

## 🔧 Technical Details

### Technologies Used

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Language** | Python 3.8+ | Main programming language |
| **Data Processing** | Pandas, NumPy | Data manipulation |
| **Storage** | Apache Parquet | Efficient columnar storage |
| **XML Parsing** | lxml | Parse PubMed XML |
| **Embeddings** | Sentence Transformers | Text → Vector conversion |
| **Model** | intfloat/e5-small | 384-dim embeddings |
| **Search** | FAISS | Fast vector similarity search |
| **LLM** | Microsoft Phi-3-mini | Answer generation |
| **Parallelization** | multiprocessing | CPU-level parallelism |

---

### How Semantic Search Works

1. **Training Phase** (One-time):
   ```
   Paper Abstract → Transformer Model → 384-number Vector
   
   Example:
   "chemotherapy improves survival" → [0.23, 0.45, -0.12, ..., 0.78]
   "cancer treatment with drugs"   → [0.21, 0.48, -0.15, ..., 0.81]
   
   These vectors are close because papers have similar meanings!
   ```

2. **Search Phase** (Every query):
   ```
   Your Question → Same Model → 384-number Vector
   
   Compare your vector with all paper vectors:
   - Distance = 0.10 → Very similar ✓
   - Distance = 0.50 → Somewhat similar
   - Distance = 5.00 → Not similar ✗
   
   Return top 5 closest matches
   ```

---

### Performance Metrics

| Stage | Input Size | Processing Time | Output Size |
|-------|-----------|-----------------|-------------|
| **Ingestion** | 100 XML files (10 GB) | ~30 min | 5 GB Parquet |
| **Embeddings** | 1M papers | ~1-2 hours | 1.5 GB |
| **Indexing** | 1M embeddings | ~5 min | 1.5 GB |
| **Search** | 1 query | < 150 ms | 5 results |
| **Answer** | 1 query + 5 papers | ~3 seconds | 1 answer |

---

### File Sizes (Approximate)

```
For 1 million papers:

Raw XML files:         ~10-20 GB
pubmed_clean.parquet:  ~5 GB
Embeddings (all):      ~1.5 GB
FAISS index:           ~1.5 GB
Models (cached):       ~2.5 GB (e5-small + Phi-3)
───────────────────────────────
Total:                 ~20-30 GB
```

---

## 🎓 Understanding the Output

### Search Results Explained

```python
{
    "rank": 1,                              # Position in results (1-5)
    "pmid": "1393742",                      # PubMed ID (for citation)
    "title": "Advances in screening...",   # Paper title
    "abstract": "ovarian cancer is...",    # Full abstract
    "score": 0.234                          # Distance score (lower = better)
}
```

**Score Interpretation:**
- **0.0 - 0.3**: Highly relevant
- **0.3 - 0.6**: Moderately relevant
- **0.6 - 1.0**: Somewhat relevant
- **> 1.0**: Less relevant

---

### LLM Answer Format

The LLM generates answers in this format:

```
[Main claim] [PMID citation]. [Supporting detail] [PMID citation].
[Another claim] [PMID citation]. [More details] [PMID citation].
```

**Example:**
```
The latest treatments for ovarian cancer include platinum-based 
chemotherapy [PMID 1500391], which has improved response rates. 
Taxol in combination shows promise [PMID 1500391]. For recurrent 
cases, cytoreductive surgery is key [PMID 1358032].
```

Every factual claim is linked to a source paper.

---

## 🚀 Next Steps & Customization

### Customize Search Parameters

In `searching.py`, modify:

```python
# Change number of results
results = search_pubmed(query, top_k=10)  # Get 10 instead of 5

# Use different query
q = "your custom question here"
```

### Customize Answer Generation

In `answer.py`, modify:

```python
# Longer answers
max_new_tokens=500  # Instead of 300

# More creative answers
temperature=0.3     # Instead of 0.0 (adds variety)

# Include more context
docs = search_pubmed(query, top_k=10)  # Use 10 papers instead of 5
```

### Add More Data

Simply:
1. Download more XML files
2. Place in `raw/` folder
3. Re-run all 4 stages

The system will process new data and add to index.

---

## 📚 Additional Resources

### Learn More About:

- **PubMed**: https://pubmed.ncbi.nlm.nih.gov/
- **FAISS**: https://github.com/facebookresearch/faiss
- **Sentence Transformers**: https://www.sbert.net/
- **Transformers**: https://huggingface.co/docs/transformers/

### Related Papers:

- "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks" (2019)
- "Billion-scale similarity search with GPUs" (2017) - FAISS paper

---

## 👥 Support & Contributing

### Need Help?

1. Check the [Troubleshooting](#troubleshooting) section
2. Review error messages carefully
3. Ensure all installation steps were followed

### Common Beginner Mistakes:

❌ Forgot to activate virtual environment  
❌ Didn't put XML files in `raw/` folder  
❌ Skipped a stage in the pipeline  
❌ Ran out of disk space  
❌ Not enough RAM for dataset size  

---

## 📄 License & Citation

This project uses open-source components:
- **FAISS**: MIT License
- **Sentence Transformers**: Apache 2.0
- **Transformers**: Apache 2.0

If you use this project in research, please cite the underlying technologies.

---

## ✅ Final Checklist

Before running the system, ensure:

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] All packages installed via pip
- [ ] Directory structure created (`raw/`, `spark_clean/`, `embeddings/`)
- [ ] PubMed XML files placed in `raw/` folder
- [ ] At least 100 GB free disk space
- [ ] At least 16 GB RAM available

### Quick Start Commands (Copy-Paste)

```bash
# Setup (one-time)
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install pandas numpy pyarrow lxml sentence-transformers faiss-cpu transformers torch tqdm

# Execution (in order)
python ingestion.py       # Step 1: Parse XML
python embeddings.py      # Step 2: Generate embeddings
python indexing.py        # Step 3: Create index
python searching.py       # Step 4a: Search only
python answer.py          # Step 4b: Search + AI answer
```

---

## 🎉 Congratulations!

You now have a fully functional semantic search system for PubMed research papers!

**What you built:**
- ✅ Data ingestion pipeline processing millions of papers
- ✅ Semantic embedding system using transformers
- ✅ Fast vector search using FAISS
- ✅ AI answer generation using LLM
- ✅ Complete offline research assistant

**Next time you need to search medical literature, use this instead of spending hours on Google Scholar!**

---

**Last Updated**: December 11, 2025  
**Version**: 1.0  
**Status**: Production Ready ✓
