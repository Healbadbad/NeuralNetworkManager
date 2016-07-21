# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1469068781.72
_enable_loop = True
_template_filename = 'views/index.html'
_template_uri = 'index.html'
_source_encoding = 'utf-8'
_exports = [u'content']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    ns = runtime.TemplateNamespace('__anon_0x3ffbeb8L', context._clean_inheritance_tokens(), templateuri=u'header.html', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, '__anon_0x3ffbeb8L')] = ns

def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x3ffbeb8L')._populate(_import_ns, [u'*'])
        def content():
            return render_content(context._locals(__M_locals))
        createHeaderBar = _import_ns.get('createHeaderBar', context.get('createHeaderBar', UNDEFINED))
        __M_writer = context.writer()
        __M_writer(u'\r\n<!DOCTYPE html>\r\n<html>\r\n   <head>\r\n      <title> Neural Network Manager </title>\r\n      <link rel="stylesheet" type="text/css" href="/css/semantic.css">\r\n      <script src="/js/jquery-3.1.0.min.js"></script>\r\n      <script src="/js/semantic.js"></script>\r\n   </head>\r\n   <body>\r\n    ')
        __M_writer(filters.decode.utf8(createHeaderBar()))
        __M_writer(u'\r\n\r\n    <div id="content-container">\r\n      ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'content'):
            context['self'].content(**pageargs)
        

        __M_writer(u'\r\n    </div>\r\n\r\n  </body>\r\n </html>\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_content(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x3ffbeb8L')._populate(_import_ns, [u'*'])
        def content():
            return render_content(context)
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"36": 1, "37": 11, "38": 11, "43": 14, "49": 14, "23": 1, "26": 0, "62": 49}, "uri": "index.html", "filename": "views/index.html"}
__M_END_METADATA
"""
