📚 PubMed Data Description

This project uses the PubMed Baseline Dataset provided by the National Center for Biotechnology Information (NCBI).
Due to the large scale of the data (millions of articles), raw data is not stored in this repository.

🔹 Data Source

Provider: NCBI – National Library of Medicine (NIH)

Dataset: PubMed Baseline

Official URL:
https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/

License: Public Domain (U.S. Government Work)

🔹 Dataset Overview
Component	Description
Format	XML (.xml.gz)
Articles	~36 million (full baseline)
Records used	~4.5 million articles
Fields extracted	PMID, Title, Abstract, Journal, Year
Storage size	~200GB uncompressed (full baseline)
🔹 Why Raw Data Is Not Included

Raw PubMed XML files are extremely large

Data is publicly available and reproducible

GitHub storage limits prohibit hosting such datasets

🔹 How to Download PubMed Data 

To fetch raw PubMed baseline XML files directly:

wget https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed25n0001.xml.gz


Or batch download (example):

for i in $(seq -w 1 70); do
  wget https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed25n00${i}.xml.gz
done


⚠️ Downloading the full baseline requires significant storage and compute resources.
This project was executed on an HPC cluster.
