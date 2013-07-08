from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from wordui.models import Inflectedforms, Words, Phrases, Texts

class WordsForm(ModelForm):
    class Meta:
        model = Words
        exclude = ('phraseid', 'id', 'charlength', 'formutf8general', 'createdate', 'reverse', )

class InflectedformsForm(ModelForm):
    class Meta:
        model = Inflectedforms
        exclude = ('wordid', 'formutf8general', 'id')

WordFormSet = inlineformset_factory(Words, Inflectedforms, extra = 0)

