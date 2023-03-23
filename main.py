from fastapi import FastAPI
import pandas as pd 
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker 
from item import SampleData
app = FastAPI()



@app.post("/upload")
async def file_upload(sample_data: SampleData):
    """
        POST endpoint that collects data from the frontend 
        and persists to the Database
    """
    dict_data = dict(sample_data)
    data_frame = pd.DataFrame.from_dict(dict_data)
    try:
        engine = create_engine('sqlite:///./app.db')
        session = sessionmaker(bind=engine)
        with session() as session:
            data_frame.to_sql('data', con=engine, if_exists='append', index = False)
    except Exception as e:
        print(e)

@app.get("/fetch_data/")
async def fetch_data(id:int):
    """
        GET end point that pulls the data from the Database for the
        requested id, and populates a scatter plot.
    """
    try:
        engine = create_engine('sqlite:///./app.db')
        with engine.connect() as con:
            data = con.execute(text(f'select x,y from data where id = {id}')).fetchall()
            df = pd.DataFrame(data, columns=['X', 'Y'])
            # Has to be done in the frontend
            df.plot.scatter('X', 'Y', s = 100)
    except Exception as e:
        print(e)

