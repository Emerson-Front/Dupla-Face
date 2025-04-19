import pandas as pd
import webview, os, sys
from mvc.controller.inicialController import inicialController
from core.inicializar import iniciar_tray


    # Verifica se os arquivos da tabela existem
if not os.path.exists('caminhos.csv') or not os.path.exists('palavras.csv'):
    # Se os arquivos não existem, cria-os
    df = pd.DataFrame(columns=['id', 'caminho_principal', 'caminho_secundario'])
    df.to_csv('caminhos.csv', index=False)
    df = pd.DataFrame(columns=['id', 'id_pasta', 'palavra'])
    df.to_csv('palavras.csv', index=False)

if __name__ == '__main__':
   
   if "--tray" in sys.argv:
      iniciar_tray()
      sys.exit()
      
   janela = webview.create_window('Dupla Face', 'mvc/view/inicialView.html', js_api=inicialController(), maximized=True)
   webview.start()
   
   iniciar_tray()
