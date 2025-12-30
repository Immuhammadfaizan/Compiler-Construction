import re

# List of keywords in C
keywords = ['int', 'float', 'char', 'if', 'else', 'for', 'while', 'return', 'void']

# List of operators
operators = ['\+', '-', '\*', '/', '=', '==', '!=', '<', '>', '<=', '>=']

# List of separators / symbols
separators = [';', ',', '\(', '\)', '{', '}', '\[', '\]']

# Regex for identifiers (variable/function names)
identifier = r'[a-zA-Z_][a-zA-Z0-9_]*'

# Regex for numeric constants
number = r'\d+(\.\d+)?'

# Combine regex
token_regex = '|'.join([
    '(?P<KEYWORD>' + '|'.join(keywords) + ')',
    '(?P<OPERATOR>' + '|'.join(operators) + ')',
    '(?P<SEPARATOR>' + '|'.join(separators) + ')',
    '(?P<NUMBER>' + number + ')',
    '(?P<IDENTIFIER>' + identifier + ')'
])

def lexer(filename):
    with open(filename, 'r') as f:
        code = f.read()
    
    
    code = re.sub(r'//.*', '', code)          
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.S)  
    
    tokens = []
    for match in re.finditer(token_regex, code):
        kind = match.lastgroup
        value = match.group()
        tokens.append((kind, value))
    
    return tokens

if __name__ == "__main__":
    filename = input("") # Enter the path to the C source code file, for example: "example.c"
    token_list = lexer(filename)
    print("\nTokens generated:\n")
    for token in token_list:
        print(token)