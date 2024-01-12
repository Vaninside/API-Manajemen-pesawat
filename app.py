from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)


def db_connection():
    conn = None
    try:
        conn = pymysql.connect(
            host="sql.freedb.tech",
            database="freedb_evanpemfung",
            user="freedb_epanpemfung",
            password="5mn2zwseXY!R4e5",
            port=3306,
            cursorclass=pymysql.cursors.DictCursor,
        )
    except pymysql.Error as e:
        print(e)
    return conn


@app.route("/pesawat", methods=["GET", "POST", "PUT", "DELETE"])
def manage_pesawat():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor.execute("SELECT * FROM data_pesawat")
        pesawat = [
            dict(
                id=row["id"],
                nama_pesawat=row["nama_pesawat"],
                tipe_pesawat=row["tipe_pesawat"],
                tipe_mesin=row["tipe_mesin"],
                max_speed=row["max_speed"],
                harga=row["harga"],
            )
            for row in cursor.fetchall()
        ]
        if pesawat is not None:
            return jsonify(pesawat)

    if request.method == "POST":
        add_nama_pesawat = request.form["nama_pesawat"]
        add_tipe_pesawat = request.form["tipe_pesawat"]
        add_tipe_mesin = request.form["tipe_mesin"]
        add_max_speed = request.form["max_speed"]
        add_harga = request.form["harga"]

        query_insert = """
            INSERT INTO data_pesawat (nama_pesawat, tipe_pesawat, tipe_mesin, max_speed, harga)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            query_insert,
            (
                add_nama_pesawat,
                add_tipe_pesawat,
                add_tipe_mesin,
                add_max_speed,
                add_harga,
            ),
        )
        conn.commit()
        return "Berhasil Menambahkan Data Pesawat."

    if request.method == "PUT":
        update_id = request.form["id"]
        update_nama_pesawat = request.form["nama_pesawat"]
        update_tipe_pesawat = request.form["tipe_pesawat"]
        update_tipe_mesin = request.form["tipe_mesin"]
        update_max_speed = request.form["max_speed"]
        update_harga = request.form["harga"]

        query_update = """
            UPDATE data_pesawat
            SET nama_pesawat=%s, tipe_pesawat=%s, tipe_mesin=%s, max_speed=%s, harga=%s
            WHERE id=%s
        """

        cursor.execute(
            query_update,
            (
                update_nama_pesawat,
                update_tipe_pesawat,
                update_tipe_mesin,
                update_max_speed,
                update_harga,
                update_id,
            ),
        )
        conn.commit()
        return "Berhasil Memperbarui Data Pesawat."

    if request.method == "DELETE":
        delete_id = request.form["id"]

        query_delete = """DELETE FROM data_pesawat WHERE id=%s"""

        cursor.execute(query_delete, (delete_id,))
        conn.commit()
        return "Berhasil Menghapus Data Pesawat."


if __name__ == "__main__":
    app.run(debug=True, port=8000, use_reloader=True)
