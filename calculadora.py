import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
)
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_NUMBER = r'\d+(\.\d+)?'  
t_ignore = ' \t'

def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

def p_expression_binop(p):
    '''expression : expression PLUS term
                | expression MINUS term
                | term'''
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])  
    else:
        p[0] = p[1]

def p_term_binop(p):
    '''term : term TIMES factor
            | term DIVIDE factor
            | factor'''
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])  
    else:
        p[0] = p[1]

def p_factor(p):
    '''factor : NUMBER
            | LPAREN expression RPAREN'''
    p[0] = float(p[1]) if len(p) == 2 else p[2]

def p_error(p):
    print("Error de sintaxis en la entrada")

parser = yacc.yacc()

def eval_arbol(arbol):
    if isinstance(arbol, tuple):
        op, left, right = arbol
        left = eval_arbol(left)
        right = eval_arbol(right)
        return { '+': left + right,
                '-': left - right,
                 '*': left * right,
                '/': left / right}[op]
    return arbol  

def calcular(expresion):
    lexer.input(expresion)
    return eval_arbol(parser.parse(expresion))

if __name__ == '__main__':
    while True:
        try:
            expr = input("Ingrese una expresión: ")
            if expr.lower() == 'salir':
                break
            print(f"Resultado: {calcular(expr)}")
        except Exception as e:
            print(f"Error: {e}")