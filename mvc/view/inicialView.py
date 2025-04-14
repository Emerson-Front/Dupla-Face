import flet as ft
import tkinter as tk
import mvc.controller.inicialController as controller

class inicialView:
        
                      
    def bloco_1(page, id, pastas_principais):
        
                                
        def dialogo(id_pasta):
            janela = tk.Tk()
            janela.resizable(False, True)
            janela.attributes('-topmost', True)
            janela.attributes('-toolwindow', True)
            janela.lift()
            janela.focus_force()

            largura = 400  # Largura fixa

            # Estilo
            janela.title("Filtro de palavras")
            janela.configure(bg="#f0f0f0")
            tk.Label(janela, text="Ignorar Pastas/Arquivos com nome:", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)
            
            frame_lista = tk.Frame(janela, bg="#f0f0f0")
            frame_lista.pack()

            for palavra in controller.inicialController.get_ignorar(id_pasta): 
                frame_item = tk.Frame(frame_lista, bg="#f0f0f0")
                frame_item.pack(anchor="w", fill="x")
                tk.Label(frame_item, text=palavra, font=("Arial", 12), bg="#f0f0f0").pack(side="left", padx=5, pady=2)
                btn_excluir = tk.Button(
                    frame_item,
                    text="❌",
                    fg='red',
                    cursor="hand2",
                    font=("Arial", 12),
                    bd=0,
                    command=lambda p=palavra:[
                        controller.inicialController.remover_ignorar(page, id_pasta, p),
                        janela.destroy(),
                    ]
                )
                btn_excluir.pack(side="right", padx=5)

            palavra = tk.Entry(janela, font=("Arial", 12))
            palavra.pack(pady=0)

            frame_botoes = tk.Frame(janela, bg="#f0f0f0")
            frame_botoes.pack(pady=20)

            tk.Button(frame_botoes, 
                    text="Adicionar", 
                    bg="#4CAF50", 
                    fg="white", 
                    font=("Arial", 12),
                    cursor="hand2",
                    command=lambda: [
                        controller.inicialController.inserir_ignorar(id_pasta, palavra.get()),
                        janela.destroy()
                    ]
                    ).pack(side="left", padx=5)

            tk.Button(frame_botoes,
                    text="Cancelar",
                    bg="#F44336", 
                    fg="white", 
                    font=("Arial", 12),
                    cursor="hand2",
                    command=janela.destroy
                    ).pack(side="left", padx=5)

            janela.update_idletasks()  # Atualiza antes de pegar altura real

            # Pega altura real agora que o layout foi carregado
            altura = janela.winfo_height()
            largura_tela = janela.winfo_screenwidth()
            altura_tela = janela.winfo_screenheight()
            pos_x = (largura_tela // 2) - (largura // 2)
            pos_y = (altura_tela // 2) - (altura // 2)

            # Define a geometria com altura real
            janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

            janela.mainloop()

       
        bloco_1 = ft.Container(
                                   
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Pastas Principais",
                        size=22,
                        weight=ft.FontWeight.BOLD
                    ),
                    *[
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.FILTER_LIST,
                                        on_click= lambda e, id=identificador: dialogo(id),
                                        ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_FOREVER_ROUNDED,
                                        on_click=lambda e, id=identificador: controller.inicialController.botao_remover(page, id),
                                        ),
                                    ft.Text(caminho),
                                ], 
                             ),
                            bgcolor=ft.Colors.GREY_300,
                            width=600,
                            
                        )
                        for caminho, identificador in zip(pastas_principais, id)
                    ]
                ],
                spacing=10,
            ),
            border_radius=10,
            border=ft.border.all(1, ft.Colors.BLACK),
            shadow=ft.BoxShadow(
                blur_radius=10,
                spread_radius=2,
                color=ft.Colors.BLACK26
            ),
            padding=15,
            alignment=ft.alignment.center,
            expand=True,
        )
        return bloco_1      

        
        
    def bloco_2(page, id, pastas_copias):
        bloco_2 = ft.Container(            
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Pastas Cópias",
                        size=22,
                        weight=ft.FontWeight.BOLD
                    ),
                    *[
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.REFRESH,
                                        hover_color=ft.Colors.BLUE_300,
                                        on_click= lambda e, id=identificador: controller.inicialController.botao_atualizar(page, id),
                                        ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_FOREVER_ROUNDED,
                                        hover_color=ft.Colors.RED,
                                        on_click=lambda e, id=identificador: controller.inicialController.botao_remover(page, id),
                                        ),
                                    ft.Text(caminho),
                                ], 
                             ),
                            bgcolor=ft.Colors.GREY_300,
                            width=600,
                            
                        )
                        for caminho, identificador in zip(pastas_copias, id)
                    ]
                ],
                spacing=10,
            ),
            border_radius=10,
            border=ft.border.all(1, ft.Colors.BLACK),
            shadow=ft.BoxShadow(
                blur_radius=10,
                spread_radius=2,
                color=ft.Colors.BLACK26
            ),
            padding=15,
            alignment=ft.alignment.center,
            expand=True,
        )
        return bloco_2

    
    
    def pageInicial(page, id, principais, copias):
        page.title = "Dupla Face"
        page.theme_mode = ft.ThemeMode.LIGHT

        
        # pastas principais
        bloco_1 = inicialView.bloco_1(page, id, principais)
        
        # pastas copias
        bloco_2 = inicialView.bloco_2(page, id, copias)
        
        # botao de adicionar
        btn_adicionar = ft.ElevatedButton(
            "Adicionar",
            icon=ft.Icons.ADD,
            on_click=lambda e: controller.inicialController.botao_adicionar(e),  # Adiciona a função de adicionar
        )


        container = ft.Column(
            controls=[
                ft.Row(
                    controls=[bloco_1, bloco_2],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=30,
                ),
                ft.Container(
                    content=ft.Row(  # Adiciona um Row para agrupar os dois botões
                        controls=[
                            btn_adicionar,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,  # Define o espaçamento entre os botões
                    ),
                    alignment=ft.alignment.center,
                ),
            ],
            spacing=20,
        )

        # Adicionar ao layout principal
        page.add(container)
        page.update()
