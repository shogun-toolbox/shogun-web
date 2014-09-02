def decode_image(image):
	import base64
	return base64.b64decode(''.join(image))

def get_first_image_raw(fname, url):
	import os
	image=None
	for line in file(fname).readlines():
		if image is not None:
			if line.startswith('">') or line.startswith('"'):
				image.append('"/></a>')
				return ''.join(image)
			else:
				image.append(line)
		else:
			if line.startswith('<img'):
				image=[]
				image.append(line.replace('<img','<a class="overlay" href="%s" ><img alt="%s" width="140" height="105"' % (url, os.path.basename(fname))))

def get_abstract(fname):
	import json
	import os
	import markdown

	try:
		js=json.load(file(fname))
		for cell in js['worksheets'][0]['cells']:
			if cell['cell_type'] == 'markdown':
				return markdown.markdown(''.join(cell['source']))
	except:
		pass
	return os.path.basename(fname)

def get_first_image(fname):
	image=None
	for line in file(fname).readlines():
		if image is not None:
			if line.startswith('">') or line.startswith('"'):
				return decode_image(image)
			else:
				image.append(line[:-1])
		else:
			if line.startswith('<img'):
				image=[]
				image.append(line[line.find(','):-1])

def get_last_image(fname):
	last_image=None
	image=None
	for line in file(fname).readlines():

		if image is not None:
			if line.startswith('">'):
				last_image=decode_image(image)
				image=None
			else:
				image.append(line[:-1])
		else:
			if line.startswith('<img'):
				image=[]
				image.append(line[line.find(','):-1])
	return last_image

#import sys
#fname=sys.argv[1]
#dst=sys.argv[2]
#
#img=get_first_image(fname)
##img=get_last_image(fname)
#file(dst,'w').write(img)

def get_notebooks(with_abstract=True):
	import os
	all_entries=[]
	for nb in get_notebook_list():
		image=(nb[2],nb[3])
		if image is None:
			continue
		if with_abstract:
			all_entries.append([image,\
					get_abstract(nb[1].replace('.html','.ipynb'))])
		else:
			all_entries.append(image)

	return all_entries

def get_notebook_list(suffix=".html"):
	import os
	import shogun.settings as settings
	nbdir=settings.NOTEBOOK_DIR
	nburl=settings.NOTEBOOK_URL
	nbs=[ '%s/%s' % (nbdir, f) for f in os.listdir(nbdir) if f.endswith(suffix) ]

	nbs=[ nb for nb in nbs if nb.find('template')==-1 ]
	nbs.sort()
	nbs=[(nbs[i][:-5]+'.ipynb', \
		nbs[i], \
		nburl + '/' + os.path.basename(nbs[i]), \
		'/notebooks/thumb/%d/' % i) for i in xrange(len(nbs))]
	return nbs

if __name__ == '__main__':
	x=get_first_image('/home/shogun/static/notebook/current/gaussian_processes.html')
	print x
