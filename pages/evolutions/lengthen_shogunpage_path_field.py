from django_evolution.mutations import ChangeField


MUTATIONS = [
    ChangeField('ShogunPage', 'path', initial=None, max_length=40)
]
