from h2ogpte import H2OGPTE, Session
import json
import os
import re
import pptx

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
        return try_and_parse(user_query, function, failed=failed, markdown=markdown)


def create_collection(client: H2OGPTE) -> str:

    return client.create_collection(
        name='Collection',
        description='Papers',
    )

def ingest_files_in_dir(client: H2OGPTE, collection_id, path="src/websearch/temp_results"):
    all_files = os.listdir(path)
    txt_files = [f"{path}/{file}" for file in all_files if file.endswith('.txt')]
    pdf_files = [f"{path}/{file}" for file in all_files if file.endswith('.pdf')]
    all_files = txt_files.copy()
    all_files.extend(pdf_files)
    
    opened_files = [open(file, "rb") for file in all_files]

    for i in range(len(opened_files)):
        all_files[i] = client.upload(all_files[i], opened_files[i])
        opened_files[i].close()

    client.ingest_uploads(collection_id, all_files)
    
