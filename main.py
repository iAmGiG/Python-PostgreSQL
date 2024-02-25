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
    The 'IF NOT EXISTS' in the query will prevent recreation of the table.
    :param conn: psycopg2.extensions.connection
        The connection object to the PostgreSQL database.
    """
    print("Starting to create table.")
    cursor = conn.cursor()
    table_create_query = """
    CREATE TABLE IF NOT EXISTS pubmed_articles (
        pmid NUMERIC(8) PRIMARY KEY,
        article_title VARCHAR(255),
        first_author VARCHAR(63),
        publisher VARCHAR(127),
        published_date DATE,
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
    print("Begining to insert data.")
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO pubmed_articles (pmid, article_title, first_author, publisher, published_date, uploader)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (pmid) DO NOTHING;
    """
    psycopg2.extras.execute_batch(cursor, insert_query, data)
    conn.commit()
    print("Finishing insert data.")
    cursor.close()


def parse_and_prepare_data(xml_root):
    """
    Parses XML data and prepares it for insertion into the database.
    Checks for missing first authors, publishers, and publication dates within PubMed articles. 
    Each element is validated for existence before attempting to extract text;
    if not found, 'None' is assigned.
    :param xml_root: The root of the parsed XML document.
    :return: A list of tuples with the data to be inserted.
    """
    print("Begining parase and prep data.")
    data = []
    for PubmedArticle in xml_root.findall('.//PubmedArticle'):
        pmid = PubmedArticle.find('.//PMID').text
        article_title = PubmedArticle.find('.//Article/ArticleTitle').text
        first_author_element = PubmedArticle.find(
            './/Article/AuthorList/Author/LastName')
        first_author = first_author_element.text if first_author_element is not None else 'None'
        publisher_element = PubmedArticle.find('.//Journal/Title')
        publisher = publisher_element.text if publisher_element is not None else 'None'

        '''To construct the published_date.
        first check if the PubDate element and its child elements (Year, Month, Day) exist.
        If the Year is not present, it defaults the entire published_date to 'None'.
        If Year is present but Month or Day are missing, it defaults them to '01' to ensure a valid date format.
        Additionally: ensure that there are checks for None at each step of accessing child elements, 
        which prevents trying to access .text on a NoneType object.
        '''
        pub_date_element = PubmedArticle.find('.//PubDate')
        year_element = pub_date_element.find(
            'Year') if pub_date_element is not None else None
        year = year_element.text if year_element is not None else 'None'
        month_element = pub_date_element.find(
            'Month') if pub_date_element is not None else None
        month = month_element.text if month_element is not None else '01'
        day_element = pub_date_element.find(
            'Day') if pub_date_element is not None else None
        day = day_element.text if day_element is not None else '01'
        published_date = f"{year}-{month}-{day}" if year != 'None' else 'None'

        uploader = 'Mr.Uploader'
        data.append((pmid, article_title, first_author,
                    publisher, published_date, uploader))
    print("Ending parase and prep data.")
    return data


def main(file_name):
    """
    Main function to process the XML file and insert data into the database.
    Can handle .gz or the raw xml files types.
    :param xml_gz_file_name: str
        The file name of the PubMed XML GZ file to be processed. 
    """
    # Open the gzip file
    if file_name.endswith('.gz'):
        with gzip.open(file_name, 'r') as file:
            byte_string = file.read()
    else:
        with open(file_name, 'r') as file:
            byte_string = file.read().encode('utf-8')

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
    main("data/pubmed24n1158.xml.gz")
