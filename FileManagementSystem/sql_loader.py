from pathlib import Path

class SQL_COMMANDS:
    def __init__(self):
        root = Path(__file__).resolve().parent
        self.commands = load_sql_commands(root / "sql")

    def __getitem__(self, item):
        return self.commands[item]

    def __repr__(self):
        return repr(self.commands)


def load_sql_commands(sql_dir: Path) -> dict:
    tree = {}

    for path in sql_dir.rglob("*.sql"):
        relative_parts = path.relative_to(sql_dir).parts
        *folders, filename = relative_parts
        key = path.stem

        current = tree
        for folder in folders:
            current = current.setdefault(folder, {})

        current[key] = path.read_text(encoding="utf-8")

    return tree
    

if __name__ == "__main__":
    sql_commands = SQL_COMMANDS()
    print(sql_commands)
