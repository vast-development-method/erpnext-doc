"""Translate the expression subset used by the pinned form metadata into data.

The tree is descriptive. No expression or callable from the source is executed.
"""

import ast
import re

TOKENS = re.compile(r"""\s*(?:(?P<string>"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')|(?P<number>\d+(?:\.\d+)?)|(?P<symbol>[A-Za-z_$][\w$]*)|(?P<op>===|!==|==|!=|>=|<=|&&|\|\||=>|\?\.|[.()\[\],;!<>+\-]))""")
OPERATORS = {
    "=>": (1, "lambda"), "||": (2, "or"), "&&": (3, "and"),
    "==": (4, "coercive_equal"), "!=": (4, "coercive_unequal"),
    "===": (4, "strict_equal"), "!==": (4, "strict_unequal"),
    "<": (5, "less"), ">": (5, "greater"), "<=": (5, "at_most"), ">=": (5, "at_least"),
    "+": (6, "plus"), "-": (6, "minus"),
}


class Parser:
    def __init__(self, raw):
        self.tokens = []
        text = raw.strip()
        pos = 0
        while pos < len(text):
            match = TOKENS.match(text, pos)
            if not match:
                raise ValueError(f"unrecognized character at {pos}")
            self.tokens.append((match.lastgroup, match.group(match.lastgroup)))
            pos = match.end()
        self.tokens.append(("end", ""))
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos][1]

    def take(self):
        token = self.tokens[self.pos]
        if token[0] == "end":
            raise ValueError("unexpected end")
        self.pos += 1
        return token

    def expect(self, value):
        if self.take()[1] != value:
            raise ValueError(f"expected {value}")

    def arguments(self, end):
        values = []
        if self.peek() != end:
            values.append(self.expression())
            while self.peek() == ",":
                self.take()
                values.append(self.expression())
        self.expect(end)
        return values

    def expression(self, minimum=1):
        kind, value = self.take()
        if kind == "string":
            result = ["literal", ast.literal_eval(value)]
        elif kind == "number":
            result = ["literal", float(value) if "." in value else int(value)]
        elif kind == "symbol":
            if value in ("true", "false", "null"):
                result = ["literal", {"true": True, "false": False, "null": None}[value]]
            else:
                result = ["symbol", value]
        elif value in ("!", "-"):
            result = ["not" if value == "!" else "negate", self.expression(7)]
        elif value == "(":
            result = self.expression()
            self.expect(")")
        elif value == "[":
            result = ["list", *self.arguments("]")]
        else:
            raise ValueError(f"unexpected prefix {value}")
        while True:
            operator = self.peek()
            if operator in (".", "?."):
                self.take()
                key_type, key = self.take()
                if key_type != "symbol":
                    raise ValueError("expected member name")
                result = ["optional_member" if operator == "?." else "member", result, key]
            elif operator == "(":
                self.take()
                result = ["call", result, *self.arguments(")")]
            elif operator == "[":
                self.take()
                result = ["subscript", result, self.expression()]
                self.expect("]")
            elif operator in OPERATORS and OPERATORS[operator][0] >= minimum:
                self.take()
                precedence, name = OPERATORS[operator]
                result = [name, result, self.expression(precedence + (operator != "=>"))]
            else:
                return result


def rule(value):
    if isinstance(value, bool):
        return ["literal", value]
    if not value.startswith("eval:"):
        if value.startswith("fn:"):
            return ["form_callback", value[3:]]
        return ["field_has_value", value]
    parser = Parser(value[5:])
    tree = parser.expression()
    while parser.peek() == ";":
        parser.take()
    if parser.peek():
        raise ValueError(f"unconsumed token {parser.peek()}")
    return tree
