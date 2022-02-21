"""
local exceptions
"""

from requests.models import Response


# ================================================================================================
class RestClientException(Exception):
    """ wrapper exception """

    pass


class RestClientResourceError(RestClientException):
    """ wrapper exception """

    pass


class RestClientConfigurationError(RestClientException):
    """ wrapper exception """

    pass


class RestClientValidationError(RestClientException):
    """ wrapper exception """

    pass


class RestClientQueryError(RestClientException):
    """ wrapper exception """

    pass


class InvalidTargetError(RestClientException):
    """An error when specifying an invalid target for a given REST API."""

    pass

    # def __init__(self, name, target):
    # """ InvalidTargetError constructor

    # :param name: The name of the REST API client
    # :type name: ``string``

    # :param target: The REST API target name
    # :type target: ``string``

    # """
    # super()"'{target}' is not a valid target for '{name}'".format(
    # target=target,
    # name=name
    # ))


class InvalidResourceError(RestClientException):
    """An error when specifying an invalid resource for a given REST API."""

    def __init__(self, name: str, resource: str):
        """ InvalidResourceError constructor

            :param name: The name of the REST API client
            :param resource: The REST API resource name

        """
        response = f"'{resource}' is not a valid resource for '{name}'"
        super().__init__(response)


class RestResourceMissingContentError(RestClientResourceError):
    """ wrapper exception """

    pass


class RestResourceNotFoundError(RestClientResourceError):
    """ wrapper exception """

    pass


class RestAccessDeniedError(RestClientResourceError):
    """ wrapper exception """

    pass


class RestCredentailsError(RestClientResourceError):
    """ wrapper exception """

    pass


class RestInternalServerError(RestClientResourceError):
    """ wrapper exception """

    pass


class RestBadRequestError(RestClientResourceError):
    """ wrapper excpetion """

    pass


def raise_on_response_error(response: Response):
    """Raise custom exception for response status (code) 400 and higher.

    If the status code is below 400, this function calls
    response.raise_for_status and it is up to that function what to do.

    """
    if response.status_code < 400:
        response.raise_for_status()
    elif response.status_code == 400:
        raise RestBadRequestError("Bad request for resource %s" % response.url)
    elif response.status_code in (401, 402, 403):
        raise RestAccessDeniedError(
            "error %d: Access is denied to resource %s" % (response.status_code, response.url)
        )
    elif response.status_code == 404:
        raise RestResourceNotFoundError("Object could not be found in database")
    elif response.status_code == 500:
        raise RestInternalServerError(
            "error %d: Internal Server error (%s)" % (response.status_code, response.reason)
        )
    else:
        raise Exception("REST error %d: %s" % (response.status_code, response.reason))
