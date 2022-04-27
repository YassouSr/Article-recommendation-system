# Article-recommendation-system

This project aims to build a scientific article recommendation system using citation network.

The data is download from [here](https://www.kaggle.com/datasets/kmader/aminer-academic-citation-dataset). Then we've applied some preprocessing techniques and upload it to postgresql.

To be able to load the data to postgresql, install spark on your machine and execute ```convert.py``` script.

To run the web application, apply the following steps :

- Create new python environment:

  ```cmd
  cd Article-recommendation-system
  python -m venv env
  ```

- Activate the environment:

  ```cmd
  .\env\Scripts\activate
  ```

- Install the required packages (if not already installed):
  
  ```cmd
  pip install -r requirements.txt
  ```

- To run the app:

  ```cmd
  python execute.py
  ```
