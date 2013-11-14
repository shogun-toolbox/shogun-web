from django.template.response import TemplateResponse
from shogun.settings import MATRIX_FILE

def fetch_spreadsheet():
	url='https://docs.google.com/spreadsheet/pub?hl=en&hl=en&key=0Aunb9cCVAP6NdDVBMzY1TjdPcmx4ei1EeUZNNGtKUHc&output=csv'
	import urllib
	f = urllib.urlopen(url)
	csv = f.read()
	file(MATRIX_FILE,'w').write(csv)


def get_matrix():
	j=0
	table=[]
	for l in file(MATRIX_FILE).readlines():
		j+=1
		if j<19:
			continue
		#l=l.replace('&', '<td>')
		if len(l)==1:
			table.append("</td></tr></tbody><tbody><tr><td>\n")
		if len(l)<=1:
			continue
		if l.find('shogun')>=0:
			continue
		s=l.split(',')

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
				table.append('<strong>%s</strong></td><td width="300">' % i)
			else:
				table.append("%s</td><td>" % i)
		table.append("%s</td></tr><tr><td>" % s2[-1])

	return ''.join(table)


def get_related_projects():
	tab=[]
	j=0
	LASTLINE=17
	for l in file(MATRIX_FILE).readlines():
		j+=1
		if j>=LASTLINE+1:
			break
		if j<4:
			continue
		if len(l)==1:
			tab.append("</td></tr><tr><td>\n")
		if len(l)<=1:
			continue
		s=l.split(',')

		s2=list()
		for i in s[1:6]:
			s2.append(i)

		if l.find('created')>=0:
			for i in s2[:-1]:
				tab.append("%s</th><th>" % i)
			tab.append("%s</th></tr></thead><tr><td>" % s2[-1])
		else:
			tab.append("<strong>%s</strong></td><td>" % s2[0])
			for i in s2[1:-1]:
				tab.append("%s</td><td>" % i)
			if j==LASTLINE:
				tab.append("%s</td></tr></table>" % s2[-1])
			else:
				tab.append("%s</td></tr><tr><td>" % s2[-1])
	return ''.join(tab)


if __name__ == '__main__':
	fetch_spreadsheet()
