from pathlib import Path

def load_input(config : object, source : str, file_path : str) -> list[str]:
    """Loads input keywords from a file."""
    try:
        file_path = Path(config[source][file_path]).resolve()
        with open(file_path, 'r', encoding='utf-8') as file:
            return [line for line in file.read().splitlines()]
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return []



def save_output(config : object, source : str, file_path: str, data: list):
    file_path = Path(config[source][file_path]).resolve()
    """Saves the output data (codes or descriptions) to a file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        for result in data:
            file.write(f"{result}\n")