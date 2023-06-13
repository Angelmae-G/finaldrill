from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "Angel"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "209820982098"
app.config["MYSQL_DB"] = "`angel_accomodation_longterm`"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data


@app.route("/guests", methods=["GET"])
def guest_id():
    data = data_fetch("""select * from guests""")
    return make_response(jsonify(data), 200)


@app.route("/guests/<int:angel>", methods=["GET"])
def guest_id_by_angel(angel):
    data = data_fetch("""SELECT * FROM guests where guest_id = {}""".format(angel))
    return make_response(jsonify(data), 200)


@app.route("/guests/<int:angel>/full_name", methods=["GET"])
def guest_id(id):
    data = data_fetch(
        """
        SELECT full_name, guests_id 
        FROM angel_accomodation_longterm.guests 
        INNER JOIN guests at unit_type_code
        ON guests = guests at unit_type_code
        INNER JOIN guests
        ON unit_type_code details = guests at full_name
        WHERE guest_id = {}
    """.format(
            id
        )
    )
    return make_response(
        jsonify({"guests_id": id, "count": len(data), "unit_type_code": data}), 3
    )


@app.route("/guests", methods=["POST"])
def add_guests():
    cur = mysql.connection.cursor()
    info = request.get_json()
    full_name = info["full name"]
    cur.execute(
        """ INSERT INTO guests]] (full_name) VALUE (%s)""",
        (full_name)
    )
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "guests added successfully", "rows_affected": rows_affected}
        ),
        3,
    )


@app.route("/guests/<int:id>", methods=["PUT"])
def update_guests(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    full_name = info["full name"]
    cur.execute(
        """ UPDATE authors SET full_name = %s WHERE idguests = %s """,
        (fullname, id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "guests updated successfully", "rows_affected": rows_affected}
        ),
        3,
    )


@app.route("/guests by angel/<int:id>", methods=["DELETE"])
def delete_guests(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM guests by angel where guests id= %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "guests by angel deleted successfully", "rows_affected": rows_affected}
        ),
        3,
    )

@app.route("/guests/format", methods=["GET"])
def guests_id():
    fmt = request.args.get('guest_id')
    foo = request.args.get('gender')
    return make_response(jsonify({"format":fmt, "foo":foo}),3)

if __name__ == "__main__":
    app.run(debug=True)
