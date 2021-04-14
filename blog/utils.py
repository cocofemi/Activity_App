from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from .models import Post

def parse_all(content):
	parts = content.split()
	mention_counter = 0
	result = {"parsed_text": "", "mentions": []}
	for index, value in enumerate(parts):
		if value.startswith("@"):
			parts[index] = "{mention" + str(mention_counter) + "}"
			mention_counter += 1
			result[u'mentions'].append(slugify(value))
	result[u'parsed_text'] = " ".join(parts)
	return result

# def mention_user(content):
#     parts = content.split()
#     result = []
#     for index, value in enumerate(parts):
#         if value.startswith("@"):
#         	results = value[1:]
#         	user = User.objects.get(username=results)
#         	result.append(user)
#     return result


