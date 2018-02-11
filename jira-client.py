"""
This client is a CLI to work with the JIRA api
This client class is used to consume jira.py there by leaving jira.py
to handle API calls only.

"""
import sys, json
from jira import Jira

class JiraClient(object):

	def __init__(self, url, username, password):
		self.jira = Jira(url, username, password)


	def get_all_project_keys(self):
		projects = self.jira.get_projects().json()
		keys = []
		for project in projects:
			keys.append(project['key'])
		return keys
	
	def get_all_project_keys_csv(self):
		result = ''
		keys = self.get_all_project_keys()
		for key in keys:
			result = result + key + ','

		return result
	
	def get_all_project_keys_csv_except(self, project_keys):
		result = ''
		keys = self.get_all_project_keys()
		ignore_project_keys = project_keys.split(',')
		for key in keys:
			if key not in ignore_project_keys:
				result = result + key + ','

		return result
	
	"""
	Delete projects with list of project keys from Jira
	"""
	def delete_projects(self, project_keys):
		keys = project_keys.split(',')
		for key in keys:
			print('Deleting project {0}'.format(key))
			result = self.jira.delete_project(key.strip())
			if result.status_code == 204:
				print('Successfully deleted {0}'.format(key))
			else:
				print('Error  deleting {0}. Error code {1}'.format(key, result.status_code))


	"""
	Delete all projects except the list of project keys from Jira
	"""
	def delete_projects_except(self, project_keys):
		all_keys = self.get_all_project_keys()
		except_keys = project_keys.split(',')
		
		for key in all_keys:
			key = key.strip()
			if key not in except_keys:
				print('Deleting project {0}'.format(key))
	                        result = self.jira.delete_project(key)
        	                if result.status_code == 204:
                	                print('Successfully deleted {0}'.format(key))
                        	else:
                                	print('Error  deleting {0}. Error code {1}'.format(key, result.status_code))
				

	"""
	Create issue type
	"""
	def create_issue_type(self, name, description='', itype='standard'):		
		if itype is '1':
			itype = 'subtask'
		else:
			itype = 'standard'

		result = self.jira.create_issue_type(name, description, itype)
		if result.status_code == 201:
				print('Successfully created issue type {0}'.format(name))
		else:
				print('Error  creating issue type {0}. Error code {1}'.format(name, result.status_code))


	"""
	Create issue types from file
	"""
	def create_issue_types_from_file(self, issue_types):
		for issue_type in issue_types:
			parts = issue_type.split(',')
			if len(parts) < 2:
				print('Input file does not have the right number of columns')
				break
			else:
				name = parts[0].strip()
				description = parts[1].strip()						
				itype = parts[2].strip()
				
				if itype is '':
					itype = 'standard'
			
				self.create_issue_type(name, description, itype)

	"""
	List all statuses
	"""
	def get_all_statuses(self):
		return self.jira.get_all_statuses()
		

	"""
	Get status 
	"""
	def get_status(self, id):
		return self.jira.get_status(id)


	"""
	List statuses of project
	"""
	def get_project_statuses(self, project_key):
		return self.jira.get_project_statuses(project_key)


	"""
	List all resolutions
	"""
	def get_all_resolutions(self):
		return self.jira.get_all_resolutions()
		
	
	"""
	Get resolution 
	"""
	def get_resolution(self, id):
		return self.jira.get_resolution(id)


	"""
	List all priorities
	"""
	def get_all_priorities(self):
		return self.jira.get_all_priorities()
		
	
	"""
	Get priority 
	"""
	def get_priority(self, id):
		return self.jira.get_priority(id)


	"""
	List all custom fields
	"""
	def get_all_custom_fields(self):
		return self.jira.get_all_custom_fields()


	"""
	List all screen fields
	"""
	def get_screen_fields(self, screen_id):
		return self.jira.get_screen_fields(screen_id)


	"""
	Create custom field
	"""
	def create_custom_field(self, name, ctype, searcher_key, description=''):
		result = self.jira.create_custom_field(name, ctype, searcher_key, description)
		if result.status_code == 201:
				print('Successfully created custom field {0}'.format(name))
		else:
				print('Error  creating custom field {0}. Error code {1}'.format(name, result.status_code))
	
	
	"""
	Create custom fields
	"""
	def create_custom_fields(self, custom_fields):
		for custom_field in custom_fields:
			self.create_custom_field(custom_field['name'], custom_field['type'], custom_field['searcher_key'], custom_field['description'])


	"""
	Write content to file
	"""
	def write_to_file(filepath, content):
		outfile = open(filepath, 'w')
		outfile.write(content)
		outfile.close()


"""
Change this main program to use the API.
"""
if __name__ == '__main__':
	with open(sys.argv[1], 'r') as config:
		conf = json.load(config)	 
		url = conf['url']
		username = conf['username']
		password = conf['password']
		client = JiraClient(url, username, password)
		exit = False
		while exit is False:
			print('1. Get All Project Keys')
			print('2. Get All Project Keys CSV')
			print('3. Get All Project Keys Except CSV')
			print('4. Delete Project')
			print('5. Delete Projects')
			print('6. Delete All Projects Except')
			print('7. Create Issue Types')
			print('8. Create Issue Types from CSV')
			print('9. Get All Statuses')
			print('10. Get Status')
			print('11. Get Statuses of Project')
			print('12. Get All Resolutions')
			print('13. Get Resolution')
			print('14. Get All Priorities')
			print('15. Get Priority')
			print('16. Get All Custom Fields')
			print('17. Get Screen Fields')
			print('18. Create Custom Fields from CSV')
			print('0. Exit')
			command = raw_input('Enter command #: ')
			
			if command is '1':
				print(client.get_all_project_keys())
			
			elif command is '2':
				print(client.get_all_project_keys_csv())

			elif command is '3':
				project_keys = raw_input('Enter project keys separated by commas: ')
				print(client.get_all_project_keys_csv_except(project_keys))

			elif command is '4':
				project_key = raw_input('Enter project key: ')
				confirm = raw_input('Delete project with key ' + project_key + ' [y/n]: ')
				if confirm is 'y':
					print(client.jira.delete_project(project_key))

			elif command is '5':
				project_keys = raw_input('Enter project keys separated by commas: ')
				confirm = raw_input('Delete all projects:\n\n ' + project_keys + ' \n\n[y/n]: ')
				if confirm is 'y':
					client.delete_projects(project_keys)

			elif command is '6':
				project_keys = raw_input('Enter project keys separated by commas: ')
				confirm = raw_input('Delete all projects except:\n\n ' + project_keys + ' \n\n[y/n]: ')
				if confirm is 'y':
					client.delete_projects_except(project_keys)
			
			elif command is '7':
				print('Enter issue type details.')
				name = raw_input('Name: ')
				description = raw_input('Description: ')
				itype = raw_input('Type (0: standard/ 1: subtask)[default=0]: ')

				issue_type_string = '\n'.join([name, description, itype])
				confirm = raw_input('Create issue types:\n\n{0}\n\n[y/n]: '.format(issue_type_string))
				if confirm is 'y':
					print(client.create_issue_type(name, description, itype))
				
			elif command is '8':
				filepath = raw_input('Enter absolute file path of file containing issue types: ')

				infile = open(filepath, 'r')
				issue_types = infile.readlines()

				for issue_type in issue_types:
					print(issue_type.strip('\n'))

				confirm = raw_input('\nCreate issue types listed above [y/n]: ')
				
				if confirm is 'y':
					client.create_issue_types_from_file(issue_types)
				
				infile.close()

			elif command is '9':
				statuses = client.get_all_statuses().json()
				for status in statuses:
					status_id = status['id']
					name = status['name']
					category = status['statusCategory']['name']
					print("{0},{1},{2}".format(status_id, name, category))

			elif command == '10':
				id_or_name = raw_input('Enter status id or name: ')
				print(client.get_status(id_or_name).json())

			elif command == '11':
				project_key = raw_input('Enter project key: ')
				issue_types = client.get_project_statuses(project_key).json()
				statuses = {}
				for issue_type in issue_types:
					for status in issue_type['statuses']:						
						statuses[status['id']] = {
							'name': status['name'],
							'category': status['statusCategory']['name']
						}

				for status in statuses:
					print("{0},{1},{2}".format(status, statuses[status]['name'], statuses[status]['category']))

			elif command == '12':
				resolutions = client.get_all_resolutions().json()
				for resolution in resolutions:
					res_id = resolution['id']
					name = resolution['name']
					description = resolution['description']
					print("{0},{1},{2}".format(res_id, name, description))

			elif command == '13':
				id = raw_input('Enter resolution id: ')
				print(client.get_resolution(id).json())

			elif command == '14':
				priorities = client.get_all_priorities().json()
				for priority in priorities:
					priority_id = priority['self'].split('/')[-1]
					name = priority['name']
					description = priority['description']
					print("{0},{1},{2}".format(priority_id, name, description))

			elif command == '15':
				id = raw_input('Enter priority id: ')
				print(client.get_priority(id).json())

			elif command == '16':
				custom_fields = client.get_all_custom_fields()
				for custom_field in custom_fields:
					custom_field_id = custom_field['schema']['customId']
					name = custom_field['name']
					field_type = custom_field['schema']['type']
					custom_field_type = custom_field['schema']['custom']
					print("{0},{1},{2},{3}".format(custom_field_id, name, field_type, custom_field_type))

			elif command == '17':
				screen_ids = raw_input('Enter screen id (CSV for multiple ids): ')
				fields = []
				screen_ids = screen_ids.split(',')
				for screen_id in screen_ids:
					print(screen_id)
					fields = fields + client.get_screen_fields(screen_id.strip()) #.json()
					print(fields)

				for field in fields:
					field_id = field['id']
					name = field['name']
					print("{0},{1}".format(field_id, name))

			elif command == '18':
				filepath = raw_input('Enter absolute file path of file containing custom fields types: ')

				infile = open(filepath, 'r')
				lines = infile.readlines()
				custom_fields = []

				for line in lines:
					print(line.strip('\n'))

				confirm = raw_input('\nCreate custom fields listed above [y/n]: ')				
				
				if confirm is 'y':
					for line in lines:
						parts = line.split(',')
						custom_field = {
							'name': parts[0].strip(),
							'description': parts[1].strip(),
							'type': parts[2].strip(),
							'searcher_key': '{0}searcher'.format(parts[2].strip())
						}

						custom_fields.append(custom_field)
					
					client.create_custom_fields(custom_fields)

				infile.close()

			else:
				exit = True
	
