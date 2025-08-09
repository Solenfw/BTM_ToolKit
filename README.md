# BTM Quote Tool version 1

A simplified version that demonstrates the core functionality (Demo / Prototype / MVP to verify the feasibility of product/solution)

## Table of Contents

- [Folder Structure](#folder-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [Contributing](#contributing)

## Folder Structure

```plaintext
project_name/
├── .git/                    # Git version control directory
├── .github/                 # GitHub-specific files (workflows, templates, etc.)
├── docs/                    # Documentation files (e.g., markdown or Sphinx)
├── src/                     # Source code directory
│   ├── project_name/        # Main package/module
│   │   ├── __init__.py      # Package initialization file
│   │   ├── module1.py       # Example module 1
│   │   └── subpackage/      # Example subpackage
│   │       └── submodule.py # Example submodule
│   └── main.py              # Main entry point of the application
├── tests/                   # Unit and integration tests
│   ├── __init__.py
│   ├── test_module1.py      # Unit tests for module1
│   └── fixtures/            # Test fixtures and mock data
├── scripts/                 # Utility scripts (setup, deployment, etc.)
├── data/                    # Data files (e.g., CSV, JSON)
├── .gitignore               # Git ignore file
├── requirements.txt         # Python dependencies file
├── pyproject.toml           # Build configuration (e.g., Poetry, PEP 518)
├── setup.py                 # Setup script for packaging and distribution
├── README.md                # Project documentation
├── LICENSE                  # License file
└── tox.ini                  # Tox configuration file for testing
```
## Requirements
* Python 3.8+ (or whichever version you're using)
* pip or poetry for dependency management

## Installation
### Clone the Repository
Start by cloning the repository to your local machine:

```bash
git clone https://github.com/BTM-DX-Squad/BTM_QuoteTool_v1.git
cd BTM_QuoteTool_v1
```
### Create a Virtual Environment (Recommended)
It’s a good practice to use a virtual environment to manage dependencies. You can create a virtual environment using venv or virtualenv.

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```
### Install Dependencies
You can install dependencies from requirements.txt using pip:

```bash
pip install -r requirements.txt
```
Alternatively, if you're using Poetry (if your project uses pyproject.toml):

```bash
poetry install
```

### Development Dependencies (Optional)
If there are separate dependencies for development (such as linters or testing tools), install those as well:

```bash
pip install -r dev-requirements.txt
```

## Usage
To run the main application:
```bash
python src/main.py
```
You can also use any script within the scripts/ folder to run setup tasks or utilities. For example:
```bash
python scripts/run_this.py
```

## Running Tests
We use pytest for unit and integration testing. You can run the tests by executing the following command:

```bash
pytest
```
If you’re using tox to run tests across multiple environments, simply run:
```bash
tox
```
## Contributing

* Commit your changes with clear commit messages and use descriptive commit messages (see Git commit guidelines in the [project documentation](https://www.notion.so/tuan7/BTM_QuoteTool_2024-Project-Process-1035bba0c1a38082a45ce03f5802d715?pvs=4#1125bba0c1a38028bc18f8a3d065e3bc)).
* Push to your branch and submit a pull request.
* Please make sure that your code passes all tests before submitting a pull request.
* Coding Guidelines
** Follow [PEP 8](https://pep8.org/) for Python code style.




