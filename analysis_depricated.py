# %%
import psycopg2
# use the main to run all test at once.
db_params = {
    "database": "mydb",
    "user": "myuser",
    "password": "mypassword",
    "host": "localhost",
    "port": "5432"
}

# %%


def connect_db(params):
    """
    Connect to the database using provided parameters.
    params: params to connect with.
    """
    try:
        return psycopg2.connect(**params)
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

# %%
# Q1


def get_date_range(conn):
    """Find the range of published dates."""
    query = """
    SELECT MIN(published_date) AS "Date From", MAX(published_date) AS "Date To"
    FROM pubmed_articles;
    """
    with conn.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()
        print(f"Date From | Date To\n{result[0]} | {result[1]}")

# %%
# Q2


def get_top_authors(conn):
    """Find the top five most prolific authors."""
    query = """
    SELECT first_author, COUNT(*) AS cnt
    FROM pubmed_articles
    GROUP BY first_author
    ORDER BY cnt DESC
    LIMIT 5;
    """
    authors = []
    with conn.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
        print("First Author | cnt")
        for row in results:
            print(f"{row[0]} | {row[1]}")
            authors.append(row[0])
    return authors

# %%
# Q3


def get_citations_by_top_authors(conn, authors):
    """
    Print all citations published by the authors identified in Q2.

    :param conn: The database connection object.
    :param authors: A list of author names identified as the most prolific.
    """
    for author in authors:
        query = """
        SELECT article_title, published_date
        FROM pubmed_articles
        WHERE first_author = %s
        ORDER BY published_date;
        """
        with conn.cursor() as cursor:
            cursor.execute(query, (author,))
            print(f"Citations by {author}:")
            for row in cursor.fetchall():
                print(f"Title: {row[0]}, Date: {row[1]}")
            print("\n")
# %%
# Q4


def get_articles_with_most_keywords(conn):
    """
    Finds articles with the most keywords associated.
    -------Unfortunatly we never made the keywords column and processing feature in main.---------
    """
    query = """
    SELECT article_title, COUNT(keyword) AS keyword_count
    FROM pubmed_articles
    GROUP BY article_title
    ORDER BY keyword_count DESC
    LIMIT 5;
    """
    with conn.cursor() as cursor:
        cursor.execute(query)
        print("Articles with the Most Keywords:")
        for row in cursor.fetchall():
            print(f"Title: {row[0]}, Keywords: {row[1]}")


def get_avg_publications_per_author_per_year(conn):
    """
    Calculates the average number of publications for each author annually,
    excluding entries with NULL published_date.
    """
    query = """
    SELECT first_author, COALESCE(EXTRACT(YEAR FROM published_date), 0) AS year, 
           COUNT(*)::float / COUNT(DISTINCT first_author) AS avg_publications
    FROM pubmed_articles
    WHERE published_date IS NOT NULL
    GROUP BY first_author, year
    ORDER BY first_author, year;
    """
    with conn.cursor() as cursor:
        cursor.execute(query)
        print("Average Publications per Author per Year:")
        for row in cursor.fetchall():
            year = int(row[1]) if row[1] != 0 else 'Unknown'  # Handle the COALESCE default value
            print(f"Author: {row[0]}, Year: {year}, Avg. Publications: {row[2]:.2f}")


# %%
if __name__ == "__main__":
    conn = connect_db(db_params)
    if conn:
        # Q1
        print("Print get date range:\n")
        get_date_range(conn)
        print("\n------\n")
        # Q2
        print("Print get top authors:\n")
        retrieved_top_authors = get_top_authors(conn)
        print("\n------\n")
        # Q3
        print("Print get citaitons by top authors:\n")
        get_citations_by_top_authors(conn, authors=retrieved_top_authors)
        print("\n------\n")
        # Q4
        # get_articles_with_most_keywords(conn) --- We never got to make the keywords process in main, scope creep.
        print("Print get average publications per authors per year:\n")
        get_avg_publications_per_author_per_year(conn)
        print("\n------\n")
        conn.close()
