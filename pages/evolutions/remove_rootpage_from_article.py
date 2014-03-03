from django_evolution.mutations import DeleteField


MUTATIONS = [
    DeleteField('Article', 'rootsubpage')
]
