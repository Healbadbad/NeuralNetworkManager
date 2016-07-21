# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1469069457.543
_enable_loop = True
_template_filename = 'views/buildLog.html'
_template_uri = 'buildLog.html'
_source_encoding = 'utf-8'
_exports = [u'content']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    pass
def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'index.html', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        def content():
            return render_content(context._locals(__M_locals))
        __M_writer = context.writer()
        __M_writer(u'\r\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'content'):
            context['self'].content(**pageargs)
        

        __M_writer(u'\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_content(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def content():
            return render_content(context)
        __M_writer = context.writer()
        __M_writer(u'\r\n    <div class="ui feed">\r\n      <div class="event">\r\n        <div class="content">\r\n          <div class="summary">\r\n            <a class="user">\r\n              Elliot Fu\r\n            </a> added you as a friend\r\n            <div class="date">\r\n              1 Hour Ago\r\n            </div>\r\n          </div>\r\n          <div class="meta">\r\n            <a class="like">\r\n              <i class="like icon"></i> 4 Likes\r\n            </a>\r\n          </div>\r\n        </div>\r\n      </div>\r\n      <div class="event">\r\n        <div class="content">\r\n          <div class="summary">\r\n            <a>Helen Troy</a> added <a>2 new illustrations</a>\r\n            <div class="date">\r\n              4 days ago\r\n            </div>\r\n          </div>\r\n          <div class="meta">\r\n            <a class="like">\r\n              <i class="like icon"></i> 1 Like\r\n            </a>\r\n          </div>\r\n        </div>\r\n      </div>\r\n      <div class="event">\r\n        <div class="content">\r\n          <div class="summary">\r\n            <a class="user">\r\n              Jenny Hess\r\n            </a> added you as a friend\r\n            <div class="date">\r\n              2 Days Ago\r\n            </div>\r\n          </div>\r\n          <div class="meta">\r\n            <a class="like">\r\n              <i class="like icon"></i> 8 Likes\r\n            </a>\r\n          </div>\r\n        </div>\r\n      </div>\r\n      <div class="event">\r\n        <div class="content">\r\n          <div class="summary">\r\n            <a>Joe Henderson</a> posted on his page\r\n            <div class="date">\r\n              3 days ago\r\n            </div>\r\n          </div>\r\n          <div class="extra text">\r\n            Ours is a life of constant reruns. We\'re always circling back to where we\'d we started, then starting all over again. Even if we don\'t run extra laps that day, we surely will come back for more of the same another day soon.\r\n          </div>\r\n          <div class="meta">\r\n            <a class="like">\r\n              <i class="like icon"></i> 5 Likes\r\n            </a>\r\n          </div>\r\n        </div>\r\n      </div>\r\n      <div class="event">\r\n        <div class="content">\r\n          <div class="summary">\r\n            <a>Justen Kitsune</a> added <a>2 new photos</a> of you\r\n            <div class="date">\r\n              4 days ago\r\n            </div>\r\n          </div>\r\n          <div class="meta">\r\n            <a class="like">\r\n              <i class="like icon"></i> 41 Likes\r\n            </a>\r\n          </div>\r\n        </div>\r\n      </div>\r\n    </div>\r\n ')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"34": 1, "39": 87, "45": 2, "51": 2, "57": 51, "27": 0}, "uri": "buildLog.html", "filename": "views/buildLog.html"}
__M_END_METADATA
"""
