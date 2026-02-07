import os


def cifrar_cesar(texto, desplazamiento):
    # Aplica el desplazamiento de caracteres según el estándar del alfabeto inglés
    resultado = ""
    for char in texto:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            # Calcula la nueva posición dentro del rango de 26 letras
            nuevo_char = chr((ord(char) - ascii_offset + desplazamiento) % 26 + ascii_offset)
            resultado += nuevo_char
        else:
            resultado += char
    return resultado


def descifrar_cesar(texto, desplazamiento):
    # Invierte el proceso de cifrado restando el desplazamiento
    return cifrar_cesar(texto, -desplazamiento)


def fuerza_bruta_cesar(texto):
    print("\n--- EJECUTANDO FUERZA BRUTA ---")
    # Prueba las 25 combinaciones posibles del cifrado César
    for i in range(1, 26):
        intento = descifrar_cesar(texto, i)
        print(f"Clave {i:02d}: {intento}")
    print("-" * 40)


def procesar_vigenere(texto, clave, modo='cifrar'):
    resultado = ""
    # Filtra la clave para extraer solo letras y evitar errores de longitud en ord()
    letras_clave = [c for c in clave if c.isalpha()]

    if not letras_clave:
        return "[Error: Clave no válida]"

    # Convierte las letras de la clave en valores numéricos de 0 a 25
    indices_clave = [ord(c.upper()) - 65 for c in letras_clave]
    posicion_clave = 0

    for char in texto:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            desplazamiento = indices_clave[posicion_clave % len(indices_clave)]

            if modo == 'descifrar':
                desplazamiento = -desplazamiento

            # Realiza la sustitución polialfabética
            nuevo_char = chr((ord(char) - ascii_offset + desplazamiento) % 26 + ascii_offset)
            resultado += nuevo_char
            posicion_clave += 1
        else:
            resultado += char

    return resultado


def ataque_diccionario_vigenere(texto):
    archivo = "rockyou.txt"
    if not os.path.exists(archivo):
        print(f"\n[!] Error crítico: El archivo '{archivo}' no existe.")
        return

    print("\n--- AJUSTES DE ATAQUE POR DICCIONARIO ---")
    print("1. Intentar con todo el archivo")
    print("2. Filtrar por longitud de clave")
    sub_op = input("Seleccione una opción: ")

    limite_longitud = 0
    if sub_op == '2':
        try:
            limite_longitud = int(input("Ingrese longitud exacta: "))
        except ValueError:
            print("Entrada no válida. Se ignorará el filtro.")

    print(f"\n--- PROCESANDO DICCIONARIO ---")
    try:
        # Lee el archivo de texto y limpia cada entrada para evitar caracteres de control
        with open(archivo, 'r', encoding='utf-8', errors='ignore') as f:
            for linea in f:
                clave_candidata = linea.strip()
                if not clave_candidata:
                    continue

                if limite_longitud > 0 and len(clave_candidata) != limite_longitud:
                    continue

                descifrado = procesar_vigenere(texto, clave_candidata, modo='descifrar')
                print(f"Clave [{clave_candidata}]: {descifrado[:60]}")
    except Exception as e:
        print(f"Error durante la lectura: {e}")



def main():
    while True:
        print("\n" + "=" * 35)
        print("   SISTEMA DE CIFRADO CIBERPOLLO")
        print("=" * 35)
        print("1. Cifrado César")
        print("2. Cifrado Vigenère")
        print("3. Descifrado César")
        print("4. Descifrado Vigenère")
        print("5. Salir")

        opcion = input("\nSeleccione una opción: ")

        if opcion == '1':
            m = input("Mensaje a cifrar: ")
            try:
                k = int(input("Clave numérica: "))
                print(f"Cifrado: {cifrar_cesar(m, k)}")
            except ValueError:
                print("Error: La clave debe ser un número entero.")

        elif opcion == '2':
            m = input("Mensaje a cifrar: ")
            k = input("Clave (texto): ")
            print(f"Cifrado: {procesar_vigenere(m, k, 'cifrar')}")

        elif opcion == '3':
            m = input("Mensaje cifrado: ")
            print("1. Usar clave conocida | 2. Fuerza bruta")
            sub = input("Opción: ")
            if sub == '1':
                try:
                    k = int(input("Clave numérica: "))
                    print(f"Descifrado: {descifrar_cesar(m, k)}")
                except ValueError:
                    print("Error: Clave inválida.")
            else:
                fuerza_bruta_cesar(m)

        elif opcion == '4':
            m = input("Mensaje cifrado: ")
            print("1. Usar clave conocida | 2. Ataque de diccionario")
            sub = input("Opción: ")
            if sub == '1':
                k = input("Clave: ")
                print(f"Descifrado: {procesar_vigenere(m, k, 'descifrar')}")
            else:
                ataque_diccionario_vigenere(m)

        elif opcion == '5':
            print("Cerrando sistema de protección. ¡Buen día!")
            break
        else:
            print("Opción fuera de rango.")


if __name__ == "__main__":
    main()