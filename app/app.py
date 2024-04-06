import streamlit as st
from src.websearch.search import clear_dir
from io import BytesIO

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Cm, Pt, Inches

from src.llm.lang import query, create_collection, start_client, ingest_files_in_dir
from src.llm.pptx import generate_ppt, decide_ppt_colour, decide_slide_titles, gen_key_words
from src.websearch.search import clear_dir, download_papers, download_wikis, search_arxiv, search_wiki

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
    if st.button('Click me'):
        
        with st.status('Generating PPT...', expanded=True) as status:
            clear_dir()
            st.write("Scouring the web...")
            client = start_client()
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


            list_of_slide_titles = decide_slide_titles(client, user_input)

            
            chat_session_id = client.create_chat_session() 
            st.write("Generating PPT...")
            prs = generate_ppt(client, chat_session_id, list_of_slide_titles, colour_dict)
            status.update(label="Done!", state="complete", expanded=False)


if __name__ == "__main__":
    main()

