from pathlib import Path

def load_input(config : object, file_path : str) -> list[str]:
    """Loads input keywords from a file."""
    try:
        file_path = Path(config[file_path]).resolve()
        with open(file_path, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return []



def save_output(config : object, file_path: str, data: list):
    file_path = Path(config[file_path]).resolve()
    """Saves the output data (codes or descriptions) to a file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        for result in data:
            file.write(f"{result}\n")