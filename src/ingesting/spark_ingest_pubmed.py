import os
import glob
import pandas as pd
from lxml import etree
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

RAW_DIR = "../raw"
OUT_PATH = "../spark_clean/pubmed_clean.parquet"

def parse_file(xml_path):
    results = []

    try:
        for event, elem in etree.iterparse(xml_path, tag="PubmedArticle", recover=True):

            # Extract fields safely
            pmid = elem.findtext(".//PMID")
            title = elem.findtext(".//ArticleTitle")
            abstract = elem.findtext(".//Abstract/AbstractText")
            journal = elem.findtext(".//Journal/Title")
            year = elem.findtext(".//DateCompleted/Year")

            if abstract:
                abstract_clean = (
                    abstract.lower()
                    .replace("\n", " ")
                    .replace("\r", " ")
                )
            else:
                abstract_clean = None

            results.append({
                "pmid": pmid,
                "title": title,
                "abstract_clean": abstract_clean,
                "journal": journal,
                "year": year
            })

            elem.clear()

    except Exception as e:
        print("Error in:", xml_path, e)

    return results


def main():
    xml_files = sorted(glob.glob(os.path.join(RAW_DIR, "*.xml")))

    print(f"Found {len(xml_files)} XML files")

    all_rows = []

    with Pool(processes=cpu_count()) as p:
        for rows in tqdm(p.imap(parse_file, xml_files), total=len(xml_files)):
            all_rows.extend(rows)

    print(f"Total parsed rows: {len(all_rows)}")
    df = pd.DataFrame(all_rows)

    df.to_parquet(OUT_PATH, index=False)
    print("Saved cleaned data to:", OUT_PATH)


if __name__ == "__main__":
    main()
