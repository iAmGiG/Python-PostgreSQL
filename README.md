# Python-PostgreSQL
This project uses a PostgreSQL database adapter to create a relation and populate it with data from a collection of PubMed citation documents. It demonstrates the integration of Python with PostgreSQL for managing and analyzing data, specifically focusing on parsing XML files, data insertion, and performing SQL queries for analysis.

# Python and PostgreSQL

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

### Configuration
Before running the application, ensure your PostgreSQL server is running and accessible. You will need to configure your database connection details (e.g., database name, user, password, host, and port) in the application.

### Usage
* Step 1: Data Preparation
Download a PubMed archive file from the National Library of Medicine at https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/. Select a .xml.gz file which contains up to 30,000 PubMed citations.

* Step 2: Parsing and Database Insertion
Run the provided Python script to parse the downloaded XML file and insert citation data into the PostgreSQL database. The script creates a table with specific attributes for each citation and handles data insertion.

* Step 3: Data Analysis
Execute the SQL queries included in the repository to analyze the citation data. The queries cover a range of analyses, such as finding the range of publication dates, identifying the most prolific authors, and more.

#### Acknowledgments
* National Library of Medicine for providing access to PubMed citation files.
* PostgreSQL Community for the database system.
* Python Community for the programming language and libraries.
