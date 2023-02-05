import src.database as db
from flask import Flask, request, jsonify
import logging.config
from src.bean import Bean

# Logging configuration
logging.config.fileConfig(fname='config/file.conf')
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/status", methods=["GET"])
def health_check():
    logger.debug("health_check")
    return jsonify("STATUS UP!"), 200


@app.route("/beans", methods=["GET"])
def get_all_beans():
    logger.debug("get_all_beans")
    connection = db.connect()
    cursor = db.get_all_beans(connection)
    connection.close()
    if cursor is not None:
        beans = []
        for row in cursor:
            bean = Bean(row[0], row[1], row[2], row[3])
            beans.append(bean.serialize())
        return {"beans": beans}, 200
    else:
        return {"beans": []}, 200


@app.route("/beans", methods=["DELETE"])
def delete_all_beans():
    logger.debug("delete_all_beans")
    connection = db.connect()
    db.delete_all_beans(connection)
    connection.commit()
    connection.close()
    return {"beans": []}, 200


@app.route("/bean/<int:bean_id>", methods=["GET"])
def get_bean(bean_id):
    logger.debug("get_bean {}".format(bean_id))
    connection = db.connect()
    cursor = db.get_beans_by_id(connection, bean_id)
    connection.close()

    if cursor is not None:
        bean = Bean(cursor[0], cursor[1], cursor[2], cursor[3])
        return bean.serialize(), 200
    else:
        bean = Bean(None, None, None, None)
        return bean.serialize(), 404


@api.route('/bean/<id>', endpoint='get_bean')
@api.doc(params={'id': 'An ID'})
@app.route("/bean/<int:bean_id>", methods=["PUT"])
def update_bean(bean_id):
    logger.debug("update_bean {}".format(bean_id))
    params = request.get_json()
    new_name = params["name"]
    new_method = params["method"]
    new_rating = params["rating"]

    connection = db.connect()
    db.update_bean(connection, bean_id, new_name, new_method, new_rating)
    connection.commit()
    connection.close()

    bean = Bean(bean_id, new_name, new_method, new_rating)
    return bean.serialize(), 200


@app.route("/bean/<int:bean_id>", methods=["DELETE"])
def delete_bean(bean_id):
    logger.debug("delete_bean {}".format(bean_id))
    connection = db.connect()
    db.delete_beans_by_id(connection, bean_id)
    connection.commit()
    connection.close()
    bean = Bean(None, None, None, None)
    return bean.serialize(), 200


@app.route("/bean", methods=["POST"])
def create_bean():
    logger.debug("create_bean")
    params = request.get_json()
    new_name = params["name"]
    new_method = params["method"]
    new_rating = params["rating"]

    connection = db.connect()
    cursor = db.add_bean(connection, new_name, new_method, new_rating)
    bean_id = cursor.lastrowid
    connection.commit()
    connection.close()

    bean = Bean(bean_id, new_name, new_method, new_rating)
    return bean.serialize(), 201


if __name__ == "__main__":
    logger.debug("Application running")
    db.create_db()
    app.run(debug=True, host="0.0.0.0", port="5000")
