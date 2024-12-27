# funções das cartas
#  criado:  27/12/24
# atualizado: 27/12/24
# 

import tkinter as tk
from tkinter import font
from tkinter import filedialog, messagebox, Label, Tk, Canvas, PhotoImage
import customtkinter as ctk
from customtkinter import CTkImage, CTkFont 
from PIL import Image, ImageDraw, ImageFont, ImageTk
import random
from back_end import Back_End


class Cartas:
    def __init__(self, root,  telas_iniciais, interface_jogo, back_end, tela_jogo):
        self.root = root  # Referência à janela principal
        self.interface_jogo = interface_jogo 
        self.telas_iniciais = telas_iniciais 
        self.back_end = back_end  
        self.tela_jogo = tela_jogo  # Agora a classe Cartas tem uma referência de Tela_Jogo
        self.back_end.load_fonts()      
        self.root.configure(bg="black")
        self.cor_Layout = self.back_end.cor_layout_atual 
        self.imagem_dado = "images/dado_grego.gif"
        
        self.canvas_abre = None  # Inicializado como None
        self.widgets_cartas = [] # widgets por casa
        
        
    def limpar_widgets_cartas(self):
        """Limpa os widgets da casa atual, incluindo o canvas e a imagem do dado."""
        for widget in self.widgets_cartas:
            widget.destroy()

        # Se o canvas ainda estiver presente, é destruido
        if hasattr(self, 'canvas') and self.canvas:
            self.canvas.destroy()
            self.canvas = None

        # Certifica que nenhuma imagem estática ou GIF fique referenciada
        if hasattr(self, 'image_on_canvas') and self.image_on_canvas:
            self.image_on_canvas = None

        # Limpa a lista de widgets dinâmicos da casa atual
        self.widgets_cartas = []
        
        
    

        
    def use_carta_Aphrodite(self):
        try:
            # Carrega a imagem usando PIL
            img = Image.open(self.back_end.cartas_deuses[0]['imagem']) 
            # Converte a imagem para PhotoImage
            self.image_carta_exibida = ImageTk.PhotoImage(img)
            # Cria um Label para exibir a imagem no Canvas
            self.label_imagem_carta = tk.Label(self.canvas_abre, image=self.image_carta_exibida, bg="black")
            self.label_imagem_carta.place(x=440, y=265, anchor="center")
            # Adiciona o Label à lista de widgets dinâmicos
            self.widgets_cartas.append(self.label_imagem_carta)

        except Exception as e:
            print(f'Sem imagens nessa carta, usando a imagem default -> {e}')


        # Botão avança 6
        botao_sim = ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 16,
        border_color= "white",
        border_width= 1,
        hover_color=self.cor_Layout,
        text="Advance 6 spaces",
        font=("Gelio Greek Diner", 18),
        command=lambda: (
            self.back_end.avanca_casa_cartas(numero_de_avanco=6, numero_retorna=0), # afrodite avança 6
            self.back_end.remove_carta_usada("Aphrodite"),
            self.tela_jogo.limpar_widgets_casa_atual(), # Limpa widgets existentes antes de atualizar a tela
            self.tela_jogo.atualizar_tela(),  # Atualiza outros elementos da tela
            self.tela_jogo.carregar_casa(self.back_end.casa_atual)  # Carrega os gadgets da nova casa# remove carta da lista
        )
        )
        
        botao_sim.place(x=600, y=380, anchor="center")
        self.widgets_cartas.append(botao_sim)
        
        # Botão NÃO
        botao_naum = ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 16,
        border_color= "white",
        border_width= 1,
        hover_color="red",
        text="no",
        font=("Gelio Greek Diner", 18),
        command= self.tela_jogo.dado_de_rolagem_implementacao()  # Chama o método de Tela_Jogo
        )
        botao_naum.place(x=700, y=380, anchor="center")
        self.widgets_cartas.append(botao_naum)
        

