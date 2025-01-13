# BTM_ToolKit
For basic tasks. Supporting Surgical Instruments classification.
## Structure

BTM_ToolKit/
├── data/                 # Folder for all data files
│   ├── raw/              # Raw data (original .csv, .txt files)
│   ├── processed/        # Processed data outputs
│   └── external/         # External data sources or references
│
├── src/                  # Source code folder
│   ├── modules/          # Reusable Python modules (functions, classes)
│   ├── scripts/          # Main scripts (entry points for specific tasks)
│   └── app/              # Web app (e.g., Flask, FastAPI)
│       ├── templates/    # HTML files for the website
│       ├── static/       # CSS, JavaScript, and images
│       ├── routes.py     # API endpoints and routes
│       └── app.py        # Main entry point for the web app
│
├── tests/                # Unit tests for your code
│   └── test_<module>.py  # Test scripts for individual modules
│
├── logs/                 # Log files for debugging or monitoring
│   └── app.log           # Example log file
│
├── notebooks/            # Jupyter notebooks (if applicable)
│   └── data_analysis.ipynb
│
├── requirements.txt      # Python dependencies
├── setup.py              # Setup script for packaging (if needed)
├── README.md             # Project overview and documentation
└── .gitignore            # Files and folders to exclude from Git
