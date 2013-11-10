import shogun.settings as settings

import json
from util import notebook
from django.http import HttpResponse,Http404

def list_notebooks(request):
	response_data=[(nb[3],nb[2]) for nb in notebook.get_notebook_list("*.ipynb")]
	response=HttpResponse(json.dumps(response_data), content_type="application/json")
	response['Access-Control-Allow-Origin']='*';
	return response

def get_notebook_thumb(request, nbnum):
	try:
		nbnum=int(nbnum)
	except:
		raise Http404

	notebooks=notebook.get_notebook_list('.html')
	if nbnum<0 or nbnum>=len(notebooks):
		raise Http404

	nb=notebooks[nbnum]
	nburl=settings.NOTEBOOK_URL
	img=notebook.get_first_image(nb[1])
	return HttpResponse(img, content_type="image/png")
