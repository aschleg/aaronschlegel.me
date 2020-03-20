#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import unicode_literals

# General Settings

AUTHOR = 'Aaron Schlegel'
SITENAME = "Aaron Schlegel's Notebook of Interesting Things"
SITESUBTITLE = ''
SITEURL = 'https://aaronschlegel.me'
SITE_SUMMARY = 'The Blog and Notebooks of Aaron Schlegel'

MARKUP = ('md', 'ipynb')

PLUGIN_PATHS = ['./plugins']
PLUGINS = ['related_posts', 'ipynb.markup', 'rmd_reader', 'render_math']

THEME = 'themes/gum'

# RMD_READER_RENAME_PLOT = 'directory'
# RMD_READER_KNITR_OPTS_CHUNK = {'fig.path': 'figure/'}

PATH = 'content'
STATIC_PATHS = ['figure']
ARTICLE_PATHS = ['posts']

IGNORE_FILES = ['content/draft', '.ipynb_checkpoints']

# Gum Theme Options

GITHUB_URL = 'https://github.com/aschleg'
TWITTER_URL = 'http://www.twitter.com/Aaron_Schlegel'
GOOGLEPLUS_URL = 'https://plus.google.com/u/0/102881569650657098667'
TWITTER_USERNAME = '@Aaron_Schlegel'
GOOGLE_ANALYTICS_ID = 'UA-48350829-2'
GOOGLE_ANALYTICS_SITENAME = 'aaronschlegel.me'

TIMEZONE = 'America/Los_Angeles'
DEFAULT_LANG = 'English'

# Feeds

FEED_DOMAIN = SITEURL
FEED_ALL_ATOM = 'feed/all.xml'
CATEGORY_FEED_ATOM = 'feed/%s.xml'
TAG_FEED_ATOM = 'feed/%s.tag.xml'
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ('R-Bloggers', 'https://www.r-bloggers.com'),
)

# Social widget
SOCIAL = (('Github', 'https://github.com/aschleg'),
          ('Linkedin', 'https://linkedin.com/in/aaronschlegel'),
          ('Twitter', 'http://www.twitter.com/Aaron_Schlegel'),)

# Pagination
DEFAULT_PAGINATION = 20

# Related Posts
RELATED_POSTS_MAX = 5

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
