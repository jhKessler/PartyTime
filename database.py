from pony import orm

db = orm.Database()
db.bind(provider='postgres', user="partytime", host="localhost", database="partytime")

class History(db.Entity):
    """Database Object for saving the Prediction History"""
    date = orm.PrimaryKey(str)
    data = orm.Required(orm.Json)

db.generate_mapping(create_tables=True)

def save_history(data_dict: dict):
    """Saves history data to Database"""
    date = data_dict["last_data_update"]
    del data_dict["last_data_update"]
    with orm.db_session:
        sql_qry = f"select count(1) from History where date = $date;"
        if db.select(sql_qry)[0] == 0:
            History(date=date, data=data_dict)