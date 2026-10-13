# Лабораторная работа №1, вариант 5
# Страна: Литва | Узор: e | Функция: y = |x|
# Условие: среднее по модулю чисел, стоящих на чётных и нечётных позициях

import os
import time

# ---------- escape-последовательности ----------
END = '\x1b[0m'              # сбросить цвет
YELLOW = '\x1b[48;5;220m'    # жёлтый фон
GREEN = '\x1b[48;5;29m'      # зелёный фон
RED = '\x1b[48;5;160m'       # красный фон
WHITE = '\x1b[47m'           # белый фон
HIDE_CURSOR = '\x1b[?25l'    # спрятать курсор
SHOW_CURSOR = '\x1b[?25h'    # показать курсор

os.system('')  # включает escape-последовательности в cmd на Windows


def clear():
    """Очистка консоли"""
    os.system('cls' if os.name == 'nt' else 'clear')


def goto(row, col):
    """Последовательность: поставить курсор в строку row, столбец col"""
    return f'\x1b[{row};{col}H'


# ---------- 1. Флаг Литвы ----------
def flag():
    width = 40                       # ширина флага в символах
    for color in (YELLOW, GREEN, RED):   # три горизонтальные полосы
        for _ in range(4):               # высота каждой полосы - 4 строки
            print(color + ' ' * width + END)


# ---------- 2. Узор e ----------
# 'X' - закрашенная клетка, пробел - пустая
MOTIF = [
    'X         X',
    'XX       XX',
    ' XX     XX ',
    '  XXX XXX  ',
    '    XXX    ',
]


def pattern_lines(color):
    """Собирает строки повторяющегося узора: 3 узора в ряд, 2 ряда"""
    lines = []
    for _ in range(2):                    # два ряда узоров
        for row in MOTIF:
            line = ''
            for _ in range(3):            # три узора в одном ряду
                for ch in row:
                    if ch == 'X':
                        line += color + '  ' + END
                    else:
                        line += '  '
                line += '  '              # промежуток между узорами
            lines.append(line)
        lines.append('')                  # пустая строка между рядами
    return lines


def pattern(color=WHITE):
    for line in pattern_lines(color):
        print(line)


# ---------- 3. Анимация из 4 кадров ----------
def animation():
    colors = [YELLOW, GREEN, RED, WHITE]   # 4 кадра - 4 цвета
    print(HIDE_CURSOR, end='')
    for frame in range(4):
        clear()                            # очищаем консоль
        col = 1 + frame * 10               # каждый кадр сдвигаем узор вправо
        row = 3
        for i, line in enumerate(pattern_lines(colors[frame])):
            print(goto(row + i, col) + line)   # ставим курсор и рисуем строку
        time.sleep(0.8)
    print(goto(row + 14, 1) + SHOW_CURSOR)


# ---------- 4. Диаграмма из sequence.txt ----------
def read_numbers(filename='sequence.txt'):
    numbers = []
    file = open(filename, 'r')
    for line in file:
        line = line.strip()
        if line != '':
            numbers.append(float(line))
    file.close()
    return numbers


def diagram():
    numbers = read_numbers()

    odd = []     # числа на нечётных позициях (1-е, 3-е, 5-е ...), берём модуль
    even = []    # числа на чётных позициях (2-е, 4-е, 6-е ...), берём модуль
    for i in range(len(numbers)):
        position = i + 1                 # позиции считаем с 1
        if position % 2 == 1:
            odd.append(abs(numbers[i]))
        else:
            even.append(abs(numbers[i]))

    avg_odd = sum(odd) / len(odd)        # среднее по модулю
    avg_even = sum(even) / len(even)

    total = avg_odd + avg_even           # сумма двух чисел = 100%
    percent_odd = avg_odd / total * 100
    percent_even = avg_even / total * 100

    print(f'Чисел в файле: {len(numbers)}')
    print(f'Среднее по модулю (нечётные позиции): {avg_odd:.3f}')
    print(f'Среднее по модулю (чётные позиции):   {avg_even:.3f}')
    print()

    bar_width = 50                       # вся шкала = 100%
    n_odd = round(percent_odd / 100 * bar_width)
    print('Общая шкала (100%):')
    print(YELLOW + ' ' * n_odd + GREEN + ' ' * (bar_width - n_odd) + END)
    print()

    for name, color, percent in (('Нечётные', YELLOW, percent_odd),
                                 ('Чётные', GREEN, percent_even)):
        bar = color + ' ' * round(percent / 100 * bar_width) + END
        print(f'{name:<10}{bar} {percent:.1f}%')
        print(f'{"":<10}{bar}')
        print()


# ---------- Допзадание: первая четверть графика y = |x| ----------
def graph():
    clear()
    size = 10                       # высота графика: 10 строк
    top = 3                         # строка, где начинается ось y
    bottom = top + size             # строка оси x
    left = 6                        # столбец оси y

    out = goto(1, 1) + 'y = |x|, первая четверть (x >= 0, y >= 0)'

    # ось y и подписи
    for row in range(top, bottom + 1):
        out += goto(row, left) + '│'
        if (bottom - row) % 2 == 0:
            out += goto(row, left - 3) + f'{bottom - row:>2}'

    # ось x и подписи
    out += goto(bottom, left) + '└' + '─' * (2 * size + 2)
    for x in range(0, size + 1, 2):
        out += goto(bottom + 1, left + 2 * x + 1) + str(x)

    # сама функция: для каждого x ставим точку (y = |x| = x)
    for x in range(0, size + 1):
        y = abs(x)
        out += goto(bottom - y, left + 2 * x + 1) + RED + '  ' + END

    out += goto(bottom + 3, 1)
    print(out, end='')              # весь график выводится одной строкой


# ---------- запуск ----------
def pause(text='Нажмите Enter, чтобы продолжить...'):
    input('\n' + text)


def main():
    clear()
    print('1. Флаг Литвы\n')
    flag()
    pause()

    clear()
    print('2. Узор e\n')
    pattern()
    pause()

    animation()
    pause('Анимация закончилась. Нажмите Enter...')

    clear()
    print('4. Диаграмма (sequence.txt)\n')
    diagram()
    pause()

    graph()
    print()


if __name__ == '__main__':
    main()
