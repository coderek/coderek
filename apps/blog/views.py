import os
import codecs
from apps.support.text import parse_markdown
from django.http import HttpResponse


from django.views.generic import View
from django.conf import settings
from django.shortcuts import render

from apps.support.decorator import route


def get_posts():
    p = settings.BASE_DIR + '/Coderek/apps/blog/_posts'
    return reversed(sorted(os.listdir(p)))


def get_post(name):
    p = settings.BASE_DIR + '/Coderek/apps/blog/_posts/' + name
    if os.path.exists(p):
        with codecs.open(p, encoding='utf-8') as f:
            return parse_markdown(f.read())


@route('^(?P<post_name>[0-9]{4}.*\.markdown)$')
class ListPosts(View):

    def get(self, request, **kwargs):
        name = kwargs['post_name']
        post, meta = get_post(name)
        if post:
            return render(request, 'coding_blog_post.jinja', {
                'post': post, 'meta': meta})
        else:
            return HttpResponse('hello')


@route('^$')
class ShowPost(View):
    template_name = 'coding_blog_list.jinja'

    def get(self, request):
        return render(request, self.template_name, {'posts': get_posts()})
