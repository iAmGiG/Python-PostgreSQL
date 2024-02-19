import gzip
import xml.etree.ElementTree as ET
import psycopg2
import psycopg2.extras

# Define database connection parameters (the default is the PostgreSQL localhost,
# so we'll use this here as we will just use a VM to run the solution.)
db_params = {
    "database": "mydb",
    "user": "myuser",
    "password": "mypassword",
    "host": "localhost",
    "port": "5432"
}


def connect_db(params):
    """
    Function to establish a connection to the database.

    :param params: dict
        A dictionary containing database connection parameters such as database, user, password, host, and port.
    """
    try:
        conn = psycopg2.connect(**params)
        print("Database connection established")
        return conn
    except Exception as e:
        print("Database connection error:", e)
        return None


def create_table(conn):
    """
    Function to create the table in the database.

    :param conn: psycopg2.extensions.connection
        The connection object to the PostgreSQL database.
    """
    cursor = conn.cursor()
    table_create_query = """
    CREATE TABLE IF NOT EXISTS pubmed_articles (
        pmid NUMERIC(8) PRIMARY KEY,
        article_title VARCHAR(255),
        first_author VARCHAR(63),
        publisher VARCHAR(127),
        publication_date DATE,
        uploader VARCHAR(127)
    );
    """
    cursor.execute(table_create_query)
    conn.commit()
    print("Table created successfully")
    cursor.close()


def insert_data(conn, data):
    """
    Function to insert data into the table.

    :param conn: psycopg2.extensions.connection
        The connection object to the PostgreSQL database.
    :param data: list of tuples
        A list of tuples, where each tuple contains data for one row to be inserted.
    """
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO pubmed_articles (pmid, article_title, first_author, publisher, published_date, uploader)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (pmid) DO NOTHING;
    """
    psycopg2.extras.execute_batch(cursor, insert_query, data)
    conn.commit()
    cursor.close()


def main(xml_gz_file_name):
    """
    Main function to process the XML file and insert data into the database.

    :param xml_gz_file_name: str
        The file name of the PubMed XML GZ file to be processed. 
    """
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
    main("data/pubmed24n1158.xml")
