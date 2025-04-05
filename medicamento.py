import pymysql
from db_config import connect_db
from flask import flash, request, Blueprint, jsonify

medicamento_bp = Blueprint("medicamento", __name__)


@medicamento_bp.route("/medicamento")
def medicamento():
    try:
        conn = connect_db()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        nome = request.args.get("nome")

        sql = "SELECT * FROM medicamento";
        parametros = [];

        if nome:
            sql += " WHERE nome LIKE %s";
            parametros.append(f"%{nome}%")

        cursor.execute(sql, parametros)
        rows = cursor.fetchall()

        if len(rows) == 0:
            return (
                jsonify({"message": "Não há medicamento cadastrado!", "success": False}),
                404,
            )

        resp = jsonify(rows)
        resp.status_code = 200

        return resp

    except Exception as e:
        print(e)
        return jsonify({"message": "Erro interno no servidor!", "success": False}), 500
    finally:
        cursor.close()
        conn.close()


@medicamento_bp.route("/medicamento/<id>")
def medicamentobyid(id):
    try:
        conn = connect_db()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM medicamento where idmedicamento = %s", (id))
        rows = cursor.fetchall()
        if len(rows) == 0:
            return jsonify({"message": "Medicamento não encontrado!", "success": False}), 404
        resp = jsonify(rows[0])
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
        return jsonify({"message": "Erro interno no servidor!", "success": False}), 500
    finally:
        cursor.close()
        conn.close()


@medicamento_bp.route("/medicamento", methods=["POST"])
def medicamentonovo():
    try:
        conn = connect_db()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        medicamento = request.json
        nome = medicamento["nome"]
        quantidade = medicamento["quantidade"]
        tipo = medicamento["tipo"]
        fabricante = medicamento["fabricante"]
        cursor.execute(
            "INSERT INTO medicamento (nome, quantidade, tipo, fabricante) VALUES (%s, %s, %s, %s)",
            (nome, quantidade, tipo, fabricante),
        )
        conn.commit()
        resp = jsonify({"message": "Medicamento inserido com sucesso!", "success": True})
        resp.status_code = 200
        return resp
    except Exception as e:
        return jsonify({"message": "Erro interno no servidor!", "success": False}), 500
    finally:
        cursor.close()
        conn.close()


@medicamento_bp.route("/medicamento/<id>", methods=["PUT"])
def medicamentoatualizar(id):
    try:
        conn = connect_db()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("SELECT idmedicamento FROM medicamento WHERE idmedicamento = %s", (id,))
        medicamento_existente = cursor.fetchone()

        if not medicamento_existente:
            return jsonify({"message": "Medicamento não encontrado!", "success": False}), 404

        medicamento = request.json
        nome = medicamento["nome"]
        quantidade = medicamento["quantidade"]
        tipo = medicamento["tipo"]
        fabricante = medicamento["fabricante"]
        cursor.execute(
            "UPDATE medicamento SET nome = %s, quantidade = %s, tipo = %s, fabricante = %s WHERE idmedicamento = %s",
            (nome, quantidade, tipo, fabricante, id),
        )
        conn.commit()
        resp = jsonify({"message": "Medicamento alterado com sucesso!", "success": True})
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
        return jsonify({"message": "Erro interno no servidor!", "success": False}), 500
    finally:
        cursor.close()
        conn.close()


@medicamento_bp.route("/medicamento/<id>", methods=["DELETE"])
def medicamentodeletar(id):
    try:
        conn = connect_db()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT idmedicamento FROM medicamento WHERE idmedicamento = %s", (id,))
        medicamento_existente = cursor.fetchone()

        if not medicamento_existente:
            return jsonify({"message": "Medicamento não encontrado", "success": False}), 404

        cursor.execute("DELETE FROM medicamento WHERE idmedicamento = %s", (id))
        conn.commit()
        resp = jsonify({"message": "Medicamento excluído com sucesso!", "success": True})
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
        return jsonify({"message": "Erro interno no servidor!", "success": False}), 500
    finally:
        cursor.close()
        conn.close()
