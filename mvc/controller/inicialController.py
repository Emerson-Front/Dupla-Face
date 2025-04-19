import os, sys
import threading
from mvc.model.inicialModel import inicialModel, Sincronizador


class inicialController:
    
    def __init__(self):
        
        threading.Thread(target=self.iniciar_sincronizacao, daemon=True).start()
        self.check = inicialModel.get_checked()
        
    # adicionar pasta
    def btn_adicionar(self):
        principal, copia = inicialModel.escolher_pasta()   
        inicialModel.adicionarPasta(principal, copia)
        threading.Thread(target=self.iniciar_sincronizacao, daemon=True).start()



    def get_dados(self):
        id, principal, secundario = inicialModel.buscarPasta()
        return id, principal, secundario
        
    def btn_deletar(self, id):
        inicialModel.deletarPasta(id)
        os.execl(sys.executable, sys.executable, *sys.argv)
        
        
    def btn_atualizar(self, id):
        # Vai apagar tudo da pasta secundaria e atualizar com a pasta principal
        inicialModel.atualizarPasta(id)
        
    def adicionar_filtro(self, id_pasta, palavra):
        inicialModel.inserir_ignorar(id_pasta, palavra)

    def get_filtro(self, id_pasta):
        lista = inicialModel.get_ignorar(id_pasta)
        return lista
    
    def remover_filtro(self, id_pasta, palavra):
        inicialModel.remover_ignorar(id_pasta, palavra)
        
    
    def iniciar_sincronizacao(self):
        inicialModel.verificar_existencia_das_pastas_e_arquivos()
        # Manter sincronização das pastas
        pastas = inicialModel.get_pastas()
        Sincronizador.monitorar_pastas(pastas)
    
    
    def btn_checkbox(self, check):
        if check:
            inicialModel.check_tray(True)
        else:
            inicialModel.check_tray(False)
    
    def get_checked(self):
        return self.check
    
    
    
    # Função para o desenvolvimento, vai recarregar o programa
    def btn_recarregar(self):
        os.execl(sys.executable, sys.executable, *sys.argv)
