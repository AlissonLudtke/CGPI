import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math
import sys

# Shaders de vértice e fragmento em GLSL
vertex_shader = """
#version 330 core
layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec3 fragNormal;
out vec3 fragPosition;

void main() {
    gl_Position = projection * view * model * vec4(position, 1.0);
    fragPosition = vec3(model * vec4(position, 1.0));
    fragNormal = mat3(transpose(inverse(model))) * normal;
}
"""

fragment_shader = """
#version 330 core
in vec3 fragNormal;
in vec3 fragPosition;

uniform vec3 lightPos;
uniform vec3 viewPos;
uniform vec3 lightColor;
uniform vec3 objectColor;
uniform int renderMode;  // 0: normal, 1: pontos, 2: wireframe

out vec4 fragColor;

void main() {
    // Modo de renderização
    if (renderMode == 1) {  // Pontos
        fragColor = vec4(objectColor, 1.0);
    }
    else if (renderMode == 2) {  // Wireframe
        fragColor = vec4(objectColor, 1.0);
    }
    else {  // Normal (preenchido com iluminação)
        // Cálculo básico de iluminação
        vec3 norm = normalize(fragNormal);
        vec3 lightDir = normalize(lightPos - fragPosition);
        
        // Componente difusa
        float diff = max(dot(norm, lightDir), 0.0);
        vec3 diffuse = diff * lightColor;
        
        // Componente ambiente
        float ambientStrength = 0.1;
        vec3 ambient = ambientStrength * lightColor;
        
        // Componente especular
        float specularStrength = 0.5;
        vec3 viewDir = normalize(viewPos - fragPosition);
        vec3 reflectDir = reflect(-lightDir, norm);
        float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
        vec3 specular = specularStrength * spec * lightColor;
        
        // Combinação final
        vec3 result = (ambient + diffuse + specular) * objectColor;
        fragColor = vec4(result, 1.0);
    }
}
"""

def create_sphere(radius, num_slices, num_stacks):
    vertices = []
    normals = []
    indices = []
    
    # Gerar vértices e normais
    for i in range(num_stacks + 1):
        phi = math.pi * i / num_stacks
        for j in range(num_slices + 1):
            theta = 2.0 * math.pi * j / num_slices
            
            x = radius * math.sin(phi) * math.cos(theta)
            y = radius * math.sin(phi) * math.sin(theta)
            z = radius * math.cos(phi)
            
            vertices.extend([x, y, z])
            
            # Normal (normalizado)
            normal_len = math.sqrt(x*x + y*y + z*z)
            nx = x / normal_len
            ny = y / normal_len
            nz = z / normal_len
            normals.extend([nx, ny, nz])
    
    # Gerar índices
    for i in range(num_stacks):
        for j in range(num_slices):
            first = i * (num_slices + 1) + j
            second = first + num_slices + 1
            
            # Primeiro triângulo
            indices.extend([first, second, first + 1])
            
            # Segundo triângulo
            indices.extend([second, second + 1, first + 1])
    
    return np.array(vertices, dtype=np.float32), np.array(normals, dtype=np.float32), np.array(indices, dtype=np.uint32)

def compile_shader(shader_code, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, shader_code)
    glCompileShader(shader)
    
    # Verificar erros de compilação
    success = glGetShaderiv(shader, GL_COMPILE_STATUS)
    if not success:
        info_log = glGetShaderInfoLog(shader).decode('utf-8')
        print(f"Erro ao compilar shader: {info_log}")
        glDeleteShader(shader)
        return 0
    
    return shader

def create_shader_program(vertex_code, fragment_code):
    vertex = compile_shader(vertex_code, GL_VERTEX_SHADER)
    fragment = compile_shader(fragment_code, GL_FRAGMENT_SHADER)
    
    program = glCreateProgram()
    glAttachShader(program, vertex)
    glAttachShader(program, fragment)
    glLinkProgram(program)
    
    # Verificar erros de ligação
    success = glGetProgramiv(program, GL_LINK_STATUS)
    if not success:
        info_log = glGetProgramInfoLog(program).decode('utf-8')
        print(f"Erro ao vincular programa: {info_log}")
        return 0
    
    # Após a vinculação bem-sucedida, os shaders podem ser excluídos
    glDeleteShader(vertex)
    glDeleteShader(fragment)
    
    return program

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Visualizador 3D - Alternar com teclas 1 (normal), 2 (pontos), 3 (wireframe)")
    
    # Configuração do OpenGL
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.1, 0.1, 0.1, 1.0)
    
    # Perspectiva
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    
    # Criar os dados da esfera
    sphere_vertices, sphere_normals, sphere_indices = create_sphere(1.0, 32, 32)
    
    # Criar e configurar o VAO e VBOs
    VAO = glGenVertexArrays(1)
    VBO_vertices = glGenBuffers(1)
    VBO_normals = glGenBuffers(1)
    EBO = glGenBuffers(1)
    
    glBindVertexArray(VAO)
    
    # Carregar vértices
    glBindBuffer(GL_ARRAY_BUFFER, VBO_vertices)
    glBufferData(GL_ARRAY_BUFFER, sphere_vertices.nbytes, sphere_vertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)
    
    # Carregar normais
    glBindBuffer(GL_ARRAY_BUFFER, VBO_normals)
    glBufferData(GL_ARRAY_BUFFER, sphere_normals.nbytes, sphere_normals, GL_STATIC_DRAW)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(1)
    
    # Carregar índices
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, sphere_indices.nbytes, sphere_indices, GL_STATIC_DRAW)
    
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)
    
    # Compilar e configurar o programa de shader
    shader_program = create_shader_program(vertex_shader, fragment_shader)
    
    # Variáveis de rotação para animação básica
    rotation_x = 0
    rotation_y = 0
    
    # Modo de renderização inicial (0: normal, 1: pontos, 2: wireframe)
    render_mode = 0
    
    clock = pygame.time.Clock()
    
    # Loop principal
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    render_mode = 0  # Modo normal
                    print("Modo: Normal")
                elif event.key == pygame.K_2:
                    render_mode = 1  # Modo de pontos
                    print("Modo: Pontos")
                elif event.key == pygame.K_3:
                    render_mode = 2  # Modo wireframe
                    print("Modo: Wireframe")
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        # Limpar a tela
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Atualizar a rotação para uma animação básica
        rotation_x += 0.5
        rotation_y += 0.3
        
        # Usar o programa de shader
        glUseProgram(shader_program)
        
        # Configurar as matrizes de transformação
        model = np.identity(4, dtype=np.float32)
        model = np.dot(model, rotation_matrix_x(math.radians(rotation_x)))
        model = np.dot(model, rotation_matrix_y(math.radians(rotation_y)))
        
        view = np.identity(4, dtype=np.float32)
        projection = perspective(45.0, display[0]/display[1], 0.1, 100.0)
        
        # Obter localização das uniforms
        model_loc = glGetUniformLocation(shader_program, "model")
        view_loc = glGetUniformLocation(shader_program, "view")
        projection_loc = glGetUniformLocation(shader_program, "projection")
        light_pos_loc = glGetUniformLocation(shader_program, "lightPos")
        view_pos_loc = glGetUniformLocation(shader_program, "viewPos")
        light_color_loc = glGetUniformLocation(shader_program, "lightColor")
        object_color_loc = glGetUniformLocation(shader_program, "objectColor")
        render_mode_loc = glGetUniformLocation(shader_program, "renderMode")
        
        # Definir valores das uniforms
        glUniformMatrix4fv(model_loc, 1, GL_TRUE, model)
        glUniformMatrix4fv(view_loc, 1, GL_TRUE, view)
        glUniformMatrix4fv(projection_loc, 1, GL_TRUE, projection)
        glUniform3f(light_pos_loc, 3.0, 3.0, 5.0)
        glUniform3f(view_pos_loc, 0.0, 0.0, 5.0)
        glUniform3f(light_color_loc, 1.0, 1.0, 1.0)
        glUniform3f(object_color_loc, 0.5, 0.7, 0.9)
        glUniform1i(render_mode_loc, render_mode)
        
        # Desenhar a esfera com o modo de renderização apropriado
        glBindVertexArray(VAO)
        
        if render_mode == 1:  # Modo de pontos
            glPolygonMode(GL_FRONT_AND_BACK, GL_POINT)
            glPointSize(3.0)
        elif render_mode == 2:  # Modo wireframe
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glLineWidth(1.0)
        else:  # Modo normal (preenchido)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
        # Desenhar usando o Element Buffer Object
        glDrawElements(GL_TRIANGLES, len(sphere_indices), GL_UNSIGNED_INT, None)
        
        # Restaurar o estado do OpenGL
        glBindVertexArray(0)
        glUseProgram(0)
        
        # Atualizar a tela
        pygame.display.flip()
        clock.tick(60)
    
    # Limpar recursos do OpenGL
    glDeleteVertexArrays(1, [VAO])
    glDeleteBuffers(1, [VBO_vertices])
    glDeleteBuffers(1, [VBO_normals])
    glDeleteBuffers(1, [EBO])
    glDeleteProgram(shader_program)
    
    pygame.quit()
    sys.exit()

def rotation_matrix_x(angle):
    """Retorna uma matriz de rotação em torno do eixo X."""
    return np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, math.cos(angle), -math.sin(angle), 0.0],
        [0.0, math.sin(angle), math.cos(angle), 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=np.float32)

def rotation_matrix_y(angle):
    """Retorna uma matriz de rotação em torno do eixo Y."""
    return np.array([
        [math.cos(angle), 0.0, math.sin(angle), 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [-math.sin(angle), 0.0, math.cos(angle), 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=np.float32)

def perspective(fovy, aspect, near, far):
    """Cria uma matriz de projeção perspectiva."""
    f = 1.0 / math.tan(math.radians(fovy) / 2.0)
    
    return np.array([
        [f / aspect, 0.0, 0.0, 0.0],
        [0.0, f, 0.0, 0.0],
        [0.0, 0.0, (far + near) / (near - far), (2.0 * far * near) / (near - far)],
        [0.0, 0.0, -1.0, 0.0]
    ], dtype=np.float32)

if __name__ == "__main__":
    main()