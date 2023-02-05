import sqlite3

CREATE_BEANS_TABLE = """CREATE TABLE IF NOT EXISTS \
                        beans (id INTEGER PRIMARY KEY, name TEXT, method TEXT, rating INTEGER);"""
INSERT_BEAN = "INSERT INTO beans (name,method,rating) VALUES (?,?,?);"
UPDATE_BEAN = "UPDATE beans SET name=?, method=?,rating=? WHERE  id=?;"
DELETE_BEAN = "DELETE FROM beans WHERE  id=?;"
DELETE_ALL_BEANS = "DELETE FROM beans;"
GET_ALL_BEANS = "SELECT * FROM beans;"
GET_BEANS_BY_NAME = "SELECT * FROM beans WHERE name = ?;"
GET_BEANS_BY_ID = "SELECT * FROM beans WHERE id = ?;"
GET_BEST_PREPARATION_FOR_BEAN = """SELECT * FROM beans WHERE name = ? 
                                    ORDER BY rating DESC LIMIT 1;"""


def create_db():
    connection = connect();
    create_tables(connection)
    connection.close()


def connect():
    return sqlite3.connect("src/beans.db")


def create_tables(connection):
    with connection:
        connection.execute(CREATE_BEANS_TABLE)


def add_bean(connection, name, method, rating):
    with connection:
        return connection.execute(INSERT_BEAN, (name, method, rating))


def update_bean(connection, bean_id, name, method, rating):
    with connection:
        return connection.execute(UPDATE_BEAN, (name, method, rating,bean_id))


def get_all_beans(connection):
    with connection:
        return connection.execute(GET_ALL_BEANS).fetchall()


def get_beans_by_name(connection, name):
    with connection:
        return connection.execute(GET_BEANS_BY_NAME, (name,)).fetchall()


def get_beans_by_id(connection, bean_id):
    with connection:
        return connection.execute(GET_BEANS_BY_ID, (bean_id,)).fetchone()


def get_best_preparation_for_bean(connection):
    with connection:
        return connection.execute(GET_BEST_PREPARATION_FOR_BEAN).fetchone()


def delete_all_beans(connection):
    with connection:
        connection.execute(DELETE_ALL_BEANS)


def delete_beans_by_id(connection, bean_id):
    with connection:
        return connection.execute(DELETE_BEAN, (bean_id,))
