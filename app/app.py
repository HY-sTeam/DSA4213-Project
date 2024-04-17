import streamlit as st
import os
from src.websearch.search import clear_dir
from io import BytesIO

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Cm, Pt, Inches
from base64 import b64encode
from src.llm.lang import (
    query,
    create_collection,
    start_client,
    ingest_files_in_dir,
    clear_all_collections,
    clear_all_documents,
    clear_all_pending_uploads
)
from src.llm.pptgen import (
    generate_ppt,
    decide_ppt_colour,
    decide_slide_titles,
    gen_key_words,
)
from src.websearch.search import (
    clear_dir,
    download_papers,
    download_wikis,
    search_arxiv,
    search_wiki,
)


# Function to download the prs generated
def get_bytes(
    ppt, file_name="presentation.pptx"
):
    ppt_bytes = BytesIO()
    ppt.save(ppt_bytes)
    # ppt_bytes.seek(0)
    # b64 = b64encode(ppt_bytes.read()).decode()
    # href = f'<a href="data:application/vnd.openxmlformats-officedocument.presentationml.presentation;base64,{b64}" download="{file_name}">{file_label}</a>'
    return ppt_bytes


def main():
    # Set page title and favicon
    st.set_page_config(page_title="Your Streamlit App", page_icon="🚀")

    # Sidebar
    st.sidebar.title("Sidebar Title")
    # Add sidebar elements
    # Example: sidebar_option = st.sidebar.selectbox("Sidebar Option", ["Option 1", "Option 2"])

    # Main content
    st.title("Main Title")
    # Add main content elements
    # Example: st.write("Hello, world!")
    wants_arxiv = wants_wiki = True
    user_input = st.text_input("I want to create a presentation about:", max_chars=150)
    user_request = "I want to create a presentation about " + user_input
    user_doesnt_care_about_colours = True
    if st.button("Click me"):

        with st.status("Generating PPT...", expanded=True) as status:

            clear_dir()
            st.write("Starting up...")
            client = start_client()
            clear_all_collections(client)
            clear_all_documents(client)
            clear_all_pending_uploads(client)
            st.write("Scouring the web...")

            collection_id = create_collection(client)
            output = gen_key_words(client, user_request)

            if wants_arxiv:
                papers = search_arxiv(output)
                download_papers(papers)
            if wants_wiki:
                wikis = search_wiki(output)
                download_wikis(wikis)

            st.write("Ingesting information...")
            ingest_files_in_dir(client, collection_id)
            st.write("Thinking about design...")
            
            colour_dict = decide_ppt_colour(client, user_input)

            files = [file.split("/")[-1] for file in os.listdir("./src/websearch/temp_results") if file.endswith(".txt") or file.endswith(".pdf")]

            list_of_slide_titles = decide_slide_titles(client, user_input, files)

            chat_session_id = client.create_chat_session()
            st.write("Generating PPT...")
            prs = generate_ppt(
                client, chat_session_id, list_of_slide_titles, colour_dict
            )
            st.download_button(label="Download File!", data=get_bytes(prs), file_name="Presentation.pptx")

            status.update(label="Done!", state="complete", expanded=True)


if __name__ == "__main__":
    main()
