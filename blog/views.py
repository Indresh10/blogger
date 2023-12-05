from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post


# Create your views here.


def index(request):
    query = request.GET.get("query", "")
    type = request.GET.get("type", "title")
    sort = request.GET.get("sort", "latest")
    posts = None
    if (sort == "latest"):
        if (type == "title"):
            posts = Post.objects.filter(
                title__icontains=query).all().order_by("-timestamp")
        else:
            posts = Post.objects.filter(
                tags__icontains=query).all().order_by("-timestamp")
    else:
        posts = Post.get_relevance_sorted_posts(type, query)

    return render(request, "blog/index.html", {
        "blogs": posts,
        "query": query,
        "type": type,
        "sort": sort
    })


def loginView(request):
    if (request.method == "POST"):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("blog:index"))
        messages.error(request, "Invalid Credentials")
        return render(request, "blog/login.html")
    return render(request, "blog/login.html")


def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse("blog:index"))


def register(request):
    if (request.method == "POST"):
        firstname = request.POST["fname"]
        lastname = request.POST["lname"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            user = User.objects.create_user(
                username, email, password, first_name=firstname, last_name=lastname)
            user.save()
            messages.success(request, "Registered Successfully")
            return HttpResponseRedirect(reverse("blog:login"))
        except Exception as ex:
            messages.error(request, "Error Registering User")
        return render(request, "blog/register.html")
    return render(request, "blog/register.html")


@login_required
def myblogs(request):
    posts = Post.objects.filter(user=request.user)
    return render(request, "blog/myblogs.html", {
        "blogs": posts
    })


def getLikes(likes: list, like: bool):
    count = 0
    for like in likes:
        if (like):
            count += 1
        else:
            count += 1
    return count


@login_required
def addblog(request):
    if (request.method == "POST"):
        title = request.POST["title"]
        tags = request.POST["tags"]
        content = request.POST["content"]
        try:
            post = Post.objects.create(
                title=title, tags=tags, content=content, user=request.user)
            post.save()
            messages.success(request, "Blog Post created Successfully")
            return HttpResponseRedirect(reverse("blog:myblogs"))
        except Exception as e:
            messages.error(request, "Error adding Blog")
    return render(request, "blog/addblog.html")


@login_required
def edit(request, pk):
    post = Post.objects.get(pk=pk)
    if (request.method == "POST"):
        title = request.POST["title"]
        tags = request.POST["tags"]
        content = request.POST["content"]
        try:
            post = Post.objects.get(pk=pk)
            post.title = title
            post.tags = tags
            post.content = content
            post.save()
            messages.success(request, "Blog Post updated Successfully")
            return HttpResponseRedirect(reverse("blog:myblogs"))
        except Exception as e:
            messages.error(request, "Error updating Blog")
            return HttpResponseRedirect(reverse("blog:myblogs"))
    return render(request, "blog/addblog.html", {
        "post": post
    })


@login_required
def delete(request):
    if request.method == "POST":
        try:
            pk = int(request.POST["pk"])
            post = Post.objects.get(pk=pk)
            post.delete()
            messages.success(
                request, f"Successfully deleted blog")
            return HttpResponseRedirect(reverse("blog:myblogs"))
        except Exception as e:
            messages.error(request, "Error deleting blog")
            return HttpResponseRedirect(reverse("blog:myblogs"))
    else:
        return HttpResponse("Only POST Request")
