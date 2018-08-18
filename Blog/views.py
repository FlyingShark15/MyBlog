import logging

from django.db.models import Count
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.paginator import Paginator,InvalidPage, EmptyPage, PageNotAnInteger

from Blog.models import Category, Ad, Article, Links, Comment, Tag

logger = logging.getLogger('blog.views')


# Create your views here.
# 定义全局变量
def global_settings(request):
    SITE_NAME = settings.SITE_NAME
    SITE_DESC = settings.SITE_DESC
    WEIBO_SINA = settings.WEIBO_SINA
    CSDN_BLOG = settings.CSDN_BLOG
    PRO_RSS = settings.PRO_RSS
    SITE_URL = settings.SITE_URL
    # 分类数据获取（导航栏）
    category_list = Category.objects.all()  # Category.objects.all()[:1] 取出一部分
    # 广告数据获取
    ad_list = Ad.objects.all()
    # 友情链接
    link_list = Links.objects.all()
    # 文章归档
    # 1.到文章中获取年月，2018-8
    archive_list = Article.objects.datetimes('date_publish', 'month', order='DESC')
    # 标签云
    # 排行榜,只要前四个
    # 1、浏览排行
    article_click_list = Article.objects.order_by('-click_count')[:4]
    # 2、评论排行
    comment_count_list = Comment.objects.values('article').annotate(comment_count=Count('article'))\
        .order_by('-comment_count')
    article_comment_list = [Article.objects.get(pk=comment['article']) for comment in comment_count_list][:4]
    # 3、站长推荐
    article_is_recommend_list = Article.objects.order_by('-is_recommend')[:4]

    # 标签
    tag_list = Tag.objects.all()
    return locals()


# 首页
def index(request):
    try:
        # 文章内容获取
        article_list = Article.objects.all()
        # 分页处理
        article_list = get_page(request, article_list)
    except Exception as e:
        logger.error(e)
    return render(request, 'index.html', locals())  # locals()把所有参数传过去


# 归档
def archive(request):
    try:
        # # 文章归档
        # # 先获得客户端提交的信息
        year = request.GET.get('year', None)
        month = request.GET.get('month', None)
        # # 文章内容获取
        article_list = Article.objects.filter(date_publish__year=year, date_publish__month=month)
        # 分页处理
        article_list = get_page(request, article_list)
    except Exception as e:
        logger.error(e)
    return render(request, 'archive.html', locals())  # locals()把所有参数传过去


# 分类
def category(request):
    try:
        category_name = request.GET.get('category', None)
        article_list = Article.objects.filter(category__name__icontains=category_name)
        article_list = get_page(request, article_list)
    except Exception as e:
        logger.error(e)
    return render(request, 'category.html', locals())


# 标签
def tag(request):
    try:
        tag = request.GET.get('tag', None)
        article_list = Article.objects.filter(tag__name__iexact=tag)   # 多对多
        article_list = get_page(request, article_list)
    except Exception as e:
        logger.error(e)
    return render(request, 'tag.html', locals())


# 文章详情
def article(request):
    try:
        # 获取文章id
        id = request.GET.get('id', None)
        try:
            # 获取文章信息
            article = Article.objects.get(pk=id)
        except Article.DoesNotExist:
            return render(request, 'failure.html', {'reason': '没有找到对应的文章'})

        # # 评论表单
        # comment_form = CommentForm({'author': request.user.username,
        #                             'email': request.user.email,
        #                             'url': request.user.url,
        #                             'article': id} if request.user.is_authenticated() else{'article': id})
        # # 获取评论信息
        # comments = Comment.objects.filter(article=article).order_by('id')
        # comment_list = []
        # for comment in comments:
        #     for item in comment_list:
        #         if not hasattr(item, 'children_comment'):
        #             setattr(item, 'children_comment', [])
        #         if comment.pid == item:
        #             item.children_comment.append(comment)
        #             break
        #     if comment.pid is None:
        #         comment_list.append(comment)
    except Exception as e:
        logger.error(e)
    return render(request, 'article.html', locals())


# 分页
def get_page(request, article_list):
    paginator = Paginator(article_list, 3)
    try:
        page = int(request.GET.get('page', 1))  # page是当前页，没有参数传入，默认为1
        article_list = paginator.page(page)
    except(EmptyPage, InvalidPage, PageNotAnInteger):
        article_list = paginator.page(1)  # 异常处理，显示第一页，有待拓展错误页
    return article_list
