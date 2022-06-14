import logging

logger = logging.getLogger(__name__)


okHeaderLevels = ('1', '2', '3', '4', '5', '6', 1, 2, 3, 4, 5, 6)
okListTypes = ('ordered', 'bullet')
eolAttributes = ('header', 'list', 'indent')

class QuillRenderState:
    def __init__(self):
        self.contextStack = []
        self.lines = []
        self.parts = [] # the current line, in chunks
        self.opi = -1

    def putChunk(self, text, attributes=None):
        if attributes:
            for attr, attrv in attributes.items():
                if attr == 'bold' and attrv:
                    text = '<strong>' + text + '</strong>'
                elif attr == 'italic' and attrv:
                    text = '<em>' + text + '</em>'
                elif attr == 'underline' and attrv:
                    text = '<u>' + text + '</u>'
                elif attr == 'link':
                    text = '<a href="' + attrv + '" target="_blank">' + text + '</a>'
                elif attr in eolAttributes:
                    pass # handle at end of line
                else:
                    logger.warn("op[%d] unknown attribute: {%r: %r}", self.opi, attr, attrv)
        self.parts.append(text)

    def popContext(self):
        if self.contextStack:
            ctx = self.contextStack.pop()
            if ctx[0] == 'ordered':
                self.lines.append('</ol>')
            elif ctx[0] == 'bullet':
                self.lines.append('</ul>')
            else:
                logger.error('unknown list type in context pop: %r', ctx)

    def pushContext(self, ctx):
        self.contextStack.append(ctx)
        if ctx[0] == 'ordered':
            if ctx[1]:
                self.lines.append('<ol class="ql-indent-{}">'.format(ctx[1]))
            else:
                self.lines.append('<ol>')
        elif ctx[0] == 'bullet':
            if ctx[1]:
                self.lines.append('<ul class="ql-indent-{}">'.format(ctx[1]))
            else:
                self.lines.append('<ul>')
        else:
            logger.error('unknown list type at push: %r', ctx)

    def endLine(self, attributes=None):
        if attributes:
            listh = attributes.get('list')
            if listh and listh in okListTypes:
                indent = attributes.get('indent', 0)
                ctx = (listh, indent)
                if self.contextStack:
                    octx = self.contextStack[-1]
                    if octx == ctx:
                        pass # ok, already in that
                    elif octx[0] == ctx[0]:
                        # same type
                        while octx[1] > ctx[1]:
                            self.popContext()
                            octx = self.contextStack[-1]
                        if ctx[1] > octx[1]:
                            self.pushContext(ctx)
                else:
                    self.pushContext(ctx)
                self.lines.append('<li>' + ''.join(self.parts) + '</li>')
                self.parts = []
                return
            self.popContext()
            header = attributes.get('header')
            if header and header in okHeaderLevels:
                header = str(header)
                self.lines.append('<h'+header+'>' + ''.join(self.parts) + '</h' + header + '>')
                self.parts = []
                return
        self.popContext()
        if self.parts:
            self.lines.append('<p>' + ''.join(self.parts) + '</p>')
            self.parts = []

    def processOps(self, ops):
        self.opi = -1
        for op in ops:
            self.opi += 1
            insert = op.get('insert')
            if insert is None:
                logger.error("op[%d] with no insert: %s", self.opi, json.dumps(op))
                continue
            il = insert.split('\n')
            attrs = op.get('attributes')
            self.putChunk(il[0], attrs)
            chunki = 1
            while chunki < len(il):
                self.endLine(attrs)
                self.putChunk(il[chunki], attrs)
                chunki += 1

    def __str__(self):
        return ''.join(self.lines)

def render_quill(ob):
    opi = -1
    ops = ob['ops']
    render = QuillRenderState()
    render.processOps(ops)
    return render.__str__()