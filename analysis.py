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
        print(
            f"Date From  |  Date To\n{'-' * 11}+{'-' * 11}\n{result[0]}  |  {result[1]}")

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
        max_name_length = max(len(row[0])
                              for row in results) if results else 10
        header_format = f"{{:<{max_name_length}}} | {{:}}\n"
        row_format = f"{{:<{max_name_length}}} | {{}}\n"
        print(header_format.format("First Author", "Count"))
        print('-' * max_name_length + '-+-' + '-' * 5)
        for row in results:
            print(row_format.format(row[0], row[1]))
            authors.append(row[0])
    return authors

# %%
# Q3


def get_citations_by_top_authors(conn, authors):
    """
    Print all citations published by the authors identified during Q2 get top authors.

    :param conn: The database connection object.
    :param authors: A list of author names identified as the most prolific.
    """
    for author in authors:
        query = """
            SELECT pmid, first_author, article_title, publisher, published_date
            FROM pubmed_articles
            WHERE first_author = %s
            ORDER BY published_date;
            """
        with conn.cursor() as cursor:
            cursor.execute(query, (author,))
            print(f"Citations by {author}:")
            print(
                f"{'PMID':<10} | {'Author':<20} | {'Title':<50} | {'Publisher':<30} ")
            print('-'*130)
            for row in cursor.fetchall():
                truncated_title = ' '.join(
                    row[2].split()[:8]) + ('...' if len(row[2].split()) > 8 else '')
                print(
                    f"{row[0]:<10} | {row[1]:<10} | {truncated_title:<20} | {row[3]:<30} ")
            print("\n")
# %%
# Q4


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
        print(f"{'Author':<20} | {'Year':<10} | {'Avg. Publications':<20}")
        print(f"{'-'*20}+{'-'*10}+{'-'*20}")
        for row in cursor.fetchall():
            year = str(row[1]) if row[1] != 0 else 'Unknown'
            print(f"{row[0]:<20} | {year:<10} | {row[2]:<20.2f}")


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
        print("Print get average publications per authors per year:\n")
        get_avg_publications_per_author_per_year(conn)
        print("\n------\n")
        conn.close()
