"""
Модуль для обращения API к базе данных SQLite.
"""
import sqlite3

class IssuesDB:
    """
    Класс IssuesDB, класс реализующий SQL запросы к базе данных SQLite.

    Методы класса:
    __init__(path): создание экземпляра класса и подключение к БД.
    check_exist(): Проверка на наличие таблицы, создание таблицы при её отсутстии.
    post_issue(row): Добавляет строку данных в таблицу БД.
    get_issues(status): Возвращает строки с выбранным статусом.
    put_issue(id, status): Изменяет статус в строке с выбранным id.
    close(): Отключается от БД.
    """
    def __init__(self, path="issues.db"):
        """
        Создаёт экземляр класса.
        Подключается к БД SQLite.
        Запускает проверк наличия таблицы.

        Парамеьры:
        path (str): путь к БД SQLite.
        """
        self.connection = sqlite3.connect(path, check_same_thread=False)
        self.check_exist()

    def check_exist(self):
        """Функция проверки существования таблицы, создаёт таблицу, если её нету."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='issues';")
        if len(cursor.fetchall()) == 0:
            cursor.execute('''
            CREATE TABLE issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            status TEXT CHECK( status IN ('wait','in_work','fixed') ),
            source TEXT CHECK( source IN ('operator','monitoring','partner') ),
            timestamp TIMESTAMP DEFAULT (datetime('now','localtime'))
            );
            ''')
            self.connection.commit()

    def post_issue(self, row):
        """
        Функция добавляющая строку в таблицу.

        Параметры:
        row (dict): словарь с данными для добавления в формате: {"column1":"value1, ...} 
        """
        row_keys, row_vals = list(row.keys()), list(map(lambda x: f"'{x}'", list(row.values())))
        cursor = self.connection.cursor()
        cursor.execute(f"""INSERT INTO issues ({", ".join(row_keys)})
                       VALUES ({", ".join(row_vals)});""")
        self.connection.commit()

    def get_issues(self, status):
        """
        Функция возвращающая строки из таблицы с выбранным статусом.
        
        Параметры:
        status (str["wait", "in_work", "fixed"]): статус инцидента, имеет 3 вариации.
        """
        cursor = self.connection.cursor()
        cursor.execute(f"""SELECT * FROM issues WHERE status = '{status}';""")
        return cursor.fetchall()

    def put_issue(self, id, status):
        """
        Функция изменения статуса строки с выбранным id.

        Параметры:
        id (int): id строки
        status (str["wait", "in_work", "fixed"]): новый статус инцидента, имеет 3 вариации.
        """
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT id FROM issues WHERE id = {id}")
        if len(cursor.fetchall()) == 0:
            return 404
        else:
            cursor.execute(f"""UPDATE issues SET status = '{status}'
                        WHERE id = {id};""")
            self.connection.commit()

    def close(self):
        """Функция закрывающая подключение к БД."""
        self.connection.close()

if __name__ == "__main__":
    IDB = IssuesDB()
    IDB.post_issue({"status": "wait", "source": "operator"})
    IDB.post_issue({"description": 'fw2', "status": "in_work", "source": "operator"})
    IDB.post_issue({"description": 'fw3', "status": "wait", "source": "operator"})
    print(IDB.get_issues("wait"))

    print(IDB.get_issues("fixed"))
    print(IDB.get_issues("in_work"))
    IDB.put_issue(1, "fixed")
    print(IDB.get_issues("wait"))

    print(IDB.get_issues("fixed"))
    print(IDB.get_issues("in_work"))
    IDB.close()