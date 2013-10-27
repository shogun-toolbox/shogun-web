def get_demos(abstract=True):
	links=[\
'<a class="overlay" href="http://demos.shogun-toolbox.org/classifier/binary/"><img src="/static/thumbnails/binary_demo_thumb.png" alt=""/></a>',
'<a class="overlay" href="http://demos.shogun-toolbox.org/dimred/tapkee/"><img src="/static/thumbnails/dimred_tapkee_thumb.png" alt=""/></a>',
'<a class="overlay" href="http://demos.shogun-toolbox.org/regression/gp/"><img src="/static/thumbnails/gp_regress_thumb.png" alt=""/></a>',
'<a class="overlay" href="http://demos.shogun-toolbox.org/misc/kernel_matrix/"><img src="/static/thumbnails/kernel_mat_thumb.png" alt=""/></a>',
'<a class="overlay" href="http://demos.shogun-toolbox.org/clustering/kmeans/"><img src="/static/thumbnails/kmeans_demo_thumb.png" alt=""/></a>',
'<a class="overlay" href="http://demos.shogun-toolbox.org/application/language_detect/"><img src="/static/thumbnails/lang_detect_thumb.png" alt=""/></a>',
'<a class="overlay" href="http://demos.shogun-toolbox.org/application/ocr/"><img src="/static/thumbnails/ocr_demo_thumb.png" alt=""/></a>',
'<a class="overlay" href="http://demos.shogun-toolbox.org/classifier/perceptron/"><img src="/static/thumbnails/perceptron_thumb.png" alt=""/></a>',
'<a class="overlay" href="http://demos.shogun-toolbox.org/regression/svr/"><img src="/static/thumbnails/svr_demo_thumb.png" alt=""/></a>',
'<a class="overlay" href="http://demos.shogun-toolbox.org/misc/tree/"><img src="/static/thumbnails/tree_demo_thumb.png" alt=""/></a>',
'<a class="overlay" href="http://demos.shogun-toolbox.org/classifier/multiclass/"><img src="/static/thumbnails/multiclass_thumb.png" alt=""/></a>']

	abstracts=["1","2","3","4","5","6","7","8","9","10"]
	if abstract:
		return zip(links,abstracts)
	else:
		return links
