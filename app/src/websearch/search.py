import arxiv
from mediawikiapi import MediaWikiAPI, WikipediaPage
import re
import os


def search_arxiv(keywords: list[str], limit=2):
    client = arxiv.Client()
    results = []
    for keyword in keywords:
        search = arxiv.Search(
            query=keyword,
            max_results=limit,
        )
        result = list(client.results(search))
        results.extend(result)
    return results  # list of papers to be downloaded.


def download_papers(papers: list[arxiv.Result]):
    for paper in papers:
        paper.download_pdf(
            dirpath="src/websearch/temp_results",
            filename="Paper_" + paper.title.replace(" ", "_") + ".pdf",
        )


def search_wiki(keywords: list[str], limit=2) -> list[WikipediaPage]:

    wiki = MediaWikiAPI()
    ls = list(map(lambda keyword: wiki.search(keyword, results=limit), keywords))

    to_return = [i for j in ls for i in j]

    return list(map(lambda title: wiki.page(title, auto_suggest=False), to_return))


def download_wikis(wikis: list[WikipediaPage], dirpath="src/websearch/temp_results"):

    for wiki in wikis:
        title = "Wiki_" + re.sub("[\W_]+", "_", wiki.title)
        dirpath_appended = f"{dirpath}/{title}.txt"

        with open(dirpath_appended, "w+", encoding="utf-8") as f:
            f.write(wiki.content)


def clear_dir(dirpath="src/websearch/temp_results"):
    all_files = os.listdir(dirpath)
    for file in all_files:
        if file.endswith(".txt") or file.endswith(".pdf"):
            os.remove(f"{dirpath}/{file}")
