import os

def create_microservice_structure():
    base_dir = "."
    directories = [
        f"{base_dir}/app",
        f"{base_dir}/tests"
    ]
    files = {
        f"{base_dir}/app/__init__.py": "",
        f"{base_dir}/app/main.py": "",
        f"{base_dir}/app/validation.py": "",
        f"{base_dir}/tests/test_validation.py": "",
        f"{base_dir}/requirements.txt": "",
        f"{base_dir}/.gitignore": "# Byte-compiled / optimized / DLL files\n*.pyc\n*.pyo\n*.pyd\n__pycache__/",
        f"{base_dir}/README.md": "# User Input Service\n\nThis microservice validates user input for the salary calculator."
    }

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

    for filepath, content in files.items():
        with open(filepath, "w") as f:
            f.write(content)
            print(f"Created file: {filepath}")

if __name__ == "__main__":
    create_microservice_structure()
    