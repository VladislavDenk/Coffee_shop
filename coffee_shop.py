import os
import json
from typing import List

# Список позиций в меню кофейни
DRINKS = "drinks.txt"
FLAVORS = "flavors.txt"
TOPPINGS = "toppings.txt"

print("Добро пожаловать в кофейню Coffee_for_Soul!\n")


def main_menu(orders: List[str]):
    """Главное меню. Получает заказ. Выводит заказ. Сохраняет заказ."""
    while True:
        order = get_order()
        if order == {}:
            print('Вы нажали "X", выполняется выход...')
            return
        print("\nПроверьте ваш заказ:")
        print_order(order)
        confirm = input(
            "\nВсё верно? Нажмите Y для создания заказа или N для выхода: "
        ).lower()
        if confirm == "y":
            orders.append(order)
            print("\nСпасибо за ваш заказ:")
            print_order(order)
        else:
            continue


def menu(
    menu_items: List[str],
    title: str = "Меню Coffee_for_Soul:",
    prompt: str = "Введите номер позиции: ",
) -> str:
    """Принимает и выводит элементы меню под своим номером.

    Params:
        menu_items: список элементов меню
        title: заголовок
        prompt: запрос на ввод значния пользователем

    :return str: индекс элемента меню и позиция меню
    """
    print(title)
    print("-" * (len(title) - 1))
    for index, elem in enumerate(menu_items):
        print(f"{index + 1}: {elem}")

    while True:
        choice = input(prompt)
        if choice != "X" or choice != "x":
            if choice.isdigit() and int(choice) in range(1, (len(menu_items) + 1)):
                answer = menu_items[int(choice) - 1]
                break
            else:
                print(f"Введите номер от 1 до {len(menu_items)}!")
                answer = ""

    return answer


def read_menu(file_name: str):
    """Функция для чтения файлов.

    :params file_name: название файла
    :params_type: str

    :rtype: List[str]
    :return: Список пунктов меню
    """
    with open(file_name, "r", encoding="utf-8") as file:
        temp = file.readlines()
        result = [item.strip() for item in temp]

    return result


def get_order():
    """Получает заказ.

    :rtype: Dict[str, str]
    :return: Значения сделанного заказа
    """
    order = {}
    name = input("\nПожалуйста, введите свое имя: ")
    if name == 'x'.lower():
        return order
    else:
        order["Имя"] = name
    
    print("Привет, {}!\n".format(order["Имя"]))

    print("--------------------")
    order["Напиток"] = menu(read_menu(DRINKS))
    order["Ароматизатор"] = menu(
        read_menu(FLAVORS), "\nВыбирите желаемый вкус:", "Введите номер вкуса: "
    )
    order["Топпинг"] = menu(
        read_menu(TOPPINGS), "\nВыбирите топпинг:", "Введите номер топпинга: "
    )

    return order


def print_order(order):
    """Выводит чек с информацией о сделаном заказе."""
    print("\nВаш заказ {}:".format(order["Имя"]))
    print("-" * 30)
    print("Напиток: {}".format(order["Напиток"]))
    print("Вкус: {}".format(order["Ароматизатор"]))
    print("Топпинг: {}".format(order["Топпинг"]))
    print("-" * 30)


def save_orders(orders, file_name):
    """Запись заказов в файл формата json.

    Args:
        orders (List[str, str]): заказы
        file_name (str): название файла
    """
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(orders, file, indent=4)
        return


def load_orders(file_name: str):
    """Проверка существования файла и его прочтение, иначе создание пустого списка.

    Args:
        file_name (str): имя файла

    Returns:
        list: список заказов
    """
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            orders = json.load(file)
            return orders
    else:
        orders = []
        return orders


orders = load_orders('orders.json')
main_menu(orders)
save_orders(orders, 'orders.json')