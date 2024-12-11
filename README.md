# config_2
Гаврилюк Алексей ИКБО-42-23
# Задание (Вариант 6)
Разработать инструмент командной строки для визуализации графа зависимостей, включая транзитивные зависимости.
Сторонние средства для получения зависимостей использовать нельзя.
Зависимости определяются для git-репозитория.
Для описания графа зависимостей используется представление Mermaid.
Визуализатор должен выводить результат на экран в виде кода.
Построить граф зависимостей для коммитов, в узлах которого находятся списки файлов и папок.
Граф необходимо строить только для тех коммитов, где фигурирует файл с заданным именем.
Конфигурационный файл имеет формат yaml и содержит:
Путь к программе для визуализации графов.
  1. Путь к анализируемому репозиторию.
  2. Путь к файлу-результату в виде кода.
  3. Файл с заданным именем в репозитории

Все функции визуализатора зависимостей должны быть покрыты тестами

#Старт
Для начала добавим git для всех файлов с помошью git add .

Затем сделаем коммит:
![image](https://github.com/user-attachments/assets/dc6c89ed-f29e-4c8d-86d6-2c4c229ecc69)

Введем команду git log, чтобы отследить коммиты:
![image](https://github.com/user-attachments/assets/9b868463-fb7f-4367-b88a-8accdd89ab91)

Запустим main.py, в аргумент которой пойдет путь yaml файла, в котором записаны все пути:
![image](https://github.com/user-attachments/assets/32311955-ff5c-4509-9820-95e93b7417fa)

В итоге, в файле output_graph.mmd запишется история изменения файлов
