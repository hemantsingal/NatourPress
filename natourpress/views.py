import re
from django.template import Context, loader, RequestContext
from natourpress.models import Author, Feed, Tag, NPAuthor, NPTag, Post
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required

class FeedForm(forms.Form):
    name = forms.CharField(max_length=100)
    url = forms.URLField()

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
                return HttpResponseRedirect('/config/feeds')
            # Redirect to a success page.
            else:
                return HttpResponse('Not Found')
            # Return a 'disabled account' error message
        else:
            return HttpResponse('Not Found')
        # Return an 'invalid login' error message.    feed = Feed(name=name,feed_url=feed_url)
     # Redirect after POST
    return render_to_response('natourpress/login.html')

@login_required
def feedList(request):
        feedList = Feed.objects.all()
        return direct_to_template(request,'natourpress/feeds.html', {'feed_list': feedList})

@login_required
def deleteFeed(request,feed_id):
    feed = Feed.objects.get(id=feed_id)
    feed.delete()
    return HttpResponseRedirect('/config/feeds')


@login_required
def authorlist(request):
    authorDict = {}
    feedList = Feed.objects.all()
    for a in feedList:
        authorList = Author.objects.filter(feed=a)
        authorDict[a] = authorList
    return direct_to_template(request,'natourpress/author.html', {'author_dict': authorDict})

@login_required
def postlist(request):
    postDict = {}
    feedList = Feed.objects.all()
    for a in feedList:
        postList = Post.objects.filter(feed=a).order_by('-date_modified')[:10]
        returnList = []
        for p in postList:
            print p
            karma = a.karma
            print a, karma
            if(p.author and p.author.np_author):
                karma = karma + p.author.np_author.karma
                print p.author.np_author, karma
            if(p.tags):
                for t in p.tags.all():
                    if(t.np_tag):
                        karma = karma+t.np_tag.karma
                        print t, t.np_tag, karma
            returnList.append((p,karma))
        postDict[a] = returnList
    return direct_to_template(request,'natourpress/posts.html', {'post_dict': postDict})

@login_required
def taglist(request):
    tagDict = {}
    feedList = Feed.objects.all()
    for a in feedList:
        tagList = Tag.objects.filter(feed=a)
        tagDict[a] = tagList
    return direct_to_template(request,'natourpress/tag.html', {'tag_dict': tagDict})

@login_required
def setkarma(request):
    if request.method == 'POST':
        for x,y in request.POST.items():
            p = re.compile('(author|feed|tag)(\d+)')
            m = p.match(x)
            print x, y, m
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

@login_required
def newFeed(request):
#    feed = Feed.objects.get(id=feed_id)
#    return render_to_response('natourpress/feedDetail.html', {'feed': feed})
    if request.method == 'POST': # If the form has been submitted...
        form = FeedForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            name = form.cleaned_data['name']
            feed_url = form.cleaned_data['url']
            feed = Feed(name=name,feed_url=feed_url)
            feed.save()
            return HttpResponseRedirect('/config/feeds') # Redirect after POST
    else:
        form = FeedForm()

    return direct_to_template(request,'natourpress/feed_form.html', {
        'form': form,
    })

@login_required
def feedDetail(request, feed_id):
    feed = Feed.objects.get(id=feed_id)
#    return render_to_response('natourpress/feedDetail.html', {'feed': feed})
    if request.method == 'POST': # If the form has been submitted...
        form = FeedForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            feed.name = form.cleaned_data['name']
            feed.feed_url = form.cleaned_data['url']
            feed.save()
            return HttpResponseRedirect('/config/feeds') # Redirect after POST
    else:
        form = FeedForm({'name':feed.name,'url':feed.feed_url})

    return direct_to_template(request,'natourpress/feedDetail.html', {
        'form': form,
        'feed_id':feed_id,
    })

@login_required
def postDetail(request, post_id):
    post = Post.objects.get(id=post_id)
    print post
    return direct_to_template(request,'natourpress/post_details.html', {
        'post' : post,
    })

@login_required
def npauthorlist(request):
    print "hi"
    authorid = request.POST.get('authorid','')
    print authorid
    npauthorList = NPAuthor.objects.all()
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
def nptaglist(request):
    tagid = request.POST.get('tagid','')
    nptagList = NPTag.objects.all()
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

def setnpauthor(request):
    authorid = request.POST.get('authorid','')
    npauthorid = request.POST.get('npauthorid','')
    a = Author.objects.get(id=authorid)
    b = NPAuthor.objects.get(id=npauthorid)
    a.np_author = b
    a.save()
    return HttpResponse("""<li>{!s}  |  {!s} <a class="selectNP" 
            authid={!r} href="#">(change)</a></li>
            """.format(a,b,int(a.id)))




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

class NPAuthorForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()



class NPTagForm(forms.Form):
    name = forms.CharField(max_length=100)
    slug = forms.CharField(max_length=100)

