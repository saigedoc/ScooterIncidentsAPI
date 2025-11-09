# ScooterIncidentsAPI
Тестовое задание по созданию API для обработки инцидентов самокатов.

Установка и запуск:
```bash
git clone https://github.com/saigedoc/ScooterIncidentsAPI.git
cd ScooterIncidentsAPI
python main.py
```

API запускается на 127.0.0.1:8000.
На основной страница возвращает мини документацию к API.
end_points:
1. /post - Добавление инцидента в БД. Обязательные аргументы: status["wait", "in_work", "fixed"], source["operator", "monitoring", "partner"].
2. /get - Получение инцидентов с выбранным статусом. Обязательные аргументы: status["wait", "in_work", "fixed"]
3. /put - Изменение статуса инцидента с выбранным id. Обязательные аргументы: id(int), status["wait", "in_work", "fixed"]

примеры:
1. 127.0.0.1:8000/post?description=Моё описание инцидента&status=wait&source=operator
2. 127.0.0.1:8000/get?status=wait
3. 127.0.0.1:8000/put?id=1&status=in_work
4. 127.0.0.1:8000/get?status=in_work
