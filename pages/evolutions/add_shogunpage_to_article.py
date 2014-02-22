from django_evolution.mutations import AddField
from django.db import models


MUTATIONS = [
    AddField('Article', 'shogunpage', models.ForeignKey, null=True, related_model=u'pages.ShogunPage')
]
