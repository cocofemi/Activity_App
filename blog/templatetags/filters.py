from django import template
from django.utils.html import format_html, escape
from blog.utils import parse_all
from notify.signals import notify

register = template.Library()

@register.filter(name='parse_content')
def parse_content(content_object, autoescape=False):
	parsed_content_dict = parse_all(content_object)

	# return a dictionary that looks like
    # {'hashtag0': <span>#hash</span", 'mention0': <a>@mike</a>}
	encoded = encode_content(parsed_content_dict)

	#merge
	parsed_content_dict[u'parsed_text'] = escape(
		parsed_content_dict[u'parsed_text'])
	statement = parsed_content_dict.get(u'parsed_text').format(**encoded)
	return statement


def encode_content(parsed_content_dict):
	result = {}

	# adding html component to mentions
	for index, value in enumerate(parsed_content_dict.get(u'mentions')):
		result['mention'+str(index)] = \
			u'<span class="mention"><a href="{link}">@{mention}</a></span>'\
			.format(mention=escape(value), link="/user/{0}"\
			.format(escape(value)))
	return result