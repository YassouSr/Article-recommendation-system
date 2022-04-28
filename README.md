# Article-recommendation-system

This project aims to build a scientific article recommendation system using citation network.

## Data used for v1.0

The data is download from [here](https://www.kaggle.com/datasets/kmader/aminer-academic-citation-dataset). Then we've applied some preprocessing techniques and upload it to postgresql.

To be able to load the data to postgresql, install spark on your machine and execute ```convert.py``` script. In addition add "admin" table with the following script :

```sql
create table admin(
  id serial primary key,
  username character varying(20) NOT NULL,
  email character varying(120) NOT NULL,
  password character varying(60) NOT NULL
)
```

After storing the data to postgresql, you must also load binary data (*.pkl files) from [here](https://www.kaggle.com/code/yassou432/recommendation-system-part-2-2/data) itno recommendation/bin folder.

## Data used for v2.0

The data is download from [here](https://github.com/SJ-palpa/curation_projet). Then we've applied some preprocessing techniques and upload it to postgresql.

Run ```convert.py``` script to load the data to postgresql, then load binary files from [here].

## Running the web application

After setting up the database (articles and admin tables) and necessary files To run the web application, apply the following steps :

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
