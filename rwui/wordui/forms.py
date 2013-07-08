from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.forms.fields import CharField
from django.forms.widgets import Textarea
from wordui.models import Inflectedforms, Words, Phrases, Texts

class WordsForm(ModelForm):
    phrase = CharField(widget = Textarea, required = False)
    url = CharField(required = False)
    def __init__(self, *args, **kwargs):
        super(WordsForm, self).__init__(*args, **kwargs)
        self.fields['form'].label = 'Base Form'
        self.fields['prefixid'].label = 'Prefix'
        self.fields['suffixid'].label = 'Suffix'
        self.fields['definition'].label = 'Definition'
        self.fields['domainid'].label = 'Domain'
        self.fields['phrase'].widget.attrs['disabled'] = 'disabled'
        self.fields['url'].widget.attrs['disabled'] = 'disabled'

    class Meta:
        model = Words
        exclude = ('id', 'phraseid', 'charlength', 'formutf8general', 'createdate', 'reverse', )

class InflectedformsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(InflectedformsForm, self).__init__(*args, **kwargs)
        self.fields['form'].label = 'Inflected Form'
        self.fields['noapp'].label = 'Number of Appearances'
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['noapp'].required = False
            self.fields['noapp'].widget.attrs['disabled'] = 'disabled'

    def clean_phraseid(self):
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.noapp
        else:
            return self.cleaned_data.get('noapp', None)

    class Meta:
        model = Inflectedforms
        exclude = ('wordid', 'formutf8general', 'id')
