import arxiv
from mediawikiapi import MediaWikiAPI, WikipediaPage
import re
import os

def search_arxiv(keyword):
    client = arxiv.Client()
    search = arxiv.Search(
        query=keyword,
        max_results=10,
    )
    results = client.results(search)
    return list(results) # list of papers to be downloaded.

def download_papers(papers: list[arxiv.Result]):
    for paper in papers:
        paper.download_pdf(dirpath="app/src/websearch/temp_results", filename= "Paper_" + paper.title.replace(" ", "_") + '.pdf')

def search_wiki(keywords:list[str], limit=3) -> list[WikipediaPage]:
 
    wiki = MediaWikiAPI()
    ls = list(map(
        lambda keyword: wiki.search(keyword, results=limit), keywords
        ))
    return list(map(lambda title: wiki.page(title, auto_suggest=False), ls))
    

def download_wikis(wikis: list[WikipediaPage], dirpath = "app/src/websearch/temp_results"):   

    for wiki in wikis:
        title = "Wiki_" + re.sub('[\W_]+', '_',  wiki.title)
        dirpath_appended = f"{dirpath}/{title}.txt"
        
        with open(dirpath_appended, "w+", encoding="utf-8") as f:
            f.write(wiki.content)


def clear_dir(dirpath="app/src/websearch/temp_results"):
    all_files = os.listdir(dirpath)
    for file in all_files:
        if file.endswith(".txt") or file.endswith(".pdf"): 
            os.remove(f"{dirpath}/{file}")

