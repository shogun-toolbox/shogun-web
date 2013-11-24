#!/usr/bin/env python

import os
import sys
import urllib2
from github import Github

# Dictionary markdown file identifier -> url with markdown content
MD_FILES = {'INSTALL': 'https://raw.github.com/shogun-toolbox/shogun/develop/INSTALL.md',
            'README': 'https://raw.github.com/shogun-toolbox/shogun/develop/README.md',
            'README_cmake': 'https://raw.github.com/shogun-toolbox/shogun/develop/README_cmake.md',
            'README_developer': 'https://raw.github.com/shogun-toolbox/shogun/develop/README_developer.md'}

def get_html_from_md(md_file='README'):
  if md_file not in MD_FILES:
    print 'Unknown markdown file %s.' % md_file
    return

  md_content = urllib2.urlopen(MD_FILES[md_file]).read()
  g = Github()
  return g.render_markdown(md_content)

if __name__ == "__main__":
  if not os.path.exists('static/md2html'):
    os.mkdir('static/md2html')
  elif os.path.isfile('static/md2html'):
    print 'Cannot write output files. Please delete or rename the file static/md2html.'
    sys.exit(0)

  for md_file in MD_FILES:
    html_content = get_html_from_md(md_file)
    html_file = open("static/md2html/%s.html" % md_file, "w")
    html_file.write(html_content)
    html_file.close()
