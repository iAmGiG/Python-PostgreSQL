import gzip
import xml.etree.ElementTree as ET
import psycopg2
import psycopg2.extras

# Define database connection parameters (replace placeholders with your actual details)
db_params = {
    "database": "your_database",
    "user": "your_username",
    "password": "your_password",
    "host": "localhost",
    "port": "5432"
}

# Function to connect to the database
def connect_db(params):
    try:
        conn = psycopg2.connect(**params)
        print("Database connection established")
        return conn
    except Exception as e:
        print("Database connection error:", e)
        return None

# Function to create table (replace with your actual table schema)
def create_table(conn):
    cursor = conn.cursor()
    table_create_query = """
    CREATE TABLE IF NOT EXISTS pubmed_articles (
        pmid VARCHAR PRIMARY KEY,
        article_title TEXT,
        publication_date DATE,
        abstract TEXT
        -- Add more fields as needed
    );
    """
    cursor.execute(table_create_query)
    conn.commit()
    print("Table created successfully")
    cursor.close()

# Function to insert data into the table
def insert_data(conn, data):
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO pubmed_articles (pmid, article_title, publication_date, abstract)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (pmid) DO NOTHING;
    """
    psycopg2.extras.execute_batch(cursor, insert_query, data)
    conn.commit()
    cursor.close()

# Main function to process the XML file and insert data into the database
def main(xml_gz_file_name):
    pubmed_file = gzip.open(xml_gz_file_name, 'r')
    byte_string = pubmed_file.read()
    content = byte_string.decode("utf-8")
    root = ET.fromstring(content)

    # Connect to the database
    conn = connect_db(db_params)
    if conn is not None:
        create_table(conn)

        # Prepare data for insertion
        data = []
        for PubmedArticle in root.findall('.//PubmedArticle'):
            pmid = PubmedArticle.find('.//PMID').text
            article_title = PubmedArticle.find('.//ArticleTitle').text
            publication_date = PubmedArticle.find('.//PubDate/Year').text
            abstract = PubmedArticle.find('.//Abstract/AbstractText').text
            # Add more fields as necessary
            data.append((pmid, article_title, publication_date, abstract))

        insert_data(conn, data)
        print("Data insertion completed")

        conn.close()

if __name__ == "__main__":
    main("your_pubmed_file.xml.gz")
