В данном репозитории представлено решение тестового задания.
1. В файле Aggregate.py ноходится строка агрегационного запроса к базе данных 
MongoDB, который возвращает результат соответствующий условию задания.
2. В файле main.py написана функция, которая обрабатывает две коллекции
Долг и Платёж, после чего формирует новую коллекцию Результат. Также в данном файле присутствует
функция, которая создает две тестовые коллекции Долг и Платеж.

Приложение обернуто в Docker для более удобного запуска.
Для запуска можно использовать команду  `docker-compose up`, она создаст контейнер для приложения и базы данных.
