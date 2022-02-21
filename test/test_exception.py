import unittest

import ddt
import requests

from qrest.exception import (
    RestAccessDeniedError,
    RestBadRequestError,
    RestInternalServerError,
    RestResourceNotFoundError,
    raise_on_response_error,
)


@ddt.ddt
class RaiseOnResponseErrorTests(unittest.TestCase):
    def test_raise_on_400(self):
        response = requests.Response()
        response.url = "https://jsonplaceholder.typicode.com/posts"
        response.status_code = 400

        with self.assertRaises(RestBadRequestError) as cm:
            raise_on_response_error(response)

        exc = cm.exception
        self.assertEqual(
            "Bad request for resource https://jsonplaceholder.typicode.com/posts", str(exc)
        )

    def test_raise_on_404(self):
        response = requests.Response()
        response.url = "https://jsonplaceholder.typicode.com/posts"
        response.status_code = 404

        with self.assertRaises(RestResourceNotFoundError) as cm:
            raise_on_response_error(response)

        exc = cm.exception
        self.assertEqual("Object could not be found in database", str(exc))

    @ddt.data(401, 402, 403)
    def test_raise_on_40x(self, status_code):
        response = requests.Response()
        response.url = "https://jsonplaceholder.typicode.com/posts"
        response.status_code = status_code

        with self.assertRaises(RestAccessDeniedError) as cm:
            raise_on_response_error(response)

        exc = cm.exception
        self.assertEqual(
            f"error {status_code}: "
            "Access is denied to resource https://jsonplaceholder.typicode.com/posts",
            str(exc),
        )

    def test_raise_on_500(self):
        response = requests.Response()
        response.url = "https://jsonplaceholder.typicode.com/posts"
        response.status_code = 500
        response.reason = "reason"

        with self.assertRaises(RestInternalServerError) as cm:
            raise_on_response_error(response)

        exc = cm.exception
        self.assertEqual("error 500: Internal Server error (reason)", str(exc))

    def test_raise_on_600(self):
        response = requests.Response()
        response.url = "https://jsonplaceholder.typicode.com/posts"
        response.status_code = 600
        response.reason = "reason"

        with self.assertRaises(Exception) as cm:
            raise_on_response_error(response)

        exc = cm.exception
        self.assertEqual("REST error 600: reason", str(exc))

    @ddt.data(100, 200, 300, 399)
    def test_status_code_below_400_doesnt_raise_an_exception(self, status_code):
        response = requests.Response()
        response.url = "https://jsonplaceholder.typicode.com/posts"
        response.status_code = status_code

        raise_on_response_error(response)
