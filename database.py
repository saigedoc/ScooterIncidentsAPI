import sqlite3

class IssuesDB:
    def __init__(self, path="issues.db"):
        self.connection = sqlite3.connect(path, check_same_thread=False)
        self.check_exist()

    def check_exist(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='issues';")
        if len(cursor.fetchall()) == 0:
            cursor.execute('''
            CREATE TABLE issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            status TEXT CHECK( status IN ('wait','in_work','fixed') ),
            source TEXT CHECK( source IN ('operator','monitoring','partner') ),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            ''')
            self.connection.commit()

    def post_issue(self, row):
        row_keys, row_vals = list(row.keys()), list(map(lambda x: f"'{x}'", list(row.values())))
        cursor = self.connection.cursor()
        cursor.execute(f"""INSERT INTO issues ({", ".join(row_keys)})
                       VALUES ({", ".join(row_vals)});""")
        self.connection.commit()

    def get_issues(self, status):
        cursor = self.connection.cursor()
        cursor.execute(f"""SELECT * FROM issues WHERE status = '{status}';""")
        return cursor.fetchall()

    def put_issue(self, id, status):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT id FROM issues WHERE id = {id}")
        if len(cursor.fetchall()) == 0:
            return 404
        else:
            cursor.execute(f"""UPDATE issues SET status = '{status}'
                        WHERE id = {id};""")
            self.connection.commit()

    def close(self):
        self.connection.close()
"""
id int
description str
status wait/in_work/fixed
source operator/monitoring/partner
timestamp time
"""
if __name__ == "__main__":
    IDB = IssuesDB()
    #IDB.post_issue({"status": "wait", "source": "operator"})
    #IDB.post_issue({"description": 'fw2', "status": "in_work", "source": "operator"})
    #IDB.post_issue({"description": 'fw3', "status": "wait", "source": "operator"})
    print(IDB.get_issues("wait"))

    print(IDB.get_issues("fixed"))
    print(IDB.get_issues("in_work"))
    IDB.put_issue(5, "fixed")
    print(IDB.get_issues("wait"))

    print(IDB.get_issues("fixed"))
    print(IDB.get_issues("in_work"))
    IDB.close()