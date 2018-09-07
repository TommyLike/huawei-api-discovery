import requests


class HuaweiCloudProxy():
    _Instance = None

    @classmethod
    def initialize_client(cls, app):
        HuaweiCloudProxy._Instance = HuaweiCloudProxy(app)

    @classmethod
    def get_instance(cls):
        if HuaweiCloudProxy._Instance:
            return HuaweiCloudProxy._Instance
        raise Exception("HuaweiCloudProxy uninitialized.")

    def __init__(self, app):
        self.app = app
        self.username = app.config['USERNAME']
        self.password = app.config['PASSWORD']
        self.domain = app.config['DOMAIN']

    def _get_auth_config(self, region):
        return {
            'auth': {
                'identity': {
                    'methods': ['password'],
                    'password': {
                        'user': {
                            'name': self.username,
                            'password': self.password,
                            'domain': {
                                'name': self.domain
                            }
                        }
                    }
                },
                'scope': {
                    'domain': {
                        'name': self.domain,
                    },
                    'project': {
                        'name': region
                    }
                }
            }
        }

    def _get_request_headers(self, token, hds):
        base = {'X-Auth-Token': token}
        if hds:
            base.update(hds)
        return base

    def _get_request_url(self, service, region, url):
        endpoints = [sv for sv in service['endpoints'] if(
                sv['region'] == region or sv['region_id'] == region)]
        if len(endpoints) == 0:
            raise Exception(
                "Can't find service endpoint in region %s" % region)
        return "%s/%s" % (endpoints[0]['url'].rstrip('/'), url.lstrip('/'))

    def _authentication(self, region, service):
        result = requests.post(
            'https://iam.%s.myhwclouds.com/v3/auth/tokens' % region,
            json=self._get_auth_config(region))
        if result.status_code != requests.codes.created:
            raise Exception("Failed to authentication with response: %s" % result.json())
        # Collect service endpoint
        body = result.json()
        services = [sv for sv in body['token']['catalog'] if sv['name'] == service]
        if len(services) == 0:
            raise Exception("Failed to locate service within name: %s" % service)
        return services[0], result.headers['X-Subject-Token']

    def proxy_request(self, region, service, url, headers, method, body,
                      parameter):
        sev, token = self._authentication(region, service)
        http_method = getattr(requests, method.lower(), None)
        if http_method is None:
            raise Exception("Unable to find http method: %s" % method)
        parameters = {
            'headers': self._get_request_headers(token, headers),
        }
        if body:
            parameters['json'] = body
        if parameters:
            parameters['params'] = parameter
        url = self._get_request_url(sev, region, url)
        self.app.logger.info(
            "*************Starting to proxy request*************")
        self.app.logger.info("[Request Url]: %s" % url)
        self.app.logger.info("[Request Parameter]: %s" % parameters)
        result = http_method(url,
                             **parameters)
        self.app.logger.info("[Response Code]: %s" % result.status_code)
        self.app.logger.info("[Response Content]: %s" % result.json())
        self.app.logger.info(
            "*************Ending to proxy request*************")
        return {
            'status_code': result.status_code,
            'content': result.json()
        }
