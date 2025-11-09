from fastapi import FastAPI
from typing import Optional, Literal
from database import IssuesDB
import uvicorn

def main():
    app = FastAPI()
    idb = IssuesDB()

    @app.get("/")
    def master():
        help = """
hi
"""
        return help

    @app.get("/post")
    def post(status: Literal["wait", "in_work", "fixed"], source: Literal["operator", "monitoring", "partner"], description: Optional[str] = None):
        idb.post_issue({"description": description, "status": status, "source": source})
        return 'post complete'

    @app.get("/get")
    def get(status: Literal["wait", "in_work", "fixed"]):
        return idb.get_issues(status)

    @app.get("/put")
    def put(id: int, status: Literal["wait", "in_work", "fixed"]):
        if idb.put_issue(id, status):
            return 404
        else:
            return "put complete"

    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()