import io, os, itertools, random

def main():
    # Чтение компонентов шаблона будущего теста для студентов

    print("Reading templates...")
    header = readFile('templates/head.tex')
    beginTest = readFile('templates/qStart.tex')
    metadata = readFile('templates/qStart2.tex')
    endTest = readFile('templates/qFinish.tex')
    footer = readFile('templates/tail.tex')

    # Чтение кол-ва заданий из папки /tasks
    print("Reading tasks...")
    tasks = readTasks()

    # Получение списка студентов из файла students.txt
    print("Reading students...")
    students = readStudents()

    # Создание теста для всех студентов
    print("Generating variants...")
    variants = generateVariants(tasks, len(students))

    # Перемешивает варианты
    random.shuffle(variants)

    os.makedirs(os.path.dirname("latex/main.tex"), exist_ok=True)
    
    out = io.open("latex/main.tex", "w", encoding='utf-8')
    print("Making main.tex file...")

    # Запись в файл /latex/main.tex результата генераций
    out.write(header)
    for i in range(len(variants)):
        out.write(beginTest + str(students[i]) + metadata)
        # Запись заданий для каждого студента
        for taskNumber, task in enumerate(tasks):
            out.write(task[variants[i][taskNumber]-1])    
        out.write(endTest)
    out.write(footer)
    out.close()


    out = io.open("latex/dump.tex", "w", encoding='utf-8')
    print("Making dump.tex file...")

    out.write(header)
    for i in range(len(tasks)):
        out.write(beginTest + str(i+1) + metadata)
        for k in range(len(tasks[i])):
            out.write(tasks[i][k])
        out.write(endTest)
    out.write(footer)
    out.close()

    print("Done!")
    

# Чтение заданий из /tasks/№/№.tex и вовзращаемый результат - прочитанные файлы
def readTasks():
    result = []
    totalTasks = len(os.listdir('tasks'))
    print(totalTasks+1)
    for i in range(1,totalTasks):
        result.append([])
        totalVariants = len(os.listdir('tasks/%d' % i))
        for k in range(1,totalVariants):
            result[i-1].append(readFile('tasks/%d/%d.tex' % (i,k)))
    return result

# Чтение файла students.txt и получение списка студентов
def readStudents():
    file = io.open("students.txt", encoding='utf-8')
    result = file.readlines()
    file.close()
    return result

# Если кол-во вариантов меньше заданного, то происходит генерация новых вариантов заданий
def generateVariants(tasks, total):
    counts = []
    for i in tasks:
        counts.append(len(i))
    result = set()
    while len(result) < total:
        result.add(generateVariant(counts))
    return list(result)

# Создание нового варианта задания и возврат его в качества кортежа
def generateVariant(counts):
    result = []
    for i in range(len(counts)):
        result.append(random.randint(1,counts[i]))
    return tuple(result)


def readFile(name):
    file = io.open(name, encoding='utf-8')
    text = file.read()
    file.close()
    return text


if __name__ == "__main__":
    main()
