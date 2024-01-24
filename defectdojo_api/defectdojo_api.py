import json
import requests
import requests.exceptions
import urllib3
import logging

import defectdojo_enums
from defectdojo_request import DefectDojoRequest
from defectdojo_user import DefectDojoUser
from defectdojo_engagement import DefectDojoEngagement

urllib3.add_stderr_logger()

# Another example code change
version = "2023.08.22"

LOGGER_NAME = "defectdojo_api"

class DefectDojoAPI(object):
    """An API wrapper for DefectDojo."""
    _defectdojo_request = None
    def __init__(self :object, host :str, api_token :str, user :str, api_version :str ='v2', 
                 verify_ssl :bool =True, timeout :int =60, proxies :dict =None, 
                 user_agent :str =None, cert :str =None, debug :bool =False):
        """ Initializes the DefectDojo API object
        :param host: str, url to the defect dojo instance where the api is served
        :param api_token: str, token to authorize access to the API
        :param user: str, username to authorize access to the API
        :param api_version: (Optional) str, major API version that the user is requesting access to
        :param verify_ssl: (Optional) bool, disables SSL warning messages if False
        :param timeout: (Optional) int, the number of seconds until calls timeout
        :param proxies: (Optional) dict, proxies to use in the calls
        :param user_agent: (Optional) str, passed as the user agent to the underlying https calls
        :param cert: (Optional) str, SSL certificate used to access the api server
        :param debug: (Optional) bool, sets logging level to DEBUG instead of WARNING
        """
        self.logger = logging.getLogger(LOGGER_NAME)
        self.logger.setLevel(logging.DEBUG)
        if not debug:
            # Configure the default logging level to warning instead of debug for request library
            logging.getLogger("requests").setLevel(logging.WARNING)
            logging.getLogger("urllib3").setLevel(logging.WARNING)
            self.logger.setLevel(logging.WARNING)

        self._defectdojo_request = DefectDojoRequest(version, host, api_token, user, api_version, verify_ssl, proxies, user_agent, timeout, cert, LOGGER_NAME)
        self.User = DefectDojoUser(self._defectdojo_request)
        self.Engagement = DefectDojoEngagement(self._defectdojo_request)

    def version_url(self :object):
        """Returns the DefectDojo API version.

        """
        return self.api_version

    def get_id_from_url(self :object, url :str):
        """Returns the ID from the DefectDojo API.

        :param url: URL returned by the API
        """
        url = url.split('/')
        return url[len(url)-2]

    def get_user_api_key(self :object, username :str, password :str):
        """Retrieves the user API key 
            is useful to import reports and findings from other tools, 
            since findings owner in API are set to the user calling the API
        :param username: str, username of the user for whom to retrieve the API key
        :param password: str, password of the user
        """
        data = {
            'username': username,
            'password': password
        }
        return self._defectdojo_request.request('POST', 'api-token-auth/', data=data)

    ###### Product API #######
    ##### ALL BELOW WILL MOVE TO PRODUCT OBJECT
    def set_product_metadata(self :object, product_id :int, name :str =None, value :str =None):
        """Add a custom field to a product.

        :param product_id: int, Product ID.
        :param name: (Optional) str, name for the metadata to set
        :param value: (Optional) str, value for the metdata to set

        """
        data = {
            'product': product_id,
            'name': name,
            'value': value
        }
        headers = {
            'product_id': '{}'.format(product_id)
        }

        return self._defectdojo_request.request('POST', 'metadata/', data=data, custom_headers=headers)

    def list_products(self, name=None, limit=200, offset=0):

        """Retrieves all the products.

        :param name: Search by product name.
        :param limit: Number of records to return.
        :param offset: The initial index from which to return the results.

        """

        params  = {}
        if limit:
            params['limit'] = limit

        if offset:
            params['offset'] = offset

        if name:
            params['name'] = name


        return self._defectdojo_request.request('GET', 'products/', params)

    def get_product(self, product_id):
        """Retrieves a product using the given product id.

        :param product_id: Product identification.

        """
        return self._defectdojo_request.request('GET', 'products/' + str(product_id) + '/')

    def get_product_list_by_name(self, product_name):
#       Retrieves a product list by using the product name 
        #Note (search is made with Like.

        return self._defectdojo_request.request('GET', 'products/?name=' + str(product_name))


    def create_product(self, name, description, prod_type):
        """Creates a product with the given properties.

        :param name: Product name.
        :param description: Product key id..
        :param prod_type: Product type.

        """

        data = {
            'name': name,
            'description': description,
            'prod_type': prod_type
        }

        return self._defectdojo_request.request('POST', 'products/', data=data)

    def create_product(self, name, description, prod_type):
        """Creates a product with the given properties.

        :param name: Product name.
        :param description: Product description..
        :param prod_type: Product type.

        """

        data = {
            'name': name,
            'description': description,
            'prod_type': prod_type
        }

        return self._defectdojo_request.request('POST', 'products/', data=data)


    def set_product(self, product_id, name=None, description=None, prod_type=None):
        """Updates a product with the given properties.

        :param product_id: Product ID
        :param name: Product name.
        :param description: Product key id..
        :param prod_type: Product type.

        """

        data = {}

        if name:
            data['name'] = name

        if description:
            data['description'] = description

        if prod_type:
            data['prod_type'] = prod_type

        return self._defectdojo_request.request('PUT', 'products/' + str(product_id) + '/', data=data)

    def delete_product(self, product_id):
        """
        Deletes a product the given id
        """
        return self._defectdojo_request.request('DELETE', 'products/' + str(product_id) + '/')


    ###### Test API #######
    def list_tests(self, engagement_id=None, test_type=None, limit=20, offset=0):
        """Retrieves all the tests.

        :param name_contains: Search by product name.
        :param limit: Number of records to return.

        """

        params  = {}
        if limit:
            params['limit'] = limit

        if offset:
            params['offset'] = offset

        if engagement_id:
            params['engagement'] = engagement_id

        # TODO fix this, it doesn't work for some reason
        if test_type:
            params['test_type'] = test_type

        return self._defectdojo_request.request('GET', 'tests/', params)

    def get_test(self, test_id):
        """Retrieves a test using the given test id.

        :param test_id: Test identification.

        """
        return self._defectdojo_request.request('GET', 'tests/' + str(test_id) + '/')

    def create_test(self, engagement_id, test_type, environment, target_start,
                    target_end, percent_complete=None, lead=None, title=None,
                    version=None, description=None):
        """Creates a product with the given properties.

        :param engagement_id: Engagement id.
        :param test_type: Test type key id.
        :param target_start: Test start date.
        :param target_end: Test end date.
        :param percent_complete: Percentage until test completion.
        :param lead: Test lead id
        :param title: Test title/name
        :param version: Test version
        :param description: Test description

        """

        data = {
            'engagement': engagement_id,
            'test_type': test_type,
            'environment': environment,
            'target_start': target_start,
            'target_end': target_end,
            'percent_complete': percent_complete
        }

        if lead:
            data['lead'] = lead

        if title:
            data['title'] = title

        if version:
            data['version'] = version

        if description:
            data['description'] = description

        return self._defectdojo_request.request('POST', 'tests/', data=data)

    def set_test(self, test_id, engagement_id=None, test_type=None,
        environment=None, target_start=None, target_end=None,
        percent_complete=None, title=None, version=None, description=None):
        """Creates a product with the given properties.

        :param engagement_id: Engagement id.
        :param test_type: Test type key id.
        :param target_start: Test start date.
        :param target_end: Test end date.
        :param percent_complete: Percentage until test completion.
        :param title: Test title/name
        :param version: Test version
        :param description: Test description


        """

        current_test = self.get_test(test_id).data

        data = {}

        if engagement_id:
            data['engagement'] = self.engagement_id

        if test_type:
            data['test_type'] = test_type

        if environment:
            data['environment'] = environment

        if target_start:
            data['target_start'] = target_start
        else:
            data['target_start'] = current_test["target_start"]
        if target_end:
            data['target_end'] = target_end
        else:
            data['target_end'] = current_test["target_end"]

        if percent_complete:
            data['percent_complete'] = percent_complete

        if title:
            data['title'] = title

        if version:
            data['version'] = version

        if description:
            data['description'] = description

        return self._defectdojo_request.request('PUT', 'tests/' + str(test_id) + '/', data=data)

    ###### Test Types API #######
    def list_test_types(self, name=None, limit=20, offset=0):
        """Returns filtered list of test types.

        :param name: Test type name.
        :param limit: Number of records to return.
        :param offset: The initial index from which to return the results.

        """

        params = {}
        if name:
            params['name'] = name

        if limit:
            params['limit'] = limit

        if offset:
            params['offset'] = offset
        
        return self._defectdojo_request.request('GET', 'test_types/', params)

    
    def create_test_type(self, name, static_tool="False", dynamic_tool="False", active="True"):
        """Creates a test type with given properties.

        :param name: Test type name.
        :param static_tool: Test type is for static tool.
        :param dynamic_tool: Test type is for dynamic tool.
        :param active: Test type is active.
        :param tags: Tags.

        """

        data = {
            'name': name,
            'static_tool': static_tool,
            'dynamic_tool': dynamic_tool,
            'active': active
        }

        return self._defectdojo_request.request('POST', 'test_types/', data=data)


    def get_test_type(self, test_type_id):
        """Retrieves a test type with the given id.

        :param test_type_id: Test type id.
        """

        return self._defectdojo_request.request('GET', 'test_types/' + str(test_type_id) + '/')

    
    def set_test_type(self, test_type_id, name, static_tool="False", dynamic_tool="False", active="True"):
        """Updates a test type with the given properties.

        :param test_type_id: Test type id.
        :param name: Test type name.
        :param static_tool: Test type is for static tool.
        :param dynamic_tool: Test type is for dynamic tool.
        :param active: Test type is active.

        """

        data = {}
        if name:
            data['name'] = name

        if static_tool:
            data['static_tool'] = static_tool

        if dynamic_tool:
            data['dynamic_tool'] = dynamic_tool

        if active:
            data['active'] = active

        return self._defectdojo_request.request('PATCH', 'test_types/' + str(test_type_id) + '/', data=data)


    

    ###### Findings API #######
    def list_findings(self, active=None, duplicate=None, mitigated=None, severity=None, verified=None, severity_lt=None,
        severity_gt=None, severity_contains=None, title_contains=None, url_contains=None, date_lt=None,
        date_gt=None, date=None, product_id_in=None, engagement_id_in=None, test_id_in=None, build=None, limit=20, offset=0,
        related_fields=False,
        is_mitigated=None, tags=None):
        """Returns filtered list of findings.

        :param active: Finding is active: (true or false)
        :param duplicate: Duplicate finding (true or false)
        :param mitigated: Mitigation date.
        :param severity: Severity: Low, Medium, High and Critical.
        :param verified: Finding verified.
        :param severity_lt: Severity less than Low, Medium, High and Critical.
        :param severity_gt: Severity greater than Low, Medium, High and Critical.
        :param severity_contains: Severity contains: (Medium, Critical)
        :param title_contains: Filter by title containing the keyword.
        :param url_contains: Filter by URL containing the keyword.
        :param date_lt: Date less than.
        :param date_gt: Date greater than.
        :param date: Return findings for a particular date.
        :param product_id_in: Product id(s) associated with a finding. (1,2 or 1)
        :param engagement_id_in: Engagement id(s) associated with a finding. (1,2 or 1)
        :param test_in: Test id(s) associated with a finding. (1,2 or 1)
        :param build_id: User specified build id relating to the build number from the build server. (Jenkins, Travis etc.).
        :param limit: Number of records to return.
        :param offset: The initial index from which to return the results
        :param is_mitigated: Mitigated finding (true or false).
        :param tags: Comma separated list of exact tags.

        """

        params  = {}
        if limit:
            params['limit'] = limit

        if offset:
            params['offset'] = offset

        if active:
            params['active'] = active

        if duplicate:
            params['duplicate'] = duplicate

        if mitigated:
            params['mitigated'] = mitigated

        if severity:
            params['severity__in'] = severity

        if verified:
            params['verified'] = verified

        if severity_lt:
            params['severity__lt'] = severity_lt

        if severity_gt:
            params['severity__gt'] = severity_gt

        if severity_contains:
            params['severity'] = severity_contains

        if title_contains:
            params['title'] = title_contains

        if url_contains:
            params['url__contains'] = url_contains

        if date_lt:
            params['date__lt'] = date_lt

        if date_gt:
            params['date__gt'] = date_gt

        if date:
            params['date'] = date

        if engagement_id_in:
            params['test__engagement'] = engagement_id_in

        if product_id_in:
            params['test__engagement__product'] = product_id_in

        if test_id_in:
            params['test'] = test_id_in

        if build:
            params['build_id__contains'] = build
        if related_fields:
            params['related_fields'] = 'true'

        if is_mitigated:
            params['is_mitigated'] = is_mitigated

        if tags:
            params['tags'] = tags

        return self._defectdojo_request.request('GET', 'findings/', params)

    def get_finding(self, finding_id):
        """
        Retrieves a finding using the given finding id.
        :param finding_id: Finding identification.
        """
        return self._defectdojo_request.request('GET', 'findings/' + str(finding_id) + '/')

    def create_finding(self, title, description, severity, cwe, date, product_id, engagement_id,
        test_id, user_id, impact, active, verified, mitigation, references=None, build=None, line=0,
        file_path=None, static_finding="False", dynamic_finding="False", false_p="False",
        duplicate="False",  out_of_scope="False", under_review="False", under_defect_review="False",
        numerical_severity=None, found_by=None, tags=None, service=""):
        """Creates a finding with the given properties.

        :param title: Finding title
        :param description: Finding detailed description.
        :param severity: Finding severity: Low, Medium, High and Critical
        :param cwe: CWE (int)
        :param date: Discovered Date.
        :param product_id: Product finding should be associated with.
        :param engagement_id: Engagement finding should be associated with.
        :param test_id: Test finding should be associated with.
        :param user_id: Reporter of finding.
        :param impact: Detailed impact of finding.
        :param active: Finding active and reported on.
        :param verified: Finding has been verified.
        :param mitigation: Steps to mitigate the finding.
        :param references: Details on finding.
        :param build: User specified build id relating to the build number from the build server. (Jenkins, Travis etc.).
        """
        
        #If numerical_severity is not set, maps numerical_severity with severity : Low then S0 Medium then S1....
        if (numerical_severity is None):
            if (severity=='Low'): numerical_severity='S1'
            elif (severity=='Medium'): numerical_severity='S2'
            elif (severity=='High'): numerical_severity='S3'
            elif (severity=='Critical'): numerical_severity='S4'


        data = {
            'title': title,
            'description': description,
            'severity': severity,
            'cwe': cwe,
            'date': date,
            'product': product_id,
            'engagement': engagement_id,
            'test': test_id,
            'reporter': user_id,
            'impact': impact,
            'active': active,
            'verified': verified,
            'mitigation': mitigation,
            'references': references,
            'build_id' : build,
            'line' : line,
            'file_path' : file_path,
            'static_finding' : static_finding,
            'dynamic_finding' : dynamic_finding,
            'false_p' : false_p,
            'duplicate' : duplicate,
            'out_of_scope' : out_of_scope,
            'under_review' : under_review,
            'under_defect_review' : under_defect_review,
            'numerical_severity' : numerical_severity,
            'found_by' : [] if found_by is None else found_by,
            'tags': [] if tags is None else tags,
	    'service': service
        }

        return self._defectdojo_request.request('POST', 'findings/', data=data)

    def set_finding(self, finding_id, product_id=None, engagement_id=None, test_id=None, title=None, description=None, severity=None, build=None,
        cwe=None, date=None, user_id=None, impact=None, active=None, verified=None,
        mitigation=None, references=None, numerical_severity=None):

        """Updates a finding with the given properties.

        :param title: Finding title
        :param description: Finding detailed description.
        :param severity: Finding severity: Low, Medium, High and Critical
        :param cwe: CWE (int)
        :param date: Discovered Date.
        :param product_id: Product finding should be associated with.
        :param engagement_id: Engagement finding should be associated with.
        :param test_id: Test finding should be associated with.
        :param user_id: Reporter of finding.
        :param impact: Detailed impact of finding.
        :param active: Finding active and reported on.
        :param verified: Finding has been verified.
        :param mitigation: Steps to mitigate the finding.
        :param references: Details on finding.
        :param build: User specified build id relating to the build number from the build server. (Jenkins, Travis etc.).
        :param numerical_severity: The numerical representation of the severity (S0, S1, S2, S3, S4).
        :param service: Service you want associate to the finding. (string)
        """

        data = {}

        if not title:
            raise ValueError('title may not be null')
        data['title'] = title

        if not description:
            raise ValueError('description may not be null')
        data['description'] = description

        if not severity:
            raise ValueError('severity may not be null')
        data['severity'] = severity

        if not numerical_severity:
            raise ValueError('numerical_severity may not be null')
        data['numerical_severity'] = numerical_severity

        if cwe:
            data['cwe'] = cwe

        if date:
            data['date'] = date

        if product_id:
            data['product'] = product_id

        if engagement_id:
            data['engagement'] = engagement_id

        if test_id:
            data['test'] = test_id

        if user_id:
            data['reporter'] = user_id

        if impact:
            data['impact'] = impact

        if active is not None:
            data['active'] = active

        if verified is not None:
            data['verified'] = verified

        if mitigation:
            data['mitigation'] = mitigation

        if references:
            data['references'] = references

        if build:
            data['build_id'] = build

        return self._defectdojo_request.request('PUT', 'findings/' + str(finding_id) + '/', data=data)

    def delete_finding(self, finding_id):

        """Deletes a finding with the given id.

        :param finding_id: ID of finding to delete.

        """

        return self._defectdojo_request.request('DELETE', 'findings/' + str(finding_id))

    ##### Build Details API #####

    def build_details(self, engagement_id, json):
        """Uploads commit file changes to an engagement.

        :param engagement_id: Engagement identifier.
        :param file: File/Json with meta data to be uploaded.

        """

        data = {
            'file': json,
            'engagement': ('', engagement_id)
        }

        return self._defectdojo_request.request(
            'POST', 'build_details/',
            files=data
        )

    ##### Upload API #####
    def upload_scan(self, engagement_id, scan_type, file, active, verified, close_old_findings, skip_duplicates, scan_date, tags=None, build=None,
        version=None, branch_tag=None, commit_hash=None, minimum_severity="Info", auto_group_by=None, environment=None, endpoint_to_add=None):
        """Uploads and processes a scan file.

        :param application_id: Application identifier.
        :param file_path: Path to the scan file to be uploaded.

        """
        if build is None:
            build = ''

        with open(file, 'rb') as f:
             filedata = f.read()

        self.logger.debug("filedata:")
        self.logger.debug(filedata)

        data = {
            'file': (file, filedata),
            'engagement': ('', engagement_id),
            'scan_type': ('', scan_type),
            'active': ('', active),
            'verified': ('', verified),
            'close_old_findings': ('', close_old_findings),
            'skip_duplicates': ('', skip_duplicates),
            'scan_date': ('', scan_date),
            'tags': ('', tags),
            'build_id': ('', build),
            'version': ('', version),
            'branch_tag': ('', branch_tag),
            'commit_hash': ('', commit_hash),
            'minimum_severity': ('', minimum_severity),
            'environment': ('', environment),
            'endpoint_to_add': ('', endpoint_to_add)
            # 'push_to_jira': ('', True)
        }

        if auto_group_by:
            data['auto_group_by'] = (auto_group_by, '')

        """
        TODO: implement these parameters:
          lead
          test_type
          scan_date
        """

        return self._defectdojo_request.request(
            'POST', 'import-scan/',
            files=data
        )

    ##### Re-upload API #####
    def reupload_scan(self, test_id, scan_type, file, active, scan_date, tags=None, build=None, version=None, branch_tag=None, commit_hash=None,
        minimum_severity="Info", auto_group_by=None, environment=None):
        """Re-uploads and processes a scan file.

        :param test_id: Test identifier.
        :param file: Path to the scan file to be uploaded.

        """
        if build is None:
            build = ''

        data = {
            'test': ('', test_id),
            'file': open(file, 'rb'),
            'scan_type': ('', scan_type),
            'active': ('', active),
            'scan_date': ('', scan_date),
            'tags': ('', tags),
            'build_id': ('', build),
            'version': ('', version),
            'branch_tag': ('', branch_tag),
            'commit_hash': ('', commit_hash),
	        'minimum_severity': ('', minimum_severity),
            'environment': ('', environment),
            # 'push_to_jira': ('', True)
        }

        if auto_group_by:
            data['auto_group_by'] = (auto_group_by, '')

        return self._defectdojo_request.request(
            'POST', 'reimport-scan/',
            files=data
        )

    ##### Credential API #####

    def list_credentials(self, name=None, username=None, limit=20):
        """Retrieves all the globally configured credentials.
        :param name_contains: Search by credential name.
        :param username: Search by username
        :param limit: Number of records to return.
        """

        params  = {}
        if limit:
            params['limit'] = limit

        if name:
            params['name__contains'] = name

        if username:
            params['username__contains'] = username

        return self._defectdojo_request.request('GET', 'credentials/', params)

    def get_credential(self, cred_id, limit=20):
        """
        Retrieves a credential using the given credential id.
        :param credential_id: Credential identification.
        """
        return self._defectdojo_request.request('GET', 'credentials/' + str(cred_id) + '/')

    ##### Credential Mapping API #####

    def list_credential_mappings(self, name=None, product_id_in=None, engagement_id_in=None, test_id_in=None, finding_id_in=None, limit=20):
        """Retrieves mapped credentials.

        :param name_contains: Search by credential name.
        :param username: Search by username
        :param limit: Number of records to return.

        """

        params  = {}
        if limit:
            params['limit'] = limit

        if name:
            params['name'] = name

        if product_id_in:
            params['product__id__in'] = product_id_in

        if engagement_id_in:
            params['engagement__id__in'] = engagement_id_in

        if test_id_in:
            params['test__id__in'] = test_id_in

        if finding_id_in:
            params['finding__id__in'] = finding_id_in

        return self._defectdojo_request.request('GET', 'credential_mappings/', params)

    def get_credential_mapping(self, cred_mapping_id, limit=20):
        """
        Retrieves a credential using the given credential id.
        :param cred_mapping_id: Credential identification.
        """
        return self._defectdojo_request.request('GET', 'credential_mappings/' + str(cred_mapping_id) + '/')

    ##### App Analysis API #####
    def list_app_analysis(self, id=None, product_id=None, name=None, limit=20):
        """Retrieves source code languages.

        :param id: Search by lanaguage id.
        :param product: Search by product id
        :param language_name: Search by language name
        :param limit: Number of records to return.

        """

        params  = {}
        if limit:
            params['limit'] = limit

        if id:
            params['id'] = id

        if product_id:
            params['product__id'] = product_id

        if name:
            params['name__icontains'] = language_name

        return self._defectdojo_request.request('GET', 'app_analysis/', params)

    def create_app_analysis(self, product_id, user_id, name, confidence, version, icon, website):
        """
        Create a application analysis to product mapping.
        :param id: Language identification.
        """

        data = {
            'product': product_id,
            'user': user_id,
            'name': name,
            'confidence': confidence,
            'version': version,
            'icon': icon,
            'website': website
        }

        return self._defectdojo_request.request('POST', 'app_analysis/', data=data)

    def delete_app_analysis(self, id):
        """
        Deletes an app analysis using the given id.
        :param id: Language identification.
        """
        return self._defectdojo_request.request('DELETE', 'app_analysis/' + str(id) + '/')

    def delete_all_app_analysis_product(self, product_id):
        """
        Delete all app analysis using the given id.
        :product_id id: Product to remove
        """
        app_analysis = self.list_app_analysis(product_id=product_id)

        if app_analysis.success:
            for app in app_analysis.data["objects"]:
                self.delete_app_analysis(self.get_id_from_url(app['resource_uri']))

    ##### Language API #####

    def list_languages(self, id=None, product_id=None, language_name=None, limit=20):
        """Retrieves source code languages.

        :param id: Search by lanaguage id.
        :param product: Search by product id
        :param language_name: Search by language name
        :param limit: Number of records to return.

        """

        params  = {}
        if limit:
            params['limit'] = limit

        if id:
            params['id'] = id

        if product_id:
            params['product__id'] = product_id

        if language_name:
            params['language_type__language__icontains'] = language_name

        return self._defectdojo_request.request('GET', 'languages/', params)

    def create_language(self, product_id, user_id, files, code, blank, comment, language_type_id=None, language_name=None):
        """
        Create a language to product mapping.
        :param product_id: Product identification.
        """
        #If language name specified then lookup
        if language_name:
            languages = self.list_language_types(language_name=language_name)

            if languages.success:
                for language in languages.data["objects"]:
                    language_type = language['resource_uri']

        data = {
            'product': product_id,
            'language_type': language_type,
            'user': user_id,
            'files': files,
            'code': code,
            'blank': blank,
            'comment': comment
        }

        return self._defectdojo_request.request('POST', 'languages/', data=data)

    def delete_language(self, id):
        """
        Deletes a language using the given id.
        :param id: Language identification.
        """
        return self._defectdojo_request.request('DELETE', 'languages/' + str(id) + '/')

    def delete_all_languages_product(self, product_id):
        """
        Delete all languages for a given product id.
        :param id: Language identification.
        """
        languages = self.list_languages(product_id=product_id)

        if languages.success:
            for language in languages.data["objects"]:
                self.delete_language(self.get_id_from_url(language['resource_uri']))

    def list_language_types(self, id=None, language_name=None, limit=20):
        """Retrieves source code languages.

        :param id: Search by lanaguage id.
        :param language_name: Search by language name
        :param limit: Number of records to return.

        """

        params  = {}
        if limit:
            params['limit'] = limit

        if id:
            params['id'] = id

        if language_name:
            params['language__icontains'] = language_name

        return self._defectdojo_request.request('GET', 'language_types/', params)

    ###### Tool API #######

    def list_tool_types(self, resource_id=None, name=None, limit=20):
        """Retrieves all the tool types.

        :param name_contains: Search by tool type name.
        :param limit: Number of records to return.

        """

        params  = {}
        if limit:
            params['limit'] = limit

        if resource_id:
            params['id'] = resource_id

        if name:
            params['name__contains'] = name

        return self._defectdojo_request.request('GET', 'tool_types/', params)

    def list_tools(self, resource_id=None, name=None, tool_type_id=None, url=None, name_icontains=None, limit=20):
        """Retrieves all the tool configurations.

        :param name_contains: Search by tool name.
        :param tool_type_id: Search by tool type id
        :param url: Search by url
        :param limit: Number of records to return.

        """

        params  = {}
        if limit:
            params['limit'] = limit

        if resource_id:
            params['id'] = resource_id

        if name:
            params['name'] = name

        if tool_type_id:
            params['tool_type__id'] = tool_type_id

        if tool_type_id:
            params['url__contains'] = tool_type_id

        if name_icontains:
            params['name__icontains'] = name_icontains

        return self._defectdojo_request.request('GET', 'tool_configurations/', params)

    def list_tool_products(self, resource_id=None, url=None, name=None, tool_configuration_id=None,
        tool_project_id=None, product_id=None, limit=20):
        """Retrieves all the tools.

        :param url_contains: Search by url.
        :param name_contains: Search by tool name.
        :param tool_configuration_id: Search by tool_configuration_id
        :param tool_project_id: Search by tool_project_id
        :param product_id: Search by product_id
        :param limit: Number of records to return.

        """

        params  = {}
        if limit:
            params['limit'] = limit

        if resource_id:
            params['id'] = resource_id

        if name:
            params['name'] = name

        if url:
            params['url__iregex'] = url

        if tool_project_id:
            params['tool_project_id__contains'] = tool_project_id

        if tool_configuration_id:
            params['tool_configuration__id'] = tool_configuration_id

        if product_id:
            params['product__id'] = product_id

        return self._defectdojo_request.request('GET', 'tool_product_settings/', params)

    def list_jira_issues(self, finding_id=None, jira_key=None, limit=100, offset=0):
        """
        Retrieves JIRA issues assigned to findings

        :param finding_id: Search for a specific finding ID
        :param jira_key: Search a specific JIRA key
        :param limit: Number of records to return.
        :param offset: The initial index from which to return the result
        """

        params = {}
        if finding_id:
            params['finding_id'] = finding_id

        if jira_key:
            params['jira_key'] = jira_key

        if limit:
            params['limit'] = limit

        if offset:
            params['offset'] = offset

        return self._defectdojo_request.request('GET', 'jira_finding_mappings/', params)

    def list_products_type(self, id=None, name=None, limit=100, offset=0):
        """
        Retrieves product types

        :param id: Search for a specific product type ID
        :param name: Search a specific product type key
        :param limit: Number of records to return.
        :param offset: The initial index from which to return the result
        """

        params = {}
        if id:
            params['id'] = id

        if name:
            params['name'] = name

        if limit:
            params['limit'] = limit

        if offset:
            params['offset'] = offset

        return self._defectdojo_request.request('GET', 'product_types/', params)
