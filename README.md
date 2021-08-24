# Hometask_Django_Quizzes

## Вариант2
Разработать сайт для формирования и прохождения тестов(опросов).
На сайте должен присутствовать каталог/список всех тестов(опросов).
Для теста должна быть возможность указать входящие в него вопросы и порядковый номер вопроса в рамках этого теста(просто числом).
На странице каждого из тестов отображается описание теста и кнопка _"Пройти тест"_.
После нажатия на кнопку _"Пройти тест"_ пользователю отображается форма/список всех вопросов теста отсортированых по порядковому номеру и поля для ввода ответа на каждый вопрос.
​
Сущности:
​
```
- Test(тест)
- Question(вопрос)
- Testrun(прохождение теста)
```
​
В тесте может быть много вопросов,
один вопрос может быть в нескольких тестах.
Один тест можно пройти много раз.
При прохождении теста на каждый вопрос должен быть
сохранен ответ.


# Запуск с Docker
docker build -t light-it-docker .
docker run --name light-it-docker -p 8000:8000 light-it-docker
