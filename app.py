import os
import json
import sqlite3
from typing import List
from flask import Flask, render_template, request


def save_order(order):
    """Запись заказов в базу данных."""
    con = sqlite3.connect('orders.db')
    cur = con.cursor()
    cur.execute(
        "INSERT INTO orders(name,drink,flavor,topping) VALUES(?,?,?,?);",
        (order["name"], order['drink'], order['flavor'], order['topping']),
    )
    con.commit()
    return


def get_orders():
    con = sqlite3.connect('orders.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM orders;")
    rows = cur.fetchall()

    return rows


def read_menu(file_name: str) -> List[str]:
    """Функция для чтения пунктов меню из файла.

    :param file_name: название файла
    :params_type: str

    :rtype: List[str]
    :return: Список пунктов меню
    """
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            result = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f'Ошибка: файл "{file_name}" не был найден.')
        result = []
    except PermissionError:
        print(f'Ошибка: У вас нет разрешения на чтение файла "{file_name}".')
        result = []
    except Exception as e:
        print(f'произошла непредвиденная ошибка: {e}')
        result = []

    return result


drinks = read_menu("drinks.txt")
flavors = read_menu("flavors.txt")
toppings = read_menu("toppings.txt")

con = sqlite3.connect('orders.db')
cur = con.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS orders(name, drink, flavor, topping);')


app = Flask(__name__)

@app.route("/index", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/order", methods=("GET", "POST"))
def order():
    if request.method == "POST":
        new_order = {
            "name": request.form["name"],
            "drink": request.form["drink"],
            "flavor": request.form["flavor"],
            "topping": request.form["topping"],
        }
        save_order(new_order)
        return render_template("print.html", new_order=new_order)

    return render_template(
        "order.html", drinks=drinks, flavors=flavors, toppings=toppings
    )

@app.route('/list', methods=['GET'])
def list():
    orders = get_orders()

    return render_template('list.html', orders=orders)


if __name__ == "__main__":
    app.run(debug=True)
