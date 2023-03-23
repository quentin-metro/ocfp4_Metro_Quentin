from tinydb import TinyDB, Query


class Manager:
    db = TinyDB('./data/data.json')
    query = Query()
