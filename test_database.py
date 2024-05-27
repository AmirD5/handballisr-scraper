import pytest
from unittest.mock import patch, MagicMock
import database

# using mock objects to test all functions of database.py


# will test the commit of the database creation
@patch('database.sqlite3.connect')
def test_create_database_commit(mock_connect):
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    database.create_database()
    mock_conn.commit.assert_called_once()


# will test the closing of the database creation
@patch('database.sqlite3.connect')
def test_create_database_close(mock_connect):
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    database.create_database()
    mock_conn.close.assert_called_once()


# will test the commit of the database save
@patch('database.sqlite3.connect')
def test_save_to_database_commit(mock_connect):
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    database.save_to_database('Test Headline', 'Test Summary', 'http://test.url')
    mock_conn.commit.assert_called_once()


# will test the closing of the database save
@patch('database.sqlite3.connect')
def test_save_to_database_close(mock_connect):
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    database.save_to_database('Test Headline', 'Test Summary', 'http://test.url')
    mock_conn.close.assert_called_once()


# test if the function fetches properly
@patch('database.sqlite3.connect')
def test_fetch_all_articles(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [('Test Headline', 'Test Summary', 'http://test.url')]
    mock_connect.return_value = mock_conn
    articles = database.fetch_all_articles()
    assert articles == [('Test Headline', 'Test Summary', 'http://test.url')]


# test if the function fetches properly
@patch('database.sqlite3.connect')
def test_fetch_article_by_headline(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = ('Test Headline', 'Test Summary', 'http://test.url')
    mock_connect.return_value = mock_conn
    article = database.fetch_article_by_headline('Test Headline')
    assert article == ('Test Headline', 'Test Summary', 'http://test.url')


# test if the function fetches properly
@patch('database.sqlite3.connect')
def test_fetch_all_headlines(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [('Test Headline',)]
    mock_connect.return_value = mock_conn
    headlines = database.fetch_all_headlines()
    assert headlines == ['Test Headline']
