from tinydb import TinyDB, Query


class Manager:
    db = TinyDB('./data/tournaments/data.json')
    query = Query()
