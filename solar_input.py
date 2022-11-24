# coding: utf-8
# license: GPLv3

from solar_objects import Star, Planet


def read_space_objects_data_from_file(input_filename):
    """Cчитывает данные о космических объектах из файла, создаёт сами объекты
    и вызывает создание их графических образов

    Параметры:

    **input_filename** — имя входного файла
    """

    objects = []
    with open(input_filename) as input_file:
        for line in input_file:
            if len(line.strip()) == 0 or line[0] == '#':
                continue  # пустые строки и строки-комментарии пропускаем
            object_type = line.split()[0].lower()
            if object_type == "star":  # FIXME: do the same for planet
                star = Star()
                parse_star_parameters(line, star)
                objects.append(star)
            else:
                planet = Planet()
                parse_planet_parameters(line, planet)
                objects.append(planet)

    return objects


def parse_star_parameters(line, star):
    """Считывает данные о звезде из строки.
    Входная строка должна иметь слеюущий формат:
    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Здесь (x, y) — координаты звезды, (Vx, Vy) — скорость.
    Пример строки:
    Star 10 red 1000 1 2 3 4

    Параметры:

    **line** — строка с описание звезды.
    **star** — объект звезды.
    """

    parameters = line.split()
    star.R = int(parameters[1])
    star.color = parameters[2]
    star.m = float(parameters[3])
    star.x = float(parameters[4])
    star.y = float(parameters[5])
    star.Vx = float(parameters[6])
    star.Vy = float(parameters[7])

def parse_planet_parameters(line, planet):
    """Считывает данные о планете из строки.
    Предполагается такая строка:
    Входная строка должна иметь слеюущий формат:
    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Здесь (x, y) — координаты планеты, (Vx, Vy) — скорость.
    Пример строки:
    Planet 10 red 1000 1 2 3 4

    Параметры:

    **line** — строка с описание планеты.
    **planet** — объект планеты.
    """
    parameters = line.split()
    planet.R = int(parameters[1])
    planet.color = parameters[2]
    planet.m = float(parameters[3])
    planet.x = float(parameters[4])
    planet.y = float(parameters[5])
    planet.Vx = float(parameters[6])
    planet.Vy = float(parameters[7])


def write_space_objects_data_to_file(output_filename, space_objects):
    """Сохраняет данные о космических объектах в файл.
    Строки должны иметь следующий формат:
    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>
    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Параметры:

    **output_filename** — имя входного файла
    **space_objects** — список объектов планет и звёзд
    """
    with open(output_filename, 'w') as out_file:
        for obj in space_objects:
            print(out_file, "%s %d %s %f %f %f %f %f" % (obj.type, obj.R, obj.color, obj.m, obj.x, obj.y, obj.Vx, obj.Vy))


def save_statistics_to_file(output_filename, obj, star, physical_time):
    """
    Сохраняет статистику в текстовый файл.

    Параметры:

    **output_filename** — имя текстового файла статистики
    **obj** — объекты планет и звёзд.
    **star** — объект звезды.
    **physical_time** — время симуляции.
    """
    with open(output_filename, 'a') as out_file:
        print("%f %s %d %s %f %f %f %f %f %f %f" % (physical_time, obj.type, obj.R, obj.color, obj.m, obj.x, obj.y, obj.Vx, obj.Vy, (obj.Vx**2 + obj.Vy**2)**0.5, ((star.x - obj.x)**2 + (star.y - obj.y)**2)**0.5), file = out_file)

if __name__ == "__main__":
    print("This module is not for direct call!")
