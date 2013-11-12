import sys
DSTFILE='matrix.html'
SRCFILE='matrix.csv'

f=file(DSTFILE,'w')


f.write('''
		<html>
		<head>
		<style>
			div.vertical
			{
				margin-top: -65px;
				margin-left: -95px;
				position: absolute;
				width: 200px;

				/* Safari/Chrome */
				-webkit-transform: rotate(-90deg);

				/* Firefox */
				-moz-transform: rotate(-90deg);

				/* Opera */
				-o-transform: rotate(-90deg);

				filter:  progid:DXImageTransform.Microsoft.BasicImage(rotation=-0.6225);  /* IE6,IE7 */

				-ms-filter: "progid:DXImageTransform.Microsoft.BasicImage(rotation=-0.6225)"; /* IE8 */
			}

			th.vertical
			{
				height: 15ex;
				line-height: 14px;
				padding-bottom: 0px;
				text-align: left;
			}
		</style>
		</head>
		<body>
<p>A comparison of shogun with the popular machine learning toolboxes weka, kernlab, dlib, nieme, orange, java-ml, pyML, mlpy, pybrain, torch3, scikit-learn. A '?' denotes unkown, '-' feature is missing. This table is availabe as a <a href="http://spreadsheets.google.com/ccc?key=0Aunb9cCVAP6NdDVBMzY1TjdPcmx4ei1EeUZNNGtKUHc&hl=en">google spreadsheet</a>.</p>
<table BORDER=1 CELLPADDING=3 CELLSPACING=1 
    RULES=GROUPS FRAME=BOX
	>
<thead>
<tr>
<th></th>
<th class="vertical"><div class="vertical">feature</div></th>
<th class="vertical"><div class="vertical">shogun</div></th>
<th class="vertical"><div class="vertical">weka</div></th>
<th class="vertical"><div class="vertical">kernlab</div></th>
<th class="vertical"><div class="vertical">dlib</div></th>
<th class="vertical"><div class="vertical">nieme</div></th>
<th class="vertical"><div class="vertical">orange</div></th>
<th class="vertical"><div class="vertical">java-ml</div></th>
<th class="vertical"><div class="vertical">pyML</div></th>
<th class="vertical"><div class="vertical">mlpy</div></th>
<th class="vertical"><div class="vertical">pybrain</div></th>
<th class="vertical"><div class="vertical">torch3</div></th>
<th class="vertical"><div class="vertical">scikit-learn</div></th>
</tr>
</thead>
<tbody>
<tr><td>
''')
j=0
for l in file(SRCFILE).readlines():
	j+=1
	if j<12:
		continue
	#l=l.replace('&', '<td>')
	if len(l)==1:
		f.write("</td></tr></tbody><tbody><tr><td>\n")
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
			i='<img alt="partial" src="media/images/partial.png">'
		elif '0' in i:
			i='<img alt="cross" src="media/images/cross.png">'
		elif '1' in i:
			i='<img alt="tick" src="media/images/tick.png">'
		elif '?' in i:
			i='<img alt="untested" src="media/images/untested.png">'
		s2.append(i)

	c=0
	for i in s2[:-1]:
		c+=1
		if c==1:
			f.write('%s</td><td width="300">' % i)
		else:
			f.write("%s</td><td>" % i)
	f.write("%s</td></tr><tr><td>" % s2[-1])
f.write('''
</td></tr><tr><td colspan=13></td></tr></tbody>
</table>
''')

f=file('related_projects.html','w')
f.write('''
<table BORDER=1 CELLPADDING=3 CELLSPACING=1 RULES=COLS FRAME=BOX
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
