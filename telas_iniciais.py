# telas_iniciais do jogo - By Bressar
# criado:  18/12/24
# atualizado: 04/01/25

from tkinter import  Canvas, PhotoImage
import customtkinter as ctk
from PIL import Image, ImageTk
from back_end import Back_End
from tela_jogo import Tela_Jogo
import webbrowser

class Telas:
    def __init__(self, root, interface_jogo):
        self.root = root  # Referência à janela principal
        self.interface_jogo = interface_jogo  # Referência à instância de Interface_Jogo -> app.py
        self.widgets_dinamicos = []  # Lista para armazenar widgets dinâmicos        
        self.back_end = Back_End()
        self.back_end.load_fonts()
        self.tela_jogo = Tela_Jogo(root, self, interface_jogo, self.back_end) 
        
            
    def on_button_click_personagem(self, personagem): # escolher personagem
        """Lida com o clique no botão, atualiza a imagem e chama o backend."""
        # Atualiza a imagem para o estado de clique
        image_click = getattr(self, f"image_{personagem.lower()}_click", None)
        img_id = getattr(self, f"img_{personagem.lower()}_id", None)
        if img_id and image_click:
            self.canvas_abre.itemconfig(img_id, image=image_click)
        # Atualiza o personagem no backend
        self.back_end.escolher_personagem(personagem)        
        print(f"Personagem {personagem} clicado e selecionado!")
      
         
    def on_button_click_carta(self, carta_num): # escolher carta
        """Lida com o clique na carta, atualiza a imagem e chama o backend."""
        # Seleciona a imagem de clique com base no número da carta
        image_click = getattr(self, f"image_carta_escolha_click{carta_num}", None)  # Usando o número da carta
        img_id = getattr(self, f"img_carta_escolhida_id{carta_num}", None)  # Usando o número da carta
        if img_id and image_click: # Verifica se as imagens e IDs existem
            # Atualiza a imagem para o estado de clique da carta
            self.canvas_abre.itemconfig(img_id, image=image_click)       
        
        self.back_end.escolher_carta()# Chama a função do backend para escolher a carta
        
        print(f"Carta {carta_num} Escolhida!")
        print(f'carta inicial: {self.back_end.carta_inicial}')
        print(f'cartas do jogador: {self.back_end.cartas_player}')
 

 # TELAS INICIAIS   # TELAS INICIAIS   # TELAS INICIAIS 
    def tela_01(self):
        self.canvas_abre = Canvas(self.root, width=800, height=600, bg="black", bd=0, highlightthickness=0)
        self.canvas_abre.place(x=0, y=0)  # Posição do Canvas na tela
        self.widgets_dinamicos.append(self.canvas_abre)        
        # Titulo                
        label_titulo = ctk.CTkLabel(
            self.root,
            text= "Ascent To Olympus",
            text_color='#DAA520', 
            bg_color="black",  
            font=("Gelio Fasolada", 45))           
        label_titulo.place(relx=0.5, y=20, anchor="n")
        self.widgets_dinamicos.append(label_titulo)
        # SubTitulo    
        label_subtitulo = ctk.CTkLabel(
            self.root,
            text= "The Ancient Greek Game",
            text_color='#FF0000',  # Cor do texto vermelho
            bg_color="black",
            font=("Gelio Greek Diner", 25) )                   
        label_subtitulo.place(relx=0.5, y=65, anchor="n")
        self.widgets_dinamicos.append(label_subtitulo)        
        # Linha           
        self.canvas_abre.create_text(
            400,  # Coordenada X (centralizado na tela)
            110,   # Coordenada Y (acima da imagem)
            text="<><><><><><><><><><><><><><><><><><><><>",  # Texto que será exibido
            fill='#B8860B',  # Cor do texto RGB color: 184/255, 134/255, 11/255, 1
            font=("Arial", 12),  # Fonte e Tamanho
            anchor="center")  # Alinhamento centralizado   
                
        self.imagem_abre = "images/abre.jpg"# caminho da imagem do abre
        
        try:
            imagem_tela_01 = Image.open(self.imagem_abre) # Carrega a imagem com Pillow
            largura_canvas, altura_canvas = 360, 262  # Dimensões da imagem
            imagem_tela_01.thumbnail((largura_canvas, altura_canvas), Image.Resampling.LANCZOS)  # Redimensionamento proporcional
            self.imagem_canvas = ImageTk.PhotoImage(imagem_tela_01)   
            # Adiciona a imagem ao Canvas 
            self.canvas_abre.create_image(220, 120, anchor="nw", image=self.imagem_canvas) # posição da imagem
        except FileNotFoundError:
            print("Erro: Não foi possível carregar a imagem:", self.imagem_abre)  
        # linha            
        self.canvas_abre.create_text(
            400,  # Coordenada X 
            387,   # Coordenada Y 
            text="<><><><><><><><><><><><><><><><><><><><>",  
            fill='#B8860B', 
            font=("Arial", 12), 
            anchor="center")  
        
        texto_abertura =(
"""Embark on a Greek Mythology Adventure!

Roll the dice, collect cards, overcome challenges,and conquer Olympus!
Move across the board by rolling the dice. Win battles by rolling 4 or more.
Use cards to overcome obstacles. Collect up to 3 cards."""
               )        
        label_texto_abertura = ctk.CTkLabel(
            self.root,
            text=texto_abertura,
            text_color="white",  
            bg_color="black", 
            font=("Cambria", 16))

        label_texto_abertura.place(relx=0.5, y=405, anchor="n")
        self.widgets_dinamicos.append(label_texto_abertura)        
               
        botao_iniciar = ctk.CTkButton(
            self.canvas_abre,
            width= 100,
            fg_color='#FF0000',
            hover_color="#FFA500", # 'laranja'  # "#FFA500"
            text="Become a Legend!", 
            font= ("Gelio Fasolada", 18),
            command=lambda: self.tela_02()
        )
        botao_iniciar.place(relx=0.5, y=520, anchor="n")
        self.widgets_dinamicos.append(botao_iniciar)  
        
        botao_about = ctk.CTkButton(
            self.canvas_abre,
            width= 100,
            text_color= 'gray',
            fg_color='black',
            hover_color="#FFA500",
            text="About this game", 
            font= ("Gelio Fasolada", 16),
            command=lambda: self.janela_about()
        )
        botao_about.place(relx=0.5, y=560, anchor="n")
        self.widgets_dinamicos.append(botao_about)    
 
    # funções do botão ABOUT da Tela 01
    def abrir_link(self):
        webbrowser.open("https://paypal.me/bressargames")
           
    def janela_about(self):
        janela_game_about = ctk.CTkToplevel(self.root)
        janela_game_about.title("About this game")
        janela_game_about.geometry("400x400")
        janela_game_about.configure(fg_color="black")
        janela_game_about.wm_attributes("-topmost", True)
        
        texto_about = """Ascent to Olympus
The Ancient Greece Game
Version 1.0 - Beta
Developed by Hermes & Bressar Games
2025

If you enjoyed the game, please consider donating 
to support the development of the final version.
If you didn’t enjoy it, feel free to send 
your suggestions to:

bressargames@gmail.com
or
github.com/Bressar
        """
        texto = ctk.CTkLabel(
            janela_game_about,
            text= texto_about,
            text_color="gray",
            font=("Cambria", 16),
            justify="center" )
        texto.place(relx=0.5, rely=0.4, anchor="center")
                
        botao_doar = ctk.CTkButton(
            janela_game_about,
            text="Donate",
            width= 100,
            font=("Gelio Fasolada", 16),
            fg_color="green",
            text_color="white",
            hover_color="orange",
            command=self.abrir_link
            )
        botao_doar.place(relx=0.5, rely=0.80, anchor="center")
        
        botao_encerrar = ctk.CTkButton(
            janela_game_about,
            width=40,
            fg_color='black',
            border_width= 1,
            text_color= "gray",
            border_color= "gray",
            hover_color="orange",
            text="EXIT",
            font=("Gelio Fasolada", 14),
            command=janela_game_about.destroy
        )
        botao_encerrar.place(relx=0.5, rely=0.92, anchor="center")
        

    def tela_02(self):
        self.canvas_abre = Canvas(self.root, width=800, height=600, bg="black", bd=0, highlightthickness=0)
        self.canvas_abre.place(x=0, y=0) 
        self.widgets_dinamicos.append(self.canvas_abre)
        
        # Titulo                
        label_titulo = ctk.CTkLabel(
            self.root,
            text= "Ascent To Olympus",
            text_color='#DAA520',  # Cor do texto amarela
            bg_color="black",  
            font=("Gelio Fasolada", 28))            
        label_titulo.place(relx=0.5, y=10, anchor="n")
        self.widgets_dinamicos.append(label_titulo)        
        # SubTitulo    
        label_subtitulo = ctk.CTkLabel(
            self.root,
            text= "The Ancient Greek Game",
            text_color='#FF0000',  # Cor do texto vermelho
            bg_color="black",
            font=("Gelio Greek Diner", 17) )                   
        label_subtitulo.place(relx=0.5, y=40, anchor="n")
        self.widgets_dinamicos.append(label_subtitulo)       
        # Linha           
        self.canvas_abre.create_text(
            400,  
            75,   
            text="<><><><><><><><><><><><><><><><><><><><><><><>",  
            fill='#B8860B',  # Cor do texto RGB color: 184/255, 134/255, 11/255, 1
            font=("Arial", 12), 
            anchor="center")  
               
        self.canvas_abre.create_text(
            400,  
            100,  
            text="Reach Mount Olympus and receive the Gods' gift!",  
            fill='white',
            font=("Cambria", 15), 
            anchor="center") 
        
        self.canvas_abre.create_text(
            400,  
            125,  
            text="<><><><><><><><><><><><><><><><><><><><><><><>", 
            fill='#B8860B',  
            font=("Arial", 12), 
            anchor="center")   
        
        self.canvas_abre.create_text(
            400,  
            170,   
            text="Choose a Player", 
            fill='#FF8C00',  # Cor do texto RGB color: 255/255, 140/255, 0/255, 1  # DarkOrange
            font=("Gelio Fasolada", 20),  
            anchor="center") 
                
        # Botões Players                
        # Botão Hippolita
        self.image_hipolita_menu = PhotoImage(file="images/carinha_hipolita_menu.png")
        self.image_hipolita_hover = PhotoImage(file="images/carinha_hipolita_hover.png")
        self.image_hipolita_click = PhotoImage(file="images/carinha_hipolita_click.png")

        # Adiciona a imagem inicial ao Canvas
        self.img_hipolita_id = self.canvas_abre.create_image(400, 240, image=self.image_hipolita_menu)
        # Evento de clique
        self.canvas_abre.tag_bind(self.img_hipolita_id, '<Button-1>', lambda event: (self.on_button_click_personagem("hippolyta"),self.canvas_abre.itemconfig(self.img_hipolita_id, image=self.image_hipolita_click)))        
        # Evento de hover (mouse entra)
        self.canvas_abre.tag_bind(self.img_hipolita_id, '<Enter>', lambda event: self.canvas_abre.itemconfig(self.img_hipolita_id, image=self.image_hipolita_hover))
        # Evento de hover (mouse sai)
        self.canvas_abre.tag_bind(self.img_hipolita_id, '<Leave>', lambda event: self.canvas_abre.itemconfig(self.img_hipolita_id, image=self.image_hipolita_menu))

        label_botao_hipolita = ctk.CTkLabel(
            self.root,
            text="Hippolita",
            text_color='white',
            bg_color="black",
            font=("Gelio Fasolada", 18)
        )
        label_botao_hipolita.place(relx=0.5, y=290, anchor="n")
        self.widgets_dinamicos.append(label_botao_hipolita)

        # Botão Odysseus
        self.image_odisseu_menu = PhotoImage(file="images/carinha_odisseu_menu.png")
        self.image_odisseu_hover = PhotoImage(file="images/carinha_odisseu_hover.png")
        self.image_odisseu_click = PhotoImage(file="images/carinha_odisseu_click.png")

        self.img_odisseu_id = self.canvas_abre.create_image(280, 240, image=self.image_odisseu_menu)
        self.canvas_abre.tag_bind(self.img_odisseu_id, '<Button-1>', lambda event: (self.on_button_click_personagem("odysseus"),self.canvas_abre.itemconfig(self.img_odisseu_id, image=self.image_odisseu_click)))
        self.canvas_abre.tag_bind(self.img_odisseu_id, '<Enter>', lambda event: self.canvas_abre.itemconfig(self.img_odisseu_id, image=self.image_odisseu_hover))
        self.canvas_abre.tag_bind(self.img_odisseu_id, '<Leave>', lambda event: self.canvas_abre.itemconfig(self.img_odisseu_id, image=self.image_odisseu_menu))
        
        label_botao_odisseu = ctk.CTkLabel(
            self.root,
            text="Odysseus",
            text_color='white',
            bg_color="black",
            font=("Gelio Fasolada", 18)
        )
        label_botao_odisseu.place(x=280, y=290, anchor="n")
        self.widgets_dinamicos.append(label_botao_odisseu)

        # Botão Achilles
        self.image_aquiles_menu = PhotoImage(file="images/carinha_aquiles_menu.png")
        self.image_aquiles_hover = PhotoImage(file="images/carinha_aquiles_hover.png")
        self.image_aquiles_click = PhotoImage(file="images/carinha_aquiles_click.png")

        self.img_aquiles_id = self.canvas_abre.create_image(160, 240, image=self.image_aquiles_menu)
        self.canvas_abre.tag_bind(self.img_aquiles_id, '<Button-1>', lambda event: (self.on_button_click_personagem("achilles"),  self.canvas_abre.itemconfig(self.img_aquiles_id, image=self.image_aquiles_click)))
        self.canvas_abre.tag_bind(self.img_aquiles_id, '<Enter>', lambda event: self.canvas_abre.itemconfig(self.img_aquiles_id, image=self.image_aquiles_hover))
        self.canvas_abre.tag_bind(self.img_aquiles_id, '<Leave>', lambda event: self.canvas_abre.itemconfig(self.img_aquiles_id, image=self.image_aquiles_menu))

        label_botao_aquiles = ctk.CTkLabel(
            self.root,
            text="Achilles",
            text_color='white',
            bg_color="black",
            font=("Gelio Fasolada", 18)
        )
        label_botao_aquiles.place(x=160, y=290, anchor="n")
        self.widgets_dinamicos.append(label_botao_aquiles)

        # Botão Atalanta
        self.image_atalanta_menu = PhotoImage(file="images/carinha_atalanta_menu.png")
        self.image_atalanta_hover = PhotoImage(file="images/carinha_atalanta_hover.png")
        self.image_atalanta_click = PhotoImage(file="images/carinha_atalanta_click.png")

        self.img_atalanta_id = self.canvas_abre.create_image(520, 240, image=self.image_atalanta_menu)
        self.canvas_abre.tag_bind(self.img_atalanta_id, '<Button-1>', lambda event: (self.on_button_click_personagem("atalanta"), self.canvas_abre.itemconfig(self.img_atalanta_id, image=self.image_atalanta_click)))
        self.canvas_abre.tag_bind(self.img_atalanta_id, '<Enter>', lambda event: self.canvas_abre.itemconfig(self.img_atalanta_id, image=self.image_atalanta_hover))
        self.canvas_abre.tag_bind(self.img_atalanta_id, '<Leave>', lambda event: self.canvas_abre.itemconfig(self.img_atalanta_id, image=self.image_atalanta_menu))
                
        label_botao_atalanta = ctk.CTkLabel(
            self.root,
            text="Atalanta",
            text_color='white',
            bg_color="black",
            font=("Gelio Fasolada", 18)
        )
        label_botao_atalanta.place(x=520, y=290, anchor="n")
        self.widgets_dinamicos.append(label_botao_atalanta)

        # Botão Theseus
        self.image_teseu_menu = PhotoImage(file="images/carinha_teseu_menu.png")
        self.image_teseu_hover = PhotoImage(file="images/carinha_teseu_hover.png")
        self.image_teseu_click = PhotoImage(file="images/carinha_teseu_click.png")

        self.img_teseu_id = self.canvas_abre.create_image(640, 240, image=self.image_teseu_menu)
        self.canvas_abre.tag_bind(self.img_teseu_id, '<Button-1>', lambda event: (self.on_button_click_personagem("theseus"), self.canvas_abre.itemconfig(self.img_teseu_id, image=self.image_teseu_click)))
        self.canvas_abre.tag_bind(self.img_teseu_id, '<Enter>', lambda event: self.canvas_abre.itemconfig(self.img_teseu_id, image=self.image_teseu_hover))
        self.canvas_abre.tag_bind(self.img_teseu_id, '<Leave>', lambda event: self.canvas_abre.itemconfig(self.img_teseu_id, image=self.image_teseu_menu))

        label_botao_teseu = ctk.CTkLabel(
            self.root,
            text="Theseus",
            text_color='white',
            bg_color="black",
            font=("Gelio Fasolada", 18)
        )
        label_botao_teseu.place(x=640, y=290, anchor="n")
        self.widgets_dinamicos.append(label_botao_teseu)
                        
        # CARTAS   # CARTAS   # CARTAS   # CARTAS   # CARTAS        
         # Escolha uma carta
        self.canvas_abre.create_text(
        400,  
        365,   
        text= "Click on a card to draw your starting card", 
        fill='#FF8C00',  # Cor do texto RGB color: 255/255, 140/255, 0/255, 1  # DarkOrange
        font=("Gelio Fasolada", 16),  
        anchor="center") 
        
        # Carta 1
        self.image_carta_escolha_menu1 = PhotoImage(file="images/carta_escolha_menu.png")
        self.image_carta_escolha_hover1 = PhotoImage(file="images/carta_escolha_hover.png")
        self.image_carta_escolha_click1 = PhotoImage(file="images/carta_escolha_click.png")

        self.img_carta_escolhida_id1 = self.canvas_abre.create_image(280, 470, image=self.image_carta_escolha_menu1)
        # Passando o número 1 para identificar a carta 1
        self.canvas_abre.tag_bind(self.img_carta_escolhida_id1, '<Button-1>', lambda event: self.on_button_click_carta(1))  
        self.canvas_abre.tag_bind(self.img_carta_escolhida_id1, '<Enter>', lambda event: self.canvas_abre.itemconfig(self.img_carta_escolhida_id1 , image=self.image_carta_escolha_hover1))
        self.canvas_abre.tag_bind(self.img_carta_escolhida_id1, '<Leave>', lambda event: self.canvas_abre.itemconfig(self.img_carta_escolhida_id1 , image=self.image_carta_escolha_menu1))
        
        # Carta 2
        self.image_carta_escolha_menu2 = PhotoImage(file="images/carta_escolha_menu.png")
        self.image_carta_escolha_hover2 = PhotoImage(file="images/carta_escolha_hover.png")
        self.image_carta_escolha_click2 = PhotoImage(file="images/carta_escolha_click.png")

        self.img_carta_escolhida_id2 = self.canvas_abre.create_image(400, 470, image=self.image_carta_escolha_menu2)
        # Passando o número 2 para identificar a carta 2
        self.canvas_abre.tag_bind(self.img_carta_escolhida_id2, '<Button-1>', lambda event: self.on_button_click_carta(2))  
        self.canvas_abre.tag_bind(self.img_carta_escolhida_id2, '<Enter>', lambda event: self.canvas_abre.itemconfig(self.img_carta_escolhida_id2 , image=self.image_carta_escolha_hover2))
        self.canvas_abre.tag_bind(self.img_carta_escolhida_id2, '<Leave>', lambda event: self.canvas_abre.itemconfig(self.img_carta_escolhida_id2 , image=self.image_carta_escolha_menu2))

        # Carta 3
        self.image_carta_escolha_menu3 = PhotoImage(file="images/carta_escolha_menu.png")
        self.image_carta_escolha_hover3 = PhotoImage(file="images/carta_escolha_hover.png")
        self.image_carta_escolha_click3 = PhotoImage(file="images/carta_escolha_click.png")

        self.img_carta_escolhida_id3 = self.canvas_abre.create_image(520, 470, image=self.image_carta_escolha_menu3)
        # Passando o número 3 para identificar a carta 3
        self.canvas_abre.tag_bind(self.img_carta_escolhida_id3, '<Button-1>', lambda event: self.on_button_click_carta(3))  
        self.canvas_abre.tag_bind(self.img_carta_escolhida_id3, '<Enter>', lambda event: self.canvas_abre.itemconfig(self.img_carta_escolhida_id3 , image=self.image_carta_escolha_hover3))
        self.canvas_abre.tag_bind(self.img_carta_escolhida_id3, '<Leave>', lambda event: self.canvas_abre.itemconfig(self.img_carta_escolhida_id3 , image=self.image_carta_escolha_menu3))

        # Botão de voltar
        botao_voltar = ctk.CTkButton(
        self.canvas_abre,
        width=50,
        fg_color='black',
        border_width= 1,
        border_color= "white",
        hover_color="black",
        text="<-",
        font=("Gelio Fasolada", 25),
        command=lambda: self.tela_01()        
        )
        botao_voltar.place(x=20, y=550)
        self.widgets_dinamicos.append(botao_voltar)

    # Botão de avançar
        botao_avancar = ctk.CTkButton(
        self.canvas_abre,
        width=50,
        fg_color='black',
        border_width= 1,
        border_color= "white",
        hover_color="black",
        text="->",
        font=("Gelio Fasolada", 25),
        command=lambda: self.tela_03()        
        )
        botao_avancar.place(x=730, y=550)
        self.widgets_dinamicos.append(botao_avancar)


    def tela_03(self):
        self.canvas_abre = Canvas(self.root, width=800, height=600, bg="black", bd=0, highlightthickness=0)
        self.canvas_abre.place(x=0, y=0) 
        self.widgets_dinamicos.append(self.canvas_abre)
            
        # Botão de voltar
        botao_voltar = ctk.CTkButton(
        self.canvas_abre,
        width=50,
        fg_color='black',
        border_width= 1,
        border_color= "white",
        hover_color="black",
        text="<-",
        font=("Gelio Fasolada", 25),
        command=lambda: self.tela_02()       
        )
        botao_voltar.place(x=20, y=550)
        self.widgets_dinamicos.append(botao_voltar)
        
        # Botão de PLAY
        botao_start = ctk.CTkButton(
            self.canvas_abre,
            width=100,
            fg_color='#FF0000',
            hover_color="#FFA500",
            text="START GAME",
            font=("Gelio Fasolada", 20),
            command=lambda: self.tela_jogo.tela_game() # vai pra Tela de jogo e carregga a primeira imagem e carta escolhida
        )
        botao_start.place(x=400, y=550, anchor="n")
        self.widgets_dinamicos.append(botao_start)
                
         # Botão de sair
        botao_avancar = ctk.CTkButton(
        self.canvas_abre,
        width=50,
        fg_color='black',
        border_width= 1,
        border_color= "white",
        hover_color="black",
        text="EXIT",
        font=("Gelio Fasolada", 18),
        command=lambda: self.interface_jogo.sair_jogo()# Função de saída!!!!
        )
        botao_avancar.place(x=730, y=550)
        self.widgets_dinamicos.append(botao_avancar)
        
        # Titulo                
        label_titulo = ctk.CTkLabel(
            self.root,
            text= "Ascent To Olympus",
            text_color='#DAA520',  # Cor do texto amarela
            bg_color="black",  
            font=("Gelio Fasolada", 28))           
        label_titulo.place(relx=0.5, y=10, anchor="n")
        self.widgets_dinamicos.append(label_titulo)       
        # SubTitulo    
        label_subtitulo = ctk.CTkLabel(
            self.root,
            text= "The Ancient Greek Game",
            text_color='#FF0000',  # Cor do texto vermelho
            bg_color="black",
            font=("Gelio Greek Diner", 17) )                   
        label_subtitulo.place(relx=0.5, y=40, anchor="n")
        self.widgets_dinamicos.append(label_subtitulo)       
        # Linha           
        self.canvas_abre.create_text(
            400,  
            75,   
            text="<><><><><><><><><><><><><><><><><><><><><><><><><><><><>",  
            fill='#B8860B',  # Cor do texto RGB color: 184/255, 134/255, 11/255, 1
            font=("Arial", 12), 
            anchor="center")  

        # Imagem Carinha Tela 3
        try:
            print(f"Tentando carregar imagem: {self.back_end.personagem_escolhido_imagem}")
            self.image_carinha_jogador = PhotoImage(file=self.back_end.personagem_escolhido_imagem)
            self.img_carinha = self.canvas_abre.create_image(230, 165, image=self.image_carinha_jogador)
            print(f"Debug Tela 3, imagem selecionada: {self.back_end.personagem_escolhido_imagem}") 
        except Exception as e:
            print(f"Erro ao carregar imagem selecionada: {e}")
            self.image_carinha_jogador = PhotoImage(file="images/carinha_default.png")
            self.img_carinha = self.canvas_abre.create_image(230, 165, image=self.image_carinha_jogador)
                    
        # Titulo nome  player             
        label_titulo_nome = ctk.CTkLabel(
            self.root,
            text= (f"Your player is: {self.back_end.personagem_escolhido_nome}"), 
            text_color='#FF8C00',  # Cor 255/255, 140/255, 0/255, 1  # DarkOrange
            bg_color="black",  
            font=("Gelio Fasolada", 22),
            )            
        label_titulo_nome.place(x=480, y=100, anchor="n") 
        self.widgets_dinamicos.append(label_titulo_nome)
        
        # Texto player   - ABOUT     
        texto_player = self.back_end.personagem_escolhido_about

        # Descrição do jogador
        label_descricao_player = ctk.CTkLabel(
            self.root,
            text=texto_player, 
            text_color="white",  
            fg_color="black", 
            font=("Cambria", 17), 
        )
        label_descricao_player.place(x=480, y=130, anchor="n")
        self.widgets_dinamicos.append(label_descricao_player)
    
    # Titulo carta              
        label_titulo_carta = ctk.CTkLabel(
            self.root,
            text= (f'Your initial card is: {self.back_end.carta_inicial[0]["nome"]}'), 
            text_color='#FF8C00',  # Cor 255/255, 140/255, 0/255, 1  # DarkOrange
            bg_color="black",  
            font=("Gelio Fasolada", 22),
            anchor="w", ) 
           
        label_titulo_carta.place(x=400, y=240, anchor="n")
        self.widgets_dinamicos.append(label_titulo_carta)
        
        # Texto carta     
        texto_carta = f'Card abilities: {self.back_end.carta_inicial[0]["action"]} '# ex.: "Card abilities: Advance 6 spaces, or roll 2 dice"      
          
        label_descricao_carta = ctk.CTkLabel(
            self.root,
            text= texto_carta, 
            text_color='white', 
            bg_color="black",  
            font=("Cambria", 17) ) 
           
        label_descricao_carta.place(x=400, y=265, anchor="n") 
        self.widgets_dinamicos.append(label_descricao_carta)
        
        # Imagem Carta
        try:
            # Verifica se o caminho da imagem está definido e tenta carregá-lo
            caminho_imagem = self.back_end.carta_inicial[0].get("imagem", None)
            if not caminho_imagem:
                raise ValueError("Caminho da imagem está indefinido ou inválido.")
            
            print(f"Tentando carregar imagem: {caminho_imagem}")
            # Tenta abrir e redimensionar a imagem
            imagem_original = Image.open(caminho_imagem)
            imagem_redimensionada = imagem_original.resize((130, 200), Image.Resampling.LANCZOS)
            self.image_carta_jogador = ImageTk.PhotoImage(imagem_redimensionada)
            self.img_carta_layout = self.canvas_abre.create_image(400, 400, image=self.image_carta_jogador)

        except Exception as e:
            print(f"Erro ao carregar imagem: {e}. Substituindo pela imagem padrão.")
            # Carrega a imagem padrão em caso de erro
            self.image_carta_jogador = PhotoImage(file="images/carta_default.png")
            self.img_carta_layout = self.canvas_abre.create_image(400, 400, image=self.image_carta_jogador)

        # Linha           
        self.canvas_abre.create_text(
            400,  
            520,   
            text="<><><><><><><><><><><><><><><><><><><><><><><><><><><><>",  
            fill='#B8860B',  # Cor do texto RGB color: 184/255, 134/255, 11/255, 1
            font=("Arial", 12), 
            anchor="center")        
 