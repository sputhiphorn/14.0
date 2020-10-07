import logging
from odoo import http,tools
from odoo.addons.restful.common import invalid_response, valid_response
from odoo.http import request
_logger = logging.getLogger(__name__)

expires_in = "restful.access_token_expires_in"
store_mapping_1 = "restful.store_mapping_1"
store_mapping_2 = "restful.store_mapping_2"


class AccessToken(http.Controller):
    """."""

    @http.route("/api/auth/token", methods=["POST"], type="http", auth="none", csrf=False)
    def token(self, **post):
        """The token URL to be used for getting the access_token:

        Args:
            **post must contain login and password.
        Returns:

            returns https response code 404 if failed error message in the body in json format
            and status code 202 if successful with the access_token.
        Example:
           import requests

           headers = {'content-type': 'text/plain', 'charset':'utf-8'}

           data = {
               'login': 'admin',
               'password': 'admin',
               'db': 'galago.ng'
            }
           base_url = 'http://odoo.ng'
           eq = requests.post(
               '{}/api/auth/token'.format(base_url), data=data, headers=headers)
           content = json.loads(req.content.decode('utf-8'))
           headers.update(access-token=content.get('access_token'))
        """
        _token = request.env["api.access.token"]
        params = ["db", "login", "password"]
        params = {key: post.get(key) for key in params if post.get(key)}
        db_name = tools.config.get('db_name')
        db, username, password = (params.get("db") or db_name,post.get("login"),post.get("password"),)
        _credentials_includes_in_body = all([db, username, password])
        if not _credentials_includes_in_body:
            # The request post body is empty the credetials maybe passed via the headers.
            headers = request.httprequest.headers
            db = headers.get("db") or db_name
            username = headers.get("login")
            password = headers.get("password")
            _credentials_includes_in_headers = all([db, username, password])
            if not _credentials_includes_in_headers:
                # Empty 'db' or 'username' or 'password:
                return invalid_response(
                    "Missing error",
                    "Either of the following are missing [username,password]",
                    403,
                )
        # Login in odoo database:
        try:
            request.session.authenticate(db, username, password)
        except Exception as e:
            # Invalid database:
            info = "The database name is not valid {}".format((e))
            error = "invalid_database"
            _logger.error(info)
            return invalid_response(error, info,400)

        uid = request.session.uid
        # odoo login failed:
        if not uid:
            info = "Authentication failed"
            error = "Authentication failed"
            _logger.error(info)
            return invalid_response(error, info,401)

        # Generate tokens
        access_token = _token.find_one_or_create_token(user_id=uid, create=True)
        # Successful response:
        return valid_response({
                    "uid": uid,
                    "access_token": access_token,
                },
            status=200,
        )

    @http.route(
        "/api/auth/token", methods=["DELETE"], type="http", auth="none", csrf=False
    )
    def delete(self, **post):
        """."""
        _token = request.env["api.access.token"]
        access_token = request.httprequest.headers.get("access_token")
        access_token = _token.search([("token", "=", access_token)])
        if not access_token:
            info = "No access token was provided in request!"
            error = "No Access Token"
            _logger.error(info)
            return invalid_response(error, info)
        return valid_response(access_token.unlink())