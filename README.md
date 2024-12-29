# reader
Repository for the term project of the course BLG-317E.

## Getting Started with the reader Project

This section explains how to set up the **reader** project locally, step by step.

---

### Prerequisites

Ensure the following tools are installed before proceeding:
- **Python 3** (latest version recommended)
- **MySQL** (ensure the server is running)
- **Flask** (will be installed via `requirements.txt`)

Install required Python packages:

**For Windows**
```bash
pip install -r requirements.txt
```
**For MacOS/Linux**
```bash
pip3 install -r requirements.txt
```


### Setup Instructions

1. **Initialize the MySQL Database:**
   
   - Start your MySQL server.

2. **Configure Application Settings:**

   Create `config.py` file in `path/to/reader/main/utils` path, then fill the file with following:

   ```python
   # config.py
    db_user = 'your_username'  # Replace with your MySQL username
    db_password = 'your_password'  # Replace with your MySQL password
    db_host = 'localhost'  # Typically localhost for local development
    db_name = 'reader'  # Database name


3. **Export Python Path**

**For Windows**
```bash
set PYTHONPATH=%cd%
```
**For MacOS/Linux**
```bash
export PYTHONPATH=$(pwd)
```

4. **Create Tables:**

   Run the `create_db` script in the `main/utils` directory to create the database with all data.

   ```bash
   cd path/to/reader/main/utils
   python3 create_db.py
   ```

5. **Run The Application:**
    From project directory run the following code.
    ```bash
    cd path/to/reader
    python3 app.py
    ```

    This will start the Flask server. By default, it runs on http://127.0.0.1:8080
    Go to http://127.0.0.1:8080 url to view the application.
