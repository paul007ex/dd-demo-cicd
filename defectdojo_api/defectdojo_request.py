import requests
import json
import logging
import urllib3
from defectdojo_response import DefectDojoResponse

class DefectDojoRequest():
    
    def __init__(self :object, version :str, host :str, api_token :str, user :str, 
                 api_version :str, verify_ssl :bool, proxies :dict, user_agent :str, 
                 timeout :int, cert :str, logger_name :str):
        """ Initializes the DefectDojo Request object
        :param version: str, the major.minor.build version of this library used as the user_agent if one is not passed in
        :param host: str, url to the defect dojo instance where the api is served
        :param api_token: str, token to authorize access to the API
        :param user: str, username to authorize access to the API
        :param api_version: str, major API version that the user is requesting access to
        :param verify_ssl: bool, disables SSL warning messages if False
        :param proxies: dict, proxies to use in the calls
        :param user_agent: str, passed to the underlying https calls
        :param timeout: int, the number of seconds until calls timeout        
        :param cert: str, SSL certificate used to access the api server
        :param logger_name: str, used to retrieve the logger
        """
        self.api_token = api_token
        self.user_agent = user_agent
        self.logger = logging.getLogger(logger_name)
        self.host = host + '/api/' + api_version + '/'
        self.api_token = api_token
        self.user = user
        self.api_version = api_version
        self.verify_ssl = verify_ssl
        self.proxies = proxies
        self.timeout = timeout
        self.logger_name = logger_name

        if not user_agent:
            self.user_agent = 'DefectDojo_api/' + version
        else:
            self.user_agent = user_agent

        self.cert = cert

        if not self.verify_ssl:
            urllib3.disable_warnings()  # Disabling SSL warning messages if verification is disabled.


    def request(self, method :str, url :str, params :dict =None, data :dict =None, files :dict =None):
        """Common handler for all HTTP requests.
        :param method: str, One of the standard http verbs GET, OPTIONS, HEAD, POST, PUT, PATCH or DELETE

        """
        if not params:
            params = {}

        if data:
            data = json.dumps(data)

        headers = {
            'User-Agent': self.user_agent,
            'Authorization' : (("ApiKey "+ self.user + ":" + self.api_token) if (self.api_version=="v1") else ("Token " + self.api_token))
        }

        if not files:
            headers['Accept'] = 'application/json'
            headers['Content-Type'] = 'application/json'

        if self.proxies:
            proxies=self.proxies
        else:
            proxies = {}

        try:
            self.logger.debug("request:")
            self.logger.debug(method + ' ' + url)
            self.logger.debug("headers: " + str(headers))
            self.logger.debug("params:" + str(params))
            self.logger.debug("data:" + str(data))
            self.logger.debug("files:" + str(files))

            response = requests.request(method=method, url=self.host + url, params=params, data=data, files=files, headers=headers,
                                        timeout=self.timeout, verify=self.verify_ssl, cert=self.cert, proxies=proxies)

            self.logger.debug("response:")
            self.logger.debug(response.status_code)
            self.logger.debug(response.text)

            try:
                if response.status_code == 201: #Created new object
                    try:
                        object_id = response.headers["Location"].split('/')
                        key_id = object_id[-2]
                        data = int(key_id)
                    except:
                        data = response.json()

                    return DefectDojoResponse(message="Upload complete", response_code=response.status_code, data=data, success=True, logger_name=self.logger_name)
                elif response.status_code == 204: #Object updates
                    return DefectDojoResponse(message="Object updated.", response_code=response.status_code, success=True, logger_name=self.logger_name)
                elif response.status_code == 400: #Object not created
                    return DefectDojoResponse(message="Error occured in API.", response_code=response.status_code, success=False, logger_name=self.logger_name, data=response.text)
                elif response.status_code == 404: #Object not created
                    return DefectDojoResponse(message="Object id does not exist.", response_code=response.status_code, success=False, logger_name=self.logger_name, data=response.text)
                elif response.status_code == 401:
                    return DefectDojoResponse(message="Unauthorized.", response_code=response.status_code, success=False, logger_name=self.logger_name, data=response.text)
                elif response.status_code == 414:
                    return DefectDojoResponse(message="Request-URI Too Large.", response_code=response.status_code, success=False, logger_name=self.logger_name)
                elif response.status_code == 500:
                    return DefectDojoResponse(message="An error 500 occured in the API.", response_code=response.status_code, success=False, logger_name=self.logger_name, data=response.text)
                else:
                    data = response.json()
                    return DefectDojoResponse(message="Success", data=data, success=True, logger_name=self.logger_name, response_code=response.status_code)
            except ValueError:
                return DefectDojoResponse(message='JSON response could not be decoded.', response_code=response.status_code, success=False, logger_name=self.logger_name, data=response.text)
        except requests.exceptions.SSLError:
            self.logger.warning("An SSL error occurred.")
            return DefectDojoResponse(message='An SSL error occurred.', response_code=response.status_code, success=False, logger_name=self.logger_name)
        except requests.exceptions.ConnectionError:
            self.logger.warning("A connection error occurred.")
            return DefectDojoResponse(message='A connection error occurred.', response_code=response.status_code, success=False, logger_name=self.logger_name)
        except requests.exceptions.Timeout:
            self.logger.warning("The request timed out")
            return DefectDojoResponse(message='The request timed out after ' + str(self.timeout) + ' seconds.', response_code=response.status_code,
                                     success=False, logger_name=self.logger_name)
        except requests.exceptions.RequestException as e:
            self.logger.warning("There was an error while handling the request.")
            self.logger.exception(e)
            return DefectDojoResponse(message='There was an error while handling the request.', response_code=response.status_code, success=False, logger_name=self.logger_name)

