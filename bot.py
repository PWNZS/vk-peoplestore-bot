#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from json import load
from random import choice, randint, uniform
from threading import Thread
from time import sleep, strftime

from requests import get


def buy_slave(id):
    """Покупает раба."""
    get(
        f"https://peostore.mydzin.ru/api/buySlave?slave_id={id}",
        headers=headers,
        params={"slave_id": id},
    )


def get_buy_slave(id):
    """Покупает раба."""
    return get(
        f"https://peostore.mydzin.ru/api/buySlave?slave_id={id}",
        headers=headers,
        params={"slave_id": id},
    ).json()


def buy_fetter(id):
    """Покупает оковы."""
    get(
        f"https://peostore.mydzin.ru/api/fetterSlave?slave_id={id}",
        headers=headers,
        params={"slave_id": id},
    )


def sell_slave(id):
    """Продаёт раба."""
    get(
        f"https://peostore.mydzin.ru/api/sellSlave?slave_id={id}",
        headers=headers,
        params={"slave_id": id},
    )


def job_slave(id):
    """Даёт работу."""
    chosen_job = choice(job)
    get(
        f"https://peostore.mydzin.ru/api/jobSlave?slave_id={id}&job_name={chosen_job}",
        headers=headers,
        params={
            "slave_id": id,
            "job_name": chosen_job,
        },
    )


def get_user(id):
    """Получает информацие о пользователе."""
    return get(
        f"https://peostore.mydzin.ru/api/user?id={id}",
        headers=headers,
    ).json()


def get_top_users():
    """Возвращает список топ игроков."""
    return get(
        "https://peostore.mydzin.ru/api/getTopUsers",
        headers=headers,
    ).json()


def get_start():
    """Получает полную информацию о своём профиле."""
    return get(
        "https://peostore.mydzin.ru/api/start?id=0",
        headers=headers,
    ).json()


def upgrade_slave(slave_id):
    """Прокачивает раба, чтобы он приносил 1000 в минуту."""
    # Получение информации о себе
    me = get_user(my_id)

    # Проверка на то, дал ли нормальный сервер нормальный ответ
    if "payload" in me.keys():
        me = me["payload"]["user"]
        # Проверка на то, хватит ли баланса для прокачки
        if me["balance"] >= 39214:
            try:
                slave_info = get_user(slave_id)
                if "payload" in slave_info.keys():
                    slave_info = slave_info["payload"]["user"]
                    if slave_info["fetter_to"] == 0:
                        while slave_info["price"] <= 26151:
                            sell_slave(slave_id)
                            print(f"Продал id{slave_id} для улучшения")
                            buy_slave(slave_id)
                            print(f"Улучшил id{slave_id}")
                            sleep(uniform(min_delay, max_delay))
                            slave_info = get_user(slave_id)["payload"]["user"]
            except Exception as e:
                print(e.args)
                sleep(uniform(min_delay, max_delay))
                pass


def upgrade_slaves():
    """Прокачивает рабов, чтобы они приносили 1000 в минуту."""
    while True:
        try:
            start = get_start()
            if "payload" in start.keys():
                start = start["payload"]
                # Перебор списка рабов
                for slave in start["slaves"]:
                    # me = get_user(my_id)
                    if "balance" in start.keys():
                        balance = start["user"]["balance"]
                        if balance >= 39214:
                            slave_info = get_user(slave["id"])
                            if "payload" in slave_info.keys():
                                slave_info = slave_info["payload"]["user"]
                                if slave_info["fetter_to"] == 0:
                                    while slave_info["price"] <= 26151:
                                        sell_slave(slave["id"])
                                        print(
                                            f"Продал id{slave['id']} для улучшения"
                                        )
                                        buy_slave(slave["id"])
                                        print(f"Улучшил id{slave['id']}")
                                        sleep(uniform(min_delay, max_delay))
                                        slave_info = get_user(slave["id"])[
                                            "payload"
                                        ]["user"]
                                        balance = get_user(my_id)["payload"][
                                            "user"
                                        ]["balance"]
        except Exception as e:
            print(e.args)
            sleep(uniform(min_delay, max_delay))


def buy_top_users_slaves():
    """То же самое, что и buy_slaves, только перекупает рабов у топ игроков."""
    while True:
        try:
            top_users = get_top_users()
            if "payload" in top_users.keys():
                for top_user in top_users["payload"]:
                    top_user_slaves = get_user(top_user["id"])
                    if "payload" in top_user_slaves.keys():
                        top_user_slaves = top_user_slaves["payload"]
                        for slave in top_user_slaves["slaves"]:
                            if slave["fetter_to"] == 0:
                                slave_id = slave["id"]
                                slave_info = get_user(slave_id)
                                if "payload" in slave_info.keys():
                                    slave_info = slave_info["payload"]["user"]
                                    if (
                                        slave_info["price"] <= max_price
                                        and slave_info["price"] >= min_price
                                    ):
                                        # Покупка раба
                                        profile = get_buy_slave(slave_id)

                                        if "payload" in profile.keys():
                                            profile = profile["payload"][
                                                "user"
                                            ]
                                            print(
                                                f"""\n==[{strftime('%d.%m.%Y %H:%M:%S')}]==
Купил id{slave_info['id']} за {slave_info['price']} у id{top_user['id']}
Баланс: {'{:,}'.format(profile['balance'])}
Рабов: {'{:,}'.format(profile['slaves_count'])}
Доход в минуту: {'{:,}'.format(profile['slaves_profit_per_min'])}\n""",
                                            )

                                            # Прокачивает раба
                                            if conf_upgrade_slaves == 1:
                                                upgrade_slave(slave_id)

                                            # Покупает оковы только что купленному рабу
                                            if buy_fetters == 1:
                                                fetter_price = get_user(
                                                    slave_id
                                                )
                                                if (
                                                    "payload"
                                                    in fetter_price.keys()
                                                ):
                                                    fetter_price = (
                                                        fetter_price[
                                                            "payload"
                                                        ]["fetter_price"]
                                                    )
                                                    if (
                                                        fetter_price
                                                        <= max_fetter_price
                                                    ):
                                                        buy_fetter(slave_id)
                                                        print(
                                                            f"Купил оковы id{slave_id} за {fetter_price}",
                                                        )
                                            sleep(
                                                uniform(min_delay, max_delay)
                                            )
        except Exception as e:
            print(e.args)
            sleep(uniform(min_delay, max_delay))


def buy_slaves():
    """Покупает и улучшает рабов, надевает оковы, если включено в config.json."""
    while True:
        try:
            # Случайный раб в промежутке
            slave_id = randint(1, 648196847)
            slave_info = get_user(slave_id)

            # Проверка раба на соотвествие настройкам цены
            if "payload" in slave_info.keys():
                slave_info = slave_info["payload"]["user"]
                while (
                    slave_info["price"] > max_price
                    or slave_info["price"] < min_price
                ):
                    sleep(uniform(min_delay, max_delay))
                    slave_id = randint(1, 648196847)
                    slave_info = get_user(slave_id)["payload"]["user"]

                if "id" in slave_info.keys():
                    # Покупка раба
                    profile = get_buy_slave(slave_id)
                    if "payload" in profile.keys():
                        profile = profile["payload"]["user"]
                        print(
                            f"""\n==[{strftime('%d.%m.%Y %H:%M:%S')}]==
Купил id{slave_info['id']} за {slave_info['price']}
Баланс: {'{:,}'.format(profile['balance'])}
Рабов: {'{:,}'.format(profile['slaves_count'])}
vk.com/onlyrab - Доход в минуту: {'{:,}'.format(profile['slaves_profit_per_min'])}\n""",
                        )

                        # Прокачивает раба
                        if conf_upgrade_slaves == 1:
                            upgrade_slave(slave_id)

                        # Покупает оковы только что купленному рабу
                        if buy_fetters == 1:
                            fetter_price = get_user(slave_id)
                            if "payload" in fetter_price.keys():
                                fetter_price = fetter_price["payload"][
                                    "fetter_price"
                                ]
                                if fetter_price <= max_fetter_price:
                                    buy_fetter(slave_id)
                                    print(
                                        f"Купил оковы id{slave_id} за {fetter_price}"
                                    )
                        sleep(uniform(min_delay, max_delay))
        except Exception as e:
            print(e.args)
            sleep(uniform(min_delay, max_delay))


def buy_from_ids():
    """То же самое, что и buy_slaves, только перекупает рабов из списка в config.json."""
    while True:
        try:
            for id in buy_from_ids_list:
                slaves = get_user(id)
                if "payload" in slaves.keys():
                    slaves = slaves["payload"]
                    for slave in slaves["slaves"]:
                        if slave["fetter_to"] == 0:
                            slave_id = slave["id"]
                            slave_info = get_user(slave_id)
                            if "payload" in slave_info.keys():
                                slave_info = slave_info["payload"]["user"]
                                if (
                                    slave_info["price"] <= max_price
                                    and slave_info["price"] >= min_price
                                ):

                                    # Покупка раба
                                    profile = get_buy_slave(slave_id)

                                    if "payload" in profile.keys():
                                        profile = profile["payload"]["user"]
                                        print(
                                            f"""\n==[{strftime('%d.%m.%Y %H:%M:%S')}]==
Купил id{slave_info['id']} за {slave_info['price']} у id{id}
Баланс: {'{:,}'.format(profile['balance'])}
Рабов: {'{:,}'.format(profile['slaves_count'])}
vk.com/onlyrab - Доход в минуту: {'{:,}'.format(profile['slaves_profit_per_min'])}\n""",
                                        )

                                        # Прокачивает раба
                                        if conf_upgrade_slaves == 1:
                                            upgrade_slave(slave_id)

                                        # Покупает оковы только что купленному рабу
                                        if buy_fetters == 1:
                                            fetter_price = get_user(slave_id)
                                            if (
                                                "payload"
                                                in fetter_price.keys()
                                            ):
                                                fetter_price = fetter_price[
                                                    "payload"
                                                ]["fetter_price"]
                                                if (
                                                    fetter_price
                                                    <= max_fetter_price
                                                ):
                                                    buy_fetter(slave_id)
                                                    print(
                                                        f"Купил оковы id{slave_id} за {fetter_price}"
                                                    )
                                        sleep(uniform(min_delay, max_delay))
        except Exception as e:
            print(e.args)
            sleep(uniform(min_delay, max_delay))


def buy_fetters():
    """Покупает оковы тем, у кого их нет."""
    while True:
        try:
            start = get_start()
            if "payload" in start.keys():
                slaves = start["payload"]["slaves"]
                # Удаление первого раба из списка,
                # чтобы не происходило коллизии с прокачкой
                if conf_upgrade_slaves == 1:
                    del slaves[0]

                # Перебор списка рабов
                for slave in slaves:
                    # Проверка на наличие оков
                    if slave["fetter_to"] == 0:
                        if slave["fetter_price"] <= max_fetter_price:
                            buy_fetter(slave["id"])
                            print(
                                f"Купил оковы id{slave['id']} за {slave['fetter_price']}"
                            )
                            sleep(uniform(min_delay, max_delay))
        except Exception as e:
            print(e.args)
            sleep(uniform(min_delay, max_delay))


def job_slaves():
    """Даёт безработным работу."""
    while True:
        try:
            start = get_start()
            if "payload" in start.keys():
                slaves = start["payload"]["slaves"]
                if buy_slaves_mode == 0 and conf_buy_fetters == 1:
                    del slaves[0]
                # Перебор списка рабов
                for slave in slaves:
                    # Проверка на наличие у раба работы
                    if slave["job"]["name"] == "":
                        job_slave(slave["id"])
                        print(f"Дал работу id{slave['id']}")
                        sleep(uniform(min_delay, max_delay))
        except Exception as e:
            print(e.args)
            sleep(uniform(min_delay, max_delay))


if __name__ == "__main__":
    print(
        """vk.com/onlyrab""",
    )

    # Конфиг
    with open("config.json") as f:
        try:
            config = load(f)
        except:
            sys.exit("Конфиг настроен некорректно.")
    auth = str((config["authorization"]).strip())
    buy_slaves_mode = int(config["buy_slaves_mode"])
    conf_buy_fetters = int(config["buy_fetters"])
    max_fetter_price = int(config["max_fetter_price"])
    min_delay = int(config["min_delay"])
    max_delay = int(config["max_delay"])
    job = list(config["job"])
    min_price = int(config["min_price"])
    max_price = int(config["max_price"])
    my_id = int(config["my_id"])
    conf_upgrade_slaves = int(config["upgrade_slaves"])
    buy_from_ids_list = list(config["buy_from_ids"])

    headers = {
        "Content-Type": "application/json",
        "Authorization": auth,
        "Origin": "https://prod-app7809644-b3ab086bcdfe.pages-ac.vk-apps.com",
        "Referer": "https://prod-app7809644-b3ab086bcdfe.pages-ac.vk-apps.com/",
        "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.41 Safari/537.36",
    }

    # Запуск
    if buy_slaves_mode == 1:
        print("Включена покупка случайных рабов.")
        Thread(target=buy_slaves).start()
    elif buy_slaves_mode == 2:
        print("Включена перекупка рабов у топеров.")
        Thread(target=buy_top_users_slaves).start()
    elif buy_slaves_mode == 3:
        print("Включена перекупка у ID шников из config.json.")
        Thread(target=buy_from_ids).start()
    if conf_upgrade_slaves == 1 and buy_slaves_mode == 0:
        Thread(target=upgrade_slaves).start()
    if conf_buy_fetters == 1:
        Thread(target=buy_fetters).start()
    Thread(target=job_slaves).start()
