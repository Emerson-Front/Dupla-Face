from mvc.view.inicialView import inicialView
from mvc.model.inicialModel import inicialModel, Sincronizador
import core.route as rota

class inicialController:
    
    def __init__(self, page):
        self.page = page
        
        id, caminho_principal, caminho_secundario = inicialModel.buscarPasta()

        self.view = inicialView.pageInicial(page, id, caminho_principal, caminho_secundario)
        
        
        # Aqui adicione um "footer" futuramente talvez
        
        
        self.iniciar_sincronizacao()
             

    # adicionar pasta
    def botao_adicionar(self):
        principal, copia = inicialModel.escolher_pasta()
        inicialModel.adicionarPasta(principal, copia)
        rota.Route(self.page.route, self.page)
    
    def botao_remover(page, id):
        inicialModel.deletarPasta(id)
        rota.Route(page.route, page)
        print("Pasta removida com sucesso")
        
    def botao_atualizar(page, id):
        # Vai apagar tudo da pasta secundaria e atualizar com a pasta principal
        inicialModel.atualizarPasta(id)
        rota.Route(page.route, page)
        
    def inserir_ignorar(id_pasta, palavra):
        inicialModel.inserir_ignorar(id_pasta, palavra)

    def get_ignorar(id_pasta):
        lista = inicialModel.get_ignorar(id_pasta)
        return lista
    
    def remover_ignorar(page, id_pasta, palavra):
        inicialModel.remover_ignorar(id_pasta, palavra)
        
    
    def iniciar_sincronizacao(self):
        inicialModel.verificar_existencia_das_pastas_e_arquivos()
        # Manter sincronização das pastas
        pastas = inicialModel.get_pastas()
        Sincronizador.monitorar_pastas(pastas)
