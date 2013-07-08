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
from wordui.forms import WordFormSet
from django.forms.models import modelformset_factory

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

def edit_word00(request, context):
    wid = int(request.path.split('/')[2])
    ifobject = Inflectedforms.objects.get(id  = wid)
    table = InflectedformsTable([ifobject])
    RequestConfig(request).configure(table)
    return render(request, "word_detail.html", {'table' : table})


def edit_word01(request, context):
    if request.method == 'POST':
        form = InflectedForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/word_detail.html')
    else:
        ifobject = Inflectedforms.objects.get(id = int(request.path.split('/')[2]))
        wordobject = ifobject.wordid
        form = WordFormSet(instance = wordobject)
        return render_to_response("word_detail.html", \
                                  {'form' : form,}, \
                                  context_instance = RequestContext(request),)

def edit_word(request, context):
    if request.method == 'POST':
        form = InflectedForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/word_detail.html')
    else:
        ifmodel = modelformset_factory(Inflectedforms, form = InflectedformsForm)
        wmodel = modelformset_factory(Words, form = WordsForm)

        ifobject = Inflectedforms.objects.get(id = int(request.path.split('/')[2]))
        wordobject = ifobject.wordid

        ifform = ifmodel(instance = ifobject)
        wform = wmodel(instance = wordobject)
        return render_to_response("word_detail.html", \
                                  {'ifform' : ifform, 'wform' : wform}, \
                                  context_instance = RequestContext(request),)
