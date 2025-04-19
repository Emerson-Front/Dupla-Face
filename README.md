# Dupla Face

**Dupla Face** é um aplicativo de sincronização de arquivos que opera localmente, mantendo pastas atualizadas de forma discreta e eficiente. Ele monitora uma pasta principal (Pasta A) e propaga automaticamente todas as alterações (adições, modificações e remoções) para uma pasta secundária (Pasta B), garantindo que ambas estejam sempre em sincronia.  
Ideal para quem deseja um controle automático e confiável dos arquivos no computador.

---

## 🎯 Objetivo

Oferecer uma solução simples e funcional para sincronização automática de arquivos entre pastas, operando em segundo plano e proporcionando total transparência e discrição ao usuário.

---

## 🚀 Funcionalidades

- **Sincronização em Tempo Real**  
  Monitora a Pasta A e reflete instantaneamente todas as alterações na Pasta B, incluindo:
  - Criação de novos arquivos  
  - Atualizações em arquivos existentes  
  - Exclusão de arquivos  

- **Início Automático**  
  Opera em segundo plano e pode ser acessado por meio dos ícones ocultos na bandeja do sistema, mantendo a interface limpa e livre de interrupções.  
  ➕ [Veja aqui como configurar o Dupla Face para iniciar junto com o Sistema](#️-iniciar-dupla-face-automaticamente-com-o-Sistema)

- **Configuração Personalizável**  
  Permite ao usuário escolher quais pastas sincronizar e aplicar filtros para ignorar arquivos ou diretórios específicos.

---

## 🔧 Tecnologias Utilizadas

- **Linguagem de Programação**: Python
- **Bibliotecas**:
  ```
  pip install pandas pyinstaller pystray pywebview watchdog pywin32 
  ``` 
  
  - [Pandas](https://pandas.pydata.org/) – Manipulação e análise de dados
  - [PyInstaller](https://www.pyinstaller.org/) – Empacota programas Python como executáveis independentes para Windows, Mac e Linux
  - [Pystray](https://pystray.readthedocs.io/) – Criação de ícones de bandeja no sistema, permitindo a integração com a barra de tarefas
  - [PyWebView](https://pywebview.flowrl.com/) – Criação de interfaces gráficas com um navegador embutido, fácil de usar para exibir páginas HTML
  - [PyWin32](https://pypi.org/project/pywin32/) – Permite a interação com as APIs do Windows, como automação e controle de componentes COM
  - [Watchdog](https://python-watchdog.readthedocs.io/) – Monitoramento de alterações no sistema de arquivos, útil para observar pastas e arquivos


---

## 📦 Download

- A versão mais recente do Dupla Face está disponível na seção de [releases do GitHub](https://github.com/emerson-front/dupla-face/releases).

---

## 🖥️ Iniciar Dupla Face automaticamente com o Sistema

Para que o Dupla Face seja iniciado automaticamente junto com o Sistema, siga os passos abaixo:

### 🔧 Passo a Passo

1. **Baixe a versão `.exe` da release.**

2. **Abra a pasta de Inicialização do Sistema**:
   - Pressione `Win + R` e digite:
     ```
     shell:startup
     ```
   - Pressione **Enter**.

3. **Crie um atalho para o executável dentro da pasta de inicialização**:
   - Clique com o botão direito dentro da pasta → **Novo** → **Atalho**.
   - Navegue até onde está o `Dupla Face.exe` e selecione-o.

4. **Adicione o argumento `--tray` ao final do caminho**:
   - No campo de destino, o caminho ficará algo como:
     ```
     "C:\caminho\para\Dupla Face.exe"
     ```
   - Adicione ` --tray` ao final, ficando assim:
     ```
     "C:\caminho\para\Dupla Face.exe" --tray
     ```
   - Clique em **Concluir**.


### ✅ Resultado

A partir do próximo reinício do sistema, o Dupla Face será iniciado automaticamente em segundo plano, com o ícone disponível na bandeja do sistema.

---