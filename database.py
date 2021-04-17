from pony import orm

db = orm.Database()
db.bind(provider='postgres', user="partytime", host="localhost", database="partytime")

class History(db.Entity):
    """Database Object for saving the Prediction History"""
    date = orm.PrimaryKey(str)
    week_nrs = orm.Required(orm.StrArray)
    history = orm.Required(orm.IntArray)

db.generate_mapping(create_tables=True)

def save_history(date: str, week_arr: list, data_arr: list):
    """Saves history data to Database"""
    with orm.db_session:
        sql_qry = f"select count(1) from History where date = $date;"
        if db.select(sql_qry)[0] == 0:
            History(date=date, week_nrs=week_arr, history=data_arr)