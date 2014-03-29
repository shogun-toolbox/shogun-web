#!/usr/bin/env python

import os, sys, getopt

try:
  from shogun.settings import SRC_DIR
except ImportError:
  print 'Module shogun.settings not found. Add the root directory of shogun-web to the PYTHONPATH.'
  print 'For instance, from shogun-web\'s root directory do: PYTHONPATH=. util/gfmarkdown.py'
  sys.exit(0)

try:
  from github import Github
except ImportError:
  print 'No github module available. Please install it with pip install PyGitHub'
  print 'or see the documentation at http://jacquev6.github.io/PyGithub/.'
  sys.exit(0)


def print_help():
  print 'markdown.py -d <root directory to recursively look for md files>'


def get_html_from_md(md_fname):
  md_file = open(md_fname, 'r')
  md_content = md_file.read()
  md_file.close()
  g = Github()
  return g.render_markdown(md_content)


# Main
if __name__ == "__main__":
  rootdir = SRC_DIR

  try:
    opts, args = getopt.getopt(sys.argv[1:], 'hd:')
  except getopt.GetoptError:
    print_help()
    sys.exit(2)

  for opt, arg in opts:
    if opt == '-h':
      print_help()
      sys.exit(0)
    elif opt == '-d':
      rootdir = arg

  print 'The root directory is %s.' % rootdir

  if not os.path.exists('templates/md2html'):
    os.mkdir('templates/md2html')
  elif os.path.isfile('templates/md2html'):
    print 'Cannot write output files. Please delete or rename the file templates/md2html.'
    sys.exit(0)

  for root, dirs, files in os.walk(rootdir):
    for fname in files:
      if fname.endswith('.md'):
        try:
          html_content = get_html_from_md(os.path.join(root, fname))
          html_file = open("templates/md2html/%s.html" % fname[:-3], "w")
          html_file.write(html_content)
          html_file.close()
          print '%s rendered to %s.html.' % (fname, fname[:-3])
        except UnicodeDecodeError:
          print 'Decoding ERROR. Could not render to HTML %s.' % fname
