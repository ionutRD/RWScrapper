# Create your views here.
from django_tables2   import RequestConfig
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import UpdateView
from django.http import HttpResponseRedirect
from wordui.models import Inflectedforms, Words, Phrases, Texts, Domains, Prefixes, Suffixes
from wordui.tables import InflectedformsTable
from wordui.forms import InflectedformsForm
from wordui.forms import WordsForm
from django.forms.models import modelformset_factory
from django.forms.models import model_to_dict

def inflectedformslower(request):
    values = Inflectedforms.objects.distinct().values('id', 'form', 'noapp')
    values = filter(lambda x : x['form'][0].islower(), values)
    table = InflectedformsTable(values)
    RequestConfig(request).configure(table)
    return render(request, 'newwords.html', {'table' : table})

def inflectedformsupper(request):
    values = Inflectedforms.objects.distinct().values('id', 'form', 'noapp')
    values = filter(lambda x : x['form'][0].isupper(), values)
    table = InflectedformsTable(values)
    RequestConfig(request).configure(table)
    return render(request, 'propernames.html', {'table' : table})

def noforms(request):
    return render(request, "index.html", {})

def edit_word(request, context):
    ifobj = Inflectedforms.objects.get(id = int(request.path.split('/')[2]))
    wordobj = ifobj.wordid
    if request.method == 'POST':
        ifform = InflectedformsForm(request.POST, instance = ifobj)
        wordform = WordsForm(request.POST, instance = wordobj)
        if ifform.is_valid() and wordform.is_valid:
            ifobj = ifform.save(commit = False)
            wordobj = wordform.save(commit = False)
            ifobj.save()
            wordobj.save()
            return HttpResponseRedirect('/word_ok.html')
    else:
        worddict = model_to_dict(wordobj)
        worddict['phrase'] = wordobj.phraseid.phrasecontent
        worddict['url'] = wordobj.phraseid.textid.canonicalurl

        ifform = InflectedformsForm(instance = ifobj)
        wform = WordsForm(initial = worddict)
        return render_to_response("word_detail.html", \
                                  {'ifform' : ifform, 'wform' : wform}, \
                                  context_instance = RequestContext(request),)
