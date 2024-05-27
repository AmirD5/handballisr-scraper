from unittest.mock import patch, MagicMock, call
import scraper


# test if response code is correctly inserted into response
@patch('requests.get')
def test_successful_http_response(mock_get):
    mock_get.return_value.status_code = 200
    response = scraper.get_response()
    assert response.status_code == 200


# test if a non 200 response code is correctly inserted into response
@patch('requests.get')
def test_non_200_http_response(mock_get):
    mock_get.return_value.status_code = 404
    response = scraper.get_response()
    assert response is None


@patch('scraper.requests.get') #replaces the actual requests.get method with mock object
def test_html_parsing(mock_get): # the mock object if passed as mock_get to the test function
    mock_response = MagicMock() #a magic mock object is created to simulate HTML response

    #setting the mock response attributes
    mock_response.status_code = 200
    mock_response.text = '''
    <html>
        <a tabindex="1" href="/test-url-1"><h2>Test Headline 1</h2></a>
        <a tabindex="1" href="/test-url-2"><h2>Test Headline 2</h2></a>
    </html>
    '''
    mock_response.encoding = 'utf-8'

    #sets the mock return value to the mock response we set earlier
    mock_get.return_value = mock_response

    # replaces the fetch_all_headlines with a mock that returns an empty set,simulating no headlines present in the db
    with patch('scraper.fetch_all_headlines', return_value=set()):
        with patch('scraper.save_to_database') as mock_save: # replaces save_to_database with mock named mock_save
            scraper.scrape_sports_news()
            calls = [
                call('Test Headline 1', 'No summary available', 'https://www.handballisr.co.il/test-url-1'),
                call('Test Headline 2', 'No summary available', 'https://www.handballisr.co.il/test-url-2')
            ]
            #now mock_save will use save_to_database once with the specified argument
            mock_save.assert_has_calls(calls, any_order=True)


@patch('scraper.requests.get')
def test_scrape_summary_from_url(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '<html><h2>Test Summary</h2></html>'
    mock_response.encoding = 'utf-8'
    mock_get.return_value = mock_response

    summary = scraper.scrape_summary_from_url('http://example.com')
    assert summary == 'Test Summary'


@patch('scraper.requests.get')
def test_scrape_summary_no_summary(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '<html></html>'
    mock_response.encoding = 'utf-8'
    mock_get.return_value = mock_response

    summary = scraper.scrape_summary_from_url('http://example.com')
    assert summary == 'No summary available'


@patch('scraper.requests.get')
def test_scrape_summary_failed_request(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    summary = scraper.scrape_summary_from_url('http://example.com')
    assert summary == 'Article not available'









