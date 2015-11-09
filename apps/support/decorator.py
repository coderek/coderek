import sys
from django.conf.urls import url


def route(*regexes, **kwargs):
    module = sys.modules.get(kwargs.get('module_name'))
    if module is None:
        caller_filename = sys._getframe(1).f_code.co_filename
        for m in sys.modules.values():
            if (m and '__file__' in m.__dict__ and
                    m.__file__.startswith(caller_filename)):
                module = m
                break

    def _wrapper(cls):
        if module:
            if 'urlpatterns' not in module.__dict__:
                module.urlpatterns = []

            handler = cls.as_view()
            view_name = kwargs.get('name')
            url_kwargs = dict(kwargs)
            url_kwargs['name'] = view_name
            if 'module_name' in url_kwargs:
                del url_kwargs['module_name']
            for regex in regexes:
                module.urlpatterns += [url(regex, handler, **url_kwargs)]
        return cls

    return _wrapper


def include_urlpatterns(regex, module):
    """
    Usage:

    # in top-level module code:
    urlpatterns = include_urlpatterns(r'^profile/', 'apps.myapp.views.profile')
    """
    if module.__class__ is str:
        module = import_module(module)
    if 'urlpatterns' in module.__dict__:
        return [RegexURLResolver(regex, module)]
    return []
