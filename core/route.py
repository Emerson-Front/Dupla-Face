from mvc.controller.inicialController import inicialController


class Route:

    def __init__(self, rota, page):

        page.clean()

        match rota:
            case '/':
                inicialController(page)
            case _:
                print('rota não encontrada')
