# Welcome to Developers Manual Guide
> We have collected and listed here for all potential errors we have encountered. Hope helps. Happy exploring ~

## Working Environments
Our working environment is basically Python, Python streamlit, PostgreSQL and Docker. 

## Streamlit Testing Purpose
Besides the manual guide from the main `README.md`, we also wish you to have a better experience in testing and debugging, so we're here to provide you some manual guide in streamlit testings. 

## Backend Model Logic Testing
As mentioned aforehand, if you wish to have a quick glance of the logic underlied in the project, you may use the IPython notebook `SlidesGenerator.ipynb`. 

Since most of our functions from pages require interactions with database, failing to create a Docker psql container beforehand may fail you from performing any testing. You can refer to our `psql.Dockerfile` and `db_scripts/DDL.sql` to construct your dockerised database. Please note that we're not able to provide any psql container here for testing purpose because it's highly possibly to collapse our system and spoil our project application, which may not meet our intention. 

Apologies for any inconvenience here! Cheers ~

### Interactive Python Notebook `SlidesGenerator.ipynb`
- If you haven't activated python environment, do this. It might take you some times: 
```sh
pipenv install --dev
pipenv shell
jupyter notebook
```
- If you have activated python environment, do the above code without `pipenv install`

### Python Script `.py`
- If you haven't activated python environment, do this. It might take you some times:
```sh
# <VS Code toolbar >> Terminal >> New Terminal>
pipenv install --dev
pipenv shell
cd </path/of/directory/streamlit.py>
pipenv run <src.py or page.py>
pipenv streamlit run <page.py> # streamlit run <streamlit.py>
# Ctrl + C (Mac OS) to quit
```
- **Remark**:  If you're done with that, proceed to do `pipenv run <page.py>` or `streamlit run <page.py>` to see the effect. 

## Docker Testing
As mentioned in the main `README.md`. Also, you would have to consider to clean your Docker environment by removing containers, images, volumes and caches relevant to this project to avoid system collapse. 

## Errors
- You may potentially encounter several errors upon testing. if you didn't do your own psql container but wish to test separate `.py`. Being redirected to port 8502, the webpage shows: 
1. *OperationalError* (app.py) because the psql port is not listening to the streamlit 
2. *ModuleNotFoundError* (pages/streamlit.py) because the imported filepath at the head of `.py` focusing only to Docker environment. 
3. *port not responding in your terminal* because the Docker is using streamlit at the same time. 
- 