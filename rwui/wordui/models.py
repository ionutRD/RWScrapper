# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models


class Inflections(models.Model):
    id = models.IntegerField(primary_key = True)
    description = models.CharField(max_length=765)
    shortform = models.CharField(max_length=30, db_column='shortForm', blank=True) # Field name made lowercase.

    def __unicode__(self):
        return unicode(self.description)

    class Meta:
        db_table = u'Inflections'

class Prefixes(models.Model):
    id = models.IntegerField(primary_key = True)
    form = models.CharField(max_length=60)
    formutf8general = models.CharField(max_length=60, db_column='formUtf8General') # Field name made lowercase.
    prefixlength = models.IntegerField(db_column='prefixLength') # Field name made lowercase.
    meaning = models.TextField(blank=True)

    def __unicode__(self):
        return unicode(self.form)

    class Meta:
        db_table = u'Prefixes'


class Suffixes(models.Model):
    id = models.IntegerField(primary_key = True)
    form = models.CharField(max_length=60)
    formutf8general = models.CharField(max_length=60, db_column='formUtf8General') # Field name made lowercase.
    suffixlength = models.IntegerField(db_column='suffixLength') # Field name made lowercase.
    meaning = models.TextField(blank=True)

    def __unicode__(self):
        return unicode(self.form)

    class Meta:
        db_table = u'Suffixes'


class Clitictokens(models.Model):
    id = models.IntegerField(primary_key = True)
    form = models.CharField(max_length=300)
    formnodia = models.CharField(max_length=300, db_column='formNoDia') # Field name made lowercase.

    def __unicode__(self):
        return unicode(self.form)

    class Meta:
        db_table = u'CliticTokens'

class Clitics(models.Model):
    id = models.IntegerField(primary_key = True)
    form = models.CharField(max_length=300)
    formnohyphen = models.CharField(max_length=300, db_column='formNoHyphen') # Field name made lowercase.
    formnodia = models.CharField(max_length=300, db_column='formNoDia') # Field name made lowercase.

    def __unicode__(self):
        return unicode(self.form)

    class Meta:
        db_table = u'Clitics'

class Domains(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length=300)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        db_table = u'Domains'


class Texts(models.Model):
    id = models.IntegerField(primary_key = True)
    url = models.CharField(max_length=600)
    canonicalurl = models.CharField(max_length=600, db_column='canonicalUrl') # Field name made lowercase.
    contentfile = models.TextField(db_column='contentFile') # Field name made lowercase.
    trigramerror = models.FloatField(db_column='trigramError') # Field name made lowercase.
    bigramerror = models.FloatField(db_column='bigramError') # Field name made lowercase.
    unigramerror = models.FloatField(db_column='unigramError') # Field name made lowercase.
    freqerror = models.FloatField(db_column='freqError') # Field name made lowercase.
    averagewordlength = models.FloatField(db_column='averageWordLength') # Field name made lowercase.
    romanianscore = models.FloatField(db_column='romanianScore') # Field name made lowercase.
    sourcetype = models.IntegerField(db_column='sourceType') # Field name made lowercase.
    createdate = models.IntegerField(db_column='createDate') # Field name made lowercase.
    nodia = models.IntegerField(db_column='noDia') # Field name made lowercase.

    def __unicode__(self):
        return u' '.join([
            unicode(self.id),
            unicode(self.url),
            unicode(self.canonicalurl),
            unicode(self.contentfile),
            unicode(self.trigramerror),
            unicode(self.bigramerror),
            unicode(self.freqerror),
            unicode(self.averagewordlength),
            unicode(self.romanianscore),
            unicode(self.sourcetype),
            unicode(self.createdate),
            unicode(self.nodia),
        ])

    class Meta:
        db_table = u'Texts'


class Phrases(models.Model):
    id = models.IntegerField(primary_key = True)
    textid = models.ForeignKey(Texts, db_column='textId') # Field name made lowercase.
    phrasecontent = models.TextField(db_column='phraseContent') # Field name made lowercase.
    romanianscore = models.FloatField(null=True, db_column='romanianScore', blank=True) # Field name made lowercase.

    def __unicode__(self):
        return unicode(self.phrasecontent)

    class Meta:
        db_table = u'Phrases'


class Words(models.Model):
    id = models.IntegerField(primary_key = True)
    phraseid = models.ForeignKey(Phrases, db_column='phraseId') # Field name made lowercase.
    form = models.CharField(max_length=300)
    formutf8general = models.CharField(max_length=300, db_column='formUtf8General') # Field name made lowercase.
    reverse = models.CharField(max_length=300)
    charlength = models.IntegerField(db_column='charLength') # Field name made lowercase.
    createdate = models.IntegerField(db_column='createDate') # Field name made lowercase.
    etymology = models.CharField(max_length=150, blank=True)
    suffixid = models.ForeignKey(Suffixes, null=True, db_column='suffixId', blank=True) # Field name made lowercase.
    prefixid = models.ForeignKey(Prefixes, null=True, db_column='prefixId', blank=True) # Field name made lowercase.
    domainid = models.ForeignKey(Domains, null=True, db_column='domainId', blank=True) # Field name made lowercase.
    definition = models.TextField(blank=True)

    def __unicode__(self):
        return self.form

    class Meta:
        db_table = u'Words'


class Inflectedforms(models.Model):
    id = models.IntegerField(primary_key = True)
    wordid = models.ForeignKey(Words, db_column='wordId') # Field name made lowercase.
    inflectionid = models.ForeignKey(Inflections, db_column='inflectionId') # Field name made lowercase.
    form = models.CharField(max_length=300)
    formutf8general = models.CharField(max_length=300, db_column='formUtf8General') # Field name made lowercase.
    noapp = models.IntegerField(null=True, db_column='noApp', blank=True) # Field name made lowercase.

    def __unicode__(self):
        return u' '.join([
            unicode(self.id),
            unicode(self.form),
            unicode(self.noapp),
        ])

    def __str__(self):
        return self.form

    class Meta:
        db_table = u'InflectedForms'

