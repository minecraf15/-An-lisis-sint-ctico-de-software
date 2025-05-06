from lexico import probar_lexico
from sintactico import analizar

def mostrar_tokens(tokens):
    print("\nTokens encontrados:")
    for token in tokens:
        print(f"Tipo: {token.type}, Valor: {token.value}, Línea: {token.lineno}")

def main():
    print("Escribe 'salir' para terminar")
    print("Opciones especiales:")
    print("-v : Mostrar tokens (modo verbose)")
    print("-d : Mostrar depuración")
    
    while True:
        try:
            entrada = input('subliminal666> ')
            
            if entrada.lower() == 'salir':
                break
                
            if entrada.startswith('-v'):
                codigo = entrada[2:].strip()
                tokens = probar_lexico(codigo)
                mostrar_tokens(tokens)
            
            resultado = analizar(entrada)
            if resultado is not None:
                print(f"Resultado: {resultado}")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()