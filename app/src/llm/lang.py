from h2ogpte import H2OGPTE
from h2ogpte.types import Job
import json
import os
import random
import re
import random

def start_client() -> H2OGPTE:
    """Connects to H2oGPTE

    Raises:
        Exception: Raised when API key is not provided

    Returns:
        H2OGPTE: Returns a client.
    """    
    if not os.environ.get("H2OGPTE_API_KEY"):
        raise Exception("NO API KEY")
    return H2OGPTE(
        address="https://h2ogpte.genai.h2o.ai",
        api_key=os.environ.get("H2OGPTE_API_KEY"),
    )


def query(
    client: H2OGPTE,
    user_query,
    system_prompt,
    llm="mistralai/Mixtral-8x7B-Instruct-v0.1",
) -> str:
    """A wrapper around the answer_question method.

    Args:
        client (H2OGPTE): A H2oGPTE Client
        user_query (str): User Prompt
        system_prompt (str): System Prompt
        llm (str, optional): LLM model. Defaults to "mistralai/Mixtral-8x7B-Instruct-v0.1".

    Returns:
        str: Output from LLM
    """    
    return client.answer_question(
        question=user_query,
        system_prompt=system_prompt,
        llm=llm,
<<<<<<< HEAD
        llm_args=dict(temperature=0.22+random.random()/10),
=======
        llm_args=dict(temperature=0.2 + random.random()/10),
>>>>>>> ccf256be16372c23c456ccd71990db6d235ab40c
    ).content


def try_and_parse(
    client: H2OGPTE,
    user_query: str,
    system_prompt: str,
    llm="mistralai/Mixtral-8x7B-Instruct-v0.1",
    failed=0,
    markdown=True,
):
    """Accepts a function and user_query, an input. Evaluates function(user_query) and
    converts string output (usually a reply from an llm) into a json value. Use markdown=True
    if the json value is contained within a code chunk.

    Args:
        client (H2OGPTE): A H2OGPTE client.
        user_query (str): A string for the user prompt.
        system_prompt (str): A string representing the system prompt
        llm (str, optional): String representing the LLM model. Defaults to "mistralai/Mixtral-8x7B-Instruct-v0.1".
        failed (int, optional): Number of times parsing to JSON fails. Defaults to 0.
        markdown (bool, optional): Whether the model outputs JSON in markdown format, and not a JSON string. Defaults to True.

    Returns:
        A python list or dictionary representing a JSON array or object.
    """    
    chosen = query(client, user_query, system_prompt, llm=llm)
    try:
        if not markdown:
            topics = json.loads(chosen)
        else:
            print(chosen)
            pattern = r"^```(?:\w+)?\s*\n(.*?)(?=^```)```"
            result = re.findall(pattern, chosen, re.DOTALL | re.MULTILINE)[0].strip()
            # print(result)
            topics = json.loads(result)

        return topics
    except Exception as e:
        failed += 1
        print(failed)
        print(e)  # CHANGE TO LOGGING STATEMENT
        return try_and_parse(
            client, user_query, system_prompt, markdown=markdown, failed=failed + 1
        )


def create_collection(client: H2OGPTE) -> str:
    """Wrapper around the create_collection method

    Args:
        client (H2OGPTE): A H2OGPTE client.

    Returns:
        str: collection ID
    """    

    return client.create_collection(
        name="Collection",
        description="Papers",
    )


def ingest_files_in_dir(
    client: H2OGPTE, collection_id: str, path: str="src/websearch/temp_results"
) -> Job:
    """Given a list of pdf or txt files in a directory, ingest them using the H2OGPTE API.

    Args:
        client (H2OGPTE): The H2OGPTE client.
        collection_id (str): Collection ID within H2OGPTE
        path (str, optional): Location of documents. Defaults to "src/websearch/temp_results".

    Returns:
        Job: A H2OGPTE job.
    """    
    all_files = os.listdir(path)
    txt_files = [f"{path}/{file}" for file in all_files if file.endswith(".txt")]
    pdf_files = [f"{path}/{file}" for file in all_files if file.endswith(".pdf")]
    all_files = txt_files.copy()
    all_files.extend(pdf_files)

    print(all_files)
    to_ingest = []
    for file in all_files:
        if file.endswith(".txt") or file.endswith(".pdf"):
            try:
                opened = open(file, "rb")
                client.upload(file.split("/")[-1], opened)
                opened.close()
            except Exception as e:
                print(e)  #

    return client.ingest_uploads(collection_id, to_ingest)


def clear_all_documents(client: H2OGPTE) -> None:
    """Clears all documents in H2OGPTE, associated with the client.

    Args:
        client (H2OGPTE): A H2OGPTE client.
    """    
    docs = client.list_recent_documents(offset=0, limit=1000)
    client.delete_documents(list(map(lambda x: x.id, docs)))
    assert client.count_documents() == 0


def clear_all_collections(client: H2OGPTE) -> None:
    """Clears all collections on H2OGPTE

    Args:
        client (H2OGPTE): A H2OGPTE client.
    """    
    col = client.list_recent_collections(0, 1000)
    client.delete_collections(list(map(lambda x: x.id, col)))
    assert client.count_collections() == 0


def clear_all_pending_uploads(client: H2OGPTE) -> None:
    """Clears all pending uploads on H2OGPTE

    Args:
        client (H2OGPTE): A H2OGPTE client.
    """    
    uploads = client.list_upload()
    if uploads:
        for upload in uploads:
            client.delete_upload(upload)
            print(f"{upload} deleted")


if __name__ == "__main__":
    ## TEST. lang.py is never run as a file.
    client = H2OGPTE(
        address="https://h2ogpte.genai.h2o.ai",
        api_key="sk-HVbr4rwCG4QJPJsQaa7AKiF47jx64RDpAkEWdeQZzwiwlrRU",
    )
    col_id = client.create_collection(
        name="Articles",
        description="Articles for presentation",
    )
    print(ingest_files_in_dir(client, col_id))