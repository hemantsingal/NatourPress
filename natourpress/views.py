import re, datetime,time
import subprocess
from django.template import Context, loader, RequestContext
from natourpress.models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required

"""Main view file for natourpress"""


""" Login and Logout"""

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')

def my_login(request):
    if request.method == 'POST': # If the form has been submitted...
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/config/feeds/')
            else:
                return HttpResponse('Not Found')
        else:
            return HttpResponse('Not Found')
    return render_to_response('natourpress/login.html')


""" Form Classes """

class FeedForm(forms.Form):
    name = forms.CharField(max_length=100)
    url = forms.URLField()

class NPAuthorForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()

class NPTagForm(forms.Form):
    name = forms.CharField(max_length=100)
    slug = forms.CharField(max_length=100)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post

class LayoutForm(forms.ModelForm):
    class Meta:
        model = Layout

class SubplaceForm(forms.ModelForm):
    class Meta:
        model = SubPlace

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic

class CellForm(forms.ModelForm):
    class Meta:
        model = Cell


""" Feed Views"""

@login_required
def feedList(request):
        feedList = Feed.objects.all()
        return direct_to_template(request,'natourpress/feeds.html', {'feed_list': feedList})

@login_required
def newFeed(request):
    if request.method == 'POST': # If the form has been submitted...
        form = FeedForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            name = form.cleaned_data['name']
            feed_url = form.cleaned_data['url']
            feed = Feed(name=name,feed_url=feed_url)
            feed.save()
            return HttpResponseRedirect('/config/feeds/') # Redirect after POST
    else:
        form = FeedForm()

    return direct_to_template(request,'natourpress/feed_form.html', {
        'form': form,
    })

@login_required
def feedDetail(request, feed_id):
    feed = Feed.objects.get(id=feed_id)
    if request.method == 'POST': 
        form = FeedForm(request.POST) 
        if form.is_valid(): 
            feed.name = form.cleaned_data['name']
            feed.feed_url = form.cleaned_data['url']
            feed.save()
            return HttpResponseRedirect('/config/feeds/') # Redirect after POST
    else:
        form = FeedForm({'name':feed.name,'url':feed.feed_url})

    return direct_to_template(request,'natourpress/feedDetail.html', {
        'form': form,
        'feed_id':feed_id,
    })

@login_required
def deleteFeed(request,feed_id):
    feed = Feed.objects.get(id=feed_id)
    feed.delete()
    return HttpResponseRedirect('/config/feeds/')


"""Author, NPAuthor views"""

@login_required
def authorlist(request):
    authorDict = {}
    feedList = Feed.objects.all()
    for a in feedList:
        authorList = Author.objects.filter(feed=a).order_by('name')
        authorDict[a] = authorList
    return direct_to_template(request,'natourpress/author.html', {'author_dict': authorDict})

@login_required
def npauthorlist(request):
    authorid = request.POST.get('authorid','')
    npauthorList = NPAuthor.objects.order_by('first_name')
    return direct_to_template(request,'natourpress/npauthor.html', {
        'author_list': npauthorList,
        'authorid': authorid,
    })

@login_required
def newnpauthor(request):
    if request.method == 'POST': # If the form has been submitted...
        form = NPAuthorForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            author = NPAuthor(first_name=first_name,last_name=last_name,author_email=email)
            author.save()
            return HttpResponse("done") # Redirect after POST
    else:
        form = NPAuthorForm() # An unbound form
        authorid = request.GET.get('authid','')
    return direct_to_template(request,'natourpress/npauthorform.html', {
        'form': form,
        'authorid':authorid,
    })

@login_required
def editnpauthor(request):
    if request.method == 'POST':
        authorid = request.POST.get('authorid','')
        form = NPAuthorForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']



@login_required
def setnpauthor(request):
    authorid = request.POST.get('authorid','')
    npauthorid = request.POST.get('npauthorid','')
    a = Author.objects.get(id=authorid)
    b = NPAuthor.objects.get(id=npauthorid)
    a.np_author = b
    a.save()
    return HttpResponse("""<td>{!s}  </td><td>  {!s} <a class="selectNP" 
            authid={!r} href="#">(change)</a></td>
            """.format(a,b,int(a.id)))

@login_required
def deletenpauthor(request):
    authorid = request.POST.get('authorid','')
    a = NPAuthor.objects.get(id=authorid)
    a.delete()
    return HttpResponse("deleted")

"""Category, NPCategory Views"""

@login_required
def taglist(request):
    tagDict = {}
    feedList = Feed.objects.all()
    for a in feedList:
        tagList = Tag.objects.filter(feed=a).order_by('name')
        tagDict[a] = tagList
    return direct_to_template(request,'natourpress/tag.html', {'tag_dict': tagDict})

@login_required
def nptaglist(request):
    tagid = request.POST.get('tagid','')
    nptagList = NPTag.objects.order_by('name')
    return direct_to_template(request,'natourpress/nptag.html', {
        'tag_list': nptagList, 
        'tagid': tagid
    })

@login_required
def newnptag(request):
    if request.method == 'POST':
        form = NPTagForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            slug = form.cleaned_data['slug']
            tag = NPTag(name=name,slug=slug)
            tag.save()
            return HTTPResponse("done")
    else:
        form = NPTagForm()
        tagid = request.GET.get('tagid','')
    return direct_to_template(request,'natourpress/nptagform.html', {
        'form': form,'tagid':tagid,
    })

@login_required
def setnptag(request):
    tagid = request.POST.get('tagid','')
    nptagid = request.POST.get('nptagid','')
    a = Tag.objects.get(id=tagid)
    b = NPTag.objects.get(id=nptagid)
    a.np_tag = b
    a.save()
    return HttpResponse("""<li>{!s}  |  {!s} <a class="selectNP" 
            tagid={!r} href="#">(change)</a></li>
            """.format(a,b,int(a.id)))


"""Karma Views"""

@login_required
def setkarma(request):
    if request.method == 'POST':
        for x,y in request.POST.items():
            p = re.compile('(author|feed|tag)(\d+)')
            m = p.match(x)
            if m == None:
                continue
            z = m.group(1)
            if z == 'feed':
                p = Feed.objects.get(id=m.group(2))
                p.karma = y
                p.save()
            elif z == 'author':
                p = NPAuthor.objects.get(id=m.group(2))
                p.karma = y
                p.save()
            elif z == 'tag':
                p = NPTag.objects.get(id=m.group(2))
                p.karma = y
                p.save()
            
    feedList = Feed.objects.all()
    tagList = NPTag.objects.all()
    authorList = NPAuthor.objects.all()
    return direct_to_template(request,'natourpress/setkarma.html',{
        'feed_list':feedList,
        'tag_list':tagList,
        'author_list':authorList,
    })


"""Post Views"""

@login_required
def postlist(request):
    if request.method == 'POST':
        for x,y in request.POST.items():
            if (x == 'title'):
                title = y
            if (x == 'description'):
                description =  y
            if (x == 'msgpost'):
                content = y
            if (x == 'datepicker'):
                datepicker = y
            if (x == 'timeval'):
                timeval = y        
            if (x == 'postid'):
                post = Post.objects.get(id=y)
        if post:
            post.title = title
            post.description = description
            post.content = content
            post.date_modified = datepicker + " " + timeval
            post.flag = 1
            post.save()
    postDict = {}
    feedList = Feed.objects.all()
    for a in feedList:
        postList = Post.objects.filter(feed=a).order_by('-date_modified')[:10]
        postDict[a] = postList
    return direct_to_template(request,'natourpress/posts.html', {'post_dict': postDict})

@login_required
def postDetail(request, post_id):
    post = Post.objects.get(id=post_id)
    time_mod = str(post.date_modified).split(' ')
    dateval = {'date':time_mod[0],'time':time_mod[1]}
    params = {
        'post':post,
        'dateval':dateval,
    }
    if post.author and post.author.np_author:
        params['np_author'] = post.author.np_author
    
    #date = time.strptime(time_mod[0], '%Y-%m-%d')
    # time1 = time.strptime(time_mod[1], '%H-%M-%S')
    # print time.strftime("%H:%M",time1)
    #print time.strftime("%B %d, %Y",date)
    #print dateval
    return direct_to_template(request,'natourpress/post_details.html', params)

@login_required
def openKarma(request, post_id):
    if request.method == 'POST':
        for x,y in request.POST.items():
            if (x == 'postid'):
                post = Post.objects.get(id=y)
            if (x == 'change'):
                change = y
        if post:
            a = post.karma
            post.karma = a + int(change)
            l = Karma_Log(oldkarma=a,newkarma=a + int(change), post=post, date=datetime.datetime.now())
            l.save()
            post.save()
            return HttpResponseRedirect('/config/posts/')
    p = Post.objects.get(id=post_id)
    loglist = Karma_Log.objects.filter(post=p)
    params = {
        'post':p,
    }
    if loglist:
        params['loglist'] = loglist
        params['initial'] = loglist[0].oldkarma
    return direct_to_template(request,'natourpress/karma.html', params)


"""Layout Views"""

@login_required
def layouts(request):
        layoutList = Layout.objects.all()
        return direct_to_template(request,'natourpress/layouts.html', {'layout_list': layoutList})

@login_required
def newLayout(request):
    if request.method == 'POST': # If the form has been submitted...
        form = LayoutForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            name = form.cleaned_data['name']
            usage = form.cleaned_data['usage']
            template = form.cleaned_data['template']
            css = form.cleaned_data['css']
            javascript = form.cleaned_data['javascript']
            layout = Layout(name=name,usage=usage, template=template, css=css, javascript=javascript)
            layout.save()
            return HttpResponseRedirect('/config/layouts/') # Redirect after POST
    else:
        form = LayoutForm()

    return direct_to_template(request,'natourpress/layout_form.html', {
        'form': form,
    })

@login_required
def layoutDetail(request, layout_id):
    layout = Layout.objects.get(id=layout_id)
    if request.method == 'POST': # If the form has been submitted...
        form = LayoutForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            layout.name = form.cleaned_data['name']
            layout.usage = form.cleaned_data['usage']
            layout.template = form.cleaned_data['template']
            layout.css = form.cleaned_data['css']
            layout.javascript = form.cleaned_data['javascript']
            #layout = Layout(name=name,usage=usage, template=template, css=css, javascript=javascript)
            layout.save()
            return HttpResponseRedirect('/config/layouts/') # Redirect after POST
    else:
        form = LayoutForm(instance=layout)
    return direct_to_template(request,'natourpress/layout_detail.html', {
        'form': form,
        'layout_id':layout_id,
    })


@login_required
def deleteLayout(request,layout_id):
    layout = Layout.objects.get(id=layout_id)
    layout.delete()
    return HttpResponseRedirect('/config/layouts/')


"""Pagemapper Views"""

@login_required
def selectCategory(request):
    categoryList = NPTag.objects.all()
    if request.method == 'POST':
        for x,y in request.POST.items():
            if x == 'objid':
                instid = y
            if x == 'mapping':
                inst = y
        if inst == 'subplace':
            obj = SubPlace.objects.get(id=instid)
        if inst == 'topic':
            obj = Topic.objects.get(id=instid)
        if inst == 'cell':
            obj = Cell.objects.get(id=instid)

        tags = obj.tags.all()
        return direct_to_template(request,'natourpress/select_category.html', {
            'category_list': categoryList,
            'mapped_tags': tags,
            'instance':inst,
            'instid':instid,
        })
    return direct_to_template(request,'natourpress/select_category.html', {
        'category_list': categoryList,
    })

@login_required
def pageMapper(request):
    if request.method == 'POST':
        tags = []
        for x,y in request.POST.items():
            if x.startswith('cat'):
                #tags.append(y)
                tags.append(NPTag.objects.get(name=y))
            if x == "instance":
                inst = y
            if x == "instid":
                instid = y
        if inst == 'subplace':
            obj = SubPlace.objects.get(id=instid)
        if inst == 'topic':
            obj = Topic.objects.get(id=instid)
        if inst == 'cell':
            obj = Cell.objects.get(id=instid)
        obj.tags.clear()
        [obj.tags.add(tcat) for tcat in tags]
    subplaceList = SubPlace.objects.all()
    topicList = Topic.objects.all()
    cellList = Cell.objects.all()
    return direct_to_template(request,'natourpress/pagemapper.html', {
        'subplaceList' : subplaceList,
        'topicList' : topicList,
        'cellList' : cellList,
    })


"""Subplace Views"""
@login_required
def addSubPlace(request):
    if request.method == 'POST': # If the form has been submitted...
        form = SubplaceForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            name = form.cleaned_data['name']
            slug = form.cleaned_data['slug']
            placename = form.cleaned_data['placename']
            placeslug = form.cleaned_data['placeslug']
            subplace = SubPlace(name=name,slug=slug, placename=placename, placeslug=placeslug)
            subplace.save()
            return HttpResponseRedirect('/config/pagemapper/') # Redirect after POST
    else:
        form = SubplaceForm()

    return direct_to_template(request,'natourpress/subplace_form.html', {
        'form': form,
    })

@login_required
def subplaceDetail(request, subplace_id):
    subplace = SubPlace.objects.get(id=subplace_id)
    if request.method == 'POST': # If the form has been submitted...
        form = SubplaceForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            subplace.name = form.cleaned_data['name']
            subplace.slug = form.cleaned_data['slug']
            subplace.placename = form.cleaned_data['placename']
            subplace.placeslug = form.cleaned_data['placeslug']
            subplace.save()
            return HttpResponseRedirect('/config/pagemapper/') # Redirect after POST
    else:
        form = SubplaceForm(instance=subplace)
    return direct_to_template(request,'natourpress/subplace_detail.html', {
        'form': form,
        'subplace_id':subplace_id,
    })


"""Topic Views"""

@login_required
def addTopic(request):
    if request.method == 'POST': # If the form has been submitted...
        form = TopicForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            name = form.cleaned_data['name']
            slug = form.cleaned_data['slug']
            topic = Topic(name=name,slug=slug)
            topic.save()
            return HttpResponseRedirect('/config/pagemapper/') # Redirect after POST
    else:
        form = TopicForm()
    return direct_to_template(request,'natourpress/topic_form.html', {
        'form': form,
    })

@login_required
def topicDetail(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method == 'POST': # If the form has been submitted...
        form = TopicForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            topic.name = form.cleaned_data['name']
            topic.slug = form.cleaned_data['slug']
            topic.save()
            return HttpResponseRedirect('/config/pagemapper/') # Redirect after POST
    else:
        form = TopicForm(instance=topic)
    return direct_to_template(request,'natourpress/topic_detail.html', {
        'form': form,
        'topic_id':topic_id,
    })


"""Cell Views"""

@login_required
def addCell(request):
    if request.method == 'POST': # If the form has been submitted...
        form = CellForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            cell = Cell(name=name,description=description)
            cell.save()
            return HttpResponseRedirect('/config/pagemapper/') # Redirect after POST
    else:
        form = CellForm()
    return direct_to_template(request,'natourpress/cell_form.html', {
        'form': form,
    })

@login_required
def cellDetail(request, cell_id):
    cell = Cell.objects.get(id=cell_id)
    if request.method == 'POST': # If the form has been submitted...
        form = CellForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            cell.name = form.cleaned_data['name']
            cell.description = form.cleaned_data['description']
            cell.save()
            return HttpResponseRedirect('/config/pagemapper/') # Redirect after POST
    else:
        form = CellForm(instance=cell)
    return direct_to_template(request,'natourpress/cell_detail.html', {
        'form': form,
        'cell_id':cell_id,
    })

#############################################################
######                                                 ######
######             TESTING PURPOSE ONLY                ######
######                                                 ######
#############################################################

def main(request):
    return render_to_response("natourpress/test.html")

def test(request):
    import random
    x = {1:'red',2:'blue',3:'green'}
    i = random.randint(1,3)
    return render_to_response("natourpress/testing.html",{'color':x[i]})


############### Fetch Feeds #####################

def fetchfeed(request):
    process = subprocess.Popen(['/home/environments/natourpress/bin/python', 'manage.py', 'fetch']) 
    return HttpResponseRedirect('/config/feeds/')

