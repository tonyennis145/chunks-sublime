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
		# urls = settings.get("chunks_urls")

		api_version = sublime.active_window().active_view().settings().get('chunks_api_version', settings.get("chunks_api_version"))
		urls = sublime.active_window().active_view().settings().get('chunks_urls', settings.get("chunks_urls"))

		create_chunk_url = urls['api_root'] + "/" + api_version + "/chunks"

		authentication_token = sublime.active_window().active_view().settings().get('chunks_authentication_token', settings.get("chunks_authentication_token"))

		default_snippet_template = sublime.active_window().active_view().settings().get('chunks_default_snippet_template', settings.get("chunks_default_snippet_template"))
		snippet_templates = sublime.active_window().active_view().settings().get('chunks_snippet_templates', settings.get("chunks_snippet_templates"))
		snippet_template = snippet_templates[default_snippet_template]

		# Get selected text
		selections = self.view.sel()

		# The following code needs to be made threadsafe
		for selection in selections:

			# Get selected text
			content = self.view.substr(selection)

			data = {
			    "chunk" : {
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

			try:
				response = urllib.request.urlopen(request)
				response_as_string = response.read().decode('utf8')
				response_as_json = json.loads(response_as_string)

				chunk_info = response_as_json["chunk"]
				
				chunk_identifier = chunk_info['identifier']
				chunk_content = chunk_info['content']

				shortened_original_content = chunk_content[:10] + (chunk_content[10:] and '..')

				replacement_text = snippet_template.replace("{identifier}", chunk_identifier)
				replacement_text = replacement_text.replace("{label}", shortened_original_content)

				# Make the replacement
				self.view.replace(edit, selection, replacement_text )

			except urllib.error.HTTPError as e:

				response_as_string = e.read().decode('utf8')
				response_as_json = json.loads(response_as_string)
				message = response_as_json['message']

				sublime.error_message(message)


