# coding: utf-8
# license: GPLv3

import tkinter
from tkinter.filedialog import *

import numpy as np

from solar_vis import *
from solar_model import *
from solar_input import *
import matplotlib.pyplot as plt

perform_execution = False
"""Флаг цикличности выполнения расчёта"""

physical_time = 0
"""Физическое время от начала расчёта.
Тип: float"""

displayed_time = None
"""Отображаемое на экране время.
Тип: переменная tkinter"""

time_step = None
"""Шаг по времени при моделировании.
Тип: float"""

space_objects = []
"""Список космических объектов."""


def execution():
    """Функция исполнения -- выполняется циклически, вызывая обработку всех небесных тел,
    а также обновляя их положение на экране.
    Цикличность выполнения зависит от значения глобальной переменной perform_execution.
    При perform_execution == True функция запрашивает вызов самой себя по таймеру через от 1 мс до 100 мс.
    """
    global physical_time
    global displayed_time
    recalculate_space_objects_positions(space_objects, time_step.get())
    for body in space_objects:
        update_object_position(space, body)
    physical_time += time_step.get()
    displayed_time.set("%.1f" % physical_time + " seconds gone")

    if perform_execution:
        space.after(101 - int(time_speed.get()), execution)

    for obj in space_objects:
        if obj.type == "star":
            star = obj
    for obj in space_objects:
        if obj.type == "planet":
            save_statistics_to_file("stats.txt", obj, star, physical_time)


def start_execution():
    """Обработчик события нажатия на кнопку Start.
    Запускает циклическое исполнение функции execution.
    """
    global perform_execution
    perform_execution = True
    start_button['text'] = "Pause"
    start_button['command'] = stop_execution

    execution()
    print('Started execution...')


def stop_execution():
    """Обработчик события нажатия на кнопку Start.
    Останавливает циклическое исполнение функции execution.
    """
    global perform_execution
    perform_execution = False
    start_button['text'] = "Start"
    start_button['command'] = start_execution
    print('Paused execution.')


def open_file_dialog():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    global space_objects
    global perform_execution
    perform_execution = False
    f = open("stats.txt", "w")
    for obj in space_objects:
        space.delete(obj.image)  # удаление старых изображений планет
    in_filename = askopenfilename(filetypes=(("Text file", ".txt"),))
    space_objects = read_space_objects_data_from_file(in_filename)
    max_distance = max([max(abs(obj.x), abs(obj.y)) for obj in space_objects])
    calculate_scale_factor(max_distance)

    for obj in space_objects:
        if obj.type == 'star':
            create_star_image(space, obj)
        elif obj.type == 'planet':
            create_planet_image(space, obj)
        else:
            raise AssertionError()


def save_file_dialog():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    out_filename = asksaveasfilename(filetypes=(("Text file", ".txt"),))
    write_space_objects_data_to_file(out_filename, space_objects)


def plot():
    """
    Открывает побочное окно с отрисованными в нём графиками V(t), r(t), V(r).
    """
    d_t = dict()
    d_v = dict()
    d_r = dict()
    for line in open("stats.txt"):
        array_st = line.split()
        d_t[array_st[3]] = d_t.get(array_st[3], []) + [float(array_st[0])]
        d_v[array_st[3]] = d_v.get(array_st[3], []) + [float(array_st[9])]
        d_r[array_st[3]] = d_r.get(array_st[3], []) + [float(array_st[10])]
    fig, ax = plt.subplots(2, 2)
    plt.subplot(2, 2, 1)
    fig.tight_layout()
    plt.xlabel('$t, c$')  # ось Ox
    plt.ylabel('$V, \\frac{m}{s}$')  # Ось Oy
    plt.title("V(t)")
    for k in d_t.keys():
        plt.plot(d_t[k], d_v[k], color = k)
    plt.subplot(2, 2, 3)
    plt.xlabel('$t, c$')  # ось Ox
    plt.ylabel('$r, m$')  # Ось Oy
    plt.title("r(t)")
    for k in d_t.keys():
        plt.plot(d_t[k], d_r[k], color = k)
    plt.subplot(1, 2, 2)
    plt.xlabel('$r, c$')  # ось Ox
    plt.ylabel('$v, \\frac{m}{s}$')  # Ось Oy
    plt.title("v(r)")
    for k in d_v.keys():
        plt.plot(d_r[k], d_v[k], color=k)
    plt.show()

def main():
    """Главная функция главного модуля.
    Создаёт объекты графического дизайна библиотеки tkinter: окно, холст, фрейм с кнопками, кнопки.
    """
    global physical_time
    global displayed_time
    global time_step
    global time_speed
    global space
    global start_button
    print('Modelling started!')
    physical_time = 0

    root = tkinter.Tk()
    # космическое пространство отображается на холсте типа Canvas
    space = tkinter.Canvas(root, width=window_width, height=window_height, bg="black")
    space.pack(side=tkinter.TOP)
    # нижняя панель с кнопками
    frame = tkinter.Frame(root)
    frame.pack(side=tkinter.BOTTOM)

    start_button = tkinter.Button(frame, text="Start", command=start_execution, width=6)
    start_button.pack(side=tkinter.LEFT)

    time_step = tkinter.DoubleVar()
    time_step.set(1)
    time_step_entry = tkinter.Entry(frame, textvariable=time_step)
    time_step_entry.pack(side=tkinter.LEFT)

    time_speed = tkinter.DoubleVar()
    scale = tkinter.Scale(frame, variable=time_speed, orient=tkinter.HORIZONTAL)
    scale.pack(side=tkinter.LEFT)

    load_file_button = tkinter.Button(frame, text="Open file...", command=open_file_dialog)
    load_file_button.pack(side=tkinter.LEFT)

    save_file_button = tkinter.Button(frame, text="Save to file...", command=save_file_dialog)
    save_file_button.pack(side=tkinter.LEFT)

    plot_button = tkinter.Button(frame, text="Plot", command=plot)
    plot_button.pack(side=tkinter.LEFT)

    displayed_time = tkinter.StringVar()
    displayed_time.set(str(physical_time) + " seconds gone")
    time_label = tkinter.Label(frame, textvariable=displayed_time, width=30)
    time_label.pack(side=tkinter.RIGHT)

    root.mainloop()
    print('Modelling finished!')

if __name__ == "__main__":
    main()
