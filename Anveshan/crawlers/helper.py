import re

def filter_text_from_content(page, query):
	content = "".join(page["content"])
	#print(query.query)
	pattern = re.compile(query.query, re.IGNORECASE)
	#print(content)
	first_line = None
	text = None
	for line in content.split("."):
		if not first_line:
			first_line = line
		text = pattern.search(line)
		if text:
			return content
	return first_line
