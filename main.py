import webview
from mvc.controller.inicialController import inicialController

if __name__ == '__main__':
   janela = webview.create_window('Inicial', 'mvc/view/inicialView.html', js_api=inicialController())
   webview.start(debug=False)
