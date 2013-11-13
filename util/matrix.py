from django.http import HttpResponse,Http404
from django.template.response import TemplateResponse
from shogun.settings import MATRIX_FILE

def fetch_spreadsheet():
	url='https://docs.google.com/spreadsheet/pub?hl=en&hl=en&key=0Aunb9cCVAP6NdDVBMzY1TjdPcmx4ei1EeUZNNGtKUHc&output=csv'
	import urllib
	f = urllib.urlopen(url)
	csv = f.read()
	file(MATRIX_FILE,'w').write(csv)

def display_matrix(request):
	j=0
	data=[]
	for l in file(MATRIX_FILE).readlines():
		j+=1
		if j<12:
			continue
		#l=l.replace('&', '<td>')
		if len(l)==1:
			data.append("</td></tr></tbody><tbody><tr><td>\n")
		if len(l)<=1:
			continue
		if l.find('shogun')>=0:
			continue
		s=l.split(',')
		if l.find('Bayes')>=0:
			print s

		k=0
		s2=list()
		for i in s:
			k+=1
			if k<3:
				i=i.replace(';', ', ')
				s2.append(i)
				continue

			if '0/1' in i or '0.5' in i:
				i='<img alt="partial" src="/static/design/partial.png">'
			elif '0' in i:
				i='<img alt="cross" src="/static/design/cross.png">'
			elif '1' in i:
				i='<img alt="tick" src="/static/design/tick.png">'
			elif '?' in i:
				i='<img alt="untested" src="/static/design/untested.png">'
			s2.append(i)

		c=0
		for i in s2[:-1]:
			c+=1
			if c==1:
				data.append('%s</td><td width="300">' % i)
			else:
				data.append("%s</td><td>" % i)
		data.append("%s</td></tr><tr><td>" % s2[-1])
	return TemplateResponse(request, 'matrix.html', {'data': ''.join(data)})


def show_related_projecs(request):
	f=file('related_projects.html','w')
	f.write('''
	<table BORDER=0 CELLPADDING=3 CELLSPACING=1 RULES=COLS FRAME=BOX
		><thead>
	<tr><th>
	''')
	j=0
	LASTLINE=9
	for l in file(SRCFILE).readlines():
		j+=1
		if j>=LASTLINE+1:
			break
		if j<5:
			continue
		#l=l.replace('&', '</td><td>')
		if len(l)==1:
			f.write("</td></tr><tr><td>\n")
		if len(l)<=1:
			continue
		s=l.split(',')
		if l.find('Bayes')>=0:
			print s

		s2=list()
		for i in s[1:]:
			s2.append(i)

		if l.find('shogun')>=0:
			for i in s2[:-1]:
				f.write("%s</th><th>" % i)
			f.write("%s</th></tr></thead><tr><td>" % s2[-1])
		else:
			for i in s2[:-1]:
				f.write("%s</td><td>" % i)
			if j==LASTLINE:
				f.write("%s</td></tr></table>" % s2[-1])
			else:
				f.write("%s</td></tr><tr><td>" % s2[-1])

	f.write('''</body></html>''')

if __name__ == '__main__':
	fetch_spreadsheet()
