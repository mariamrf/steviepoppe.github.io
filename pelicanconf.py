#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from pyembed.markdown import PyEmbedMarkdown

AUTHOR = 'Stevie Poppe'
SITENAME = 'Onoreto'
SITEURL = 'http://localhost:8000'
#SITEURL = 'https://steviepoppe.net'
PATH = 'content'
TIMEZONE = 'Europe/Paris'
DISPLAY_PAGES_ON_MENU = 'True'
DEFAULT_LANG = 'en'

DEFAULT_DATE_FORMAT = '%a %d %B %Y'
DATE_FORMATS = {
    'en': ('usa','%a %d %B %Y'),
    'jp': ('jpn','%Y-%m-%d(%a)'),
}
DEFAULT_PAGINATION = 10
HOME_MAX_ARTICLES = 4
HOME_MAX_PUBLICATIONS = 4
PAGINATION_PATTERNS = (
    (1, '{base_name}/', '{base_name}/index.html'),
    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
)

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

#SITE_THUMBNAIL = "/images/pp-thumbnail-small.png"
SITE_THUMBNAIL = "logo2.png"

INDEX_KEYWORDS = "Stevie Poppe, blog, Japan, Japanese, language"
INDEX_DESCRIPTION = "A personal blog on Japan, Japanese Studies at university, and other more technical or general issues pertaining my academic studies."
# NEST Template
THEME = 'nest'
SITESUBTITLE = u'| Onoreto'
# Minified CSS
NEST_CSS_MINIFY = False
# Add items to top menu before pages
MENUITEMS = [('Home', '/'), ('Blog', '/blog/'),('Categories','/blog/category/')]
# Add header background image from content/images : 'background.jpg'
NEST_HEADER_IMAGES = ''
NEST_HEADER_LOGO = '/image/logo2.png'
# Footer
NEST_SITEMAP_COLUMN_TITLE = u'Sitemap'
NEST_SITEMAP_MENU = [('Home','/'),('Blog','/blog/'),('Categories','/blog/category/'),('Tagcloud','/blog/tags/')]
NEST_COPYRIGHT = u'Copyright © Stevie Poppe 2016-2023 (CC BY-NC-SA 4.0)'
# archives.html
NEST_ARCHIVES_CONTENT_TITLE = u'Archives'
NEST_ARTICLE_HEADER_MODIFIED = u'modified'
NEST_ARTICLE_HEADER_IN = u'in category'
# categories.html
NEST_CATEGORIES_HEAD_TITLE = u'Categories'
# category.html
NEST_CATEGORY_HEAD_TITLE = u'Category'

# tag.html
NEST_TAG_HEAD_TITLE = u'Tag'
# pagination.html
NEST_PAGINATION_PREVIOUS = u'Previous'
NEST_PAGINATION_NEXT = u'Next'
# # period_archives.html
NEST_PERIOD_ARCHIVES_CONTENT_TITLE = u'Archives for'
# # tags.html
NEST_TAGS_CONTENT_TITLE = u'Tagcloud'
NEST_TAGS_CONTENT_LIST = u'tagged'
NEST_TAGS_HEAD_TITLE = u'Tags'
NEST_INDEX_HEAD_TITLE = u'Home'

# search.html
SEARCH_HEAD_TITLE = u'Search'

# Static files
STATIC_PATHS = ['images', 'extra/robots.txt', 'extra/favicon-32.png', 'extra/favicon-96.png', 'extra/favicon-128.png', 'extra/favicon-180.png', 'extra/favicon-192.png', 'files','extra/CNAME']
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon-32.png': {'path': 'favicon-32.png'},
    'extra/favicon-96.png': {'path': 'favicon-96.png'},
    'extra/favicon-128.png': {'path': 'favicon-128.png'},
    'extra/favicon-180.png': {'path': 'favicon-180.png'},
    'extra/favicon-192.png': {'path': 'favicon-192.png'},
    'extra/CNAME': {'path': 'CNAME'}
}
#TEMPLATE_PAGES = {'src/aboutme.html': 'pages/aboutme.html'}
RELATED_POSTS_MAX = 5

TIPUE_SEARCH = 'true'
FEED_USE_SUMMARY = True
SUMMARY_FOOTNOTES_MODE = "remove"
PLUGIN_PATHS = ['./pelican-plugins/']
#PLUGINS = ['tipue_search', "better_figures_and_images",'extract_toc','summary_footnotes',
#'related_posts',"tag_cloud",'pin_to_top','summary','assets','pelican_youtube','feed_summary']

PLUGINS = ['tipue_search','extract_toc','summary_footnotes','pelican.plugins.neighbors', 'pelican.plugins.liquid_tags',
'related_posts',"tag_cloud",'pin_to_top','summary','assets','feed_summary']
DIRECT_TEMPLATES = (('index', 'tags', 'categories', 'archives', 'search', 'sitemap'))
PAGINATED_TEMPLATES = {'archives': None, 'index': 50, 'category': None, 'author': None}
SITEMAP_SAVE_AS = 'sitemap.xml'
#MD_EXTENSIONS = ['codehilite','extra','smarty', 'toc(anchorlink=True)', 'japanese', 'del_ins', 'pullquote','furigana',PyEmbedMarkdown()]

LIQUID_TAGS = ["img","youtube"]
LIQUID_CONFIGS = (('PATH', '.', "The default path"), ('SITENAME', 'Default Sitename', 'The name of the site'))


PYGMENTS_RST_OPTIONS = {'classprefix': 'pgcss', 'linenos': 'table'}

MARKDOWN = {
    'extensions' : ['smarty', 'toc', 'markdown.extensions.japanese', 'markdown.extensions.furigana', 'markdown_del_ins', 'markdown.extensions.pullquote'],

    #'extensions' : ['codehilite','extra','smarty', 'toc', 'markdown.extensions.japanese', 'markdown_del_ins', 'markdown.extensions.pullquote','furigana',PyEmbedMarkdown()],
    'output_format': 'html5',
    'extension_configs': {
        'markdown.extensions.extra': {},
        'markdown.extensions.admonition': {},
        # 'markdown.extensions.codehilite': {
        #     'css_class': 'highlight',
        #     'linenums': 'True'
        # },
        'pymdownx.keys': {
            #'separator': '?'
        },
        'pymdownx.smartsymbols': {},
        'pymdownx.highlight': {'css_class': 'highlight','linenums': 'True','linenums_style': 'table', 'pygments_style': 'emacs'},
        'pymdownx.superfences': {},
        'pymdownx.inlinehilite': {},
        #'pymdownx.emoji': {},
        #'markdown.extensions.meta': {},
        'smarty' : {
            'smart_angled_quotes' : 'true'
        },
        'footnotes' : {
            'SEPARATOR' : '-'
        },
        'markdown.extensions.toc': {
          #  'permalink': 'true',
            'anchorlink': 'true',
        },
     'markdown.extensions.meta': {}
       # 'pyembed.markdown': {}
    }
     #  'codehilite' : {'noclasses':True, 'pygments_style':"native"}, 'extra'
}

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
#AUTHOR_FEED_ATOM = None
#AUTHOR_FEED_RSS = None
#FEED_ALL_RSS = None
CATEGORY_FEED_RSS = 'feeds/{slug}.rss.xml'
FEED_RSS = 'feeds/rss.xml'
FEED_ALL_RSS = 'feeds/all.rss.xml'

FEED_DOMAIN = SITEURL

SUMMARY_MAX_LENGTH = 400
SUMMARY_MAX_LENGTH_HOME = 200
#SUMMARY_USE_FIRST_PARAGRAPH = True

ALLOW_MENU_ICON = True

# Social widget
SOCIAL = (('Google Scholar', 'https://scholar.google.com/citations?user=Sok6SPoAAAAJ'),
          ('ORCID', 'https://orcid.org/0000-0002-8795-7336'),
          ('Linkedin', 'https://be.linkedin.com/in/stevie-poppe'),
          ('SoundCloud', 'https://soundcloud.com/onoreto'),
		  # ('YouTube', 'https://www.youtube.com/channel/UC-wW8gg1lGVn99X9ue6_eVA'),
          # ('Flickr', 'https://www.flickr.com/photos/147061735@N04/'),
          ('Twitter', 'https://twitter.com/PoppeStevie'))

#SOCIAL = (('Linkedin', 'https://be.linkedin.com/in/stevie-poppe-9048b395'),
#		  ('YouTube', 'https://www.youtube.com/channel/UC-wW8gg1lGVn99X9ue6_eVA'),
#          ('Flickr', 'https://www.flickr.com/photos/147061735@N04/'),
#          ('Twitter', 'https://twitter.com/PoppeStevie'),
#          ('Goodreads', 'https://www.goodreads.com/user/show/35676792-stevie-poppe'))

#GZIP_CACHE = True
DISQUS_SITENAME = 'steviepoppe'

#GOOGLE_ANALYTICS = 'UA-82857115-1'
RESPONSIVE_IMAGES = True

GOOGLE_PLUS_ID = '112676714486792414615'

#ARTICLE_URL = 'blog/{slug}'
#ARTICLE_SAVE_AS = 'blog/{slug}/index.html'
ARTICLE_URL = "blog/{date:%Y}/{date:%m}/{slug}/"
ARTICLE_SAVE_AS = "blog/{date:%Y}/{date:%m}/{slug}/index.html"

ARCHIVES_URL = 'blog/'
ARCHIVES_SAVE_AS = 'blog/index.html'

PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'

TAGS_URL = 'blog/tags/'
TAGS_SAVE_AS = 'blog/tags/index.html'

TAG_URL = 'blog/tags/{slug}/'
TAG_SAVE_AS = 'blog/tags/{slug}/index.html'

CATEGORY_URL = 'blog/category/{slug}/'
CATEGORY_SAVE_AS = 'blog/category/{slug}/index.html'
CATEGORIES_URL = 'blog/category/'
CATEGORIES_SAVE_AS = 'blog/category/index.html'


#SEARCH_URL = 'search'
#SEARCH_SAVE_AS = 'search.html'

#INDEX_URL = 'blog'
#INDEX_SAVE_AS = "blog/index.html"

TAG_CLOUD_STEPS = 4
TAG_CLOUD_MAX_ITEMS = 100
TAG_CLOUD_SORTING = 'random'
TAG_CLOUD_BADGE = True