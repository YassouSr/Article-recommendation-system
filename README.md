# Article-recommendation-system

This project aims to build a scientific article recommendation system using citation network.

## Data used for v1.0

The data is download from [here](https://www.aminer.org/citation). Then we've applied some preprocessing techniques and upload it to postgresql.

To be able to load the data to postgresql, install spark on your machine and execute ```convert.py``` script and the queries listed in ```query_sql.txt```.

After storing the data to postgresql, you must also load binary data (*.pkl files) from [here](https://www.kaggle.com/code/yassou432/recommendation-system-part-2-2/data) into recommendation/bin folder.

## Data used for v2.0

The data is download from [here](https://github.com/SJ-palpa/curation_projet). Then we've applied some preprocessing techniques and upload it to postgresql.

Run ```convert.py``` script to load the data to postgresql, then load binary files from [here](https://www.kaggle.com/code/yassou432/random-data-for-recommendation-system-part-02/data).

## Running the web application

After setting up the database and necessary files. Execute the following commands to run the web application :

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
