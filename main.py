import io
import os
import random

from models.file import File
from models.template import Template


def main():
    # Чтение компонентов шаблона будущего теста для студентов

    print("Reading templates...")
    template = Template()

    # Чтение кол-ва заданий из папки /tasks
    print("Reading tasks...")
    tasks = read_tasks()

    # Получение списка студентов из файла students.txt
    print("Reading students...")
    students = File('students.txt').read_file(newline=True)

    # Создание теста для всех студентов
    print("Generating variants...")
    variants = generate_variants(tasks, len(students))

    # Перемешивает варианты
    random.shuffle(variants)

    os.makedirs(os.path.dirname("latex/main.tex"), exist_ok=True)

    out = io.open("latex/main.tex", "w", encoding='utf-8')
    print("Making main.tex file...")

    # Запись в файл /latex/main.tex результата генераций
    out.write(template.header)
    for i in range(len(variants)):
        out.write(template.begin_test + str(students[i]) + template.metadata)
        # Запись заданий для каждого студента
        for taskNumber, task in enumerate(tasks):
            out.write(task[variants[i][taskNumber] - 1])
        out.write(template.end_test)
    out.write(template.footer)
    out.close()

    # Запись в файл /latex/dump.tex всех заданий
    out = io.open("latex/dump.tex", "w", encoding='utf-8')
    print("Making dump.tex file...")

    out.write(template.header)
    for i in range(len(tasks)):
        out.write(template.begin_test + str(i + 1) + template.metadata)
        for k in range(len(tasks[i])):
            out.write(tasks[i][k])
        out.write(template.end_test)
    out.write(template.footer)
    out.close()

    print("Done!")


# Чтение заданий из /tasks/№/№.tex и вовзращаемый результат - прочитанные файлы
def read_tasks():
    result = []
    total_tasks = len(os.listdir('tasks'))
    print(total_tasks + 1)
    for i in range(1, total_tasks):
        result.append([])
        total_variants = len(os.listdir('tasks/%d' % i))
        for k in range(1, total_variants):
            result[i - 1].append(File('tasks/%d/%d.tex' % (i, k)).read_file())
    return result


# Если кол-во вариантов меньше заданного, то происходит генерация новых вариантов заданий
def generate_variants(tasks, total):
    counts = []
    for i in tasks:
        counts.append(len(i))
    result = set()
    while len(result) < total:
        result.add(generate_variant(counts))
    return list(result)


# Создание нового варианта задания и возврат его в качества кортежа
def generate_variant(counts):
    result = []
    for i in range(len(counts)):
        result.append(random.randint(1, counts[i]))
    return tuple(result)


if __name__ == "__main__":
    main()
