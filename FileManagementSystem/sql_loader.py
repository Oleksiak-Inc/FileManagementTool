import os

class SQL_COMMANDS(dict):
    def __init__(self):
        root = os.path.dirname(os.path.abspath(__file__))
        sql_dir = os.path.join(root, "sql")
        super().__init__(sql_commands_loader(sql_dir))

def sql_commands_loader(sql_dir) -> dict:
    sql_dict = dict()
    for root, dirs, files in os.walk(sql_dir):
        for file in files:
            if file.endswith(".sql"):
                full_path = os.path.join(root, file)
                filename, _ = os.path.splitext(file)
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()
                sql_dict[filename] = content
    return sql_dict
    

if __name__ == "__main__":
    sql_commands = SQL_COMMANDS()
    print(sql_commands)
