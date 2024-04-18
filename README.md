# DSA4213-Project Motivation

> *Have you ever imagined a world where you can generate a bundle of slides with just a single touch? Hooray! Say goodbye to tedious and time-consuming slide presentations. We're proud to introduce the DSA4213-Rojak Slides Generator, designed to help you quickly grasp the contents of various research papers or even just a general search.*

## Problem Statement
AI-driven tools like the PPT Generator are increasingly popular as they streamline the transformation of academic papers into engaging presentation slides, making communication more effective. This tool is ideal for academics, students, and professionals who frequently share research findings or data-heavy reports. The PPT Generator employs a large language model to intelligently analyze and distill key information from texts. Then, leveraging the RAG (Retrieval-Augmented Generation) pipeline, it creatively designs slides that are not only informative but also visually appealing, effectively eliminating the manual labor typically involved in slide creation. 

## Project Description
---
![Solution Workflow](details/solution_workflow.jpeg)
---

The workflow is designed to optimize the creation of presentation slides from user queries. Firstly, users may key in his or her a query, which is then processed by a Large Language Model (mixtral) to generate a refined search query. It's flexible for users to specify their query preference, where the tailored query is parsed to conduct a general search (Wikipedia), an advanced search (Arxiv) or both, leveraging chain-of-thought prompting for depth and precision. 

The results undergo a filtration process to ensure relevance and are then assembled into a collection. This collection is used to download necessary resources, ensuring that the content for the slides is authoritative and accurate. The heart of the system is the h2oGPTe RAG API, which intelligently synthesizes the downloaded resources to craft relevant headings and generate the slide content. Concurrently, the system decides on the formatting rules to ensure that the slides are not just informative but also visually engaging. 

Once the content is generated and formatted, it is available for users to download the completed slides as a .pptx file, and it is well-stored in a database for slides record retrieval. This seamless process, from query, data collection, slides generation, slides exportation and slides installment, epitomizes the potential of AI to revolutionize the way we prepare and consume information for academic and professional purposes. 

### Functionalities
Leveraging h2oGPTe as our client, the solution is mainly deployed in an Python environment and dockerised, consisting of the usage of: 
[X] user queries refinement and keyword generation through Mixtral-v0.1 LLM
[X] dataset scrapping and data collections with user specific demands
[X] slides headings, contents and design layout generations
[X] exporting the slides in .pptx form, enabling download and future slides information retrieval
[X] database interactions for slides and users details via PostgreSQL
[X] cleaning filepaths and caches to guarantee application deployment

We also offer our readers a flavour to exploring around our jupyter notebook for a backend model demonstration purpose. 

### Installation guide.
1. Cloning GitHub repository. 
```sh
git clone https://github.com/HY-sTeam/DSA4213-Project
```
2. Environment Configuration - put all your environment variables here, u can always refer to sample.env for a list of relevant environment variables used in this project. 
```sh 
nano .env
```
3. Install pipenv and relevant packages in Pipfile. 
```sh
pip install pipenv
pipenv install --dev
```
4. Activate python virtual environment. 
```sh
pipenv shell
```
5. After activating your python virtual environment, do this if you wish to run the python notebook. 
```sh
jupyter notebook
```
6. After activating your python virtual environment, do this if you wish to test out the whole project. 
   - In your terminal, type: `docker-compose up --build`
   - Note that it takes some time for the dockerised process to be well-built. 
   - Once it's done, copy this to your browser to have a look on **streamlit interface**: `http://0.0.0.0:8501`, you can consider to navigate between pages and key in user inputs for any content generation. 
   - We would also like to have a look on the interactions with database, we can open the Docker Destop app, switch to the container `dsa4213-project-postgres-1` ***exec*** panel. In the ***exec*** panel of the psql container, type accordingly: 
     - switch yourself to psql shell: `psql -U myuser -d mydatabase` --> The step succeeds if your prompt shows: `mydatabase=#`
     - check database information: `mydatabase=# \conninfo`
     - check relations status: `mydatabase=# \d` --> We should see 3 relations, Users, Slides and Temps here
     - to check each relation: `mydatabase=# SELECT * FROM <RELATION>;`
     - you may consider to perform some SQL here by using some `WHERE` clause to check out if things work successfully. 
7. To deactivate python pipenv environment:
```sh
exit
```
8. Wish you a happy exploring! 🎉🎉🎉
9. We treasure and welcome any discussion and suggestion for future development of this project. 

## Limitations and Potential Deployment
- expand our search engines from only arxiv and wikipedia to other possibilities, ie google-search
- collect more user query for configurations to refine our model training procedures, including: 
  - font and color preferences
  - slides length 
  - images to be added onto the slides
- By default, we only allow registered people to generate slides and so, we can store the slides correspondingly to the timestamp and the users id. However, we also notice the potential to allow slides generation from both registered and non-registered people, whose slides will be generated and stored in database if the users are from the former group, and whose slides will be generated but not stored if they are from the latter group. 