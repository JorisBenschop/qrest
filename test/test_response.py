import unittest
import unittest.mock as mock

import requests

from qrest.response import JSONResponse

# the following content has been copied from the response to
# https://jsonplaceholder.typicode.com/posts and extended
_POSTS = [
    {
        "userId": 1,
        "id": 1,
        "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
        "body": {
            "intro": "alea iacta est",
            "main": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto",
        },
    },
    {
        "userId": 1,
        "id": 2,
        "title": "qui est esse",
        "body": {
            "intro": "et tu, Brute?",
            "main": "est rerum tempore vitae\nsequi sint nihil reprehenderit dolor beatae ea dolores neque\nfugiat blanditiis voluptate porro vel nihil molestiae ut reiciendis\nqui aperiam non debitis possimus qui neque nisi nulla",
        },
    },
]


class JSONResponseTests(unittest.TestCase):
    def test_fetch_all_posts(self):
        mock_response = mock.Mock(spec=requests.Response)
        mock_response.headers = {"Content-type": "application/json; charset=UTF-8"}
        mock_response.json = mock.Mock(return_value=_POSTS)

        response = JSONResponse()(mock_response)

        expected_content = _POSTS
        self.assertEqual(expected_content, response.fetch())

    def test_fetch_single_post(self):
        single_post = _POSTS[0]

        mock_response = mock.Mock(spec=requests.Response)
        mock_response.headers = {"Content-type": "application/json; charset=UTF-8"}
        mock_response.json = mock.Mock(return_value=single_post)

        response = JSONResponse()(mock_response)

        expected_content = single_post
        self.assertEqual(expected_content, response.fetch())

    def test_fetch_body_of_single_post(self):
        single_post = _POSTS[0]

        mock_response = mock.Mock(spec=requests.Response)
        mock_response.headers = {"Content-type": "application/json; charset=UTF-8"}
        mock_response.json = mock.Mock(return_value=single_post)

        response = JSONResponse(extract_section=["body"])(mock_response)

        expected_content = single_post["body"]
        self.assertEqual(expected_content, response.fetch())
        self.assertEqual(expected_content, response.results)

    def test_fetch_intro_of_single_post(self):
        single_post = _POSTS[0]

        mock_response = mock.Mock(spec=requests.Response)
        mock_response.headers = {"Content-type": "application/json; charset=UTF-8"}
        mock_response.json = mock.Mock(return_value=single_post)

        response = JSONResponse(extract_section=["body", "intro"])(mock_response)

        expected_content = single_post["body"]["intro"]
        self.assertEqual(expected_content, response.fetch())
        self.assertEqual(expected_content, response.results)
