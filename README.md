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
- [x] user queries refinement and keyword generation through Mixtral-v0.1 LLM
- [x] dataset scrapping and data collections with user specific demands
- [x] generating slides headings, contents and design layout 
- [x] exporting the slides in .pptx form, enabling download and future slides information retrieval
- [x] database interactions for slides and users details via PostgreSQL
- [x] cleaning filepaths and caches to guarantee application deployment

We also offer our readers a flavour to exploring around our jupyter notebook for a backend model demonstration purpose. 

### Step-by-Step Manual Guide
1. Cloning GitHub repository. 
```sh
git clone https://github.com/HY-sTeam/DSA4213-Project
cd </path/to/the/cloned/github/directory>
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
5. Do this if you wish to run the python notebook after activating your python virtual environment. 
```sh
jupyter notebook
```
6. Do this if you wish to run separate `streamlit.py` after activating your python virtual environment and `docker-compose up --build`. 
However, it prolly won't work, with most of the time redirecting you to port 8502 but showing *OperationalError* (app.py) or *ModuleNotFoundError* (pages/streamlit.py) in your browser because the filepath during importing only focusing on Docker environment, instead of individual testing purpose. 
Sometimes, it ***might*** shows *port not responding in your terminal* because the Docker is using streamlit at the same time. 
We will put the idea here on how to run separate `streamlit.py` as an inspiration for people's interest. 


```sh
# <VS Code toolbar >> Terminal >> New Terminal>
pipenv install
pipenv shell
cd </path/of/directory/streamlit.py>
streamlit run <streamlit.py>
# Ctrl + C (Mac OS) to quit
```
7. After activating your python virtual environment, do this if you wish to test out the whole project. 
   - In your terminal, type: `docker-compose up --build`
   - Note that it takes some time for the dockerised process to be well-built. 
   - Once it's done, copy this to your browser to have a look on **streamlit interface**: `http://0.0.0.0:8501`, you can consider to navigate between pages and key in user inputs for any content generation. 
   - We would also like to have a look on the interactions with **psql database**, we can open the Docker Destop app, switch to the container `dsa4213-project-postgres-1` ***exec*** panel. In the ***exec*** panel of the psql container, type accordingly: 
     - switch yourself to psql shell: `psql -U myuser -d mydatabase` --> The step succeeds if your prompt shows: `mydatabase=#`
     - check database information: `mydatabase=# \conninfo`
     - check relations status: `mydatabase=# \d` --> We should see 3 relations, Users, Slides and Temps here
     - to check each relation: `mydatabase=# SELECT * FROM <RELATION>;`
     - you may consider to perform some SQL here by using some `WHERE` clause to check out if things work successfully. 
   - On your keyboard, press Ctrl+C to quit (Mac OS environment) if you wish to do so. 
8. To deactivate python pipenv environment:
```sh
exit
```
1. Wish you a happy exploring! 🎉🎉🎉
2.   We treasure and welcome any discussion and suggestion for future development of this project. 

<!-- ### Highlights
<table>
	<tr>
		<th width="50%">
			<p><a title="show-whitespace"></a> Makes whitespace characters visible
			<p><img src="https://user-images.githubusercontent.com/1402241/61187598-f9118380-a6a5-11e9-985a-990a7f798805.png">
		<th width="50%">
			<p><a title="resolve-conflicts"></a> Adds one-click merge conflict fixers
			<p><img src="https://user-images.githubusercontent.com/1402241/54978791-45906080-4fdc-11e9-8fe1-45374f8ff636.png">
	<tr>
		<th width="50%">
			<p><a title="pr-base-commit"></a> Shows how far behind a PR head branch is + tells you its base commit
			<p><img src="https://user-images.githubusercontent.com/1402241/234492651-b54bf9ba-c218-4a30-bed4-f85a7f037297.png">
		<th width="50%">
			<p><a title="conversation-activity-filter"></a> Lets you hide every event except comments or unresolved comments in issues and PRs
			<p><img src="https://github-production-user-asset-6210df.s3.amazonaws.com/83146190/252116522-053bce84-5c55-477b-8cc2-42a48104fb02.png">
	<tr>
		<th width="50%">
			<p><a title="status-subscription"></a> Lets you subscribe to opening/closing events of issues in one click
			<p><img src="https://github-production-user-asset-6210df.s3.amazonaws.com/1402241/238186901-cbc98b51-d173-40c6-b21e-5f0bae3d800c.png">
		<th width="50%">
			<p><a title="default-branch-button"></a> Adds a link to the default branch on directory listings and files
			<p><img src="https://github-production-user-asset-6210df.s3.amazonaws.com/83146190/252176294-9130783c-51aa-4df9-9c35-9b87c179199a.png">
	<tr>
		<th width="50%">
			<p><a title="restore-file"></a> Adds a button to discard all the changes to a file in a PR
			<p><img src="https://user-images.githubusercontent.com/1402241/236630610-e11a64f6-5e70-4353-89b8-39aae830dd16.gif">
		<th width="50%">
			<p><a title="select-notifications"></a> Select notifications by type and status
			<p><img src="https://user-images.githubusercontent.com/83146190/252175851-e0826d3b-1990-4bff-ba09-71892463818e.gif">
</table> -->

### Limitations and Potential Deployment
- expand our search engines from only arxiv and wikipedia to other possibilities, ie google-search
- collect more user query for configurations to refine our model training procedures, including: 
  - font and color preferences
  - slides length 
  - images to be added onto the slides
- By default, we only allow registered people to generate slides and so, we can store the slides correspondingly to the timestamp and the users id. However, we also notice the potential to allow slides generation from both registered and non-registered people, whose slides will be generated and stored in database if the users are from the former group, and whose slides will be generated but not stored if they are from the latter group. 