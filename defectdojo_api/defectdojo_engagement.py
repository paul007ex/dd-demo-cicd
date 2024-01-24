from datetime import date
from defectdojo_response import DefectDojoResponse
from defectdojo_enums import DefectDojoEngagementStatus, DefectDojoEngagementOrder, DefectDojoEngagementType
from defectdojo_request import DefectDojoRequest

class DefectDojoEngagement:

    def __init__(self :object, request :DefectDojoRequest) -> None:
        """ Initializes the defectdojoengagement object
        :param request: DefectDojoRequest this Engagement will use for queries
        """
        self._defectdojo_request = request



    def list(self :object, **kwargs) -> DefectDojoResponse:    
        """ List the engagements that match the parameters requested
            :param kwargs: (Optional) keyword arguments that can be any of the following:
            
            :param id: int, engagement id
            :param limit: int, maximum engagements to return
            :param offset: int, offset into the returned engagements
            :param name: str, name of the engagements
            :param order: DefectDojoEngagementOrder, order to return results
            :param active: bool, True or False indicating the engagement is active or not
            :param api_test: bool, is there an API test
            :param pen_test: bool, is there a pen test
            :param product_id: int, product id for the engagements
            :param product__prod_type: [int], product types for the engagements
            :param product__tags: [str], array of tags on the product
            :param not_product_tags: [str], array of tags not on the product
            :param report_type: int, report type that the engagement represents
            :param requester_id: int, id of the requester
            :param status: DefectDojoEngagementStatus, status of the engagements
            :param tags: [str], tags that are on the engagement
            :param not_tags: [str], tags that are not on the engagement
            :param target_start: date, when the engagement started
            :param target_end: date, when the engagement ends/ended
            :param threat_model: bool, is there a threat model
            :param updated: date, when the engagement was updated
            :param version: str, the version of the engagement
        """
        params  = {}
        
        if kwargs:
            num_args = len(kwargs)
            args_found = 0

            param = kwargs.get('id')
            if param:
                params['id'] = param
                args_found+=1

            if args_found < num_args:    
                param = kwargs.get('limit')
                if param:
                    params['limit'] = param
                    args_found+=1

            if args_found < num_args:   
                param = kwargs.get('offset')
                if param:
                    params['offset'] = param
                    args_found+=1
            if args_found < num_args:                       
                param = kwargs.get('product_id')
                if param:
                    params['product'] = param
                    args_found+=1
                
            if args_found < num_args:   
                param = kwargs.get('status')
                if param:
                    params['status'] = param.value
                    args_found+=1
            
            if args_found < num_args:   
                param = kwargs.get('name')
                if param:
                    params['name'] = param
                    args_found+=1

            if args_found < num_args:
                param = kwargs.get('active')
                if param != None:
                    params['active'] = param
                    args_found+=1

            if args_found < num_args:
                param = kwargs.get('api_test')
                if param != None:
                    params['api_test'] = param
                    args_found+=1
            
            if args_found < num_args:
                param = kwargs.get('pen_test')
                if param != None:
                    params['pen_test'] = param
                    args_found+=1
            
            if args_found < num_args:
                param = kwargs.get('threat_model')
                if param != None:
                    params['threat_model'] = param
                    args_found+=1

            if args_found < num_args:   
                param = kwargs.get('order')
                if param:
                    params['o'] = param.value
                    args_found+=1
            
            if args_found < num_args:   
                param = kwargs.get('product__prod_type')
                if param:
                    params['product__prod_type'] = ",".join(param)
                    args_found+=1

            if args_found < num_args:   
                param = kwargs.get('product__tags')
                if param:
                    params['product__tags'] = ",".join(param)
                    args_found+=1

            if args_found < num_args:   
                param = kwargs.get('not_product_tags')
                if param:
                    params['not_product_tags'] = ",".join(param)
                    args_found+=1
            
            if args_found < num_args:   
                param = kwargs.get('report_type')
                if param:
                    params['report_type'] = param
                    args_found+=1
                
            if args_found < num_args:   
                param = kwargs.get('requester_id')
                if param:
                    params['requester'] = param
                    args_found+=1
            
            if args_found < num_args:   
                param = kwargs.get('tags')
                if param:
                    params['tags'] = ",".join(param)
                    args_found+=1

            if args_found < num_args:       
                param = kwargs.get('not_tags')
                if param:
                    params['not_tags'] = ",".join([param])
                    args_found+=1
            
            if args_found < num_args:   
                param = kwargs.get('target_start')
                if param:
                    params['target_start'] = param.strftime("%Y-%m-%d")
                    args_found+=1

            if args_found < num_args:   
                param = kwargs.get('target_end')
                if param:
                    params['target_end'] = param.strftime("%Y-%m-%d")
                    args_found+=1

            if args_found < num_args:       
                param = kwargs.get('updated')
                if param:
                    params['updated'] = param.strftime('%Y-%m-%d')
                    args_found+=1
            
            if args_found < num_args:   
                param = kwargs.get('version')
                if param:
                    params['version'] = param
                    args_found+=1

        return self._defectdojo_request.request('GET', 'engagements/', params)

    def create(self, target_start :date, target_end :date, product :int, **kwargs) -> DefectDojoResponse:
        """Creates an engagement with the given properties.

        :param target_start: date, engagement start date.
        :param target_end: date, engagement end date.
        :param product: int, product key id.
        :param kwargs: (Optional) keyword arguments that can be any of the following:

        :param tags: [str], list of tags to add to engagement
        :param name: str, engagement name
        :param description: str, engagement description
        :param version: str, version of the product this engagement references        
        :param first_contacted: date, first contact date
        :param reason: str, reason for engagement
        :param tracker: str, link to epic or ticket system with changes to version.
        :param lead: int, testing lead from the user table
        :param requester: int, id of requester
        :param preset: int, settings and notes for performing engagement
        :param report_type: int, type of report
        :param status: DefectDojoEngagementStatus, engagement status
        :param check_list: bool, engagement includes check list
        :param test_strategy: str, test strategy URLs
        :param threat_model: bool, engagement includes threat model
        :param api_test: bool, engagement includes api test
        :param pen_test: bool, engagement includes pen test
        :param engagement_type: DefectDojoEngagementType, interactive or CI/CD
        :param build_id: str, build id of the product the engagement references
        :param commit_hash: str, commit hash from source code management
        :param branch_tag: str, branch or tag from source code management
        :param build_server: int, build server id responsible for ci/cd test
        :param source_code_management_server: int, id of source code management server
        :param source_code_management_uri: str, uri of source code management server
        :param deduplication_on_engagement: bool, if enabled deduplication will only mark a finding in this engagement as duplicate of another finding if both findings are in this engagement; if disabled, deduplication is on the product level
        :param orchestration_engine: int, id of orchestration engine service
        """

        data = {
            'product': product,
            'target_start': target_start.strftime('%Y-%m-%d'),
            'target_end': target_end.strftime('%Y-%m-%d'),            
        }

        
        if kwargs:
            num_args = len(kwargs)
            args_found = 0

            param = kwargs.get('tags')
            if param:
                data['tags'] = ",".join(param)
                args_found+=1

            if args_found < num_args:
                param = kwargs.get('name')
                if param:
                    data['name'] = param
                    args_found+=1

            if args_found < num_args:
                param = kwargs.get('description')
                if param:
                    data['description'] = param
                    args_found+=1

            if args_found < num_args:
                param = kwargs.get('version')
                if param:
                    data['version'] = param
                    args_found+=1

            if args_found < num_args:
                param = kwargs.get('first_contacted')
                if param:
                    data['first_contacted'] = param.strftime("%Y-%m-%d")
                    args_found+=1

            if args_found < num_args:
                param = kwargs.get('reason')
                if param:
                    data['reason'] = param
                    args_found+=1

            if args_found < num_args:
                param = kwargs.get('tracker')
                if param:
                    data['tracker'] = param
                    args_found+=1

            if args_found < num_args:
                param = kwargs.get('lead')
                if param:
                    data['lead'] = param
                    args_found+=1

            if args_found < num_args:
                param = kwargs.get('requester')
                if param:
                    data['requester'] = param
                    args_found+=1
            if args_found < num_args:
                param = kwargs.get('preset')
                if param:
                    data['preset'] = param
                    args_found+=1

            if args_found < num_args:
                param = kwargs.get('report_type')
                if param:
                    data['report_type'] = param
                    args_found+=1

            if args_found < num_args:
                param = kwargs.get('status')
                if param:
                    data['status'] = param.value
                    args_found+=1

            if args_found < num_args:
                param = kwargs.get('check_list')
                if param != None:
                    data['check_list'] = param
                    args_found+=1

            if args_found < num_args:
                param = kwargs.get('test_strategy')
                if param:
                    data['test_strategy'] = param
                    args_found+=1
            
            if args_found < num_args:
                param = kwargs.get('threat_model')
                if param != None:
                    data['threat_model'] = param
                    args_found+=1
            
            if args_found < num_args:
                param = kwargs.get('api_test')
                if param != None:
                    data['api_test'] = param
                    args_found+=1

            if args_found < num_args:
                param = kwargs.get('pen_test')
                if param != None:
                    data['pen_test'] = param
                    args_found+=1

            if args_found < num_args:
                param = kwargs.get('engagement_type')
                if param:
                    data['engagement_type'] = param.value
                    args_found+=1

            if args_found < num_args:
                param = kwargs.get('build_id')
                if param:
                    data['build_id'] = param
                    args_found+=1

            if args_found < num_args:
                param = kwargs.get('commit_hash')
                if param:
                    data['commit_hash'] = param
                    args_found+=1

            if args_found < num_args:
                param = kwargs.get('branch_tag')
                if param:
                    data['branch_tag'] = param
                    args_found+=1

            if args_found < num_args:
                param = kwargs.get('build_server')
                if param:
                    data['build_server'] = param
                    args_found+=1

            if args_found < num_args:
                param = kwargs.get('source_code_management_server')
                if param:
                    data['source_code_management_server'] = param
                    args_found+=1

            if args_found < num_args:
                param = kwargs.get('source_code_management_uri')
                if param:
                    data['source_code_management_uri'] = param
                    args_found+=1

            if args_found < num_args:
                param = kwargs.get('deduplication_on_engagement')
                if param != None:
                    data['deduplication_on_engagement'] = param
                    args_found+=1

            if args_found < num_args:
                param = kwargs.get('orchestration_engine')
                if param:
                    data['orchestration_engine'] = param
                    args_found+=1

        return self._defectdojo_request.request('POST', 'engagements/', data=data)
    
    def get(self, engagement_id :int) -> DefectDojoResponse:
        """Retrieves an engagement using the given engagement id.

        :param engagement_id: Engagement identification.

        """
        return self._defectdojo_request.request('GET', 'engagements/' + str(engagement_id) + '/')    

    def update(self, id :int, **kwargs) -> DefectDojoResponse:

        """Updates an engagement with the given properties.

        :param id: int, engagement id.
        :param kwargs: (Optional) keyword arguments that can be one of the following:

        :param name: str, engagement name
        :param description: str, engagement description
        :param version: str, version of engagement
        :param product: int, product key id
        :param lead: int, testing lead from the user table
        :param status: DefectDojoEngagementStatus, engagement status
        :param first_contacted: date, when engagement client first contacted
        :param target_start: date, engagement start date
        :param target_end: date, engagement end date
        :param reason: str, reason for engagement
        :param check_list: bool, engagement has a check list
        :param test_strategy: str, link to test Strategy URL
        :param engagement_type: DefectDojoEngagementType, interactive or CI/CD
        :param build_id: int, build id from the build server
        :param commit_hash: str, commit hash from source code management
        :param branch_tag: str, branch or tag from source code management
        :param build_server: int, tool configuration id of build server
        :param source_code_management_server: str, URL of source code management
        :param source_code_management_uri: str, link to source code commit
        :param orchestration_engine: str, URL of orchestration engine
        :param tags: [str], list of tags on engagement
        :param tracker: str, link to epic or ticket system
        :param threat_model: bool, engagement includes threat model
        :param api_test: bool, engagement includes api test
        :param pen_test: bool, engagement includes pen test
        :param requester: int, id of requester
        :param preset: int, settings and notes for performing this engagement
        :param report_type: int, type of report
        """

        data = {
        }

        if kwargs:
            num_args = len(kwargs)
            args_found = 0

            param = kwargs.get('name')
            if param:
                data['name'] = param
                args_found+=1

            if args_found < num_args:
                param = kwargs.get('description')
                if param:
                    data['description'] = param
                    args_found +=1
            
            if args_found < num_args:
                param = kwargs.get('version')
                if param:
                    data['version'] = param
                    args_found+=1

            if args_found < num_args:
                param = kwargs.get('product')
                if param:
                    data['product'] = param
                    args_found+=1
            
            if args_found < num_args:
                param = kwargs.get('lead')
                if param:
                    data['lead'] = param
                    args_found+=1
                
            if args_found < num_args:
                param = kwargs.get('status')
                if param:
                    data['status'] = param.value
                    args_found+=1

            if args_found < num_args:
                param = kwargs.get('first_contacted')
                if param:
                    data['first_contacted'] = param.strftime("%Y-%m-%d")
                    args_found+=1
            
            if args_found < num_args:
                param - kwargs.get('target_start')
                if param:
                    data['target_start'] = param.strftime("%Y%m%d")
                    args_found+=1

            if args_found < num_args:
                param - kwargs.get('target_end')
                if param:
                    data['target_end'] = param.strftime("%Y%m%d")
                    args_found+=1
                    
        return self._defectdojo_request.request('PATCH', 'engagements/' + str(id) + '/', data=data)

    def delete(self, id):
        """Deletes an engagement with the given id
        :param id: Enagement id.
        """

        self._defectdojo_request.request('DELETE', f'engagements/{id}/')

    def accept_risks(self, id, vulnerability_id, justification, accepted_by):
        """Accepts the risks for the engagement with the given id
        :param id: Engagement id.
        :param vulnerability_id: An id of a vulnerability in a security advisory associated with this finding. Can be a Common Vulnerabilities and Exposure (CVE) or from other sources.
        :param justification: Justification for accepting findings with this vulnerability id.
        :param accepted_by: Name or email of person who accepts the risk.
        """
        data = {
            'vulnerability_id': vulnerability_id,
            'justification': justification,
            'accepted_by': accepted_by
        }

        self._defectdojo_request.request('POST', f'engagements/{id}/accept_risks/', data=data)

    def close(self, id):

        """Closes an engagement with the given id.
        :param id: Engagement id.
        """

        self._defectdojo_request.request('POST', f'engagements/{id}/close/')

    def get_complete_checklist(self, id):
        """Gets complete checklist for engagement 
        :param id: Engagement id.
        """

        self._defectdojo_request.request('GET', f'engagements/{id}/complete_checklist/')
