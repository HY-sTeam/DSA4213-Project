import streamlit as st
from src.websearch.search import clear_dir
from io import BytesIO

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
    user_input = st.text_input("Enter your text here:", max_chars=150)
    user_doesnt_care_about_colours = True
    if st.button('Click me'):
        
        with st.status('Generating PPT...', expanded=True) as status:
            clear_dir()
            st.write("Scouring the web...")
            client = start_client()
            collection_id = create_collection(client)
            output = gen_key_words(client, user_input)

            if wants_arxiv:
                papers = search_arxiv(output)
                download_papers(papers)
            if wants_wiki:
                wikis = search_wiki(output)
                download_wikis(wikis)
            st.write("Ingesting information...")
            ingest_files_in_dir(client, collection_id)
            st.write("Thinking about design...")
            
            decide_ppt_colour()

            status.update(label="Done!", state="complete", expanded=False)





if __name__ == "__main__":
    main()

