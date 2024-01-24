class DefectDojoUser:

    def __init__(self, request):
        self._defectdojo_request = request

    def list(self, email=None, username=None, first_name=None, last_name=None, id=None, is_active=None, is_superuser=None, limit=20, offset=None):
        """Retrieves all the users.

        :param username: Search by username.
        :param limit: Number of records to return.

        """
        params  = {}
        if limit:
            params['limit'] = limit

        if email:
            params['email'] = email

        if username:
            params['username'] = username

        if first_name:
            params['first_name'] = first_name
        
        if last_name:
            params['last_name'] = last_name

        if id:
            params['id'] = id

        if is_active is not None:
            params['is_active'] = is_active
        
        if is_superuser is not None:
            params['is_superuser'] = is_superuser
        
        if offset:
            params['offset'] = offset
            
        return self._defectdojo_request.request('GET', 'users/', params)
    
    def get(self, user_id):
        """Retrieves a user using the given user id.

        :param user_id: User identification.

        """
        return self._defectdojo_request.request('GET', 'users/' + str(user_id) + '/')
    
    def update(self, user_id, data):
        """modifies a user using the given user id.

        :param user_id: User identification.

        """
        return self._defectdojo_request.request('PATCH', 'users/' + str(user_id) + '/', data=data)
    
    def create(self, username, first_name, last_name, email, is_active, is_superuser, password, configuration_permissions = None):
        """creates a user with the given parameters

        :param user_id: User identification.
        :param username: Unique username used to log in.
        :param first_name: First name of user.
        :param last_name: Surname of user.
        :param email: User's email address.
        :param is_active: True if the user should be active or False otherwise.
        :param is_superuser: True if the user should have superuser access or False otherwise.
        :param password: The user's password used to log in.
        :param configuration_permissions:  The user's permissions for configuration.

        """
        data = {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'is_active': is_active,
            'is_superuser': is_superuser,
            'password': password,
        }

        if configuration_permissions and len(configuration_permissions) > 0:
            data['configuration_permissions'] = configuration_permissions

        return self._defectdojo_request.request('POST', 'users/', data=data)

    def delete(self, user_id):
        """deletes the user with the id user_id

        :param user_id: User identification.

        """

        return self._defectdojo_request.request('DELETE', f'users/{user_id}')