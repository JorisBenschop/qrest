import unittest
import unittest.mock as mock

import pytest
import requests

import rest_client
from rest_client import APIConfig
from rest_client import QueryParameter, BodyParameter, ResourceConfig
from rest_client.response import Response


class JsonPlaceHolderConfig(APIConfig):
    url = "https://jsonplaceholder.typicode.com"
    default_headers = {"Content-type": "application/json; charset=UTF-8"}

    all_posts = ResourceConfig(path=["posts"], method="GET", description="retrieve all posts")

    filter_posts = ResourceConfig(
        path=["posts"],
        method="GET",
        description="retrieve all posts by filter criteria",
        parameters={
            "user_id": QueryParameter(
                name="userId",
                required=False,
                # default='',
                # choices=[],
                description="the user Id that made the post",
            ),
        },
    )

    single_post = ResourceConfig(
        path=["posts", "{item}"],
        method="GET",
        description="Retrieve a single post",
        path_description={"item": "select the post ID to retrieve"},
        headers={"X-test-post": "qREST python ORM"},
    )

    comments = ResourceConfig(
        path=["posts", "{post_id}", "comments"],
        method="GET",
        description="Retrieve comments for a single post",
        path_description={"post_id": "select the post ID to retrieve"},
    )

    create_post = ResourceConfig(
        path=["posts"],
        method="POST",
        description="Create a new post",
        parameters={
            "title": BodyParameter(
                name="title",
                required=True,
                # default='',
                # choices=[],
                description="The title of the post",
            ),
            "content": BodyParameter(
                name="body",
                required=True,
                # default='',
                # choices=[],
                description="The title of the post",
            ),
            "user_id": BodyParameter(
                name="userId",
                required=False,
                default=101,
                # choices=[],
                description="The id of the user creating the post",
            ),
        },
    )


class PassthroughResponse(Response):
    """Provide access to the requests.Response that is wrapped.

    The rest_client.API uses a Response to process the requests.Response it
    receives from the endpoint. That processing requires specific responses and
    would make the setup of the API tests much more elaborate and the tests
    themselves much less focussed on the API. To work around that, we use a
    PassthroughResponse for the tests, which does no processing at all.

    Note that Response objects have their own tests and do not have to be
    tested by the API tests.

    """

    def __init__(self):
        pass

    def fetch(self):
        """Return the requests.Response object received."""
        return self._response

    def _check_content(self):
        pass

    def _parse(self):
        pass


class TestJsonPlaceHolderGet(unittest.TestCase):
    def setUp(self):
        self.config = JsonPlaceHolderConfig()

    def test_all_posts_queries_the_right_endpoint(self):
        api = rest_client.API(self.config)
        api.all_posts.response_class = PassthroughResponse()

        with mock.patch("requests.request") as mock_request:
            mock_response = mock.Mock(spec=requests.Response)
            mock_response.status_code = 200
            mock_response.content = b"Hello World!"
            # for this test we're not interested in the headers attribute of
            # the requests.Response but our Response object requires it
            mock_response.headers = {}
            mock_request.return_value = mock_response

            response = api.all_posts.fetch()

            mock_request.assert_called_with(
                method="GET",
                auth=None,
                verify=False,
                url="https://jsonplaceholder.typicode.com/posts",
                params={},
                json={},
                headers={"Content-type": "application/json; charset=UTF-8"},
            )

            self.assertEqual(b"Hello World!", response.content)

    def test_single_post_queries_the_right_endpoint(self):
        api = rest_client.API(self.config)
        api.single_post.response_class = PassthroughResponse()

        with mock.patch("requests.request") as mock_request:
            mock_response = mock.Mock(spec=requests.Response)
            mock_response.status_code = 200
            mock_response.content = b"Hello World!"
            # for this test we're not interested in the headers attribute of
            # the requests.Response but our Response object requires it
            mock_response.headers = {}
            mock_request.return_value = mock_response

            response = api.single_post.fetch(item=1)

            mock_request.assert_called_with(
                method="GET",
                auth=None,
                verify=False,
                url="https://jsonplaceholder.typicode.com/posts/1",
                params={},
                json={},
                headers={
                    "Content-type": "application/json; charset=UTF-8",
                    "X-test-post": "qREST python ORM",
                },
            )

            self.assertEqual(b"Hello World!", response.content)

    @pytest.mark.skip(reason="unable to reach jsonplaceholder.typicode.com")
    def test_filter_posts_fetch(self):
        """
        check method or path
        """
        x = rest_client.API(self.config)
        response = x.filter_posts.fetch(user_id=1)
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 10)

    @pytest.mark.skip(reason="unable to reach jsonplaceholder.typicode.com")
    def test_filter_posts_response(self):
        """
        check method or path
        """
        x = rest_client.API(self.config)
        resource = x.filter_posts(user_id=1)
        response = resource.data

        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 10)

    @pytest.mark.skip(reason="unable to reach jsonplaceholder.typicode.com")
    def test_posts_comments(self):
        """
        check method or path
        """
        x = rest_client.API(self.config)
        response = x.comments.fetch(post_id=1)
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 5)


class TestJsonPlaceHolderPost(unittest.TestCase):
    def setUp(self):
        self.config = JsonPlaceHolderConfig()

    @pytest.mark.skip(reason="unable to reach jsonplaceholder.typicode.com")
    def test_new_post(self):
        """
        create a new post
        """
        x = rest_client.API(self.config)
        print(x.create_post.help("title"))

        title = "new post using qREST ORM"
        content = "this is the new data posted using qREST"
        user_id = 200

        # send data to jsonplaceholder server
        response = x.create_post(title=title, content=content, user_id=user_id)
        self.assertIsInstance(response.data, dict)

        self.assertEqual(response.data["userId"], user_id)

        # also test using default values
        response = x.create_post(title=title, content=content)
        self.assertIsInstance(response.data, dict)

        self.assertEqual(response.data["userId"], 101)
