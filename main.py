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


def parse_and_prepare_data(xml_root):
    """
    Parses XML data and prepares it for insertion into the database.

    :param xml_root: The root of the parsed XML document.
    :return: A list of tuples with the data to be inserted.
    """
    data = []
    for PubmedArticle in xml_root.findall('.//PubmedArticle'):
        pmid = PubmedArticle.find('.//PMID').text
        article_title = PubmedArticle.find('.//Article/ArticleTitle').text
        first_author = PubmedArticle.find(
            './/Article/AuthorList/Author/LastName').text  # Adjust path as needed
        publisher = PubmedArticle.find(
            './/Journal/Title').text  # Adjust path as needed
        published_date = PubmedArticle.find(
            './/ArticleDate/Year').text  # Adjust path as needed
        uploader = 'Your Name'  # Replace with your name or a variable
        # Adjust the fields and paths according to your XML structure and requirements
        data.append((pmid, article_title, first_author,
                    publisher, published_date, uploader))
    return data


def main(xml_gz_file_name):
    """
    Main function to process the XML file and insert data into the database.

    :param xml_gz_file_name: str
        The file name of the PubMed XML GZ file to be processed. 
    """
    # Open the gzip file
    with gzip.open(xml_gz_file_name, 'r') as pubmed_file:
        byte_string = pubmed_file.read()

    content = byte_string.decode("utf-8")
    root = ET.fromstring(content)

    # Connect to the database
    conn = connect_db(db_params)
    if conn is not None:
        create_table(conn)

        # Prepare data for insertion
        data = parse_and_prepare_data(root)

        insert_data(conn, data)
        print("Data insertion completed")

        conn.close()


if __name__ == "__main__":
    main("data/pubmed24n1158.xml")
