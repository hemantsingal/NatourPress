from django.db import models
from django.utils.translation import ugettext_lazy as _ 

# Create your models here.
class Feed(models.Model):
    feed_url = models.URLField('feed url', unique=True)
    name = models.CharField(_('name'), max_length=50)
    description = models.CharField(_('description'), max_length=250, null=True, blank=True)
    is_active = models.BooleanField(_('is active'), default=True)
    language = models.CharField(_('language'), blank=True, null=True, max_length=10)
    title = models.CharField(_('title'), max_length=200, blank=True, null=True,)
    link = models.URLField(_('link'), blank=True, null=True,)
    last_modified = models.DateTimeField(_('last modified'), null=True, blank=True)
    last_checked = models.DateTimeField(_('last checked'), null=True, blank=True)
    etag = models.CharField(_('etag'), max_length=50, blank=True, null=True,)
    ttl = models.IntegerField(_('ttl'), blank=True, null=True,)
    karma = models.IntegerField(_('karma'), blank=True, null=True, default=30)
    def __unicode__(self):
        return self.name

class NPTag(models.Model):
    name = models.CharField(_('name'), max_length=50, unique=True)
    slug = models.CharField(_('slug'), max_length=100, unique=True)
    karma = models.IntegerField(_('karma'), blank=True, null=True, default=30)
    def __unicode__(self):
        return self.name

class Topic(models.Model):
    name = models.CharField(_('name'), max_length=50)
    slug = models.CharField(_('slug'), max_length=250, null=True, blank=True)
    tags = models.ManyToManyField(NPTag, verbose_name=_('tags'), null=True, blank=True)
    def __unicode__(self):
        return self.name

class SubPlace(models.Model):
    name = models.CharField(_('name'), max_length=50)
    slug = models.CharField(_('slug'), max_length=250, null=True, blank=True)
    placename = models.CharField(_('placename'), max_length=50)
    placeslug = models.CharField(_('placeslug'), max_length=50)
    tags = models.ManyToManyField(NPTag, verbose_name=_('tags'), null=True, blank=True)
    def __unicode__(self):
        return self.name

class Cell(models.Model):
    name = models.CharField(_('name'), max_length=50)
    description = models.CharField(_('description'), max_length=250, null=True, blank=True)
    tags = models.ManyToManyField(NPTag, verbose_name=_('tags'), null=True, blank=True)
    def __unicode__(self):
        return self.name

class Layout(models.Model):
    name = models.CharField(_('name'), max_length=50)
    usage = models.CharField(_('usage'), max_length=50)
    template = models.CharField(_('template'), max_length=150)
    css = models.CharField(_('css'), max_length=150)
    javascript = models.CharField(_('javascript'), max_length=150)
    cells = models.ManyToManyField(Cell, verbose_name=_('cells'), null=True, blank=True)
    def __unicode__(self):
        return self.name


class Atom(models.Model):
    feed = models.ForeignKey(Feed, verbose_name=_('feed'), null=False, blank=False) 
    rel = models.CharField(_('rel'), max_length=50)

class Update(models.Model):
    feed = models.ForeignKey(Feed, verbose_name=_('feed'), null=False, blank=False)
    update_period = models.CharField(_('update period'),max_length=25)
    update_frequency = models.IntegerField()
    def __unicode__(self):
        return self.feed.title


class FeedImage(models.Model):
    feed = models.ForeignKey(Feed, verbose_name=_('feed'), null=False, blank=False)
    image_url = models.URLField('image url', unique=True)
    title = models.CharField(_('title'), max_length=200, blank=True)
    link = models.URLField(_('link'), blank=True)
    def __unicode__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(_('name'), max_length=50, unique=True)
    feed = models.ForeignKey(Feed, verbose_name=_('feed'), null=False, blank=False)
    np_tag = models.ForeignKey(NPTag, verbose_name=_('np_tag'), null=True, blank=True)
    def __unicode__(self):
        return self.name


class NPAuthor(models.Model):
    first_name = models.CharField(_('first name'), max_length=50, blank=True)
    last_name = models.CharField(_('last name'), max_length=50, blank=True)
    author_email = models.EmailField(_('author email'), blank=True)
    karma = models.IntegerField(_('karma'), blank=True, null=True, default=30)
    def __unicode__(self):
        return self.first_name+" "+self.last_name


class Author(models.Model):
    name = models.CharField(_('name'), max_length=50, blank=True)
    email = models.EmailField(_('email'), blank=True)
    np_author = models.ForeignKey(NPAuthor, verbose_name=_('np_author'), null=True, blank=True)
    feed = models.ForeignKey(Feed, verbose_name=_('feed'), null=False, blank=False)
    def __unicode__(self):
        return self.name

class Post(models.Model):
    feed = models.ForeignKey(Feed, verbose_name=_('feed'), null=False, blank=False)
    title = models.CharField(_('title'), max_length=255)
    link = models.URLField(_('link'), )
    content = models.TextField(_('content'), blank=True)
    date_modified = models.DateTimeField(_('date modified'), null=True, blank=True)
    guid = models.CharField(_('guid'), max_length=200, db_index=True)
    author = models.ForeignKey(Author, verbose_name=_('author'), null=True, blank=True)
#    author_email = models.EmailField(_('author email'), blank=True)
    comments = models.URLField(_('comments'), blank=True)
    tags = models.ManyToManyField(Tag, verbose_name=_('tags'))
    pub_date = models.DateField(_('pub_date'), auto_now_add=True)
    description = models.CharField(_('description'), max_length=350)
    karma = models.IntegerField(_('karma'), blank=False, null=False)
    flag = models.IntegerField(_('flag'), blank=False, null=False, default=0)
    def __unicode__(self):
        return self.title

class Karma_Log(models.Model):
    oldkarma = models.IntegerField(_('karma'), blank=False, null=False)
    newkarma = models.IntegerField(_('karma'), blank=False, null=False)
    date = models.DateTimeField(_('date'), null=False, blank=False)
    post = models.ForeignKey(Post, verbose_name=_('post'), null=False, blank=False, db_index=True)
    def __unicode__(self):
        return self.post.title

class Media(models.Model):
    post = models.ForeignKey(Post, verbose_name=_('feed'), null=False, blank=False)
    link = models.URLField(_('link'), )
    medium = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    def __unicode__(self):
        return self.title

class Link(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    link = models.URLField(_('link'), verify_exists=True)
    def __unicode__(self):
        return self.name

