"""
    Portions of this file are covered under the following license:
    
    :copyright: Copyright 2006-2010 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.

    The rest of the work is placed in the public domain by Fish Software, Inc.
"""

import re

from pygments.lexer import Lexer, DelegatingLexer, RegexLexer, bygroups, \
     include, using, this

from pygments.lexer import RegexLexer
from pygments.token import *

class ObjectiveJLexer(RegexLexer):
    """
    For Objective-J source code.
    """

    name = 'Objective-J'
    aliases = ['objectivej', 'objective-j', 'obj-j', 'objj']
    filenames = ['*.j']
    mimetypes = ['text/x-objective-j']
    _ws = r'(?:\s|//.*?\n|/[*].*?[*]/)+'
    tokens = {
        'commentsandwhitespace': [
            (r'^\s*#(?:include|if|pragma)\s*', Comment.Preproc, "expression"),
            (r'^\s*#(else|endif)', Comment.Preproc),
            (r'\s+', Text),
            (r'<!--', Comment),
            (r'//.*?\n', Comment.Single),
            (r'//(\n|(.|\n)*?[^\\]\n)', Comment.Single),
            (r'/(\\\n)?[*](.|\n)*?[*](\\\n)?/', Comment.Multiline),
        ],
        'slashstartsregex': [
            include('commentsandwhitespace'),
            (r'/(\\.|[^[/\\\n]|\[(\\.|[^\]\\\n])*])+/'
             r'([gim]+\b|\B)', String.Regex, '#pop'),
            (r'(?=/)', Text, ('#pop', 'badregex')),
            (r'', Text, '#pop')
        ],
        'badregex': [
            ('\n', Text, '#pop')
        ],
        'root': [
            include('commentsandwhitespace'),
            (r'^(?=\s|/|<!--)', Text, 'slashstartsregex'),
            (r'([$a-zA-Z_][a-zA-Z0-9_]*)(\[)', bygroups(Name.Other, Punctuation), ("rightbracket", "expression")),
            (r'(\[\])', bygroups(Punctuation)),
            (r'(\[)', bygroups(Keyword), ("message", "whitespace", "expression")),
            (r'([$a-zA-Z_][a-zA-Z0-9_]*)(\()', bygroups(Name.Function, Punctuation), ("rightparen", "expression")),
            (r'\+\+|--|~|&&|\?|:|\|\||\\(?=\n)|'
             r'(<<|>>>?|===?|==?|!=?|[-<>+*%&\|\^/])=?', Operator, 'slashstartsregex'),
            (r'[{(\;,]', Punctuation, 'slashstartsregex'),
            (r'[})\.]', Punctuation),
            (r'(for|in|while|do|break|return|continue|switch|case|default|if|else|'
             r'throw|try|catch|finally|new|delete|typeof|instanceof|self|'
             r'this)\b', Keyword, 'slashstartsregex'),
            (r'(var|with|function)\b', Keyword.Declaration, 'slashstartsregex'),
            (r'(abstract|boolean|byte|char|class|const|debugger|double|enum|export|'
             r'extends|final|float|goto|implements|import|int|interface|long|native|'
             r'package|private|protected|public|short|static|super|synchronized|throws|'
             r'transient|volatile)\b', Keyword.Reserved),
            (r'(true|false|null|NaN|Infinity|undefined|YES|NO)\b', Keyword.Constant),
            (r'(Array|Boolean|Date|Error|Function|Math|netscape|'
             r'Number|Object|Packages|RegExp|String|sun|decodeURI|'
             r'decodeURIComponent|encodeURI|encodeURIComponent|'
             r'Error|eval|isFinite|isNaN|parseFloat|parseInt|document|this|'
             r'window)\b', Name.Builtin),
            ('[a-zA-Z_][a-zA-Z0-9_]*:(?!:)', Name.Label),
            (r'[$a-zA-Z_][a-zA-Z0-9_]*', Name.Other),
            (r'[0-9][0-9]*\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float),
            (r'0x[0-9a-fA-F]+', Number.Hex),
            (r'[0-9]+', Number.Integer),
            (r'@"(\\\\|\\"|[^"])*"', String.Double),
            (r"@'(\\\\|\\'|[^'])*'", String.Single),
            (r'"(\\\\|\\"|[^"])*"', String.Double),
            (r"'(\\\\|\\'|[^'])*'", String.Single),
            (r'(@import)(\s+)("(\\\\|\\"|[^"])*")', bygroups(Keyword, Text, String.Double)),
            (r'(@import)(\s+)(<(\\\\|\\>|[^>])*>)', bygroups(Keyword, Text, String.Double)),
            (r'(@implementation)(\s+)', bygroups(Keyword, Text), 'classname'),
            (r'(@end)(\s+)', bygroups(Keyword, Text)),
        ],
        'whitespace' : [
            (r'(\s+)', Text, "#pop"),
            ],
        'maybewhitespace' : [
            (r'(\s*)', Text, "#pop"),
            ],
        'rightbracket' : [
            (r'\]', Punctuation, "#pop"),
            ],
        'rightparen' : [
            (r'\)', Punctuation, "#pop"),
            ],
        'expression' : [
            (r'(\s*)//.*?\n', Comment.Single),
            (r'(\s*)/(\\\n)?[*](.|\n)*?[*](\\\n)?/(\s*)', Comment.Multiline),
            (r'([$a-zA-Z_][a-zA-Z0-9_]*)(\[)', bygroups(Name.Other, Punctuation), ("rightbracket", "expression")),
            (r'(\[\])', bygroups(Punctuation)),
            (r'(\[)', bygroups(Keyword), ("message", "whitespace", "expression")),
            (r'([$a-zA-Z_][a-zA-Z0-9_]*)(\()', bygroups(Name.Function, Punctuation), ("rightparen", "expression")),
            (r'(\s*)(\+\+|--|~|&&|\?|:|\|\||\\(?=\n)|'
             r'(?:<<|>>>?|===?|==?|!=?|[-<>+*%&\|\^/])=?)(\s*)', bygroups(Text,Operator, Text), ("expression", 'slashstartsregex')),
            (r'\(', Punctuation, ("rightparen", "expression")),
            (r'[.,]', Punctuation, 'slashstartsregex'),
            (r'[$a-zA-Z_][a-zA-Z0-9_]*', Name.Other),
            (r'[0-9][0-9]*\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float),
            (r'0x[0-9a-fA-F]+', Number.Hex),
            (r'[0-9]+', Number.Integer),
            (r'@"(\\\\|\\"|[^"])*"', String.Double),
            (r"@'(\\\\|\\'|[^'])*'", String.Single),
            (r'"(\\\\|\\"|[^"])*"', String.Double),
            (r"'(\\\\|\\'|[^'])*'", String.Single),
            (r"(@selector)(\()((?:[a-zA-Z_][a-zA-Z0-9_]*:)|(?:[a-zA-Z_][a-zA-Z0-9_]*))(\))", bygroups(Keyword, Punctuation, Name.Label, Punctuation)),
            (r'', Text, "#pop")
            ],
        'classname' : [
            # interface definition that inherits
            ('([a-zA-Z_][a-zA-Z0-9_]*)(\s*:\s*)([a-zA-Z_][a-zA-Z0-9_]*)?(\s*)({)',
             bygroups(Name.Class, Text, Name.Class, Text, Punctuation), 'members'),
            # interface definition for a category
            ('([a-zA-Z_][a-zA-Z0-9_]*)(\s*)(\()([a-zA-Z_][a-zA-Z0-9_]*)(\))(\s*)',
             bygroups(Name.Class, Text, Punctuation, Name.Class, Punctuation, Text), '#pop'),
            # simple interface / implementation
            ('([a-zA-Z_][a-zA-Z0-9_]*)(\s*)({)', bygroups(Name.Class, Punctuation, Text), 'members')
            ],
        'members' : [
            include('commentsandwhitespace'),
            ('}', Punctuation, '#pop'),
            ('([a-zA-Z_][a-zA-Z0-9_]*)(\s+)([a-zA-Z_][a-zA-Z0-9_]*)(\s*)(;)', bygroups(Keyword.Type, Text, Name, Text, Punctuation))
            ],
        'message' : [
            (r'(\s*)([a-zA-Z_][a-zA-Z0-9_]*:)', bygroups(Text, Name.Label), ("expression", "maybewhitespace")),
            (r'(\s*)([a-zA-Z_][a-zA-Z0-9_]*)', bygroups(Text, Name.Label)),
            (r'(\s*)(\])', bygroups(Text, Keyword), "#pop")
            ],
        }

