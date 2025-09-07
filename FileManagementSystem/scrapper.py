import os

def collect_code(root_dir, output_file):
    with open(output_file, "w", encoding="utf-8") as outfile:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Exclude .venv and __pycache__ directories
            dirnames[:] = [d for d in dirnames if d not in (".venv", "__pycache__", "scrapper.py")]

            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as infile:
                        outfile.write(f"# --- {filepath} ---\n")
                        outfile.write(infile.read())
                        outfile.write("\n\n")
                except Exception as e:
                    print(f"Skipping {filepath} due to error: {e}")

if __name__ == "__main__":
    project_root = os.path.dirname(os.path.abspath(__file__))  # current folder
    output_txt = "all_code.txt"
    collect_code(project_root, output_txt)
    print(f"✅ Code collected into {output_txt}")
