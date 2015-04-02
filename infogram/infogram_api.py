try:
    import simplejson as json
except ImportError:
    import json
import requests
import six
import urllib
import hmac
import base64

from infogram.exceptions import *
from decimal import Decimal
from hashlib import sha1
from collections import OrderedDict

class Infogram(object):
    def __init__(self, api_key, api_secret, url='https://infogr.am/service/v1', timeout=None):
        self.url        = url.strip('/')
        self.session    = requests.Session()
        self.api_key    = api_key
        self.api_secret = api_secret
        self.timeout    = timeout

    def _extend_exception(self, exception, message):
        if not exception.args:
            exception.args = ('',)
        exception.args = (message + ': ' + exception.args[0],) + exception.args[1:]

    def _decode_params(self, params):
        return '&'.join(['{}={}'.format(k, urllib.quote(params[k], '')) for k in OrderedDict(sorted(params.items()))])

    def _sign(self, method, path, params):
        signatureBase = '&'.join(filter(None, [
            method.upper(),
            urllib.quote((self.url + path).replace('+', ' '), ''),
            urllib.quote(self._decode_params(params), '') if params else None,
        ]))

        digest = hmac.new(self.api_secret, signatureBase, sha1).digest()
        return base64.b64encode(digest).decode()

    def _query(self, method, path, params=None, retry=0):
        if not path.startswith('/'):
            if six.PY2:
                path = '/' + six.text_type(path.decode('utf-8'))
            else:
                path = '/' + path

        params = OrderedDict(params) if params else OrderedDict()
        #param: params[param] for param in params if params[param] is not None} if params is not None else {}
        params['api_key'] = self.api_key

        try:
            return self._request(method, path, params)
        except InfogramPythonError as e:
            if retry and 500 <= e[1] < 600:
                return self._query(method, path, params, retry - 1)
            else:
                raise

    def _request(self, method, path, params):
        if params:
            for key in params:
                value = params[key]
                if isinstance(value, (list, dict, set)):
                    params[key] = json.dumps(value, separators=(',', ':'))
                elif isinstance(value, bool):
                    params[key] = str(value).lower()
                elif value == None:
                    params[key] = 'null'
                else:
                    params[key] = str(value)
                #params[key] = urllib.quote(str(params[key]), '')
        else:
            params = {}

        params['api_sig'] = self._sign(method, path, params)

        try:
            if method in ['GET', 'DELETE']:
                response = self.session.request(
                    method,
                    self.url + path,
                    params          = tuple(params.items()),
                    allow_redirects = True,
                    timeout         = self.timeout
                )
            else:
                response = self.session.request(
                    method,
                    self.url + path,
                    data            = tuple(params.items()),
                    allow_redirects = True,
                    timeout         = self.timeout
                )
        except requests.RequestException as e:
            raise HTTPError(e)

        return self._parse(response)

    def _parse(self, response):
        if response.status_code not in [200, 201]:
            raise HTTPError(response.reason, response.status_code, response.content)

        data = response.content
        if data:
            if type(data) == type(bytes()):
                # infogr.am API does not return Content-Type when an
                # infographic is requested in formats pdf or png, so we need
                # to check for that before decoding with utf-8
                if data[:4][1:] not in ['PNG', 'PDF']:
                    data = json.loads(data.decode('utf-8'), parse_float=Decimal)

        return data

    def themes_list(self, retry=3):
        try:
            response = self._query(
                method = 'GET',
                path   = '/themes',
                retry  = retry
            )
        except InfogramPythonError as e:
            self._extend_exception(e, 'Could not get themes')
            raise
        else:
            return response

    def users_get(self, user_id, retry=3):
        try:
            response = self._query(
                method = 'GET',
                path   = '/users/{}'.format(user_id),
                retry  = retry
            )
        except InfogramPythonError as e:
            self._extend_exception(e, 'Could not get user {}'.format(user_id))
            raise
        else:
            return response

    def users_get_infographics(self, user_id, retry=3):
        try:
            response = self._query(
                method = 'GET',
                path   = '/users/{}/infographics'.format(user_id),
                retry  = retry
            )
        except InfogramPythonError as e:
            self._extend_exception(e, 'Could not get infographics for user {}'.format(user_id))
            raise
        else:
            return response

    def infographics_list(self, retry=3):
        try:
            response = self._query(
                method = 'GET',
                path   = '/infographics',
                retry  = retry
            )
        except InfogramPythonError as e:
            self._extend_exception(e, 'Could not get infographics')
            raise
        else:
            return response

    def infographics_get(self, infographic_id, format=None, retry=3):
        try:
            response = self._query(
                method = 'GET',
                path   = '/infographics/{}'.format(infographic_id),
                params = {'format': format} if format else None,
                retry  = retry
            )
        except InfogramPythonError as e:
            self._extend_exception(e, 'Could not get infographic {}'.format(infographic_id))
            raise
        else:
            return response

    def infographics_create(self, params, retry=3):
        try:
            response = self._query(
                method = 'POST',
                path   = '/infographics',
                params = params,
                retry  = retry
            )
        except InfogramPythonError as e:
            self._extend_exception(e, 'Could not create infographic')
            raise
        else:
            return response

    def infographics_update(self, infographic_id, params, retry=3):
        try:
            response = self._query(
                method = 'PUT',
                path   = '/infographics/{}'.format(infographic_id),
                params = params,
                retry  = retry
            )
        except InfogramPythonError as e:
            self._extend_exception(e, 'Could not update infographic {}'.format(infographic_id))
            raise
        else:
            return response

    def infographics_destroy(self, infographic_id, retry=3):
        try:
            response = self._query(
                method = 'DELETE',
                path   = '/infographics/{}'.format(infographic_id),
                retry  = retry
            )
        except InfogramPythonError as e:
            self._extend_exception(e, 'Could not delete infographic {}'.format(infographic_id))
            raise
        else:
            return response
