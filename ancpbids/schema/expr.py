"""BIDS schema expression language (parse + eval).

Oracle: ``meta.expression_tests`` in the vendored schema JSON.
"""
import re


_TOKEN = re.compile(
    r"\s+|"
    r"==|!=|<=|>=|\|\||&&|"
    r"[+\-*/%!()\[\]{}.,]|"
    r"\d+\.\d+|\d+|"
    r"'(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\""
    r"|[A-Za-z_][A-Za-z0-9_]*"
)

_OPS = {
    '||': 1, '&&': 2,
    '==': 3, '!=': 3, '<': 3, '>': 3, '<=': 3, '>=': 3, 'in': 3,
    '+': 4, '-': 4,
    '*': 5, '/': 5, '%': 5,
}


class _Tok:
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value


def _tokenize(text):
    tokens = []
    for match in _TOKEN.finditer(text):
        raw = match.group(0)
        if raw.isspace():
            continue
        tokens.append(_classify(raw))
    tokens.append(_Tok('eof', None))
    return tokens


def _classify(raw):
    if raw in ('true', 'false', 'null', 'in'):
        return _Tok(raw, raw)
    if raw[0] in '\'"':
        return _Tok('string', raw[1:-1])
    if raw[0].isdigit():
        return _Tok('number', float(raw) if '.' in raw else int(raw))
    if raw.isidentifier():
        return _Tok('id', raw)
    return _Tok(raw, raw)


class _Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def peek(self):
        return self.tokens[self.i]

    def take(self, kind=None):
        tok = self.peek()
        if kind is not None and tok.kind != kind:
            raise ValueError('expected %s, got %s' % (kind, tok.kind))
        self.i += 1
        return tok

    def parse(self):
        node = self._expr(0)
        if self.peek().kind != 'eof':
            raise ValueError('unexpected token %s' % self.peek().kind)
        return node

    def _expr(self, min_prec):
        left = self._unary()
        while True:
            tok = self.peek()
            prec = _OPS.get(tok.kind)
            if prec is None or prec < min_prec:
                return left
            op = self.take().kind
            right = self._expr(prec + 1)
            left = ('op', op, left, right)

    def _unary(self):
        kind = self.peek().kind
        if kind == '!':
            self.take()
            return ('not', self._unary())
        if kind == '-':
            self.take()
            return ('neg', self._unary())
        return self._postfix()

    def _postfix(self):
        node = self._primary()
        while True:
            kind = self.peek().kind
            if kind == '.':
                self.take()
                name = self.take('id').value
                node = ('dot', node, name)
            elif kind == '[':
                self.take()
                index = self._expr(0)
                self.take(']')
                node = ('idx', node, index)
            else:
                return node

    def _primary(self):
        tok = self.peek()
        literal = _LITERALS.get(tok.kind)
        if literal is not None:
            self.take()
            return ('lit', literal(tok))
        if tok.kind == '(':
            self.take()
            node = self._expr(0)
            self.take(')')
            return node
        if tok.kind == '[':
            return ('list', self._bracket_list())
        if tok.kind == '{':
            self.take()
            self.take('}')
            return ('lit', {})
        if tok.kind == 'id':
            name = self.take().value
            if self.peek().kind == '(':
                return ('call', name, self._paren_list())
            return ('var', name)
        raise ValueError('unexpected token %s' % tok.kind)

    def _bracket_list(self):
        self.take('[')
        items = []
        if self.peek().kind != ']':
            items.append(self._expr(0))
            while self.peek().kind == ',':
                self.take()
                items.append(self._expr(0))
        self.take(']')
        return items

    def _paren_list(self):
        self.take('(')
        items = []
        if self.peek().kind != ')':
            items.append(self._expr(0))
            while self.peek().kind == ',':
                self.take()
                items.append(self._expr(0))
        self.take(')')
        return items


_LITERALS = {
    'number': lambda tok: tok.value,
    'string': lambda tok: tok.value,
    'true': lambda tok: True,
    'false': lambda tok: False,
    'null': lambda tok: None,
}


def evaluate(expression, context=None):
    if context is None:
        context = {'sidecar': {}}
    return _eval(_Parser(_tokenize(expression)).parse(), context)


def _eval(node, ctx):
    kind = node[0]
    if kind == 'lit':
        return node[1]
    if kind == 'var':
        return ctx[node[1]] if node[1] in ctx else None
    if kind == 'list':
        return [_eval(item, ctx) for item in node[1]]
    if kind == 'not':
        return _not(_eval(node[1], ctx))
    if kind == 'neg':
        return _neg(_eval(node[1], ctx))
    if kind == 'dot':
        return _dot(_eval(node[1], ctx), node[2])
    if kind == 'idx':
        return _idx(_eval(node[1], ctx), _eval(node[2], ctx))
    if kind == 'call':
        args = [_eval(arg, ctx) for arg in node[2]]
        return _call(node[1], args, ctx)
    if kind == 'op':
        return _op(node[1], node[2], node[3], ctx)
    raise ValueError('unknown node %s' % kind)


def _not(value):
    return value is not True


def _neg(value):
    if value is None:
        return None
    return -value


def _dot(obj, name):
    if obj is None:
        return None
    if isinstance(obj, dict):
        return obj[name] if name in obj else None
    return getattr(obj, name, None)


def _idx(obj, index):
    if obj is None or index is None:
        return None
    try:
        return obj[index]
    except (TypeError, IndexError, KeyError):
        return None


def _op(op, left_node, right_node, ctx):
    if op == '&&':
        return _and(_eval(left_node, ctx), lambda: _eval(right_node, ctx))
    if op == '||':
        return _or(_eval(left_node, ctx), lambda: _eval(right_node, ctx))
    left = _eval(left_node, ctx)
    right = _eval(right_node, ctx)
    if op == 'in':
        return _in(left, right)
    if op in ('+', '-', '*', '/', '%') and (left is None or right is None):
        return None
    return _cmp_or_arith(op, left, right)


def _and(left, right_fn):
    if left is False:
        return False
    right = right_fn()
    if right is False:
        return False
    if left is None or right is None:
        return None
    return True


def _or(left, right_fn):
    if left is True:
        return True
    right = right_fn()
    if right is True:
        return True
    if left is None or right is None:
        return None
    return False


def _in(left, right):
    if right is None:
        return None
    if isinstance(right, dict):
        return left in right
    if isinstance(right, list):
        return left in right
    return None


def _cmp_or_arith(op, left, right):
    if op in ('<', '>', '<=', '>=') and (left is None or right is None):
        return None
    ops = {
        '==': lambda a, b: a == b,
        '!=': lambda a, b: a != b,
        '<': lambda a, b: a < b,
        '>': lambda a, b: a > b,
        '<=': lambda a, b: a <= b,
        '>=': lambda a, b: a >= b,
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / float(b),
        '%': lambda a, b: a % b,
    }
    return ops[op](left, right)


def _call(name, args, ctx):
    if name == 'exists':
        return _exists_call(args, ctx)
    func = _FUNCS.get(name)
    if func is None:
        bound = ctx.get(name)
        if callable(bound):
            return bound(*args)
        return None
    return func(*args)


def _exists_call(args, ctx):
    arg = args[0] if args else None
    rule = args[1] if len(args) > 1 else None
    if arg is None or rule is None:
        return 0
    files = ctx.get('_files') if isinstance(ctx, dict) else None
    if files is None:
        return 0
    return files.count(arg, rule, ctx)


def _intersects(left, right):
    if left is None or right is None:
        return False
    if not isinstance(left, list) or not isinstance(right, list):
        return False
    shared = [item for item in left if item in right]
    return shared if shared else False


def _allequal(left, right):
    if left is None or right is None:
        return False
    if not isinstance(left, list) or not isinstance(right, list):
        return False
    return left == right


def _match(value, pattern):
    if value is None:
        return None
    if pattern is None:
        return False
    return re.search(pattern, value) is not None


def _substr(value, start, end):
    if value is None or start is None or end is None:
        return None
    return value[start:end]


def _length(value):
    if value is None:
        return None
    return len(value)


def _count(values, item):
    if values is None:
        return None
    return values.count(item)


def _index(values, item):
    if values is None:
        return None
    try:
        return values.index(item)
    except ValueError:
        return None


def _sorted(values, method=None):
    if values is None:
        return None
    if method == 'lexical':
        return sorted(values, key=lambda item: str(item))
    if method == 'numeric':
        return _numeric_sort(values)
    return sorted(values)


def _numeric_sort(values):
    numeric_slots = []
    numeric_values = []
    for i, item in enumerate(values):
        number = _as_number(item)
        if number is None:
            continue
        numeric_slots.append(i)
        numeric_values.append((number, item))
    numeric_values.sort(key=lambda pair: pair[0])
    result = list(values)
    for slot, (_, item) in zip(numeric_slots, numeric_values):
        result[slot] = item
    return result


def _as_number(value):
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None
    return None


def _minmax(values, picker):
    if values is None:
        return None
    if not isinstance(values, list):
        return values
    numbers = [_as_number(item) for item in values]
    numbers = [item for item in numbers if item is not None]
    if not numbers:
        return None
    picked = picker(numbers)
    for item in values:
        if _as_number(item) == picked:
            return item
    return picked


def _unique(values):
    if values is None:
        return None
    result = []
    for item in values:
        if any(item == seen for seen in result):
            continue
        result.append(item)
    return result


def _type_name(value):
    if value is None:
        return 'null'
    if isinstance(value, bool):
        return 'boolean'
    if isinstance(value, (int, float)):
        return 'number'
    if isinstance(value, list):
        return 'array'
    if isinstance(value, dict):
        return 'object'
    if isinstance(value, str):
        return 'string'
    return type(value).__name__


_FUNCS = {
    'intersects': _intersects,
    'allequal': _allequal,
    'match': _match,
    'substr': _substr,
    'length': _length,
    'count': _count,
    'index': _index,
    'sorted': _sorted,
    'min': lambda values: _minmax(values, min),
    'max': lambda values: _minmax(values, max),
    'unique': _unique,
    'type': _type_name,
}
