#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 9
# С использованием многопоточности для заданного значения x найти сумму ряда S
# с точностью члена ряда по абсолютному значению e=10^-7 и произвести
# сравнение полученной суммы с контрольным значением функции y для двух
# бесконечных рядов.
# Варианты 16 и 17

import math
from threading import Thread, Lock

epsilon = 1e-7
lock = Lock()


def func(x, result):
    sum = 0
    n = 0
    term = 1
    factor = 1
    x_pow_n = 1
    while abs(term) > epsilon:
        sum += term
        n += 1
        factor *= n
        x_pow_n *= x ** 2
        term = (-1)**n * x_pow_n / factor
    with lock:
        result.append(sum)


def func2(x, result):
    sum = 0
    n = 1
    x_pow_n = (x - 1) / (x + 1)
    x_term = x_pow_n
    while True:
        term = 1 / (2 * n - 1) * x_pow_n
        x_pow_n *= x_term**2
        if abs(term) < epsilon:
            break
        else:
            sum += term
            n += 1
    with lock:
        result.append(sum)


def main():
    result1 = []
    result2 = []

    thread1 = Thread(target=func, args=(-0.7, result1))
    thread2 = Thread(target=func2, args=(0.6, result2))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    sum_func = result1[0]
    sum_func2 = result2[0]

    test1 = math.exp(-(-0.7)**2)
    test2 = 1/2 * math.log(0.6)

    print(f"Результат функции 1: {sum_func}")
    print(f"Контрольное значение для функции 1: {test1}")
    print(f"Результат функции 2: {sum_func2}")
    print(f"Контрольное значение для функции 2: {test2}")

    if abs(sum_func - test1) < epsilon:
        print("func: Верно.")
    else:
        print("func: Неверно.")

    if abs(sum_func2 - test2) < epsilon:
        print("series_solution: Верно.")
    else:
        print("series_solution: Неверно.")


if __name__ == "__main__":
    main()
