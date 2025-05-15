import turtle

def generate_l_system(axiom, rules, iterations):
    """
    Gera a string do L-System aplicando as regras de produção ao axioma
    por um número específico de iterações.
    """
    result = axiom
    
    for _ in range(iterations):
        new_result = ""
        for char in result:
            if char in rules:
                new_result += rules[char]
            else:
                new_result += char
        result = new_result
    
    return result

def draw_l_system(l_system, angle, distance):
    """
    Desenha o L-System usando a biblioteca turtle.
    
    Args:
        l_system: String gerada pelo L-System
        angle: Ângulo de rotação (em graus)
        distance: Distância para avançar ao desenhar uma linha
    """
    stack = []
    
    for symbol in l_system:
        if symbol == 'F':
            # Desenhar uma linha para frente
            turtle.forward(distance)
        elif symbol == '+':
            # Girar à direita pelo ângulo especificado
            turtle.right(angle)
        elif symbol == '-':
            # Girar à esquerda pelo ângulo especificado
            turtle.left(angle)
        elif symbol == '[':
            # Salvar a posição e orientação atuais
            stack.append((turtle.position(), turtle.heading()))
        elif symbol == ']':
            # Restaurar a posição e orientação anteriores
            if stack:
                position, heading = stack.pop()
                turtle.penup()
                turtle.goto(position)
                turtle.setheading(heading)
                turtle.pendown()

def main():
    # Configurações do L-System conforme o enunciado
    axiom = "F"
    rules = {"F": "F[+F]F[-F]F"}
    iterations = 4
    angle = 25
    distance = 10
    
    # Configurações da tartaruga
    turtle.setup(800, 800)
    turtle.title("L-System Árvore Fractal")
    turtle.bgcolor("black")
    turtle.color("green")
    turtle.speed(0)  # Velocidade máxima
    
    # Posicionar a tartaruga na parte inferior da tela
    turtle.penup()
    turtle.goto(0, -300)
    turtle.setheading(90)  # Apontar para cima
    turtle.pendown()
    
    # Gerar a string do L-System
    l_system = generate_l_system(axiom, rules, iterations)
    print(f"L-System gerado: {l_system}")
    
    # Desenhar o L-System
    draw_l_system(l_system, angle, distance)
    
    # Manter a janela aberta até ser fechada manualmente
    turtle.exitonclick()

if __name__ == "__main__":
    main()