import ply.yacc as yacc
from lexico import tokens, lexer

# Precedencia de operadores
precedence = (
    ('right', 'UMENOS'),  # Negativo unario
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIDO'),
    ('nonassoc', 'MENOR', 'MENOR_IGUAL', 'MAYOR', 'MAYOR_IGUAL'),
    ('left', 'IGUAL', 'NO_IGUAL'),
    ('left', 'Y'),
    ('left', 'O')
)

# Tabla de variables
variables = {}

# Reglas gramaticales
def p_programa(p):
    '''programa : declaraciones'''
    p[0] = p[1]

def p_declaraciones(p):
    '''declaraciones : declaracion
                     | declaraciones declaracion'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]

def p_declaracion(p):
    '''declaracion : expresion PUNTO_Y_COMA
                   | asignacion PUNTO_Y_COMA
                   | si_declaracion
                   | mientras_declaracion
                   | imprimir_declaracion PUNTO_Y_COMA'''
    p[0] = p[1]

def p_imprimir_declaracion(p):
    '''imprimir_declaracion : IMPRIMIR PARENTESIS_IZQ expresion PARENTESIS_DER'''
    print(f"Imprimiendo: {p[3]}")
    p[0] = ('imprimir', p[3])

def p_expresion_binaria(p):
    '''expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion POR expresion
                 | expresion DIVIDIDO expresion
                 | expresion IGUAL expresion
                 | expresion NO_IGUAL expresion
                 | expresion MENOR expresion
                 | expresion MENOR_IGUAL expresion
                 | expresion MAYOR expresion
                 | expresion MAYOR_IGUAL expresion
                 | expresion Y expresion
                 | expresion O expresion'''
    op = p[2]
    if op == '+': p[0] = p[1] + p[3]
    elif op == '-': p[0] = p[1] - p[3]
    elif op == '*': p[0] = p[1] * p[3]
    elif op == '/': p[0] = p[1] / p[3]
    elif op == '==': p[0] = p[1] == p[3]
    elif op == '!=': p[0] = p[1] != p[3]
    elif op == '<': p[0] = p[1] < p[3]
    elif op == '<=': p[0] = p[1] <= p[3]
    elif op == '>': p[0] = p[1] > p[3]
    elif op == '>=': p[0] = p[1] >= p[3]
    elif op == 'y': p[0] = p[1] and p[3]
    elif op == 'o': p[0] = p[1] or p[3]

def p_expresion_negativa(p):
    '''expresion : MENOS expresion %prec UMENOS'''
    p[0] = -p[2]

def p_expresion_agrupada(p):
    '''expresion : PARENTESIS_IZQ expresion PARENTESIS_DER'''
    p[0] = p[2]

def p_expresion_numero(p):
    '''expresion : ENTERO
                 | DECIMAL'''
    p[0] = p[1]

def p_expresion_cadena(p):
    '''expresion : CADENA'''
    p[0] = p[1]

def p_expresion_booleano(p):
    '''expresion : VERDADERO
                 | FALSO'''
    p[0] = True if p[1] == 'verdadero' else False

def p_expresion_identificador(p):
    '''expresion : IDENTIFICADOR'''
    if p[1] in variables:
        p[0] = variables[p[1]]
    else:
        print(f"Variable no definida: '{p[1]}'")
        p[0] = None

def p_asignacion(p):
    '''asignacion : IDENTIFICADOR ASIGNACION expresion'''
    variables[p[1]] = p[3]
    p[0] = ('asignacion', p[1], p[3])

def p_si_declaracion(p):
    '''si_declaracion : SI expresion HACER declaraciones FIN
                      | SI expresion HACER declaraciones SINO HACER declaraciones FIN'''
    if len(p) == 6:
        if p[2]: p[0] = p[4]
    else:
        p[0] = p[4] if p[2] else p[7]

def p_mientras_declaracion(p):
    '''mientras_declaracion : MIENTRAS expresion HACER declaraciones FIN'''
    while p[2]:
        p[0] = p[4]

def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}' en la línea {p.lineno}")
    else:
        print("Error de sintaxis al final del código")

# Construcción del parser
parser = yacc.yacc()

def analizar(codigo):
    return parser.parse(codigo, lexer=lexer)

if __name__ == '__main__':
    prueba = '''
    x = -5 + 3 * 2;
    si x > 0 hacer
        imprimir("Positivo");
    sino hacer
        imprimir("Negativo");
    fin
    '''
    resultado = analizar(prueba)
    print("Resultado final:", resultado)
