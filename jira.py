"""
This class is used to consume the JIRA API. It has only been tested with JIRA 7.2.4
"""
import requests, json

class Jira(object):
	def __init__(self, url, username, password):
		self.url = url
		self.api_url = url + '/rest/api/2'
		self.username = username
		self.password = password

	"""
	Print JSON response to stdout
	"""
	def printResponse(r):
        	print '{} {}\n'.format(json.dumps(r.json(), sort_keys=True, indent=4, separators=(',', ': ')), r)


	"""
	GET /rest/api/2/project
	"""
	def get_projects(self):
		projects_get_url = '{0}/project'.format(self.api_url)
		return requests.get(projects_get_url, auth=(self.username, self.password))
	
	"""
	GET /rest/api/2/project/<project_key>
	"""
	def get_project(self, project_key):
		project_get_url = '{0}/project/{1}'.format(self.api_url, project_key)
		return requests.get(project_get_url, auth=(self.username, self.password))


	"""
	DELETE /rest/api/2/project/<project_key>
	"""
	def delete_project(self, project_key):
		project_delete_url = '{0}/project/{1}'.format(self.api_url, project_key)
		return requests.delete(project_delete_url, auth=(self.username, self.password))
	

	"""
	CREATE /rest/api/2/issuetype
	"""
	def create_issue_type(self, name, description='', itype='standard'):
		issue_type_create_url = '{0}/issuetype'.format(self.api_url)
		data = {
				'name': name,
				'description': description,
				'type': itype
		}
		return requests.post(issue_type_create_url, data=json.dumps(data), auth=(self.username, self.password), headers=({'Content-Type': 'application/json'}))


	"""
	GET /rest/api/2/status/<idOrName>
	"""
	def get_status(self, id_or_name):
		status_get_url = '{0}/status/{1}'.format(self.api_url, id_or_name)
		return requests.get(status_get_url, auth=(self.username, self.password))


	"""
	GET /rest/api/2/status
	"""
	def get_all_statuses(self):
		status_get_all_url = '{0}/status'.format(self.api_url)
		return requests.get(status_get_all_url, auth=(self.username, self.password))


	"""
	GET /rest/api/2/project/<project_key>/statuses
	"""
	def get_project_statuses(self, project_key):
		project_status_get_url = '{0}/project/{1}/statuses'.format(self.api_url, project_key)
		return requests.get(project_status_get_url, auth=(self.username, self.password))

	
	"""
	GET /rest/api/2/resolution/<id>
	"""
	def get_resolution(self, id):
		resolution_get_url = '{0}/resolution/{1}'.format(self.api_url, id)
		return requests.get(resolution_get_url, auth=(self.username, self.password))


	"""
	GET /rest/api/2/resolution
	"""
	def get_all_resolutions(self):
		resolution_get_all_url = '{0}/resolution'.format(self.api_url)
		return requests.get(resolution_get_all_url, auth=(self.username, self.password))


	"""
	GET /rest/api/2/priority/<id>
	"""
	def get_priority(self, id):
		priority_get_url = '{0}/priority/{1}'.format(self.api_url, id)
		return requests.get(priority_get_url, auth=(self.username, self.password))


	"""
	GET /rest/api/2/priority
	"""
	def get_all_priorities(self):
		priority_get_all_url = '{0}/priority'.format(self.api_url)
		return requests.get(priority_get_all_url, auth=(self.username, self.password))


	"""
	GET /rest/api/2/field
	"""
	def get_all_fields(self):
		field_get_all_url = '{0}/field'.format(self.api_url)
		return requests.get(field_get_all_url, auth=(self.username, self.password))


	"""
	Use get_all_fields method to get fields and return custom fields only
	"""
	def get_all_custom_fields(self):
		fields = self.get_all_fields().json()
		custom_fields = []
		for field in fields:
			if field['custom'] == True:
				custom_fields.append(field)
		return custom_fields


	"""
	GET /rest/api/2/screens/<screenId>/availableFields
	"""
	def get_all_screen_fields(self, id):
		screen_available_fields_url = '{0}/screens/{1}/availableFields'.format(self.api_url, id)
		return requests.get(screen_available_fields_url, auth=(self.username, self.password))


	"""
	GET /rest/api/2/screens/<screenId>/tabs
	"""
	def get_screen_tabs(self, screen_id):
		screen_tabs_url = '{0}/screens/{1}/tabs'.format(self.api_url, screen_id)
		return requests.get(screen_tabs_url, auth=(self.username, self.password))


	"""
	GET /rest/api/2/screens/<screenId>/tabs/<tabId>
	"""
	def get_screen_tab_fields(self, screen_id, tab_id):
		screen_tab_fields_url = '{0}/screens/{1}/tabs/{2}/fields'.format(self.api_url, screen_id, tab_id)
		return requests.get(screen_tab_fields_url, auth=(self.username, self.password))


	"""
	Return all fields of a screen
	"""
	def get_screen_fields(self, screen_id):
		screen_tabs = self.get_screen_tabs(screen_id).json()
		fields = []
		for screen_tab in screen_tabs:
			tab_fields = self.get_screen_tab_fields(screen_id, screen_tab['id']).json()
			fields = fields + tab_fields
		return fields
		

	
	"""
	CREATE /rest/api/2/field
	"""
	def create_custom_field(self, name, ctype, searcher_key, description=''):
		custom_field_create_url = '{0}/field'.format(self.api_url)
		data = {
				"name": name,
				"description": description,
				"type": ctype,
				"searcherKey": self.get_custom_field_searcher(ctype)
		}
		print(data)
		return requests.post(custom_field_create_url, data=json.dumps(data), auth=(self.username, self.password), headers=({'Content-Type': 'application/json'}))


	"""
	Return searcherKey for a given custom field type
	"""

	def get_custom_field_searcher(self, ctype):
		ctype_searcher_mapping = {
			'com.atlassian.jira.plugin.system.customfieldtypes:datepicker': 'com.atlassian.jira.plugin.system.customfieldtypes:daterange',
			'com.atlassian.jira.plugin.system.customfieldtypes:select': 'com.atlassian.jira.plugin.system.customfieldtypes:multiselectsearcher',
			'com.atlassian.jira.plugin.system.customfieldtypes:float': 'com.atlassian.jira.plugin.system.customfieldtypes:exactnumber',
			'com.atlassian.jira.plugin.system.customfieldtypes:textarea': 'com.atlassian.jira.plugin.system.customfieldtypes:textsearcher',
			'com.atlassian.jira.plugin.system.customfieldtypes:textfield': 'com.atlassian.jira.plugin.system.customfieldtypes:textsearcher'
		}

		if ctype in ctype_searcher_mapping:
			return ctype_searcher_mapping[ctype]
		else:
			return None