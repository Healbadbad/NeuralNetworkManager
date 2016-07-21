# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1469069456.318
_enable_loop = True
_template_filename = 'views/savedStates.html'
_template_uri = 'savedStates.html'
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
        __M_writer(u'\r\n    <div class="ui cards">\r\n      <div class="card">\r\n        <div class="content">\r\n          <div class="header">\r\n            Elliot Fu\r\n          </div>\r\n          <div class="meta">\r\n            Friends of Veronika\r\n          </div>\r\n          <div class="description">\r\n            Elliot requested permission to view your contact details\r\n          </div>\r\n        </div>\r\n        <div class="extra content">\r\n          <div class="ui two buttons">\r\n            <div class="ui basic green button">Approve</div>\r\n            <div class="ui basic red button">Decline</div>\r\n          </div>\r\n        </div>\r\n      </div>\r\n      <div class="card">\r\n        <div class="content">\r\n          <div class="header">\r\n            Jenny Hess\r\n          </div>\r\n          <div class="meta">\r\n            New Member\r\n          </div>\r\n          <div class="description">\r\n            Jenny wants to add you to the group <b>best friends</b>\r\n          </div>\r\n        </div>\r\n        <div class="extra content">\r\n          <div class="ui two buttons">\r\n            <div class="ui basic green button">Approve</div>\r\n            <div class="ui basic red button">Decline</div>\r\n          </div>\r\n        </div>\r\n      </div>\r\n    </div>\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"34": 1, "39": 43, "45": 2, "51": 2, "57": 51, "27": 0}, "uri": "savedStates.html", "filename": "views/savedStates.html"}
__M_END_METADATA
"""
