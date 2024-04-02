from h2ogpte import H2OGPTE, Session
import json
import os
import re


def start_client():

    return H2OGPTE(
        address="https://h2ogpte.genai.h2o.ai",
        api_key=os.environ.get('H2OGPTE_API_KEY')
        )


def query(client: H2OGPTE, user_query, system_prompt, llm='mistralai/Mixtral-8x7B-Instruct-v0.1'):
    return client.answer_question(
        question=user_query,
        system_prompt=system_prompt,
        llm=llm
    ).content

def try_and_parse(client, user_query, system_prompt, llm='mistralai/Mixtral-8x7B-Instruct-v0.1', failed=0, markdown=True):
    '''
    Accepts a function and user_query, an input. Evaluates function(user_query) and 
    converts string output (usually a reply from an llm) into a json value. Use markdown=True
    if the json value is contained within a code chunk.
    '''
    chosen = query(client, user_query, system_prompt, llm=llm)
    try:
        if not markdown:
            topics = json.loads(chosen)
        else:
            print(chosen)
            pattern = r'^```(?:\w+)?\s*\n(.*?)(?=^```)```'
            result = re.findall(pattern, chosen, re.DOTALL | re.MULTILINE)[0].strip() 
            #print(result)
            topics = json.loads(result)
            
        return topics
    except Exception as e:
        failed+=1
        print(failed)
        print(e)# CHANGE TO LOGGING STATEMENT
        return try_and_parse(client, user_query, system_prompt, markdown=markdown, failed=failed+1)


def create_collection(client: H2OGPTE) -> str:

    return client.create_collection(
        name='Collection',
        description='Papers',
    )

def ingest_files_in_dir(client: H2OGPTE, collection_id, path="app/src/websearch/temp_results"):
    all_files = os.listdir(path)
    txt_files = [f"{path}/{file}" for file in all_files if file.endswith('.txt')]
    pdf_files = [f"{path}/{file}" for file in all_files if file.endswith('.pdf')]
    all_files = txt_files.copy()
    all_files.extend(pdf_files)


    
    
    print(all_files)
    to_ingest = []
    for file in all_files:
        if file.endswith(".txt") or file.endswith(".pdf"):
            try:
                opened = open(file, "rb")
                client.upload(file.split("/")[-1], opened)
                file.close()
            except Exception as e:
                print(e) #

    return client.ingest_uploads(collection_id, to_ingest)
    

if __name__ == "__main__":
    ## TEST
    client = H2OGPTE(
        address="https://h2ogpte.genai.h2o.ai",
        api_key="sk-HVbr4rwCG4QJPJsQaa7AKiF47jx64RDpAkEWdeQZzwiwlrRU"
        )
    col_id = client.create_collection(
        name='Articles',
        description='Articles for presentation',
    )
    print(ingest_files_in_dir(client, col_id))