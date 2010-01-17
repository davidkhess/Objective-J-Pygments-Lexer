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
    #flags = re.DOTALL
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
        #'methods' : [
        #    include('commentsandwhitespace'),
        #    ('
        }

# class ObjectiveJLexer(RegexLexer):
#     """
#     For Objective-C source code with preprocessor directives.
#     """

#     name = 'Objective-J'
#     aliases = ['objective-j', 'objectivej', 'obj-j', 'objj']
#     #XXX: objc has .h files too :-/
#     filenames = ['*.j']
#     mimetypes = ['text/x-objective-j']

#     #: optional Comment or Whitespace
#     _ws = r'(?:\s|//.*?\n|/[*].*?[*]/)+'

#     tokens = {
#         'whitespace': [
#             (r'^(\s*)(#if\s+0)', bygroups(Text, Comment.Preproc), 'if0'),
#             (r'^(\s*)(#)', bygroups(Text, Comment.Preproc), 'macro'),
#             (r'\n', Text),
#             (r'\s+', Text),
#             (r'\\\n', Text), # line continuation
#             (r'//(\n|(.|\n)*?[^\\]\n)', Comment.Single),
#             (r'/(\\\n)?[*](.|\n)*?[*](\\\n)?/', Comment.Multiline),
#         ],
#         'statements': [
#             (r'(L|@)?"', String, 'string'),
#             (r"(L|@)?'(\\.|\\[0-7]{1,3}|\\x[a-fA-F0-9]{1,2}|[^\\\'\n])'",
#              String.Char),
#             (r'(\d+\.\d*|\.\d+|\d+)[eE][+-]?\d+[lL]?', Number.Float),
#             (r'(\d+\.\d*|\.\d+|\d+[fF])[fF]?', Number.Float),
#             (r'0x[0-9a-fA-F]+[Ll]?', Number.Hex),
#             (r'0[0-7]+[Ll]?', Number.Oct),
#             (r'\d+[Ll]?', Number.Integer),
#             (r'[~!%^&*+=|?:<>/-]', Operator),
#             (r'[()\[\],.]', Punctuation),
#             (r'(auto|break|case|const|continue|default|do|else|enum|extern|'
#              r'for|goto|if|register|restricted|return|sizeof|static|struct|'
#              r'switch|typedef|union|volatile|virtual|while|in|@selector|'
#              r'@private|@protected|@public|@encode'
#              r'@synchronized|@try|@throw|@catch|@finally|@end|@property|'
#              r'@synthesize|@dynamic)\b', Keyword),
#             (r'(int|long|float|short|double|char|unsigned|signed|void|'
#              r'id|BOOL|IBOutlet|IBAction|SEL)\b', Keyword.Type),
#             (r'(_{0,2}inline|naked|restrict|thread|typename)\b',
#              Keyword.Reserved),
#             (r'__(asm|int8|based|except|int16|stdcall|cdecl|fastcall|int32|'
#              r'declspec|finally|int64|try|leave)\b', Keyword.Reserved),
#             (r'(TRUE|FALSE|nil|NULL)\b', Name.Builtin),
#             ('[a-zA-Z_][a-zA-Z0-9_]*:(?!:)', Name.Label),
#             ('[a-zA-Z_][a-zA-Z0-9_]*', Name),
#         ],
#         'root': [
#             include('whitespace'),
#             # functions
#             (r'((?:[a-zA-Z0-9_*\s])+?(?:\s|[*]))'    # return arguments
#              r'([a-zA-Z_][a-zA-Z0-9_]*)'             # method name
#              r'(\s*\([^;]*?\))'                      # signature
#              r'(' + _ws + r')({)',
#              bygroups(using(this), Name.Function,
#                       using(this), Text, Punctuation),
#              'function'),
#             (r'(var|with|function)\b', Keyword.Declaration),

#             # function declarations
#             (r'((?:[a-zA-Z0-9_*\s])+?(?:\s|[*]))'    # return arguments
#              r'([a-zA-Z_][a-zA-Z0-9_]*)'             # method name
#              r'(\s*\([^;]*?\))'                      # signature
#              r'(' + _ws + r')(;)',
#              bygroups(using(this), Name.Function,
#                       using(this), Text, Punctuation)),
#             (r'(@interface|@implementation)(\s+)', bygroups(Keyword, Text),
#              'classname'),
#             (r'(@import)(\s+)".*"', bygroups(Keyword, Text)),
#             (r'(@class|@protocol)(\s+)', bygroups(Keyword, Text),
#              'forward_classname'),
#             (r'(\s*)(@end)(\s*)', bygroups(Text, Keyword, Text)),
#             ('', Text, 'statement'),
#         ],
#         'classname' : [
#             # interface definition that inherits
#             ('([a-zA-Z_][a-zA-Z0-9_]*)(\s*:\s*)([a-zA-Z_][a-zA-Z0-9_]*)?',
#              bygroups(Name.Class, Text, Name.Class), '#pop'),
#             # interface definition for a category
#             ('([a-zA-Z_][a-zA-Z0-9_]*)(\s*)(\([a-zA-Z_][a-zA-Z0-9_]*\))',
#              bygroups(Name.Class, Text, Name.Label), '#pop'),
#             # simple interface / implementation
#             ('([a-zA-Z_][a-zA-Z0-9_]*)', Name.Class, '#pop')
#         ],
#         'forward_classname' : [
#           ('([a-zA-Z_][a-zA-Z0-9_]*)(\s*,\s*)',
#            bygroups(Name.Class, Text), 'forward_classname'),
#           ('([a-zA-Z_][a-zA-Z0-9_]*)(\s*;?)',
#            bygroups(Name.Class, Text), '#pop')
#         ],
#         'statement' : [
#             include('whitespace'),
#             include('statements'),
#             ('[{}]', Punctuation),
#             (';', Punctuation, '#pop'),
#         ],
#         'function': [
#             include('whitespace'),
#             include('statements'),
#             (';', Punctuation),
#             ('{', Punctuation, '#push'),
#             ('}', Punctuation, '#pop'),
#         ],
#         'string': [
#             (r'"', String, '#pop'),
#             (r'\\([\\abfnrtv"\']|x[a-fA-F0-9]{2,4}|[0-7]{1,3})', String.Escape),
#             (r'[^\\"\n]+', String), # all other characters
#             (r'\\\n', String), # line continuation
#             (r'\\', String), # stray backslash
#         ],
#         'macro': [
#             (r'[^/\n]+', Comment.Preproc),
#             (r'/[*](.|\n)*?[*]/', Comment.Multiline),
#             (r'//.*?\n', Comment.Single, '#pop'),
#             (r'/', Comment.Preproc),
#             (r'(?<=\\)\n', Comment.Preproc),
#             (r'\n', Comment.Preproc, '#pop'),
#         ],
#         'if0': [
#             (r'^\s*#if.*?(?<!\\)\n', Comment.Preproc, '#push'),
#             (r'^\s*#endif.*?(?<!\\)\n', Comment.Preproc, '#pop'),
#             (r'.*?\n', Comment),
#         ]
#     }

#     def analyse_text(text):
#         if '@"' in text: # strings
#             return True
#         if re.match(r'\[[a-zA-Z0-9.]:', text): # message
#             return True
#         return False
