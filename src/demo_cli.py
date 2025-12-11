import os
import sys
from query_embed_and_search import search_pubmed
from rag_answer import answer_query

# Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
MAGENTA = "\033[95m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"

def banner():
    print(f"{CYAN}{BOLD}")
    print("==============================================")
    print("             PubMed RAG Demo")
    print("==============================================")
    print(f"{RESET}")
    print(f"{YELLOW}Enter a biomedical question and press ENTER.")
    print("Example: 'genetic biomarkers for breast cancer'")
    print(f"{RESET}")

def show_docs(docs):
    print(f"\n{GREEN}{BOLD}------ Retrieved Documents ------{RESET}\n")
    for d in docs:
        print(f"{CYAN}{BOLD}Document {d['rank']} (PMID {d['pmid']}){RESET}")
        print(f"{BOLD}{d['title']}{RESET}")
        print(d['abstract'][:500] + "...")
        print(f"{MAGENTA}" + "-"*50 + f"{RESET}\n")

def show_answer(answer_text):
    print(f"\n{MAGENTA}{BOLD}------ LLM Answer ------{RESET}\n")
    print(answer_text)
    print(f"\n{MAGENTA}" + "="*50 + f"{RESET}")


def main():
    banner()

    while True:
        query = input(f"{YELLOW}Your Query: {RESET}")
        if not query.strip():
            print(f"{RED}Please enter a valid query.{RESET}")
            continue

        print(f"\n{CYAN}Searching PubMed...{RESET}")
        docs = search_pubmed(query, top_k=5)
        show_docs(docs)

        print(f"{CYAN}Generating LLM answer...{RESET}")
        answer = answer_query(query)
        show_answer(answer)

        again = input(f"{GREEN}Ask another question? (y/n): {RESET}")
        if again.lower().strip() != "y":
            break


if __name__ == "__main__":
    main()
