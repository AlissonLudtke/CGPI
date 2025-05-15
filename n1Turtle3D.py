import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

class Turtle3D:
    def __init__(self):
        # Inicializa a posição da tartaruga na origem
        self.position = np.array([0.0, 0.0, 0.0])
        
        # Inicializa a orientação da tartaruga (frente, cima, direita)
        self.direction = np.array([1.0, 0.0, 0.0])  # Inicialmente apontando para o eixo X positivo
        self.up_vector = np.array([0.0, 1.0, 0.0])  # Inicialmente apontando para o eixo Y positivo
        self.right_vector = np.array([0.0, 0.0, 1.0])  # Inicialmente apontando para o eixo Z positivo
        
        # Inicializa a matriz de transformação como a identidade
        self.transform_matrix = np.identity(4)
        
        # Pilha para armazenar estados anteriores (para transformações hierárquicas)
        self.stack = []
        
        # Lista de linhas para desenhar (cada linha é um par de pontos)
        self.lines = []
        
        # Caneta (True para desenhar, False para não desenhar enquanto se move)
        self.pen_down = True
        
        # Distância padrão para movimentos
        self.default_step = 0.1
        self.default_angle = 10.0  # em graus
        
    def forward(self, distance):
        """Move a tartaruga para frente na direção atual"""
        old_position = self.position.copy()
        
        # Calcula a nova posição
        self.position = self.position + self.direction * distance
        
        # Se a caneta estiver abaixada, adiciona uma linha à lista
        if self.pen_down:
            self.lines.append((old_position, self.position))
            
        return self
    
    def backward(self, distance):
        """Move a tartaruga para trás"""
        return self.forward(-distance)
    
    def move_up(self, distance):
        """Move a tartaruga para cima na direção atual"""
        old_position = self.position.copy()
        
        # Calcula a nova posição
        self.position = self.position + self.up_vector * distance
        
        # Se a caneta estiver abaixada, adiciona uma linha à lista
        if self.pen_down:
            self.lines.append((old_position, self.position))
            
        return self
    
    def move_down(self, distance):
        """Move a tartaruga para baixo"""
        return self.move_up(-distance)
    
    def move_right(self, distance):
        """Move a tartaruga para a direita na direção atual"""
        old_position = self.position.copy()
        
        # Calcula a nova posição
        self.position = self.position + self.right_vector * distance
        
        # Se a caneta estiver abaixada, adiciona uma linha à lista
        if self.pen_down:
            self.lines.append((old_position, self.position))
            
        return self
    
    def move_left(self, distance):
        """Move a tartaruga para a esquerda"""
        return self.move_right(-distance)
    
    def rotate_x(self, angle_deg):
        """Rotaciona a tartaruga em torno do eixo X"""
        angle_rad = math.radians(angle_deg)
        rotation_matrix = np.array([
            [1, 0, 0],
            [0, math.cos(angle_rad), -math.sin(angle_rad)],
            [0, math.sin(angle_rad), math.cos(angle_rad)]
        ])
        
        # Rotaciona os vetores de direção
        self.direction = np.dot(rotation_matrix, self.direction)
        self.up_vector = np.dot(rotation_matrix, self.up_vector)
        self.right_vector = np.dot(rotation_matrix, self.right_vector)
        
        # Normaliza os vetores para evitar erros de arredondamento
        self.direction = self.direction / np.linalg.norm(self.direction)
        self.up_vector = self.up_vector / np.linalg.norm(self.up_vector)
        self.right_vector = self.right_vector / np.linalg.norm(self.right_vector)
        
        return self
    
    def rotate_y(self, angle_deg):
        """Rotaciona a tartaruga em torno do eixo Y"""
        angle_rad = math.radians(angle_deg)
        rotation_matrix = np.array([
            [math.cos(angle_rad), 0, math.sin(angle_rad)],
            [0, 1, 0],
            [-math.sin(angle_rad), 0, math.cos(angle_rad)]
        ])
        
        # Rotaciona os vetores de direção
        self.direction = np.dot(rotation_matrix, self.direction)
        self.up_vector = np.dot(rotation_matrix, self.up_vector)
        self.right_vector = np.dot(rotation_matrix, self.right_vector)
        
        # Normaliza os vetores para evitar erros de arredondamento
        self.direction = self.direction / np.linalg.norm(self.direction)
        self.up_vector = self.up_vector / np.linalg.norm(self.up_vector)
        self.right_vector = self.right_vector / np.linalg.norm(self.right_vector)
        
        return self
    
    def rotate_z(self, angle_deg):
        """Rotaciona a tartaruga em torno do eixo Z"""
        angle_rad = math.radians(angle_deg)
        rotation_matrix = np.array([
            [math.cos(angle_rad), -math.sin(angle_rad), 0],
            [math.sin(angle_rad), math.cos(angle_rad), 0],
            [0, 0, 1]
        ])
        
        # Rotaciona os vetores de direção
        self.direction = np.dot(rotation_matrix, self.direction)
        self.up_vector = np.dot(rotation_matrix, self.up_vector)
        self.right_vector = np.dot(rotation_matrix, self.right_vector)
        
        # Normaliza os vetores para evitar erros de arredondamento
        self.direction = self.direction / np.linalg.norm(self.direction)
        self.up_vector = self.up_vector / np.linalg.norm(self.up_vector)
        self.right_vector = self.right_vector / np.linalg.norm(self.right_vector)
        
        return self
    
    def set_pen_up(self):
        """Levanta a caneta (parar de desenhar)"""
        self.pen_down = False
        return self
    
    def set_pen_down(self):
        """Abaixa a caneta (começar a desenhar)"""
        self.pen_down = True
        return self
    
    def save_state(self):
        """Salva o estado atual da tartaruga na pilha"""
        state = {
            'position': self.position.copy(),
            'direction': self.direction.copy(),
            'up_vector': self.up_vector.copy(),
            'right_vector': self.right_vector.copy(),
            'transform_matrix': self.transform_matrix.copy(),
            'pen_down': self.pen_down
        }
        self.stack.append(state)
        return self
    
    def restore_state(self):
        """Restaura o último estado salvo da tartaruga"""
        if self.stack:
            state = self.stack.pop()
            self.position = state['position']
            self.direction = state['direction']
            self.up_vector = state['up_vector']
            self.right_vector = state['right_vector']
            self.transform_matrix = state['transform_matrix']
            self.pen_down = state['pen_down']
        return self
    
    def clear(self):
        """Limpa todas as linhas desenhadas"""
        self.lines = []
        return self
    
    def reset(self):
        """Reseta a tartaruga para o estado inicial"""
        self.__init__()
        return self
    
    def draw(self):
        """Desenha todas as linhas criadas pela tartaruga"""
        # Desenhar as linhas
        glBegin(GL_LINES)
        for line in self.lines:
            glVertex3fv(line[0])
            glVertex3fv(line[1])
        glEnd()
        
        # Desenhar a tartaruga como um pequeno triângulo na posição atual
        # Esta é uma representação simples da tartaruga
        turtle_size = 0.05
        
        # Calcular os três pontos do triângulo
        tip = self.position + self.direction * turtle_size
        base1 = self.position - self.direction * (turtle_size/2) + self.right_vector * (turtle_size/2)
        base2 = self.position - self.direction * (turtle_size/2) - self.right_vector * (turtle_size/2)
        
        # Desenhar o triângulo (tartaruga)
        glBegin(GL_TRIANGLES)
        glColor3f(1.0, 0.0, 0.0)  # Vermelho para a tartaruga
        glVertex3fv(tip)
        glVertex3fv(base1)
        glVertex3fv(base2)
        glEnd()
        
        # Restaurar a cor
        glColor3f(1.0, 1.0, 1.0)


# Variáveis globais
turtle = None
camera_distance = 5.0
camera_rotation_x = 30.0
camera_rotation_y = 45.0
help_display = True  # Mostrar ajuda de comandos

# Função de inicialização do OpenGL
def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glEnable(GL_DEPTH_TEST)


# Função de display
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    # Configurar a câmera para orbitar ao redor da origem
    x = camera_distance * math.sin(math.radians(camera_rotation_y)) * math.cos(math.radians(camera_rotation_x))
    y = camera_distance * math.sin(math.radians(camera_rotation_x))
    z = camera_distance * math.cos(math.radians(camera_rotation_y)) * math.cos(math.radians(camera_rotation_x))
    
    gluLookAt(x, y, z,  # posição da câmera
              0.0, 0.0, 0.0,  # ponto para onde a câmera está olhando
              0.0, 1.0, 0.0)  # vetor "up" da câmera
    
    # Desenhar os eixos
    glBegin(GL_LINES)
    # Eixo X - Vermelho
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(1.0, 0.0, 0.0)
    # Eixo Y - Verde
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 1.0, 0.0)
    # Eixo Z - Azul
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 1.0)
    glEnd()
    
    # Desenhar as linhas da tartaruga
    glColor3f(1.0, 1.0, 1.0)
    turtle.draw()
    
    # Desenhar o texto de ajuda
    if help_display:
        draw_help_text()
    
    glutSwapBuffers()


# Função para desenhar texto na tela
def draw_help_text():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, glutGet(GLUT_WINDOW_WIDTH), 0, glutGet(GLUT_WINDOW_HEIGHT), -1, 1)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glColor3f(1.0, 1.0, 1.0)
    
    # Posição inicial do texto
    x, y = 10, glutGet(GLUT_WINDOW_HEIGHT) - 20
    line_height = 15
    
    # Função de ajuda para desenhar uma linha de texto e avançar a posição y
    def draw_line(text):
        nonlocal y
        glRasterPos2f(x, y)
        for c in text:
            glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(c))
        y -= line_height
    
    # Comandos da tartaruga
    draw_line("COMANDOS DA TARTARUGA:")
    draw_line("W/S: Mover para frente/trás")
    draw_line("A/D: Mover para esquerda/direita")
    draw_line("R/F: Mover para cima/baixo")
    draw_line("Q/E: Rotacionar no eixo Z")
    draw_line("1/2: Rotacionar no eixo X")
    draw_line("3/4: Rotacionar no eixo Y")
    draw_line("Espaço: Alternar caneta (levantar/abaixar)")
    draw_line("P: Salvar estado da tartaruga na pilha")
    draw_line("O: Restaurar último estado da pilha")
    draw_line("C: Limpar desenho")
    draw_line("X: Resetar tartaruga")
    draw_line("Z: Alternar ajuda")
    
    # Comandos da câmera
    y -= line_height
    draw_line("COMANDOS DA CÂMERA:")
    draw_line("Setas: Rotacionar câmera")
    draw_line("+/-: Aproximar/afastar câmera")
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


# Função de redimensionamento
def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, width / height if height > 0 else 1, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


# Funções de controle do teclado
def keyboard(key, x, y):
    global turtle, camera_distance, camera_rotation_x, camera_rotation_y, help_display
    
    key = key.decode('utf-8') if isinstance(key, bytes) else key
    
    # Comandos da tartaruga
    if key == 'w':
        turtle.forward(turtle.default_step)
    elif key == 's':
        turtle.backward(turtle.default_step)
    elif key == 'a':
        turtle.move_left(turtle.default_step)
    elif key == 'd':
        turtle.move_right(turtle.default_step)
    elif key == 'r':
        turtle.move_up(turtle.default_step)
    elif key == 'f':
        turtle.move_down(turtle.default_step)
    elif key == 'q':
        turtle.rotate_z(turtle.default_angle)
    elif key == 'e':
        turtle.rotate_z(-turtle.default_angle)
    elif key == '1':
        turtle.rotate_x(turtle.default_angle)
    elif key == '2':
        turtle.rotate_x(-turtle.default_angle)
    elif key == '3':
        turtle.rotate_y(turtle.default_angle)
    elif key == '4':
        turtle.rotate_y(-turtle.default_angle)
    elif key == ' ':  # Espaço
        turtle.pen_down = not turtle.pen_down
    elif key == 'p':
        turtle.save_state()
    elif key == 'o':
        turtle.restore_state()
    elif key == 'c':
        turtle.clear()
    elif key == 'x':
        turtle.reset()
    elif key == 'z':
        help_display = not help_display
    
    glutPostRedisplay()


# Funções de controle das teclas especiais (setas)
def special_keyboard(key, x, y):
    global camera_rotation_x, camera_rotation_y, camera_distance
    
    # Controle da câmera
    if key == GLUT_KEY_UP:
        camera_rotation_x = min(camera_rotation_x + 5, 90)
    elif key == GLUT_KEY_DOWN:
        camera_rotation_x = max(camera_rotation_x - 5, -90)
    elif key == GLUT_KEY_LEFT:
        camera_rotation_y = (camera_rotation_y - 5) % 360
    elif key == GLUT_KEY_RIGHT:
        camera_rotation_y = (camera_rotation_y + 5) % 360
    elif key == GLUT_KEY_PAGE_UP:
        camera_distance = max(camera_distance - 0.5, 1.5)
    elif key == GLUT_KEY_PAGE_DOWN:
        camera_distance = min(camera_distance + 0.5, 20.0)
    
    glutPostRedisplay()


# Exemplo de uso: desenhar uma estrutura fractal 3D
def draw_tree(turtle, length, depth):
    if depth == 0:
        return
    
    # Avança e desenha o tronco
    turtle.forward(length)
    
    # Salva o estado para retornar a ele após desenhar cada ramo
    turtle.save_state()
    
    # Primeiro ramo (para cima + direita)
    turtle.rotate_x(45)
    turtle.rotate_z(45)
    draw_tree(turtle, length * 0.7, depth - 1)
    turtle.restore_state()
    
    turtle.save_state()
    # Segundo ramo (para cima + esquerda)
    turtle.rotate_x(45)
    turtle.rotate_z(-45)
    draw_tree(turtle, length * 0.7, depth - 1)
    turtle.restore_state()
    
    turtle.save_state()
    # Terceiro ramo (para frente + cima)
    turtle.rotate_y(45)
    turtle.rotate_x(45)
    draw_tree(turtle, length * 0.7, depth - 1)
    turtle.restore_state()
    
    turtle.save_state()
    # Quarto ramo (para frente + baixo)
    turtle.rotate_y(45)
    turtle.rotate_x(-45)
    draw_tree(turtle, length * 0.7, depth - 1)
    turtle.restore_state()


# Função principal
def main():
    global turtle
    
    # Inicializa a tartaruga
    turtle = Turtle3D()
    
    # Inicializa o OpenGL
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Turtle 3D Interativa")
    
    init()
    
    # Registra as funções de callback
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keyboard)
    
    # Inicia o loop principal
    print("=== Controlando a Tartaruga 3D ===")
    print("Use as teclas W, A, S, D, R, F para movimentar a tartaruga.")
    print("Use as teclas Q, E, 1, 2, 3, 4 para rotacionar a tartaruga.")
    print("Use a barra de espaço para levantar/abaixar a caneta.")
    print("Use P para salvar o estado e O para restaurar.")
    print("Use C para limpar o desenho e X para resetar a tartaruga.")
    print("Use Z para alternar a exibição da ajuda.")
    print("Use as setas para rotacionar a câmera e Page Up/Down para aproximar/afastar.")
    
    glutMainLoop()


if __name__ == "__main__":
    import sys
    main()