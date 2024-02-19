import unittest
from analysis import get_date_range, get_top_authors, get_citations_by_top_authors, get_articles_with_most_keywords, get_avg_publications_per_author_per_year, connect_db


class TestAnalysis(unittest.TestCase):

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
        pass

    def test_get_top_authors(self):
        pass

    def test_get_citations_by_top_authors(self):
        pass

    def test_avg_publications_per_author_per_year(self):
        pass

if __name__ == '__main__':
    unittest.main()
