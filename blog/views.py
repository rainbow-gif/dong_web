from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from blog.models import *
from django.core.paginator import Paginator
import markdown
def black(request):
    return render(request,'blog/black.html')
def hello_world(request):
    return HttpResponse('hello world')
def article_content(request):
    pass

def get_index_page(request):
    page = request.GET.get('page')
    if page:
        page = int(page)
    else:
        page = 1
    #print(page)
    all_article = Article_1.objects.all()
    top5 = Article_1.objects.order_by('-publish_date')[:4]
    paginator = Paginator(all_article,7)
    page_num = paginator.num_pages


    page_article_list = paginator.page(page)

    #print(page_num,page, page_article_list)
    if page_article_list.has_next():
        next_page = page+1
        #print(next_page)
    else:
        next_page = page
        #print(next_page)
    if page_article_list.has_previous():
        previous_page =  page -1
        #print(previous_page)
    else:
        previous_page = page
        #print(previous_page)
    return render(request,'blog/index.html',{
        'article_list':page_article_list,
        'page_num':range(1,page_num+1),
        'curr_page':page,
        'next_page':next_page,
        'previous_page':previous_page,
        'top5_article':top5
    })


def get_detail_page(request,article_id):
    all_article = Article_1.objects.all()
    curr_article = None
    previous_index = 0
    next_index = 0
    for index,article in enumerate(all_article):
        if index == 0 and index==len(all_article)-1:
            previous_index = 0
            next_index = 0
        elif index == 0:
            previous_index = 0
            next_index = index+1
        elif index==len(all_article)-1:
            previous_index = index-1
            next_index = index
        else:
            previous_index = index-1
            next_index = index+1

        if article.article_id == article_id:
            curr_article = article
            previous = all_article[previous_index]
            next = all_article[next_index]
            break

    content = markdown.markdown(curr_article.content,
                                  extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                  ])
    #section_list = [x+' '*10 for x in section_list]
    return render(request,'blog/detail.html',{
        'curr_article':curr_article,
        'section_list':content,
        'previous':previous,
        'next':next
    })


def search(request):
    ctx = request.POST['q']
    if ctx == '入场动画':
        return render(request,'blog/black.html')
    elif ctx == '游锦旭':
        return render(request,'blog/youshen.html')
    page_article_list = []
    all_article = Article_1.objects.all()
    for article in all_article:
        if ctx in article.brief_content or ctx in article.title:
            page_article_list.append(article)


    return render(request,'blog/search.html',{
        'article_list':page_article_list,

    })