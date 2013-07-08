# tutorial/tables.py
import django_tables2 as tables
from django_tables2.utils import Accessor  # alias for Accessor
from wordui.models import Inflectedforms

class InflectedformsTable(tables.Table):
    edit_entries = tables.TemplateColumn('<a href="/wid/{{record.id}}">Edit</a>')
    Form = tables.Column(accessor = 'form')
    NoApp = tables.Column(accessor = 'noapp')
    class Meta:
        attrs = {'class': 'paleblue'}
