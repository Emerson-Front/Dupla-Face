import sys
import flet as ft
from core.route import Route
from core.inicializar import iniciar_tray, main
import pandas as pd
import os


    # Verifica se os arquivos da tabela existem
if not os.path.exists('caminhos.csv') or not os.path.exists('palavras.csv'):
    # Se os arquivos não existem, cria-os
    df = pd.DataFrame(columns=['id', 'caminho_principal', 'caminho_secundario'])
    df.to_csv('caminhos.csv', index=False)
    df = pd.DataFrame(columns=['id', 'id_pasta', 'palavra'])
    df.to_csv('palavras.csv', index=False)


if __name__ == "__main__":
    # Verifica se o programa foi iniciado com argumento --tray
    if "--tray" in sys.argv:
        iniciar_tray()
    else:
        ft.app(target=main)
 
 
iniciar_tray()
                                                                                          