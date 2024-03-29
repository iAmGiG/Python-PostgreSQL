# Python-PostgreSQL

This project uses a PostgreSQL database adapter to create a relation and populate it with data from a collection of PubMed citation documents. It demonstrates the integration of Python with PostgreSQL for managing and analyzing data, specifically focusing on parsing XML files, data insertion, and performing SQL queries for analysis.

## Python and PostgreSQL

A detailed set up guild. ping from the VM.

## Description

This project uses a PostgreSQL database adapter to create a relation and populate it with data from a collection of PubMed citation documents. It demonstrates the integration of Python with PostgreSQL for managing and analyzing data, specifically focusing on parsing XML files, data insertion, and performing SQL queries for analysis.

## Getting Started

### Dependencies

- Python 3.x
- PostgreSQL
- Python libraries: `lxml`, `psycopg2`
- An XML file of PubMed citations

### Installing

1. **PostgreSQL Installation**: Follow the instructions at [PostgreSQL Official Download Page](https://www.postgresql.org/download/) to install PostgreSQL on your system.
2. **Python Environment Setup**: If you're new to Python or need to set up a virtual environment, refer to Python's official documentation.
3. **Install Required Python Packages**:

   ```sh
   python -m pip install lxml psycopg2
   ```

## Linux/Ubuntu Setup Instructions

1. **Install PostgreSQL**:
   - Update your package list: `sudo apt update`
   - Install PostgreSQL: `sudo apt install postgresql postgresql-contrib`

2. **Setup PostgreSQL**:
   - Start the PostgreSQL service: `sudo service postgresql start`
   - Log in to the PostgreSQL DBMS: `sudo -u postgres psql`
   - Create a new database and user (replace `your_database`, `your_username`, and `your_password` with your chosen names and passwords):

     ```sql
     CREATE DATABASE your_database;
     CREATE USER your_username WITH ENCRYPTED PASSWORD 'your_password';
     GRANT ALL PRIVILEGES ON DATABASE your_database TO your_username;
     \q
     ```

3. **Install Python and Pip** (if not already installed):
   - Install Python: `sudo apt install python3`
   - Install pip: `sudo apt install python3-pip`

4. **Set up your Python environment**:
   - Navigate to your project directory: `cd path/to/your/project`
   - Install required Python packages: `pip3 install -r requirements.txt`

5. **Configure the Python script**:
   - Open the Python script in your editor: `nano your_script.py`
   - Replace the placeholder values for the database connection parameters (`your_database`, `your_username`, `your_password`, etc.) with the actual values you used when setting up PostgreSQL.

6. **Run your Python script**:
   - Execute the script: `python3 your_script.py`

## Windows Setup Instructions

1. **Install PostgreSQL**:
   - Download the PostgreSQL installer from the [official website](https://www.postgresql.org/download/windows/) and follow the installation instructions.

2. **Setup PostgreSQL**:
   - Use the Stack Builder (included in the PostgreSQL installation) or the command line to create your database and user.

3. **Install Python**:
   - Download the Python installer from [python.org](https://www.python.org/downloads/windows/) and follow the installation instructions. Ensure you add Python to your PATH.

4. **Install Python Packages**:
   - Open Command Prompt as Administrator and navigate to your project directory.
   - Install required Python packages using pip: `pip install -r requirements.txt`.

5. **Configure the Python Script**:
   - Open your script in a text editor (like Notepad or VS Code) and adjust the database connection parameters with your actual PostgreSQL setup details.

6. **Run Your Python Script**:
   - In the Command Prompt, run your script: `python your_script.py`.

### Configuration

Before running the application, ensure your PostgreSQL server is running and accessible. You will need to configure your database connection details (e.g., database name, user, password, host, and port) in the application.

Update the README:
Add a section in your README that specifies how to download and prepare the PubMed data files for processing. Here's an example snippet you might add:

## PubMed Data Preparation

The project uses PubMed citation XML files for data processing. To download a specific file:

1. Create a data directory within the project:

```bash
mkdir -p data
```

2. Download the desired PubMed XML file to the data directory:

```bash
wget https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed24n1158.xml.gz -P ./data
```

3. If necessary, unzip the file for processing:

```bash
gunzip ./data/pubmed24n1158.xml.gz -k
```

(-k option used to keep OG zip file)

### Usage

- Step 1: Data Preparation
Download a PubMed archive file from the National Library of Medicine at <https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/>. Select a .xml.gz file which contains up to 30,000 PubMed citations.

- Step 2: Parsing and Database Insertion
Run the provided Python script to parse the downloaded XML file and insert citation data into the PostgreSQL database. The script creates a table with specific attributes for each citation and handles data insertion.

- Step 3: Data Analysis
Execute the SQL queries included in the repository to analyze the citation data. The queries cover a range of analyses, such as finding the range of publication dates, identifying the most prolific authors, and more.

## Running the Main Script

Ensure Python and necessary libraries are installed. Navigate to the project directory and run:

```bash
python main.py
```

### Running 'main.py'

- Ensure you have Python and necessary libraries (psycopg2, lxml, etc.) installed.
- Use the terminal or command prompt to navigate to your project directory.
- Run the script with python main.py, assuming it's configured to connect to your database and process an XML file.

### Using `analysis.py`

```markdown
## Analysis Script Usage

After setting up the database with `main.py`, you can run analysis queries:

```bash
python analysis.py
```

### Using 'analysis.py'

- Same prerequisites as main.py.
- Run specific analysis functions directly by calling them in the script and then executing python analysis.py.

### VSCode Pylance/Jupyter # %% Commenting

- This feature allows you to create interactive Python sessions in VSCode. By placing # %% at the start of a cell, you can execute that section independently in an interactive window.
- Ensure you have the Python extension for VSCode installed, which includes Pylance.
- You can write your analysis code in segments separated by # %% and run each block independently, making it easier to develop and test parts of your code.


### Unit Testing with `test_analysis.py`

```markdown
## Unit Testing

Ensure you have a test database setup. Run the unit tests to verify the functionality:

```bash
python -m unittest test_analysis.py
```

#### Acknowledgments

- National Library of Medicine for providing access to PubMed citation files.

- PostgreSQL Community for the database system.
- Python Community for the programming language and libraries.
