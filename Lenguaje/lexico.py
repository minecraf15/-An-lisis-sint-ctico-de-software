import ply.lex as lex

# Palabras reservadas en español
reservadas = {
    'si': 'SI',
    'sino': 'SINO',
    'mientras': 'MIENTRAS',
    'imprimir': 'IMPRIMIR',
    'verdadero': 'VERDADERO',
    'falso': 'FALSO',
    'hacer': 'HACER',
    'fin': 'FIN',
    'y': 'Y',
    'o': 'O'
}

# Lista completa de tokens
tokens = [
    'ENTERO',
    'DECIMAL',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'PARENTESIS_IZQ',
    'PARENTESIS_DER',
    'LLAVE_IZQ',
    'LLAVE_DER',
    'PUNTO_Y_COMA',
    'ASIGNACION',
    'IDENTIFICADOR',
    'IGUAL',
    'NO_IGUAL',
    'MENOR',
    'MENOR_IGUAL',
    'MAYOR',
    'MAYOR_IGUAL',
    'CADENA',
    'UMENOS'
] + list(reservadas.values())

# Definición de tokens simples
t_MAS = r'\+'
t_MENOS = r'-'
t_POR = r'\*'
t_DIVIDIDO = r'/'
t_PARENTESIS_IZQ = r'\('
t_PARENTESIS_DER = r'\)'
t_LLAVE_IZQ = r'\{'
t_LLAVE_DER = r'\}'
t_PUNTO_Y_COMA = r';'
t_ASIGNACION = r'='
t_IGUAL = r'=='
t_NO_IGUAL = r'!='
t_MENOR = r'<'
t_MENOR_IGUAL = r'<='
t_MAYOR = r'>'
t_MAYOR_IGUAL = r'>='

# Caracteres a ignorar
t_ignore = ' \t'

def t_CADENA(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]  # Elimina las comillas
    return t

def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value.lower(), 'IDENTIFICADOR')
    return t

def t_DECIMAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_nueva_linea(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Carácter no válido '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

def probar_lexico(codigo):
    """
    Función para probar el analizador léxico
    Devuelve una lista de tokens encontrados
    """
    lexer.input(codigo)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(tok)
    return tokens

if __name__ == '__main__':
    data = '''
    si x > 5 hacer
        imprimir("Hola mundo");
    fin
    '''
    tokens = probar_lexico(data)
    
    print("Tokens encontrados:")
    for tok in tokens:
        print(f"Tipo: {tok.type}, Valor: {tok.value}, Línea: {tok.lineno}")