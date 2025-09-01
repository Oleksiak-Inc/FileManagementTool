import os

class SQL_COMMANDS():
    def __init__(self):
        self.ROOT = os.path.dirname(os.path.abspath(__file__))
        self.SQL_DIR = os.path.join(self.ROOT, "sql")
        self.SQL_DICT = sql_commands_loader(self.SQL_DIR)

def sql_commands_loader(sql_dir) -> dict:
    sql_dict = dict()
    for file in os.listdir(sql_dir):
        if file.endswith(".sql"):
            full_path = os.path.join(sql_dir, file)
            filename, _ = os.path.splitext(file)
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
            sql_dict[filename] = content
    return sql_dict
    

if __name__ == "__main__":
    sql_commands = SQL_COMMANDS().SQL_DICT
    print(sql_commands)
