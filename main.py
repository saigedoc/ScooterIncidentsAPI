"""
Главный исполняемый модуль.
Создаёт приложение FastAPI и его end points и запускает его с помощью unicorn.
"""
from fastapi import FastAPI
from typing import Optional, Literal
from database import IssuesDB
import uvicorn

def main():
    app = FastAPI()
    idb = IssuesDB()

    @app.get("/")
    def master():
        """Функция исполняемая при переходи на основную страницу API, возвращает вспомогательную информацию в формате json."""
        help = {
            "title": "Это API для получения и изменения данных о инцидентах самкатов.",
            "table_format": {"name": "issues", "columns": 
                             [
                                 "id (integer): автоматически выставляется, не указывается при добавлении инцидента.",
                                 "description (string): необязательный аргумент описание инцидента.",
                                 'status (string["wait", "in_work", "fixed"]): статус инцидента - обязательный аргумент имеющий 3 описанных варианта.',
                                 'source (string["operator", "monitoring", "partner"]): источник сообщения о инциденте - обязательный аргумент имеющий 3 описанных варианта.',
                                 "timestamp (timestamp): автоматически выставляется, не указывается при добавлении инцидента."
                                ]
                            },
            "end_points": [
                {
                    "end_point": "/post",
                    "description": "Добавление нового инцидента.",
                    "parameters": ["status", "source", "description"]
                },
                {
                    "description": "Получить данные о инцидентах со статусом {status}",
                    "end_point": "/get",
                    "parameters": ["status"]
                },
                {
                    "description": "Изменить статус инцидента под id #{id} на {status}",
                    "end_point": "/put",
                    "parameters": ["id", "status"]
                }
            ]
        }
        return help

    @app.get("/post")
    def post(status: Literal["wait", "in_work", "fixed"], source: Literal["operator", "monitoring", "partner"], description: Optional[str] = None):
        """Функция добавления инцидента в базу даных."""
        idb.post_issue({"description": description, "status": status, "source": source})
        return 'post complete'

    @app.get("/get")
    def get(status: Literal["wait", "in_work", "fixed"]):
        """Функция получения инцидентов с выбранный статусом из базы данных."""
        return idb.get_issues(status)

    @app.get("/put")
    def put(id: int, status: Literal["wait", "in_work", "fixed"]):
        """Функция изменения статуса инцидента в базе данных"""
        if idb.put_issue(id, status):
            return 404
        else:
            return "put complete"

    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()