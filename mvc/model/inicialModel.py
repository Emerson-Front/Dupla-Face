import os, stat, time, shutil, sys, win32com.client
import tkinter as tk
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from tkinter import filedialog

class inicialModel:
            
    # adiciona o caminho das pastas ao banco de dados 
    def adicionarPasta(caminho_principal, caminho_secundario):
        if caminho_principal == "" or caminho_secundario == "" or caminho_principal == caminho_secundario:
            print("Cancelado!")
            return

        df = pd.read_csv('caminhos.csv')    
        id = 1 if df.empty else df["id"].max() + 1
        dados = {
            "id": id,
            "caminho_principal": caminho_principal,
            "caminho_secundario": caminho_secundario
        }
        df = pd.concat([df, pd.DataFrame([dados])], ignore_index=True)
        df.to_csv('caminhos.csv', index=False) # Salvar

    
    # seleciona as pastas pra serem sincronizadas
    def escolher_pasta():
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True) # Obriga a ser janela em primeiro plano
        desktop_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
        caminho_principal = filedialog.askdirectory(initialdir=desktop_path, title="Escolha a pasta Principal")
        copia = filedialog.askdirectory(initialdir=desktop_path,title="Escolha a pasta de Cópia")
        root.destroy()
        return caminho_principal, copia

    # busca o caminho das pastas no banco de dados
    def buscarPasta():
        df = pd.read_csv('caminhos.csv')
        id = df["id"].tolist()
        caminho_principal = df["caminho_principal"].tolist()
        caminho_secundario = df["caminho_secundario"].tolist()
        return id, caminho_principal, caminho_secundario
    
    # deleta o caminho das pastas do banco de dados
    def deletarPasta(id):
        df = pd.read_csv('caminhos.csv')
        df = df[df["id"] != id]
        df.to_csv('caminhos.csv', index=False)
        
        df = pd.read_csv('palavras.csv')
        df = df[df["id_pasta"] != id]
        df.to_csv('palavras.csv', index=False)
    
    # retorna as pastas do banco de dados
    def get_pastas():
        df = pd.read_csv('caminhos.csv')
        caminhos = list(df[['caminho_principal', 'caminho_secundario']].itertuples(index=False, name=None))
        return caminhos
 
    # adiciona palavras a serem ignoradas
    def inserir_ignorar(id_pasta, palavra):
        if palavra == "": return
        
        df = pd.read_csv('palavras.csv')
        id = 1 if df.empty else df["id"].max() + 1
        dados = {
            "id": id,
            "id_pasta": id_pasta,
            "palavra": palavra
        }
        df = pd.concat([df, pd.DataFrame([dados])], ignore_index=True)
        df.to_csv('palavras.csv', index=False) # Salvar
    
    # retorna as palavras a serem ignoradas
    def get_ignorar(id_pasta):
        df = pd.read_csv('palavras.csv')
        palavras = df[df["id_pasta"] == id_pasta]["palavra"].tolist()
        return palavras
    
    def remover_ignorar(id_pasta, palavra):
        df = pd.read_csv('palavras.csv')
        df["id_pasta"] = df["id_pasta"].astype(str).str.strip()
        df["palavra"] = df["palavra"].astype(str).str.strip()

        id_pasta = str(id_pasta).strip()
        palavra = str(palavra).strip()

        df = df[~((df["id_pasta"] == id_pasta) & (df["palavra"] == palavra))]
        df.to_csv('palavras.csv', index=False)
        

    def verificar_existencia_das_pastas_e_arquivos():            
        # Verifica se as pastas existem
        df = pd.read_csv('caminhos.csv')
        caminhos = df['caminho_principal']
        caminho = len(caminhos)
        for caminho in caminhos:
            if os.path.exists(caminho):
                pass
            else:
                # Se a pasta não existir, apaga da tabela
                df = df[df['caminho_principal'] != caminho]
                df.to_csv('caminhos.csv', index=False)
                
        return caminhos

    def atualizarPasta(id):
        # Localiza a pasta principal e secundária
        df = pd.read_csv('caminhos.csv')
        principal = df[df['id'] == id]['caminho_principal'].iloc[0]
        secundario = df[df['id'] == id]['caminho_secundario'].iloc[0]

        
        # Função usada para lidar com erros ao tentar apagar arquivos/pastas protegidos
        def handle_remove_readonly(func, path, exc_info):
            os.chmod(path, stat.S_IWRITE)
            func(path)
                            
        # Apaga a pasta secundária e copia a principal recriando a secundária
        if os.path.exists(secundario):
            shutil.rmtree(secundario, onexc=handle_remove_readonly)
            shutil.copytree(principal, secundario)
            
        # Depois de copiar tudo vai eliminar as pastas e arquivos bloqueados (filtro)
        # Lê as palavras bloqueadas (com extensão)
        df_palavras = pd.read_csv('palavras.csv')
        palavras_bloqueadas = [p.lower() for p in df_palavras[df_palavras['id_pasta'] == id]['palavra'].tolist()]

        # Percorre todos os arquivos e pastas dentro da cópia
        for root, dirs, files in os.walk(secundario, topdown=False):
            # Remove pastas com nomes bloqueados
            for nome in dirs:
                if nome.lower() in palavras_bloqueadas:
                    caminho = os.path.join(root, nome)
                    shutil.rmtree(caminho, onexc=handle_remove_readonly)
                    print(f"{nome} (diretório) -- Ignorado")

            # Remove arquivos com nomes completos (com extensão) bloqueados
            for nome in files:
                if nome.lower() in palavras_bloqueadas:
                    caminho = os.path.join(root, nome)
                    os.remove(caminho)
                    print(f"{nome} -- Ignorado")

    def check_tray(check):
        caminho_do_programa = os.path.abspath(sys.executable)
        startup_path = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
        caminho_do_atalho = os.path.join(startup_path, "Dupla Face.exe.lnk")
        
        if check:
            shell = win32com.client.Dispatch("WScript.Shell")
            atalho = shell.CreateShortCut(caminho_do_atalho)
            atalho.Targetpath = caminho_do_programa
            atalho.Arguments = "--tray"
            atalho.WorkingDirectory = os.path.dirname(caminho_do_programa)
            atalho.IconLocation = caminho_do_programa
            atalho.save()
            print("Tray está ativado e está no startup")
                
        else:
            if os.path.exists(caminho_do_atalho):
                os.remove(caminho_do_atalho)
                print("Tray está desativado e foi removido do startup")
            else:
                print("Tray não está ativado e não está no startup")

    def get_checked():
        startup_path = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
        caminho_do_atalho = os.path.join(startup_path, "Dupla Face.exe.lnk")
        if os.path.exists(caminho_do_atalho):
            return True




class Sincronizador(FileSystemEventHandler):
    """
    Classe que gerencia a sincronização entre pastas,
    monitorando eventos e refletindo as alterações na cópia.

    Defina os pares de pastas para sincronizar nesse formato
    pares_de_pastas = [
        ("C:/Users/etads/Desktop/a", "C:/Users/etads/Desktop/b"),
        ("C:/Users/etads/Desktop/c", "C:/Users/etads/Desktop/d"),
    ]
    
    para usar:
    Sincronizador.monitorar_pastas(pares_de_pastas)
    """

    def __init__(self, caminho_original: str, caminho_da_copia: str) -> None:
        self.caminho_original = caminho_original
        self.caminho_da_copia = caminho_da_copia
        
        
    def copiar_para_destino(self, src_path: str) -> None:
        """
        Copia arquivos e pastas.
        :param src_path: Caminho do arquivo ou pasta a ser copiado.
        """
        
        caminho_relativo = os.path.relpath(src_path, self.caminho_original)
        destino = os.path.join(self.caminho_da_copia, caminho_relativo)

        
        try:
            if os.path.isdir(src_path):
                if not os.path.exists(destino):                    
                    os.makedirs(destino)
                    print(f"Pasta criada na cópia: {destino}")
            elif os.path.isfile(src_path):
                pasta_destino = os.path.dirname(destino)
                if not os.path.exists(pasta_destino):
                    os.makedirs(pasta_destino)
                shutil.copy2(src_path, destino)
                print(f"Arquivo copiado: {src_path} -> {destino}")
        except Exception as e:
            print(f"Erro ao copiar {src_path}: {e}")

    def remover_do_destino(self, src_path: str) -> None:
        """
        Remove arquivos e pastas da cópia, preservando a hierarquia.
        :param src_path: Caminho do arquivo ou pasta a ser removido.
        """
        caminho_relativo = os.path.relpath(src_path, self.caminho_original)
        destino = os.path.join(self.caminho_da_copia, caminho_relativo)
                
        try:
            if os.path.exists(destino):
                if os.path.isdir(destino):
                    shutil.rmtree(destino)
                    print(f"Pasta removida da cópia: {destino}")
                else:
                    os.remove(destino)
                    print(f"Arquivo removido da cópia: {destino}")
        except Exception as e:
            print(f"Erro ao remover {destino}: {e}")

    # Métodos de manipulação de eventos do watchdog e filtro de nome de arquivos e pastas:

    def on_any_event(self, event):
        print(f"[{event.event_type.upper()}] - {event.src_path}")

        caminho_secundario = event.dest_path if event.event_type == "moved" and hasattr(event, "dest_path") else event.src_path
        caminho_secundario = os.path.normpath(caminho_secundario)  # normaliza para evitar erros com / e \
        nome_da_pasta = os.path.basename(caminho_secundario)

        print(f"Nome da pasta/arquivo: {nome_da_pasta}")
        print(f"Caminho completo analisado: {caminho_secundario}")

        palavra_bloqueada = self.filtro(caminho_secundario)

        if palavra_bloqueada:
            print(f"CAMINHO BLOQUEADO contendo '{palavra_bloqueada}' DETECTADO - Ignorado!")
            self.remover_do_destino(event.src_path)
            return

        # Continua normalmente com os eventos
        match event.event_type:
            case "created":
                self.copiar_para_destino(event.src_path)
            case "modified":
                self.copiar_para_destino(event.src_path)
            case "moved":
                self.remover_do_destino(event.src_path)
                self.copiar_para_destino(event.dest_path)
            case "deleted":
                self.remover_do_destino(event.src_path)




    @classmethod
    def monitorar_pastas(cls, pares_de_pastas: list[tuple[str, str]]) -> None:
        """
        Monitora múltiplas pastas e sincroniza as alterações de acordo com os pares informados.
        :param pares_de_pastas: Lista de tuplas contendo (caminho_original, caminho_da_copia).
        """
        observers = []  # Lista para armazenar os observadores

        for caminho_original, caminho_da_copia in pares_de_pastas:
            print(f"Monitorando '{caminho_original}' -> '{caminho_da_copia}'")
            event_handler = cls(caminho_original, caminho_da_copia)
            observer = Observer()
            observer.schedule(event_handler, path=caminho_original, recursive=True)
            observer.start()
            observers.append(observer)

        try:
            while True:
                time.sleep(1)  # Mantém o programa em execução
        except KeyboardInterrupt:
            for observer in observers:
                observer.stop()
            for observer in observers:
                observer.join()


    def filtro(self, caminho_completo):
        caminho_completo = os.path.normpath(caminho_completo)

        df = pd.read_csv('caminhos.csv')
        df['caminho_principal'] = df['caminho_principal'].apply(os.path.normpath)

        id = None
        for _, row in df.iterrows():
            if caminho_completo.startswith(row['caminho_principal']):
                id = row['id']
                break

        if id is None:
            return None

        df_palavras = pd.read_csv('palavras.csv')
        palavras_bloqueadas = [palavra.lower() for palavra in df_palavras[df_palavras['id_pasta'] == id]['palavra'].tolist()]

        # Divida o caminho em partes, sem remover a extensão
        partes_do_caminho = caminho_completo.split(os.sep)
        
        # Agora, vamos comparar cada parte (pasta ou arquivo com a extensão)
        for parte in partes_do_caminho:
            if parte.lower() in palavras_bloqueadas:
                return parte

        return None
