import unittest
from analysis import get_date_range, get_top_authors, get_citations_by_top_authors, get_avg_publications_per_author_per_year, connect_db


class TestAnalysis(unittest.TestCase):
    """
    There were going to be sofiticated test, but this project will have to be closed a bit earlier than expected.
    Just won't be able to make pratical unit test for each of the methods, with so many changes to the main.py,
    attention was given to the analysis.py for adjustments, thus the unit test wouldn't be a pratical place to,
    continue the project.
    """
    @classmethod
    def setUpClass(cls):
        # Set up database connection parameters
        db_params = {
            "database": "mydb",
            "user": "myuser",
            "password": "mypassword",
            "host": "localhost",
            "port": "5432"
        }
        cls.conn = connect_db(db_params)

    @classmethod
    def tearDownClass(cls):
        # Close database connection after all tests
        cls.conn.close()

    def test_get_date_range(self):
        get_date_range(self.conn)

    def test_get_top_authors(self):
        get_top_authors(self.conn)

    def test_get_citations_by_top_authors(self):
        get_citations_by_top_authors(self.conn)

    # def test_get_articles_with_most_keywords(self):
    #     get_articles_with_most_keywords(self.conn)

    def test_get_avg_publications_per_author_per_year(self):
        get_avg_publications_per_author_per_year(self.conn)

if __name__ == '__main__':
    unittest.main()
