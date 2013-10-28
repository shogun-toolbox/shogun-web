def get_demos(abstract=True):
	relpath,abstracts=get_abstract(abstract)
	links=[]
	for path in relpath:
		links.append('<a class="overlay" href="http://demos.shogun-toolbox.org/%s"><img src="/static/thumbnails/%s" alt=""/></a>' % (path))

	if abstract:
		return zip(links,abstracts)
	else:
		return links


def get_abstract(abstract):
	import os
	import shogun.settings as settings
	dmodir=settings.DEMO_DIR
	relpath=[]
	abstracts=[]
	for base, dirs, files in os.walk(dmodir, topdown=True):
		for name in [ os.path.join(dmodir, base, f) for f in files if f.endswith(".desc") ]:
			relpath.append(('/'.join(name.split('/')[-2:])[:-5]+'/', '_'.join(name.split('/')[-2:])[:-5] + '.png'))
			if abstract:
				abstracts.append(file(name).read())
	return relpath,abstracts
