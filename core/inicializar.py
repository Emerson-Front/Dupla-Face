import threading
import os
import webview
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
from mvc.controller.inicialController import inicialController



# Função para criar o ícone do Yin Yang
def criar_icone():
    largura = 64
    altura = 64
    imagem = Image.new('RGB', (largura, altura), 'white')
    draw = ImageDraw.Draw(imagem)

    # Círculo externo
    draw.ellipse((0, 0, largura, altura), fill='white', outline='black')
    centro_x = largura // 2
    centro_y = altura // 2
    raio = largura // 2

    # Metade preta (esquerda)
    draw.pieslice((0, 0, largura, altura), 90, 270, fill='black')

    # Semicírculo branco na parte superior (dentro da preta)
    draw.ellipse((centro_x - raio // 2, 0, centro_x + raio // 2, centro_y), fill='white')

    # Semicírculo preto na parte inferior (dentro da branca)
    draw.ellipse((centro_x - raio // 2, centro_y, centro_x + raio // 2, altura), fill='black')

    # Bolinha preta no topo (dentro do branco)
    draw.ellipse((centro_x - 4, centro_y // 2 - 4, centro_x + 4, centro_y // 2 + 4), fill='black')

    # Bolinha branca na base (dentro do preto)
    draw.ellipse((centro_x - 4, centro_y + centro_y // 2 - 4, centro_x + 4, centro_y + centro_y // 2 + 4), fill='white')

    return imagem

# Ação quando o item de menu é clicado
def on_click(icon, item):
    if item.text == "Mostrar Janela":
        webview.create_window('Dupla Face', 'mvc/view/inicialView.html', js_api=inicialController(), maximized=True)
        webview.start()


def sincronizar_no_tray():
    inicialController.iniciar_sincronizacao(None, 'start')
    
    
# Inicializa e executa o ícone na bandeja
def iniciar_tray():
    
    icone = Icon("Meu Programa")
    icone.icon = criar_icone()
    icone.menu = Menu(
        MenuItem("Mostrar Janela", on_click),
        MenuItem("Sair", lambda icon, item: os._exit(0))
    )
    
    # Cria e inicia a thread para o programa principal
    thread = threading.Thread(target=sincronizar_no_tray)
    thread.daemon = True # Fecha a thread quando o programa principal fechar
    thread.start()
    
    icone.run()

