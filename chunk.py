import sublime, sublime_plugin, urllib, urllib.request, json

class ChunkCommand(sublime_plugin.TextCommand):

	# To do:
	# Threading
	# Getting 
	# Warning if user accidentally hits the shortcut twice and tries to chunk the resulting snippet

	def run(self, edit):

		# Load settings
		settings = sublime.load_settings("Chunks.sublime-settings")

		# Get variables from settings
		urls = settings.get("urls")
		create_chunk_url = urls['create_chunk']
		authentication_token = settings.get("authentication_token")
		project_id = settings.get("project_id")

		default_snippet_template = settings.get("default_snippet_template")
		snippet_templates = settings.get("snippet_templates")
		snippet_template = snippet_templates[default_snippet_template]

		# Get selected text
		selections = self.view.sel()

		# The following code needs to be made threadsafe
		for selection in selections:

			# Get selected text
			content = self.view.substr(selection)

			data = {
			    "chunk" : {
			        "project_id" : project_id,
			        "content" : content
			    },
			    "authentication_token" : authentication_token
			}

			# Urllib only accepts encoded data
			params = json.dumps(data).encode('utf8')

			request = urllib.request.Request(
				create_chunk_url, 
				data=params, 
				headers={'Content-Type': 'application/json','User-Agent': 'Mozilla/5.0' }
			)

			response = urllib.request.urlopen(request)
			response_as_string = response.read().decode('utf8')
			response_as_json = json.loads(response_as_string)

			chunk_identifier = response_as_json['identifier']
			chunk_content = response_as_json['content']

			shortened_original_content = chunk_content[:10] + (chunk_content[10:] and '..')

			replacement_text = snippet_template.replace("{identifier}", chunk_identifier)
			replacement_text = replacement_text.replace("{label}", shortened_original_content)

			# Make the replacement
			self.view.replace(edit, selection, replacement_text )