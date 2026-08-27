# E++ (Español++) - Guía de Uso

## Índice
1. [Instalación](#instalación)
2. [Ejecutar tu primer programa](#ejecutar-tu-primer-programa)
3. [Sintaxis de E++](#sintaxis-de-e)
4. [Motor Gráfico para Juegos](#motor-gráfico-para-juegos)
5. [Ejemplos de código](#ejemplos-de-código)
6. [Referencia rápida](#referencia-rápida)
7. [Solución de problemas](#solución-de-problemas)

---

## Instalación

### Paso 1: Instalar Python

E++ requiere **Python 3.8 o superior**.

**Windows:**
1. Ve a https://python.org/downloads
2. Descarga Python 3.11 o superior
3. Ejecuta el instalador y **marca "Add Python to PATH"**
4. Verifica la instalación abriendo CMD y escribiendo:
```cmd
python --version
```

**Mac:**
```bash
# Usando Homebrew
brew install python3

# Verificar
python3 --version
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip
python3 --version
```

### Paso 2: Instalar Pygame (para juegos gráficos)

```bash
# Windows
pip install pygame

# Mac / Linux
pip3 install pygame
```

### Paso 3: Descargar E++

Descarga los archivos del intérprete:
- `interprete.py` - El intérprete principal
- `mi_juego.epp` - Ejemplo de juego

---

## Ejecutar tu primer programa

### Método 1: Archivo .epp

1. Crea un archivo de texto llamado `hola.epp`
2. Escribe el siguiente código:

```epp
// Mi primer programa en E++
di: "Hola Mundo!"
di: "Estoy programando en espanol!"

nombre = "Juan"
edad = 25

di: "Me llamo " + nombre
di: "Tengo " + convertir_texto(edad) + " anos"
```

3. Ejecuta en la terminal:

```bash
# Windows
python interprete.py hola.epp

# Mac / Linux
python3 interprete.py hola.epp
```

### Método 2: Modo interactivo (REPL)

```bash
python interprete.py
```

Se abrirá el modo interactivo donde puedes escribir código línea por línea:

```
E++ > di: "Hola!"
Hola!
E++ > x = 10
E++ > di: x * 2
20
E++ > salir
```

---

## Sintaxis de E++

### 1. Impresión por consola

```epp
di: "Hola mundo"
di: 42
di: "El resultado es: " + convertir_texto(10 + 5)
```

### 2. Variables (tipado dinámico)

```epp
// Asignación directa
nombre = "María"
edad = 30
altura = 1.75
activo = verdadero

// También puedes usar 'guarda' (opcional)
guarda nombre = "María"
```

### 3. Operaciones matemáticas

```epp
suma = 10 + 5       // 15
resta = 10 - 3      // 7
mult = 4 * 3        // 12
div = 15 / 3        // 5
mod = 10 % 3        // 1
pot = 2 ** 3        // 8
```

### 4. Condicionales (si / si no)

```epp
puntuacion = 100

si puntuacion > 50:
    di: "Ganaste!"
si no:
    di: "Sigue intentando"
fin

// Condiciones complejas
vidas = 3
nivel = 5

si vidas == 0 y nivel < 10:
    di: "Game Over"
si no:
    si nivel >= 10:
        di: "Nivel avanzado!"
    fin
fin
```

**Operadores de comparación:**
- `==` igual
- `!=` diferente
- `>` mayor que
- `<` menor que
- `>=` mayor o igual
- `<=` menor o igual
- `y` AND lógico
- `o` OR lógico
- `no` NOT lógico

### 5. Bucles

```epp
// Repetir N veces
repetir 5 veces:
    di: "Hola!"
fin

// Bucle mientras
contador = 0
mientras contador < 10:
    di: contador
    contador = contador + 1
fin

// Bucle para (for)
para i en 1 hasta 5:
    di: "Iteracion: " + convertir_texto(i)
fin
```

### 6. Funciones

```epp
// Definir funcion
funcion saludar(nombre):
    di: "Hola, " + nombre + "!"
fin

// Llamar funcion
saludar("Ana")
saludar("Luis")

// Funcion con retorno
funcion sumar(a, b):
    retorna a + b
fin

resultado = sumar(10, 20)
di: resultado  // 30

// Funcion con factorial
funcion factorial(n):
    si n <= 1:
        retorna 1
    fin
    retorna n * factorial(n - 1)
fin

di: factorial(5)  // 120
```

### 7. Listas

```epp
// Crear lista
frutas = ["manzana", "pera", "uva"]
numeros = [1, 2, 3, 4, 5]

// Acceder por índice
primera = frutas[0]     // "manzana"

// Longitud
cantidad = longitud(frutas)

// Iterar
para i en 0 hasta longitud(frutas) - 1:
    di: frutas[i]
```

---

## Motor Gráfico para Juegos

### Configuración de pantalla

```epp
// Crear ventana del juego
Resolucion de la pantalla de prueba en 800x600
titulo = "Mi Juego Increíble"
Fondo color "azul"
```

### Colores disponibles

| Color en E++ | Color visual |
|-------------|-------------|
| `"blanco"` | `#FFFFFF` |
| `"negro"` | `#000000` |
| `"rojo"` | `#FF0000` |
| `"verde"` | `#00FF00` |
| `"azul"` | `#0000FF` |
| `"amarillo"` | `#FFFF00` |
| `"naranja"` | `#FFA500` |
| `"morado"` | `#800080` |
| `"rosa"` | `#FFC0CB` |
| `"gris"` | `#808080` |
| `"celeste"` | `#87CEEB` |
| `"dorado"` | `#FFD700` |
| `"noche"` | `#0F121B` |
| `"carbon"` | `#333333` |
| `"esmeralda"` | `#50C878` |
| `"ruby"` | `#E0115F` |

### Crear entidades (objetos del juego)

```epp
// Jugador - cuadrado verde por defecto
Genera un "jugador", en "Centro"

// En coordenadas específicas
Genera un "jugador", en "100, 200"

// Tipos de entidades predefinidos:
// "jugador"  -> cuadrado verde (50x50)
// "bloque"   -> cuadrado rojo (40x40)
// "moneda"   -> círculo amarillo (radio 15)
// "enemigo"  -> cuadrado naranja (45x45)
// "meta"     -> cuadrado dorado (60x60)
// "proyectil"-> círculo blanco pequeño
```

### Posiciones especiales

```epp
// "Centro"  -> centro de la pantalla
// "Arriba"  -> parte superior centrada
// "Abajo"   -> parte inferior centrada
// "Izquierda" -> lado izquierdo centrado
// "Derecha"  -> lado derecho centrado
// "100, 200" -> coordenadas X=100, Y=200
```

### Controles y movimiento

```epp
// Mover con teclas de dirección
Al presionar tecla "derecha":
    Mueve "jugador" hacia "derecha" por 10

Al presionar tecla "izquierda":
    Mueve "jugador" hacia "izquierda" por 10

Al presionar tecla "arriba":
    Mueve "jugador" hacia "arriba" por 10

Al presionar tecla "abajo":
    Mueve "jugador" hacia "abajo" por 10

// Otras teclas comunes:
// "espacio", "enter", "escape"
// "a", "b", "c", ... (cualquier letra)
// "0", "1", "2", ... (cualquier número)
```

### Destruir entidades

```epp
// Eliminar una entidad del juego
Destruye "moneda"
```

### Configuración del juego

```epp
// Cambiar título de la ventana
titulo = "Mi Juego"

// Cambiar fondo
Fondo color "negro"

// Configurar puntuación inicial
Puntuacion = 0

// Configurar vidas
Vidas = 3

// Configurar FPS (velocidad del juego)
FPS = 60

// Configurar gravedad (para juegos de plataformas)
Gravedad = 0.5
```

---

## Ejemplos de código

### Ejemplo 1: Calculadora simple

```epp
// calculadora.epp

funcion calculadora():
    di: "=== CALCULADORA E++ ==="
    
    di: "Primer numero:"
    a = convertir_numero(entrada("> "))
    
    di: "Segundo numero:"
    b = convertir_numero(entrada("> "))
    
    di: "Operacion (+, -, *, /):"
    op = entrada("> ")
    
    si op == "+":
        resultado = a + b
    si no:
        si op == "-":
            resultado = a - b
        si no:
            si op == "*":
                resultado = a * b
            si no:
                si op == "/":
                    resultado = a / b
                fin
            fin
        fin
    fin
    
    di: "Resultado: " + convertir_texto(resultado)
fin

calculadora()
```

### Ejemplo 2: Juego de adivinar número

```epp
// adivina.epp

di: "=== ADIVINA EL NUMERO ==="
di: "Estoy pensando en un numero entre 1 y 100"

secreto = aleatorio(1, 100)
intentos = 0
adivinado = falso

mientras no adivinado:
    di: ""
    di: "Tu intento:"
    intento = convertir_numero(entrada("> "))
    intentos = intentos + 1
    
    si intento == secreto:
        di: "Correcto! Lo adivinaste en " + convertir_texto(intentos) + " intentos"
        adivinado = verdadero
    si no:
        si intento < secreto:
            di: "Mas alto..."
        si no:
            di: "Mas bajo..."
        fin
    fin
fin
```

### Ejemplo 3: Juego con gráficos - Esquivar bloques

```epp
// esquivar.epp

Resolucion de la pantalla de prueba en 800x600
titulo = "Esquivar Bloques - E++"
Fondo color "noche"

// Crear jugador
Genera un "jugador", en "Centro"

// Crear bloques enemigos
Genera un "bloque", en "100, 50"
Genera un "bloque2", en "300, 100"
Genera un "bloque3", en "500, 150"
Genera un "bloque4", en "700, 80"

// Crear moneda objetivo
Genera un "moneda", en "400, 300"

// Controles
Al presionar tecla "derecha":
    Mueve "jugador" hacia "derecha" por 8
fin

Al presionar tecla "izquierda":
    Mueve "jugador" hacia "izquierda" por 8
fin

Al presionar tecla "arriba":
    Mueve "jugador" hacia "arriba" por 8
fin

Al presionar tecla "abajo":
    Mueve "jugador" hacia "abajo" por 8
fin

Puntuacion = 0
Vidas = 3

di: "=== ESQUIVAR BLOQUES ==="
di: "Usa las flechas para moverte"
di: "Recoge la moneda amarilla!"
di: "Evita los bloques rojos!"
```

### Ejemplo 4: Figuras geométricas con bucles

```epp
// figuras.epp

Resolucion de la pantalla de prueba en 600x600
titulo = "Figuras con E++"
Fondo color "negro"

// Crear jugador en el centro
Genera un "jugador", en "Centro"

// Mover en círculo
para angulo en 0 hasta 360:
    radianes = angulo * 3.14159 / 180
    dx = redondear(coseno(radianes) * 5)
    dy = redondear(seno(radianes) * 5)
    // El movimiento se acumula

di: "¡Figura completa!"
```

---

## Referencia rápida

### Comandos del lenguaje

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `di:` | Imprime en consola | `di: "Hola"` |
| `=` | Asigna variable | `x = 10` |
| `si:` / `si no:` / `fin` | Condicional | `si x > 5:` ... `fin` |
| `mientras:` / `fin` | Bucle while | `mientras x < 10:` ... `fin` |
| `repetir N veces:` / `fin` | Bucle for fijo | `repetir 5 veces:` ... `fin` |
| `para i en A hasta B:` / `fin` | Bucle for | `para i en 1 hasta 10:` ... `fin` |
| `funcion nombre():` / `fin` | Define funcion | `funcion suma(a, b):` ... `fin` |
| `retorna` | Retorna valor | `retorna a + b` |
| `esperar N segundos` | Pausa | `esperar 2 segundos` |

### Motor de juegos

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `Resolucion... en WxH` | Tamaño pantalla | `Resolucion... en 800x600` |
| `Fondo color "X"` | Color fondo | `Fondo color "azul"` |
| `Genera un "tipo", en "pos"` | Crea entidad | `Genera un "jugador", en "100,200"` |
| `Al presionar tecla "X":` ... `fin` | Evento tecla | `Al presionar tecla "espacio":` ... `fin` |
| `Mueve "E" hacia "D" por N` | Mover entidad | `Mueve "jugador" hacia "arriba" por 10` |
| `Destruye "E"` | Eliminar entidad | `Destruye "moneda"` |
| `Puntuacion = N` | Puntuación | `Puntuacion = 0` |
| `Vidas = N` | Vidas | `Vidas = 3` |
| `FPS = N` | Velocidad juego | `FPS = 60` |
| `titulo = "X"` | Título ventana | `titulo = "Mi Juego"` |

### Funciones integradas

| Función | Descripción | Ejemplo |
|---------|-------------|---------|
| `entrada("msg")` | Lee del usuario | `nombre = entrada("Nombre: ")` |
| `convertir_numero(x)` | Texto → número | `n = convertir_numero("42")` |
| `convertir_texto(x)` | Número → texto | `t = convertir_texto(42)` |
| `aleatorio(min, max)` | Número aleatorio | `n = aleatorio(1, 10)` |
| `redondear(x)` | Redondea | `r = redondear(3.7)` → 4 |
| `absoluto(x)` | Valor absoluto | `a = absoluto(-5)` → 5 |
| `raiz(x)` | Raíz cuadrada | `r = raiz(16)` → 4 |
| `seno(x)` | Seno (radianes) | `s = seno(3.14159)` |
| `coseno(x)` | Coseno (radianes) | `c = coseno(0)` → 1 |
| `longitud(lista)` | Tamaño lista | `l = longitud([1,2,3])` → 3 |
| `tipo(x)` | Tipo de dato | `t = tipo(42)` → "int" |

---

## Solución de problemas

### Error: "python no se reconoce como comando"

**Windows:** Reinstala Python y marca "Add Python to PATH"

**Mac/Linux:** Usa `python3` en lugar de `python`

### Error: "No module named 'pygame'"

```bash
pip install pygame
# o
pip3 install pygame
```

### Error: "Archivo no encontrado"

Asegúrate de estar en el directorio correcto:
```bash
cd /ruta/del/proyecto
python interprete.py mi_juego.epp
```

### La ventana del juego no aparece

1. Verifica que pygame esté instalado: `pip list | grep pygame`
2. Intenta con una resolución más pequeña: `800x600` o `640x480`
3. Verifica que tu tarjeta gráfica soporte OpenGL

### El juego va lento

Reduce la resolución o los FPS:
```epp
Resolucion de la pantalla de prueba en 640x480
FPS = 30
```

### Error de codificación (caracteres extraños)

Asegúrate de guardar el archivo `.epp` con codificación **UTF-8**.

---

## Estructura de archivos recomendada

```
mi_proyecto_e++/
├── interprete.py        <- Intérprete de E++
├── mi_juego.epp         <- Tu código en E++
├── juegos/
│   ├── plataformas.epp
│   ├── snake.epp
│   └── puzzle.epp
└── assets/
    ├── imagenes/
    └── sonidos/
```

---

## Próximos pasos

1. **Experimenta** con el modo interactivo
2. **Modifica** `mi_juego.epp` para entender cómo funciona
3. **Crea** tu propio juego desde cero
4. **Consulta** la ayuda en el REPL escribiendo `ayuda`

---

Hecho con Python + Pygame
Lenguaje E++ (Español++) v1.0
