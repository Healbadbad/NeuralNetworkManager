# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1469069453.422
_enable_loop = True
_template_filename = u'views/header.html'
_template_uri = u'header.html'
_source_encoding = 'utf-8'
_exports = ['createHeaderBar']


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer(u'\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_createHeaderBar(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\r\n  <div class="ui tiered nav menu">\r\n    <div class="container">\r\n      <a class="item logo" href="/">\r\n        <b>Neural Network</b> Manager\r\n      </a>\r\n      <a class="item" href="/savedStates"> Saved States </a>\r\n      <a class="item" href="/buildLog"> Build Log </a>\r\n    </div>\r\n  </div>\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"16": 0, "37": 31, "27": 1, "21": 11, "31": 1}, "uri": "header.html", "filename": "views/header.html"}
__M_END_METADATA
"""
