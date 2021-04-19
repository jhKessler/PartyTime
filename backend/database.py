from pony import orm
import os

database_host = 'localhost' if not 'database_host' in os.environ else os.environ['database_host']

db = orm.Database()
db.bind(provider='postgres', user="partytime", host=database_host, database="partytime")

class History(db.Entity):
    """Database Object for saving the Prediction History"""
    date = orm.PrimaryKey(str)
    data = orm.Required(orm.Json)

db.generate_mapping(create_tables=True)

def save_history(date: str, data_dict: dict):
    """Saves history data to Database"""
    with orm.db_session:
        sql_qry = f"select count(1) from History where date = $date;"
        if db.select(sql_qry)[0] == 0:
            History(date=date, data=data_dict)
