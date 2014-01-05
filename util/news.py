def convert_news(srcname, dstname):
	dst=file(dstname,'w')
	dst.write('<new>\n')
	first=False
	content=[]
	for line in file(srcname).readlines():
		if line.startswith('2'):
			if not first:
				date=line.split()[0]
				author=line[len(date):].split('<')[0].strip()
				mail=line.split('<')[1].split('>')[0]
				first=True
				continue
			else:
				break

		if line.find('* SHOGUN Release') != -1:
			sg_ver=line.strip().split()[4]
			libshogun_ver=line.split('(')[1].split()[1][:-1]
			data_ver=line.split('(')[1].split()[3][:-1]
			param_ver=line.split('(')[1].split()[5][:-1]
			continue
		content.append(line)


	dst.write('    <updated_date>%s</updated_date>\n' % date)
	dst.write('    <author>%s</author>\n' % author)
	dst.write('    <sg_ver>%s</sg_ver>\n' % sg_ver)
	dst.write('    <sg_bver>%s</sg_bver>\n' % sg_ver)
	dst.write('    <libshogun_ver>%s</libshogun_ver>\n' % libshogun_ver)
	dst.write('    <data_ver>%s</data_ver>\n' % data_ver)
	dst.write('    <param_ver>%s</param_ver>\n' % param_ver)
	dst.write('    <content>\n')
	dst.write(''.join(content))
	dst.write('    </content>\n')
	dst.write('</new>\n')
	dst.close()

if __name__ == '__main__':
	import sys
	convert_news(sys.argv[1], sys.argv[2])
