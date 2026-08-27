#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║  E++ (Español++) - Interprete Oficial v1.0                                   ║
║  Un lenguaje de programación en español para principiantes y game dev         ║
║  Creado con Python + Pygame                                                   ║
╚═══════════════════════════════════════════════════════════════════════════════╝

Uso: python interprete.py archivo.epp
     python interprete.py          (modo interactivo)
"""

import re
import sys
import os
import math
import random

# ═══════════════════════════════════════════════════════════════
# CONFIGURACIÓN DEL MOTOR GRÁFICO
# ═══════════════════════════════════════════════════════════════
try:
    import pygame
    from pygame.locals import *
    PYGAME_DISPONIBLE = True
except ImportError:
    PYGAME_DISPONIBLE = False

# ═══════════════════════════════════════════════════════════════
# COLORES SOPORTADOS POR E++
# ═══════════════════════════════════════════════════════════════
PALETA_COLORES = {
    "blanco": (255, 255, 255), "negro": (0, 0, 0),
    "rojo": (255, 0, 0), "verde": (0, 255, 0), "azul": (0, 0, 255),
    "amarillo": (255, 255, 0), "naranja": (255, 165, 0),
    "morado": (128, 0, 128), "rosa": (255, 192, 203),
    "cafe": (139, 69, 19), "gris": (128, 128, 128),
    "celeste": (135, 206, 235), "turquesa": (64, 224, 208),
    "dorado": (255, 215, 0), "plateado": (192, 192, 192),
    "marron": (139, 69, 19), "cyan": (0, 255, 255),
    "magenta": (255, 0, 255), "lima": (50, 205, 50),
    "salmon": (250, 128, 114), "indigo": (75, 0, 130),
    "violeta": (238, 130, 238), "coral": (255, 127, 80),
    "esmeralda": (80, 200, 120), "ruby": (224, 17, 95),
    "zafiro": (8, 37, 103), "ambar": (255, 191, 0),
    "perla": (234, 224, 200), "marfil": (255, 255, 240),
    "lavanda": (230, 230, 250), "menta": (189, 252, 201),
    "arena": (194, 178, 128), "piedra": (145, 142, 133),
    "noche": (15, 18, 27), "carbon": (51, 51, 51),
    "nieve": (255, 250, 250), "crema": (255, 253, 208),
}


# ═══════════════════════════════════════════════════════════════
# EXCEPCIONES PERSONALIZADAS
# ═══════════════════════════════════════════════════════════════
class ContinueIteration(Exception):
    pass


# ═══════════════════════════════════════════════════════════════
# CLASE ENTIDAD
# ═══════════════════════════════════════════════════════════════
class Entidad:
    """Representa cualquier objeto en el juego."""

    def __init__(self, nombre, tipo, x=0, y=0, z=0, **props):
        self.nombre = nombre
        self.tipo = tipo
        self.x = x
        self.y = y
        self.z = z
        self.ancho = props.get('ancho', 50)
        self.alto = props.get('alto', 50)
        self.color = props.get('color', 'blanco')
        self.visible = True
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.radio = props.get('radio', 0)
        self.texto = props.get('texto', '')
        self.tamano_texto = props.get('tamano_texto', 24)
        self.imagen = None
        self.rotacion = 0
        self.escala = 1.0
        self.opacidad = 255
        self.colisionable = True

    def obtener_rect(self):
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)

    def colisiona_con(self, otra):
        if not self.colisionable or not otra.colisionable:
            return False
        if self.radio > 0 and otra.radio > 0:
            dx = self.x - otra.x
            dy = self.y - otra.y
            distancia = math.sqrt(dx*dx + dy*dy)
            return distancia < (self.radio + otra.radio)
        return self.obtener_rect().colliderect(otra.obtener_rect())

    def centro(self):
        return (self.x + self.ancho//2, self.y + self.alto//2)

    def __repr__(self):
        return f"Entidad({self.nombre}, tipo={self.tipo}, x={self.x}, y={self.y})"


# ═══════════════════════════════════════════════════════════════
# MOTOR GRÁFICO E++
# ═══════════════════════════════════════════════════════════════
class MotorGraficoEpp:
    """Motor gráfico integrado de E++ para crear juegos 2D."""

    def __init__(self):
        self.pantalla = None
        self.ancho = 800
        self.alto = 600
        self.titulo = "Juego E++"
        self.fondo_color = (0, 0, 0)
        self.entidades = {}
        self.ejecutando = False
        self.reloj = None
        self.fps = 60
        self.teclas_presionadas = set()
        self.funciones_tecla = {}
        self.funciones_colision = {}
        self.funciones_actualizar = []
        self.funciones_dibujar = []
        self.puntuacion = 0
        self.vidas = 3
        self.delta_tiempo = 0
        self.fuentes = {}

    def iniciar(self):
        if not PYGAME_DISPONIBLE:
            print("[ERROR] Pygame no está instalado. No se puede iniciar el modo gráfico.")
            print("  Instálalo con: pip install pygame")
            return False
        pygame.init()
        pygame.font.init()
        self.reloj = pygame.time.Clock()
        self.pantalla = pygame.display.set_mode((self.ancho, self.alto))
        pygame.display.set_caption(self.titulo)
        self.ejecutando = True
        return True

    def cerrar(self):
        self.ejecutando = False
        if PYGAME_DISPONIBLE:
            pygame.quit()

    def cambiar_resolucion(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        if self.pantalla and PYGAME_DISPONIBLE:
            self.pantalla = pygame.display.set_mode((ancho, alto))

    def cambiar_titulo(self, titulo):
        self.titulo = titulo
        if PYGAME_DISPONIBLE:
            pygame.display.set_caption(titulo)

    def fondo(self, color_o_imagen):
        if isinstance(color_o_imagen, str) and color_o_imagen.lower() in PALETA_COLORES:
            self.fondo_color = PALETA_COLORES[color_o_imagen.lower()]
        elif isinstance(color_o_imagen, tuple) and len(color_o_imagen) == 3:
            self.fondo_color = color_o_imagen

    def crear_entidad(self, nombre, tipo, x, y, z=0, **props):
        entidad = Entidad(nombre, tipo, x, y, z, **props)
        self.entidades[nombre] = entidad
        return entidad

    def destruir_entidad(self, nombre):
        if nombre in self.entidades:
            del self.entidades[nombre]

    def obtener_entidad(self, nombre):
        return self.entidades.get(nombre)

    def mover_entidad(self, nombre, dx, dy):
        entidad = self.entidades.get(nombre)
        if entidad:
            entidad.x += dx
            entidad.y += dy

    def posicionar_entidad(self, nombre, x, y):
        entidad = self.entidades.get(nombre)
        if entidad:
            entidad.x = x
            entidad.y = y

    def registrar_tecla(self, tecla, funcion):
        tecla_lower = tecla.lower().strip('"').strip("'")
        if tecla_lower not in self.funciones_tecla:
            self.funciones_tecla[tecla_lower] = []
        self.funciones_tecla[tecla_lower].append(funcion)

    def registrar_colision(self, nombre1, nombre2, funcion):
        clave = (nombre1, nombre2)
        if clave not in self.funciones_colision:
            self.funciones_colision[clave] = []
        self.funciones_colision[clave].append(funcion)

    def registrar_actualizar(self, funcion):
        self.funciones_actualizar.append(funcion)

    def procesar_eventos(self):
        self.teclas_presionadas = set()
        if not PYGAME_DISPONIBLE:
            return
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                nombre_tecla = pygame.key.name(evento.key).lower()
                self.teclas_presionadas.add(nombre_tecla)
                # Mapeo de teclas comunes
                mapeo_teclas = {
                    'return': 'enter',
                    'space': 'espacio',
                    'escape': 'escape',
                    'up': 'arriba',
                    'down': 'abajo',
                    'left': 'izquierda',
                    'right': 'derecha',
                    'left ctrl': 'ctrl',
                    'right ctrl': 'ctrl',
                    'left shift': 'shift',
                    'right shift': 'shift',
                }
                tecla_mapeada = mapeo_teclas.get(nombre_tecla, nombre_tecla)
                if tecla_mapeada in self.funciones_tecla:
                    for funcion in self.funciones_tecla[tecla_mapeada]:
                        funcion()
                if nombre_tecla in self.funciones_tecla:
                    for funcion in self.funciones_tecla[nombre_tecla]:
                        funcion()

    def actualizar(self):
        for funcion in self.funciones_actualizar:
            funcion()

    def dibujar(self):
        if not self.pantalla or not PYGAME_DISPONIBLE:
            return
        self.pantalla.fill(self.fondo_color)
        entidades_ordenadas = sorted(self.entidades.values(), key=lambda e: e.z)
        for entidad in entidades_ordenadas:
            if not entidad.visible:
                continue
            color = entidad.color
            if isinstance(color, str) and color.lower() in PALETA_COLORES:
                color = PALETA_COLORES[color.lower()]
            elif not isinstance(color, tuple):
                color = (255, 255, 255)
            if entidad.radio > 0:
                pygame.draw.circle(self.pantalla, color,
                                   (int(entidad.x), int(entidad.y)),
                                   int(entidad.radio * entidad.escala))
            else:
                rect = pygame.Rect(
                    int(entidad.x), int(entidad.y),
                    int(entidad.ancho * entidad.escala),
                    int(entidad.alto * entidad.escala)
                )
                pygame.draw.rect(self.pantalla, color, rect)
                if entidad.tipo == "jugador":
                    pygame.draw.rect(self.pantalla, (255, 255, 255), rect, 2)
            if entidad.texto:
                tamano = entidad.tamano_texto
                if tamano not in self.fuentes:
                    self.fuentes[tamano] = pygame.font.SysFont('arial', tamano)
                fuente = self.fuentes[tamano]
                texto_surface = fuente.render(str(entidad.texto), True, (255, 255, 255))
                texto_rect = texto_surface.get_rect(center=entidad.centro())
                self.pantalla.blit(texto_surface, texto_rect)
        puntos_texto = None
        if 24 not in self.fuentes:
            self.fuentes[24] = pygame.font.SysFont('arial', 24)
        puntos_texto = self.fuentes[24].render(f"Puntos: {self.puntuacion}  Vidas: {self.vidas}", True, (255, 255, 255))
        self.pantalla.blit(puntos_texto, (10, 10))
        pygame.display.flip()

    def ciclo(self):
        if not PYGAME_DISPONIBLE:
            self.ejecutando = False
            return False
        self.delta_tiempo = self.reloj.tick(self.fps) / 1000.0
        self.procesar_eventos()
        self.actualizar()
        self.dibujar()
        return self.ejecutando

    def ejecutar(self):
        if not PYGAME_DISPONIBLE:
            return
        while self.ejecutando:
            if not self.ciclo():
                break
        self.cerrar()


# ═══════════════════════════════════════════════════════════════
# LEXER
# ═══════════════════════════════════════════════════════════════
class LexerEpp:
    """Convierte código E++ en tokens."""

    PATRONES = [
        # Comentarios (al inicio para tener prioridad)
        ('COMENTARIO', r'\/\/.*'),
        # Dimensiones tipo 800x600
        ('DIMENSION', r'\d+x\d+'),
        # Cadenas entre comillas dobles
        ('CADENA', r'"(?:[^"\\]|\\.)*"'),
        # Cadenas entre comillas simples
        ('CADENA_SIMPLE', r"'(?:[^'\\]|\\.)*'"),
        # Palabras clave - orden importa (más específicas primero)
        ('RESOLUCION', r'\bResolucion\b'),
        ('DI', r'\bdi\b'),
        ('GUARDA', r'\bguarda\b'),
        ('SI_NO', r'\bsi\s+no\b'),
        ('SI', r'\bsi\b'),
        ('MIENTRAS', r'\bmientras\b'),
        ('REPETIR', r'\brepetir\b'),
        ('VECES', r'\bveces\b'),
        ('PARA', r'\bpara\b'),
        ('EN', r'\ben\b'),
        ('HASTA', r'\bhasta\b'),
        ('DESDE', r'\bdesde\b'),
        ('FUNCION', r'\bfuncion\b'),
        ('RETORNA', r'\bretorna\b'),
        ('ROMPER', r'\bromper\b'),
        ('CONTINUAR', r'\bcontinuar\b'),
        ('FIN', r'\bfin\b'),
        ('ESPERAR', r'\besperar\b'),
        ('SEGUNDOS', r'\bsegundos\b'),
        ('MILISEGUNDOS', r'\bmilisegundos\b'),
        # Motor gráfico
        ('FONDO', r'\bFondo\b'),
        ('GENERA', r'\bGenera\b'),
        ('DESTRUYE', r'\bDestruye\b'),
        ('CREA', r'\bCrea\b'),
        ('MUEVE', r'\bMueve\b'),
        ('AL_PRESIONAR', r'\bAl\s+presionar\b'),
        ('TECLA', r'\btecla\b'),
        ('HACIA', r'\bhacia\b'),
        ('POR', r'\bpor\b'),
        ('UN', r'\bun\b'),
        ('EL', r'\bel\b'),
        ('LA', r'\bla\b'),
        ('DE', r'\bde\b'),
        ('PANTALLA', r'\bpantalla\b'),
        ('COLOR', r'\bcolor\b'),
        ('PRUEBA', r'\bprueba\b'),
        # Direcciones
        ('ARRIBA', r'\barriba\b'),
        ('ABAJO', r'\babajo\b'),
        ('IZQUIERDA', r'\bizquierda\b'),
        ('DERECHA', r'\bderecha\b'),
        ('CENTRO', r'\b[Cc]entro\b'),
        # Entidades
        ('TOCA', r'\btoca\b'),
        ('TEXTO', r'\btexto\b'),
        ('TITULO', r'\btitulo\b'),
        ('PUNTUACION', r'\bPuntuacion\b'),
        ('VIDAS', r'\bVidas\b'),
        ('FPS', r'\bFPS\b'),
        ('GRAVEDAD', r'\bGravedad\b'),
        # Booleanos
        ('BOOLEANO', r'\b(?:verdadero|falso)\b'),
        # Operadores de comparación (antes que operadores simples)
        ('IGUAL_IGUAL', r'=='),
        ('DIFERENTE', r'!='),
        ('MAYOR_IGUAL', r'>='),
        ('MENOR_IGUAL', r'<='),
        ('MAYOR', r'>'),
        ('MENOR', r'<'),
        # Operadores compuestos
        ('MAS_IGUAL', r'\+='),
        ('MENOS_IGUAL', r'-='),
        ('MULT_IGUAL', r'\*='),
        ('DIV_IGUAL', r'/='),
        # Operadores aritméticos
        ('MAS', r'\+'),
        ('MENOS', r'-'),
        ('POTENCIA', r'\*\*'),
        ('MULT', r'\*'),
        ('DIV', r'/'),
        ('MOD', r'%'),
        # Asignación
        ('ASIGNAR', r'='),
        # Lógicos
        ('Y_LOGICO', r'\by\b'),
        ('O_LOGICO', r'\bo\b'),
        ('NO_LOGICO', r'\bno\b'),
        # Números
        ('NUMERO', r'\d+(?:\.\d+)?'),
        # Identificadores
        ('IDENTIFICADOR', r'[a-zA-Z_áéíóúÁÉÍÓÚñÑüÜ][a-zA-Z0-9_áéíóúÁÉÍÓÚñÑüÜ]*'),
        # Símbolos
        ('DOS_PUNTOS', r':'),
        ('COMA', r','),
        ('PUNTO', r'\.'),
        ('PARENTESIS_ABRE', r'\('),
        ('PARENTESIS_CIERRA', r'\)'),
        ('CORCHETE_ABRE', r'\['),
        ('CORCHETE_CIERRA', r'\]'),
        ('LLAVE_ABRE', r'\{'),
        ('LLAVE_CIERRA', r'\}'),
        # Ignorar espacios y nueva línea
        ('ESPACIO', r'[ \t]+'),
        ('NUEVA_LINEA', r'\n'),
        ('IGNORAR', r'.'),
    ]

    def tokenizar(self, codigo):
        tokens = []
        linea_actual = 1
        pos = 0

        # Compilar regex en cada llamada para evitar problemas de pickling
        patrones_regex = '|'.join(f'(?P<{nombre}>{patron})' for nombre, patron in self.PATRONES)
        regex = re.compile(patrones_regex, re.UNICODE)

        for match in regex.finditer(codigo):
            tipo = match.lastgroup
            valor = match.group()

            if tipo == 'ESPACIO':
                continue
            elif tipo == 'NUEVA_LINEA':
                linea_actual += 1
                continue
            elif tipo == 'IGNORAR':
                print(f"[ADVERTENCIA LEXER] Caracter no reconocido en línea {linea_actual}: '{valor}'")
                continue
            elif tipo == 'COMENTARIO':
                # Los comentarios pueden contener nuevas líneas, contarlas
                linea_actual += valor.count('\n')
                continue

            tokens.append({
                'tipo': tipo,
                'valor': valor,
                'linea': linea_actual
            })

        tokens.append({'tipo': 'EOF', 'valor': '', 'linea': linea_actual})
        return tokens


# ═══════════════════════════════════════════════════════════════
# PARSER
# ═══════════════════════════════════════════════════════════════
class ParserEpp:
    """Analiza tokens y construye el AST."""

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.ast = []

    def token_actual(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return {'tipo': 'EOF', 'valor': '', 'linea': 0}

    def avanzar(self):
        token = self.token_actual()
        self.pos += 1
        return token

    def coincidir(self, tipo_esperado):
        token = self.token_actual()
        if token['tipo'] == tipo_esperado:
            return self.avanzar()
        return None

    def esperar(self, tipo_esperado, mensaje=None):
        token = self.coincidir(tipo_esperado)
        if token:
            return token
        actual = self.token_actual()
        msg = mensaje or f"Se esperaba {tipo_esperado} pero se encontró {actual['tipo']}('{actual['valor']}') en línea {actual['linea']}"
        raise SyntaxError(msg)

    def parsear(self):
        while self.token_actual()['tipo'] != 'EOF':
            nodo = self.parsear_instruccion()
            if nodo:
                self.ast.append(nodo)
        return self.ast

    def parsear_instruccion(self):
        token = self.token_actual()
        tipo = token['tipo']

        if tipo == 'DI':
            return self.parsear_di()
        elif tipo == 'IDENTIFICADOR':
            return self.parsear_asignacion_o_llamada()
        elif tipo == 'SI':
            return self.parsear_si()
        elif tipo == 'MIENTRAS':
            return self.parsear_mientras()
        elif tipo == 'REPETIR':
            return self.parsear_repetir()
        elif tipo == 'PARA':
            return self.parsear_para()
        elif tipo == 'FUNCION':
            return self.parsear_funcion()
        elif tipo == 'ROMPER':
            self.avanzar()
            return {'tipo': 'romper'}
        elif tipo == 'CONTINUAR':
            self.avanzar()
            return {'tipo': 'continuar'}
        elif tipo == 'RETORNA':
            return self.parsear_retorna()
        elif tipo == 'ESPERAR':
            return self.parsear_esperar()
        elif tipo == 'RESOLUCION':
            return self.parsear_resolucion()
        elif tipo == 'FONDO':
            return self.parsear_fondo()
        elif tipo == 'GENERA':
            return self.parsear_genera()
        elif tipo == 'AL_PRESIONAR':
            return self.parsear_al_presionar()
        elif tipo == 'MUEVE':
            return self.parsear_mueve()
        elif tipo == 'DESTRUYE':
            return self.parsear_destruye()
        elif tipo == 'CREA':
            return self.parsear_crea()
        elif tipo == 'PUNTUACION':
            return self.parsear_puntuacion()
        elif tipo == 'VIDAS':
            return self.parsear_vidas()
        elif tipo == 'FPS':
            return self.parsear_fps_cmd()
        elif tipo == 'TITULO':
            return self.parsear_titulo_cmd()
        elif tipo == 'GRAVEDAD':
            return self.parsear_gravedad()
        elif tipo == 'NUEVA_LINEA':
            self.avanzar()
            return None
        else:
            print(f"[ADVERTENCIA] Instrucción no reconocida en línea {token['linea']}: {token['tipo']} = '{token['valor']}'")
            self.avanzar()
            return None

    def parsear_bloque(self):
        """Parsea un bloque después de ':', termina con 'fin' o EOF."""
        self.esperar('DOS_PUNTOS')
        bloque = []
        while True:
            token = self.token_actual()
            if token['tipo'] in ('EOF', 'FIN', 'SI_NO'):
                if token['tipo'] == 'FIN':
                    self.avanzar()  # consumir 'fin'
                break
            if token['tipo'] == 'NUEVA_LINEA':
                self.avanzar()
                continue
            nodo = self.parsear_instruccion()
            if nodo:
                bloque.append(nodo)
            else:
                if self.token_actual()['tipo'] in ('FIN', 'SI_NO', 'EOF'):
                    break
                self.avanzar()
        return bloque

    def parsear_expresion(self):
        return self.parsear_or()

    def parsear_or(self):
        izq = self.parsear_and()
        while self.coincidir('O_LOGICO'):
            der = self.parsear_and()
            izq = {'tipo': 'op_binaria', 'op': 'o', 'izq': izq, 'der': der}
        return izq

    def parsear_and(self):
        izq = self.parsear_igualdad()
        while self.coincidir('Y_LOGICO'):
            der = self.parsear_igualdad()
            izq = {'tipo': 'op_binaria', 'op': 'y', 'izq': izq, 'der': der}
        return izq

    def parsear_igualdad(self):
        izq = self.parsear_comparacion()
        while True:
            if self.coincidir('IGUAL_IGUAL'):
                der = self.parsear_comparacion()
                izq = {'tipo': 'op_binaria', 'op': '==', 'izq': izq, 'der': der}
            elif self.coincidir('DIFERENTE'):
                der = self.parsear_comparacion()
                izq = {'tipo': 'op_binaria', 'op': '!=', 'izq': izq, 'der': der}
            else:
                break
        return izq

    def parsear_comparacion(self):
        izq = self.parsear_suma()
        while True:
            if self.coincidir('MAYOR'):
                der = self.parsear_suma()
                izq = {'tipo': 'op_binaria', 'op': '>', 'izq': izq, 'der': der}
            elif self.coincidir('MENOR'):
                der = self.parsear_suma()
                izq = {'tipo': 'op_binaria', 'op': '<', 'izq': izq, 'der': der}
            elif self.coincidir('MAYOR_IGUAL'):
                der = self.parsear_suma()
                izq = {'tipo': 'op_binaria', 'op': '>=', 'izq': izq, 'der': der}
            elif self.coincidir('MENOR_IGUAL'):
                der = self.parsear_suma()
                izq = {'tipo': 'op_binaria', 'op': '<=', 'izq': izq, 'der': der}
            else:
                break
        return izq

    def parsear_suma(self):
        izq = self.parsear_multiplicacion()
        while True:
            if self.coincidir('MAS'):
                der = self.parsear_multiplicacion()
                izq = {'tipo': 'op_binaria', 'op': '+', 'izq': izq, 'der': der}
            elif self.coincidir('MENOS'):
                der = self.parsear_multiplicacion()
                izq = {'tipo': 'op_binaria', 'op': '-', 'izq': izq, 'der': der}
            else:
                break
        return izq

    def parsear_multiplicacion(self):
        izq = self.parsear_unario()
        while True:
            if self.coincidir('MULT'):
                der = self.parsear_unario()
                izq = {'tipo': 'op_binaria', 'op': '*', 'izq': izq, 'der': der}
            elif self.coincidir('DIV'):
                der = self.parsear_unario()
                izq = {'tipo': 'op_binaria', 'op': '/', 'izq': izq, 'der': der}
            elif self.coincidir('MOD'):
                der = self.parsear_unario()
                izq = {'tipo': 'op_binaria', 'op': '%', 'izq': izq, 'der': der}
            else:
                break
        return izq

    def parsear_unario(self):
        if self.coincidir('MENOS'):
            operando = self.parsear_unario()
            return {'tipo': 'op_unaria', 'op': '-', 'operando': operando}
        if self.coincidir('NO_LOGICO'):
            operando = self.parsear_unario()
            return {'tipo': 'op_unaria', 'op': 'no', 'operando': operando}
        return self.parsear_primario()

    def parsear_primario(self):
        token = self.token_actual()

        if self.coincidir('NUMERO'):
            valor = token['valor']
            if '.' in valor:
                return {'tipo': 'numero', 'valor': float(valor)}
            return {'tipo': 'numero', 'valor': int(valor)}

        if self.coincidir('CADENA') or self.coincidir('CADENA_SIMPLE'):
            valor = token['valor'][1:-1]
            valor = valor.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"').replace("\\'", "'")
            return {'tipo': 'cadena', 'valor': valor}

        if self.coincidir('BOOLEANO'):
            return {'tipo': 'booleano', 'valor': token['valor'].lower() == 'verdadero'}

        if self.coincidir('DIMENSION'):
            return {'tipo': 'dimension', 'valor': token['valor']}

        if self.coincidir('CENTRO'):
            return {'tipo': 'cadena', 'valor': 'Centro'}

        if self.coincidir('PARENTESIS_ABRE'):
            expr = self.parsear_expresion()
            self.esperar('PARENTESIS_CIERRA')
            return expr

        if token['tipo'] == 'IDENTIFICADOR':
            return self.parsear_identificador()

        print(f"[ERROR] Expresión no válida en línea {token['linea']}: '{token['valor']}'")
        self.avanzar()
        return {'tipo': 'nulo', 'valor': None}

    def parsear_identificador(self):
        nombre = self.avanzar()['valor']
        if self.coincidir('CORCHETE_ABRE'):
            indice = self.parsear_expresion()
            self.esperar('CORCHETE_CIERRA')
            return {'tipo': 'acceso_lista', 'nombre': nombre, 'indice': indice}
        if self.token_actual()['tipo'] == 'PARENTESIS_ABRE':
            return self.parsear_llamada_funcion(nombre)
        return {'tipo': 'variable', 'nombre': nombre}

    def parsear_llamada_funcion(self, nombre):
        self.esperar('PARENTESIS_ABRE')
        argumentos = []
        if self.token_actual()['tipo'] != 'PARENTESIS_CIERRA':
            argumentos.append(self.parsear_expresion())
            while self.coincidir('COMA'):
                argumentos.append(self.parsear_expresion())
        self.esperar('PARENTESIS_CIERRA')
        return {'tipo': 'llamada', 'nombre': nombre, 'argumentos': argumentos}

    # ─── Instrucciones ───

    def parsear_di(self):
        self.avanzar()  # consumir DI
        self.coincidir('DOS_PUNTOS')  # consumir ':' opcional (di: o di :)
        expr = self.parsear_expresion()
        return {'tipo': 'di', 'expresion': expr}

    def parsear_asignacion_o_llamada(self):
        nombre_token = self.avanzar()
        nombre = nombre_token['valor']
        operadores = {'MAS_IGUAL': '+=', 'MENOS_IGUAL': '-=', 'MULT_IGUAL': '*=', 'DIV_IGUAL': '/='}
        for tipo_op, op in operadores.items():
            if self.coincidir(tipo_op):
                expr = self.parsear_expresion()
                return {'tipo': 'asignacion_compuesta', 'nombre': nombre, 'op': op, 'expresion': expr}
        if self.coincidir('ASIGNAR'):
            expr = self.parsear_expresion()
            return {'tipo': 'asignacion', 'nombre': nombre, 'expresion': expr}
        if self.token_actual()['tipo'] == 'PARENTESIS_ABRE':
            return self.parsear_llamada_funcion(nombre)
        return {'tipo': 'variable', 'nombre': nombre}

    def parsear_si(self):
        self.avanzar()
        condicion = self.parsear_expresion()
        cuerpo = self.parsear_bloque()
        rama_si_no = []
        if self.coincidir('SI_NO'):
            rama_si_no = self.parsear_bloque()
        return {'tipo': 'si', 'condicion': condicion, 'cuerpo': cuerpo, 'si_no': rama_si_no}

    def parsear_mientras(self):
        self.avanzar()
        condicion = self.parsear_expresion()
        cuerpo = self.parsear_bloque()
        return {'tipo': 'mientras', 'condicion': condicion, 'cuerpo': cuerpo}

    def parsear_repetir(self):
        self.avanzar()
        veces = self.parsear_expresion()
        self.coincidir('VECES')
        self.esperar('DOS_PUNTOS')
        cuerpo = []
        while True:
            token = self.token_actual()
            if token['tipo'] in ('EOF', 'FIN'):
                if token['tipo'] == 'FIN':
                    self.avanzar()
                break
            if token['tipo'] == 'NUEVA_LINEA':
                self.avanzar()
                continue
            nodo = self.parsear_instruccion()
            if nodo:
                cuerpo.append(nodo)
            else:
                break
        return {'tipo': 'repetir', 'veces': veces, 'cuerpo': cuerpo}

    def parsear_para(self):
        self.avanzar()
        variable = self.esperar('IDENTIFICADOR')
        self.esperar('EN')
        inicio = self.parsear_expresion()
        self.esperar('HASTA')
        fin = self.parsear_expresion()
        self.esperar('DOS_PUNTOS')
        cuerpo = []
        while True:
            token = self.token_actual()
            if token['tipo'] in ('EOF', 'FIN'):
                if token['tipo'] == 'FIN':
                    self.avanzar()
                break
            if token['tipo'] == 'NUEVA_LINEA':
                self.avanzar()
                continue
            nodo = self.parsear_instruccion()
            if nodo:
                cuerpo.append(nodo)
            else:
                break
        return {'tipo': 'para', 'variable': variable['valor'], 'inicio': inicio, 'fin': fin, 'cuerpo': cuerpo}

    def parsear_funcion(self):
        self.avanzar()
        nombre = self.esperar('IDENTIFICADOR')
        self.esperar('PARENTESIS_ABRE')
        parametros = []
        if self.token_actual()['tipo'] == 'IDENTIFICADOR':
            parametros.append(self.avanzar()['valor'])
            while self.coincidir('COMA'):
                parametros.append(self.esperar('IDENTIFICADOR')['valor'])
        self.esperar('PARENTESIS_CIERRA')
        self.esperar('DOS_PUNTOS')
        cuerpo = []
        while True:
            token = self.token_actual()
            if token['tipo'] in ('EOF', 'FIN', 'FUNCION'):
                if token['tipo'] == 'FIN':
                    self.avanzar()
                break
            if token['tipo'] == 'NUEVA_LINEA':
                self.avanzar()
                continue
            nodo = self.parsear_instruccion()
            if nodo:
                cuerpo.append(nodo)
            else:
                break
        return {'tipo': 'funcion_def', 'nombre': nombre['valor'], 'parametros': parametros, 'cuerpo': cuerpo}

    def parsear_retorna(self):
        self.avanzar()
        expr = self.parsear_expresion()
        return {'tipo': 'retorna', 'expresion': expr}

    def parsear_esperar(self):
        self.avanzar()
        tiempo = self.parsear_expresion()
        unidad = 'segundos'
        if self.coincidir('SEGUNDOS'):
            unidad = 'segundos'
        elif self.coincidir('MILISEGUNDOS'):
            unidad = 'milisegundos'
        return {'tipo': 'esperar', 'tiempo': tiempo, 'unidad': unidad}

    # ─── Motor Gráfico ───

    def parsear_resolucion(self):
        """Resolucion de la pantalla de prueba en 800x600"""
        self.avanzar()  # RESOLUCION
        # Consumir: de la pantalla [de prueba] en
        while self.token_actual()['tipo'] in ('DE', 'LA', 'EL', 'UN', 'PANTALLA', 'PRUEBA', 'EN'):
            self.avanzar()
        dim_token = self.token_actual()
        if dim_token['tipo'] == 'DIMENSION':
            self.avanzar()
            partes = dim_token['valor'].lower().split('x')
            return {'tipo': 'resolucion', 'ancho': int(partes[0]), 'alto': int(partes[1])}
        elif dim_token['tipo'] == 'NUMERO':
            self.avanzar()
            return {'tipo': 'resolucion', 'ancho': int(dim_token['valor']), 'alto': 600}
        return {'tipo': 'resolucion', 'ancho': 800, 'alto': 600}

    def parsear_fondo(self):
        """Fondo color "azul" """
        self.avanzar()  # FONDO
        self.coincidir('COLOR')
        color = self.parsear_expresion()
        return {'tipo': 'fondo', 'color': color}

    def parsear_genera(self):
        """Genera un "bloque", en "100, 200" """
        self.avanzar()  # GENERA
        self.coincidir('UN')  # opcional
        tipo_entidad = self.parsear_expresion()
        self.coincidir('COMA')  # coma opcional
        self.esperar('EN')
        posicion = self.parsear_expresion()
        return {'tipo': 'genera', 'entidad': tipo_entidad, 'posicion': posicion}

    def parsear_al_presionar(self):
        """Al presionar tecla "derecha": Mueve ... fin"""
        self.avanzar()  # AL_PRESIONAR
        self.coincidir('TECLA')  # opcional
        tecla = self.parsear_expresion()
        self.esperar('DOS_PUNTOS')
        acciones = []
        while True:
            token = self.token_actual()
            if token['tipo'] in ('EOF', 'FIN', 'AL_PRESIONAR', 'RESOLUCION', 'FUNCION'):
                if token['tipo'] == 'FIN':
                    self.avanzar()
                break
            if token['tipo'] == 'NUEVA_LINEA':
                self.avanzar()
                continue
            if token['tipo'] == 'MUEVE':
                acciones.append(self.parsear_mueve())
            elif token['tipo'] == 'DI':
                acciones.append(self.parsear_di())
            elif token['tipo'] == 'DESTRUYE':
                acciones.append(self.parsear_destruye())
            elif token['tipo'] == 'SI':
                acciones.append(self.parsear_si())
            else:
                nodo = self.parsear_instruccion()
                if nodo:
                    acciones.append(nodo)
                else:
                    break
        return {'tipo': 'al_presionar', 'tecla': tecla, 'acciones': acciones}

    def parsear_mueve(self):
        """Mueve "jugador" hacia "arriba" por 10"""
        self.avanzar()  # MUEVE
        entidad = self.parsear_expresion()
        self.esperar('HACIA')
        direccion = self.parsear_expresion()
        self.esperar('POR')
        cantidad = self.parsear_expresion()
        return {'tipo': 'mueve', 'entidad': entidad, 'direccion': direccion, 'cantidad': cantidad}

    def parsear_destruye(self):
        """Destruye "entidad" """
        self.avanzar()
        entidad = self.parsear_expresion()
        return {'tipo': 'destruye', 'entidad': entidad}

    def parsear_crea(self):
        """Crea texto "Hola" en 100, 200"""
        self.avanzar()
        tipo_obj = self.avanzar()['valor'] if self.token_actual()['tipo'] == 'IDENTIFICADOR' else 'texto'
        contenido = self.parsear_expresion()
        self.coincidir('EN')
        x = self.parsear_expresion()
        self.coincidir('COMA')
        y = self.parsear_expresion()
        return {'tipo': 'crea', 'tipo_obj': tipo_obj, 'contenido': contenido, 'x': x, 'y': y}

    def parsear_puntuacion(self):
        self.avanzar()
        self.esperar('ASIGNAR')
        valor = self.parsear_expresion()
        return {'tipo': 'puntuacion', 'valor': valor}

    def parsear_vidas(self):
        self.avanzar()
        self.esperar('ASIGNAR')
        valor = self.parsear_expresion()
        return {'tipo': 'vidas', 'valor': valor}

    def parsear_fps_cmd(self):
        self.avanzar()
        self.esperar('ASIGNAR')
        valor = self.parsear_expresion()
        return {'tipo': 'fps_cmd', 'valor': valor}

    def parsear_titulo_cmd(self):
        self.avanzar()
        self.esperar('ASIGNAR')
        valor = self.parsear_expresion()
        return {'tipo': 'titulo', 'valor': valor}

    def parsear_gravedad(self):
        self.avanzar()
        self.esperar('ASIGNAR')
        valor = self.parsear_expresion()
        return {'tipo': 'gravedad', 'valor': valor}


# ═══════════════════════════════════════════════════════════════
# INTERPRETE
# ═══════════════════════════════════════════════════════════════
class InterpreteEpp:
    """Ejecuta el AST."""

    def __init__(self):
        self.variables = {}
        self.funciones = {}
        self.motor = MotorGraficoEpp()
        self.retornando = False
        self.valor_retorno = None
        self.entorno_actual = self.variables
        self.pila_entornos = []
        self.gravedad = 0

    def evaluar(self, nodo):
        if nodo is None:
            return None

        tipo = nodo.get('tipo')

        if tipo == 'numero':
            return nodo['valor']
        if tipo == 'cadena':
            return nodo['valor']
        if tipo == 'dimension':
            return nodo['valor']
        if tipo == 'booleano':
            return nodo['valor']
        if tipo == 'nulo':
            return None
        if tipo == 'variable':
            nombre = nodo['nombre']
            if nombre in self.entorno_actual:
                return self.entorno_actual[nombre]
            if nombre in self.variables:
                return self.variables[nombre]
            print(f"[ERROR] Variable no definida: '{nombre}'")
            return None
        if tipo == 'acceso_lista':
            nombre = nodo['nombre']
            indice = self.evaluar(nodo['indice'])
            lista = self.entorno_actual.get(nombre) or self.variables.get(nombre)
            if isinstance(lista, (list, tuple, str)):
                try:
                    return lista[indice]
                except IndexError:
                    print(f"[ERROR] Índice fuera de rango: {indice}")
                    return None
            print(f"[ERROR] '{nombre}' no es una lista")
            return None
        if tipo == 'llamada':
            return self.ejecutar_llamada(nodo)
        if tipo == 'op_binaria':
            izq = self.evaluar(nodo['izq'])
            der = self.evaluar(nodo['der'])
            op = nodo['op']
            if izq is None or der is None:
                return None
            if op == '+':
                if isinstance(izq, str) or isinstance(der, str):
                    return str(izq) + str(der)
                return izq + der
            elif op == '-': return izq - der
            elif op == '*': return izq * der
            elif op == '/':
                if der == 0:
                    print("[ERROR] División por cero")
                    return 0
                return izq / der
            elif op == '%': return izq % der
            elif op == '**': return izq ** der
            elif op == '==': return izq == der
            elif op == '!=': return izq != der
            elif op == '>': return izq > der
            elif op == '<': return izq < der
            elif op == '>=': return izq >= der
            elif op == '<=': return izq <= der
            elif op == 'y': return bool(izq) and bool(der)
            elif op == 'o': return bool(izq) or bool(der)
        if tipo == 'op_unaria':
            operando = self.evaluar(nodo['operando'])
            if nodo['op'] == '-':
                return -operando
            elif nodo['op'] == 'no':
                return not operando
        return None

    def ejecutar_llamada(self, nodo):
        nombre = nodo['nombre']
        argumentos = [self.evaluar(arg) for arg in nodo['argumentos']]

        funciones_builtin = {
            'di': lambda args: print(args[0]) if args else None,
            'tipo': lambda args: type(args[0]).__name__ if args else None,
            'longitud': lambda args: len(args[0]) if args else 0,
            'aleatorio': lambda args: random.randint(args[0], args[1]) if len(args) >= 2 else random.randint(0, args[0]) if args else random.random(),
            'redondear': lambda args: round(args[0]) if args else 0,
            'absoluto': lambda args: abs(args[0]) if args else 0,
            'raiz': lambda args: math.sqrt(args[0]) if args else 0,
            'seno': lambda args: math.sin(args[0]) if args else 0,
            'coseno': lambda args: math.cos(args[0]) if args else 0,
            'entrada': lambda args: input(args[0]) if args else input(),
            'convertir_numero': lambda args: float(args[0]) if args and '.' in str(args[0]) else int(args[0]) if args else 0,
            'convertir_texto': lambda args: str(args[0]) if args else "",
            'mayusculas': lambda args: str(args[0]).upper() if args else "",
            'minusculas': lambda args: str(args[0]).lower() if args else "",
        }

        if nombre in funciones_builtin:
            return funciones_builtin[nombre](argumentos)

        if nombre in self.funciones:
            funcion = self.funciones[nombre]
            entorno_local = {}
            for i, param in enumerate(funcion['parametros']):
                entorno_local[param] = argumentos[i] if i < len(argumentos) else None
            self.pila_entornos.append(self.entorno_actual)
            self.entorno_actual = entorno_local
            self.retornando = False
            self.valor_retorno = None
            for instruccion in funcion['cuerpo']:
                self.ejecutar(instruccion)
                if self.retornando:
                    break
            self.entorno_actual = self.pila_entornos.pop()
            resultado = self.valor_retorno
            self.retornando = False
            self.valor_retorno = None
            return resultado

        print(f"[ERROR] Función no definida: '{nombre}'")
        return None

    def ejecutar(self, nodo):
        if nodo is None:
            return
        if self.retornando:
            return

        tipo = nodo.get('tipo')

        if tipo == 'di':
            valor = self.evaluar(nodo['expresion'])
            print(valor)

        elif tipo == 'asignacion':
            nombre = nodo['nombre']
            valor = self.evaluar(nodo['expresion'])
            self.entorno_actual[nombre] = valor
            self.variables[nombre] = valor

        elif tipo == 'asignacion_compuesta':
            nombre = nodo['nombre']
            valor_actual = self.entorno_actual.get(nombre, 0) or self.variables.get(nombre, 0)
            valor_nuevo = self.evaluar(nodo['expresion'])
            op = nodo['op']
            if op == '+=': resultado = valor_actual + valor_nuevo
            elif op == '-=': resultado = valor_actual - valor_nuevo
            elif op == '*=': resultado = valor_actual * valor_nuevo
            elif op == '/=': resultado = valor_actual / valor_nuevo if valor_nuevo != 0 else 0
            else: resultado = valor_nuevo
            self.entorno_actual[nombre] = resultado
            self.variables[nombre] = resultado

        elif tipo == 'si':
            try:
                condicion = self.evaluar(nodo['condicion'])
                if condicion:
                    for instruccion in nodo['cuerpo']:
                        self.ejecutar(instruccion)
                        if self.retornando:
                            break
                else:
                    for instruccion in nodo['si_no']:
                        self.ejecutar(instruccion)
                        if self.retornando:
                            break
            except Exception as e:
                print(f"[ERROR en condicional]: {e}")

        elif tipo == 'mientras':
            max_iter = 10000
            iteraciones = 0
            while iteraciones < max_iter:
                try:
                    cond = self.evaluar(nodo['condicion'])
                    if not cond:
                        break
                except:
                    break
                for instruccion in nodo['cuerpo']:
                    try:
                        self.ejecutar(instruccion)
                    except StopIteration:
                        iteraciones = max_iter
                        break
                    except ContinueIteration:
                        break
                    if self.retornando:
                        return
                iteraciones += 1
            if iteraciones >= max_iter:
                print("[ADVERTENCIA] Bucle detenido por límite de seguridad")

        elif tipo == 'repetir':
            veces = self.evaluar(nodo['veces']) or 1
            for _ in range(int(veces)):
                for instruccion in nodo['cuerpo']:
                    try:
                        self.ejecutar(instruccion)
                    except StopIteration:
                        return
                    except ContinueIteration:
                        break
                    if self.retornando:
                        return

        elif tipo == 'para':
            inicio = self.evaluar(nodo['inicio'])
            fin = self.evaluar(nodo['fin'])
            variable = nodo['variable']
            for i in range(int(inicio), int(fin) + 1):
                self.entorno_actual[variable] = i
                self.variables[variable] = i
                for instruccion in nodo['cuerpo']:
                    try:
                        self.ejecutar(instruccion)
                    except StopIteration:
                        return
                    except ContinueIteration:
                        break
                    if self.retornando:
                        return

        elif tipo == 'funcion_def':
            self.funciones[nodo['nombre']] = nodo

        elif tipo == 'retorna':
            self.valor_retorno = self.evaluar(nodo['expresion'])
            self.retornando = True

        elif tipo == 'romper':
            raise StopIteration

        elif tipo == 'continuar':
            raise ContinueIteration

        elif tipo == 'esperar':
            tiempo = self.evaluar(nodo['tiempo'])
            import time
            if nodo.get('unidad') == 'milisegundos':
                time.sleep(tiempo / 1000)
            else:
                time.sleep(tiempo)

        elif tipo == 'llamada':
            self.ejecutar_llamada(nodo)

        # Motor Gráfico
        elif tipo == 'resolucion':
            ancho = nodo.get('ancho', 800)
            alto = nodo.get('alto', 600)
            self.motor.cambiar_resolucion(ancho, alto)
            if not self.motor.pantalla:
                self.motor.iniciar()

        elif tipo == 'fondo':
            color = self.evaluar(nodo['color'])
            self.motor.fondo(color)

        elif tipo == 'genera':
            tipo_entidad = str(self.evaluar(nodo['entidad'])).lower().strip('"').strip("'")
            posicion = str(self.evaluar(nodo['posicion']))
            x, y = 100, 100
            if 'centro' in posicion.lower():
                x = self.motor.ancho // 2 - 25
                y = self.motor.alto // 2 - 25
            else:
                partes = posicion.replace(' ', '').split(',')
                if len(partes) >= 2:
                    try:
                        x = int(float(partes[0]))
                        y = int(float(partes[1]))
                    except:
                        pass
            props = {'ancho': 50, 'alto': 50}
            if tipo_entidad == 'jugador':
                props = {'color': 'verde', 'ancho': 50, 'alto': 50}
            elif tipo_entidad == 'bloque':
                props = {'color': 'rojo', 'ancho': 40, 'alto': 40}
            elif tipo_entidad == 'moneda':
                props = {'color': 'amarillo', 'radio': 15, 'ancho': 30, 'alto': 30}
            elif tipo_entidad == 'enemigo':
                props = {'color': 'naranja', 'ancho': 45, 'alto': 45}
            elif tipo_entidad == 'meta':
                props = {'color': 'dorado', 'ancho': 60, 'alto': 60}
            elif tipo_entidad == 'proyectil':
                props = {'color': 'blanco', 'radio': 5, 'ancho': 10, 'alto': 10}
            self.motor.crear_entidad(tipo_entidad, tipo_entidad, x, y, 0, **props)

        elif tipo == 'mueve':
            entidad = str(self.evaluar(nodo['entidad'])).strip('"').strip("'")
            direccion = str(self.evaluar(nodo['direccion'])).lower().strip('"').strip("'")
            cantidad = self.evaluar(nodo['cantidad']) or 10
            dx, dy = 0, 0
            if 'arriba' in direccion: dy = -cantidad
            elif 'abajo' in direccion: dy = cantidad
            elif 'izquierda' in direccion: dx = -cantidad
            elif 'derecha' in direccion: dx = cantidad
            self.motor.mover_entidad(entidad, dx, dy)

        elif tipo == 'destruye':
            entidad = str(self.evaluar(nodo['entidad'])).strip('"').strip("'")
            self.motor.destruir_entidad(entidad)

        elif tipo == 'al_presionar':
            tecla = str(self.evaluar(nodo['tecla'])).lower().strip('"').strip("'")
            acciones = nodo['acciones']
            def crear_funcion(accs, interp):
                def funcion():
                    for acc in accs:
                        interp.ejecutar(acc)
                return funcion
            self.motor.registrar_tecla(tecla, crear_funcion(acciones, self))

        elif tipo == 'crea':
            tipo_obj = nodo.get('tipo_obj', 'texto')
            contenido = self.evaluar(nodo['contenido'])
            x = self.evaluar(nodo['x']) or 100
            y = self.evaluar(nodo['y']) or 100
            if tipo_obj.lower() == 'texto':
                self.motor.crear_entidad(f"texto_{contenido}", "texto", x, y,
                                         texto=contenido, tamano_texto=24, ancho=200, alto=30, colisionable=False)

        elif tipo == 'puntuacion':
            self.motor.puntuacion = self.evaluar(nodo['valor']) or 0

        elif tipo == 'vidas':
            self.motor.vidas = self.evaluar(nodo['valor']) or 3

        elif tipo == 'fps_cmd':
            self.motor.fps = self.evaluar(nodo['valor']) or 60

        elif tipo == 'titulo':
            titulo = self.evaluar(nodo['valor'])
            self.motor.cambiar_titulo(str(titulo))

        elif tipo == 'gravedad':
            self.gravedad = self.evaluar(nodo['valor']) or 0

    def ejecutar_ast(self, ast):
        for nodo in ast:
            self.ejecutar(nodo)


# ═══════════════════════════════════════════════════════════════
# FUNCIÓN PRINCIPAL
# ═══════════════════════════════════════════════════════════════
def ejecutar_archivo(ruta_archivo):
    if not os.path.exists(ruta_archivo):
        print(f"[ERROR] Archivo no encontrado: {ruta_archivo}")
        return

    print(f"\n{'='*60}")
    print(f"  E++ (Español++) - Ejecutando: {ruta_archivo}")
    print(f"{'='*60}\n")

    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        codigo = f.read()

    print("--- CÓDIGO FUENTE ---")
    for i, linea in enumerate(codigo.split('\n'), 1):
        if linea.strip():
            print(f"  {i:3d} | {linea}")
    print("-" * 40)
    print()

    print("[1/3] Analizando léxico...")
    lexer = LexerEpp()
    tokens = lexer.tokenizar(codigo)
    print(f"      {len([t for t in tokens if t['tipo'] != 'EOF'])} tokens encontrados")

    print("[2/3] Analizando sintaxis...")
    parser = ParserEpp(tokens)
    try:
        ast = parser.parsear()
    except SyntaxError as e:
        print(f"[ERROR DE SINTAXIS] {e}")
        return
    print(f"      {len(ast)} instrucciones parseadas")

    print("[3/3] Ejecutando código...")
    print()
    print("=" * 40)
    print("SALIDA DEL PROGRAMA:")
    print("=" * 40)

    interprete = InterpreteEpp()
    interprete.ejecutar_ast(ast)

    print("=" * 40)

    if interprete.motor.pantalla:
        print("\n[*] Iniciando motor gráfico...")
        print("     Presiona ESC o cierra la ventana para salir\n")
        interprete.motor.ejecutar()

    print(f"\n{'='*60}")
    print("  Programa finalizado correctamente")
    print(f"{'='*60}\n")


def modo_interactivo():
    print("\n" + "="*60)
    print("  E++ (Español++) - Modo Interactivo v1.0")
    print("  Escribe 'salir' para terminar, 'ayuda' para comandos")
    print("="*60 + "\n")

    interprete = InterpreteEpp()
    lexer = LexerEpp()

    while True:
        try:
            linea = input("E++ > ")
            if linea.lower() in ('salir', 'exit', 'quit'):
                print("Hasta luego!")
                break
            if linea.lower() == 'ayuda':
                mostrar_ayuda()
                continue
            if linea.lower() == 'limpiar':
                os.system('cls' if os.name == 'nt' else 'clear')
                continue
            if not linea.strip():
                continue

            tokens = lexer.tokenizar(linea)
            parser = ParserEpp(tokens)
            ast = parser.parsear()
            for nodo in ast:
                interprete.ejecutar(nodo)

        except KeyboardInterrupt:
            print("\nHasta luego!")
            break
        except Exception as e:
            print(f"[ERROR] {e}")


def mostrar_ayuda():
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                    AYUDA DE E++ v1.0                           ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║  COMANDOS BASICOS:                                            ║
    ║    di: "mensaje"          - Imprime en consola                ║
    ║    variable = valor       - Crea o asigna variable            ║
    ║    si condicion:          - Condicional                       ║
    ║    si no:                                                     ║
    ║    repetir N veces:       - Repite N veces                    ║
    ║    mientras condicion:    - Bucle while                       ║
    ║    para i en 1 hasta 10:  - Bucle for                         ║
    ║    funcion nombre():      - Define funcion                    ║
    ║    retorna valor          - Retorna valor                     ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║  MOTOR GRAFICO:                                               ║
    ║    Resolucion... en 800x600                                   ║
    ║    Fondo color "azul"                                         ║
    ║    Genera un "jugador", en "Centro"                           ║
    ║    Al presionar tecla "derecha":                              ║
    ║      Mueve "jugador" hacia "derecha" por 5                    ║
    ║    Destruye "bloque"                                          ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║  FUNCIONES: entrada(), aleatorio(), redondear(), raiz()       ║
    ║  OPERADORES: +  -  *  /  %  ==  !=  >  <  >=  <=  y  o  no   ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║  COMANDOS: ayuda, limpiar, salir                              ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)


def mostrar_banner():
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║      ███████╗ ██████╗ ██████╗                               ║
    ║      ██╔════╝██╔═══██╗██╔══██╗                              ║
    ║      █████╗  ██║   ██║██████╔╝                              ║
    ║      ██╔══╝  ██║   ██║██╔═══╝                               ║
    ║      ███████╗╚██████╔╝██║                                  ║
    ║      ╚══════╝ ╚═════╝ ╚═╝                                  ║
    ║                                                               ║
    ║           E s p a ñ o l   +   +   v 1 . 0                    ║
    ║                                                               ║
    ║     El lenguaje de programacion en espanol                    ║
    ║     para crear juegos y aplicaciones facilmente               ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    mostrar_banner()

    if len(sys.argv) > 1:
        archivo = sys.argv[1]
        ejecutar_archivo(archivo)
    else:
        modo_interactivo()
