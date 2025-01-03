# Tela onde o jogo se desenrola - By Bressar
# criado:  20/12/24
# atualizado: 03/01/25

import tkinter as tk
from tkinter import font
from tkinter import filedialog, messagebox, Label, Tk, Canvas, PhotoImage
import customtkinter as ctk
from customtkinter import CTkImage, CTkFont 
from PIL import Image, ImageDraw, ImageFont, ImageTk
import random
from back_end import Back_End

class Tela_Jogo:
    def __init__(self, root, telas_iniciais, interface_jogo, back_end):
        self.root = root  # Referência à janela principal
        self.interface_jogo = interface_jogo  # Referência à instância de Interface_Jogo
        self.telas_iniciais = telas_iniciais   # Referência à instância de Telas    
        self.back_end = back_end  #  Back_End 
        self.canvas_abre = None  # Inicialmente vazio
        self.back_end.load_fonts()       
        self.root.configure(bg="black")
        self.cor_Layout = self.back_end.cor_layout_atual # busca a cor do layout do backend
        # para evitar erros na atualização das labels das cartinhas
        self.label_carta_menu1 = None
        self.label_carta_menu2 = None
        self.label_carta_menu3 = None
        self.imagem_dado = "images/dado_grego.gif"
        self.widgets_dinamicos = []  # Lista para armazenar widgets dinâmicos
        self.widgets_casa_atual = [] # widgets para as casas
        self.image_referencias_cartas = []  # Lista para manter referências às imagens das cartas
        

    def limpar_referencias_cartas(self):# Método de limpeza PARA AS CARTINHAS QUE NÂO ATUALIZAVAM.....
        self.image_referencias_cartas.clear()
        
                    
    # def atualizar_cor(self, nova_cor):
    #     self.cor_Layout = nova_cor
    #     self.atualizar_tela()
   
    
    def play_gif(self):# Reproduz a animação do GIF no canvas
        if not hasattr(self, "image_on_canvas") or self.image_on_canvas is None: # verifica o canvas
            print("Erro: 'image_on_canvas' não foi inicializado!")
            return
        if self.animacao_ativa:
            if self.current_frame < len(self.frames):
                self.canvas.itemconfig(self.image_on_canvas, image=self.frames[self.current_frame])
                self.current_frame += 1
                self.root.after(500, self.play_gif)  # Controla a velocidade da animação
            else:
                self.current_frame = 0  # Reinicia o índice para repetir


    def limpar_widgets_casa_atual(self): # Limpa os widgets da casa atual, incluindo o canvas e a imagem do dado.
        for widget in self.widgets_casa_atual:
            widget.destroy()
        # Se o canvas ainda estiver presente, é destruido
        if hasattr(self, 'canvas') and self.canvas:
            self.canvas.destroy()
            self.canvas = None
        # Certifica que nenhuma imagem estática ou GIF fique referenciada
        if hasattr(self, 'image_on_canvas') and self.image_on_canvas:
            self.image_on_canvas = None
        
        self.widgets_casa_atual = [] # Limpa a lista de widgets dinâmicos da casa atual

    # removi o o game win!! 
    def atualizar_estado_jogo(self): # """Atualiza os estados do jogo e verifica condições de vitória ou derrota.
        estado = self.back_end.verificar_condicoes()  # Verifica o estado do jogo
        print(f"Estado do jogo: {estado}")  # Debug
        
        if estado == "game_over":
            self.game_over()
        # elif estado == "game_win":
        #     self.game_win()        
        else:
            print("O jogo continua...") # Debug


    def game_over(self): #  """Exibe a tela de Game Over e encerra o jogo principal, mantendo apenas a mensagem.
        # Fecha a janela principal
        self.root.destroy()
        # Cria a janela de mensagem
        janela_game_over = ctk.CTk()
        janela_game_over.title("Game Over")
        janela_game_over.geometry("250x150")
        janela_game_over.configure(fg_color="black") 
        janela_game_over.wm_attributes("-topmost", True)
               

        texto = ctk.CTkLabel(
            janela_game_over,
            text="You lost\nall your lives.\nGame over.",
            text_color="red",
            font=("Gelio Fasolada", 20),
            justify="center"
        )
        texto.place(relx=0.5, rely=0.4, anchor="center")

        botao_encerrar = ctk.CTkButton(
            janela_game_over,
            width= 40,
            text="EXIT",
            font=("Gelio Fasolada", 16),
            fg_color="darkred",
            text_color="white",
            hover_color="red",
            command=janela_game_over.destroy  # Fecha apenas a janela de mensagem
        )
        botao_encerrar.place(relx=0.5, rely=0.8, anchor="center")

        janela_game_over.mainloop() # Mantém a janela de mensagem aberta

    # Removi a função.... deixar o placar na opção do final...
    def game_win(self): # """Exibe a tela de vitória e encerra o jogo.
        janela_game_win = ctk.CTkToplevel(self.root)
        janela_game_win.title("Game Win")
        janela_game_win.geometry("250x150")
        janela_game_win.configure(fg_color="black")
        janela_game_win.wm_attributes("-topmost", True)

        texto = ctk.CTkLabel(
            janela_game_win,
            text="Congratulations!\nYou win!",
            text_color="green",
            font=("Gelio Fasolada", 20),
            justify="center" )
        texto.place(relx=0.5, rely=0.4, anchor="center")

        botao_encerrar = ctk.CTkButton(
            janela_game_win,
            text="Quer gravar o placar",
            width= 40,
            font=("Gelio Fasolada", 16),
            fg_color="darkgreen",
            text_color="white",
            hover_color="green",
            command=self.casa_evento_126() #self.root.destroy  # Fecha o root ao clicar no botão
        )
        botao_encerrar.place(relx=0.5, rely=0.8, anchor="center")

     
# TELA ONDE O JOGO É EXIBIDO !! # TELA ONDE O JOGO É EXIBIDO !! # TELA ONDE O JOGO É EXIBIDO !! 
    def tela_game(self):
        self.canvas_abre = Canvas(self.root, width=800, height=600, bg="black", bd=0, highlightthickness=0)
        self.canvas_abre.place(x=0, y=0) 
        self.widgets_dinamicos.append(self.canvas_abre)
        
        self.limpar_referencias_cartas() # Limpa referências antigas de imagens de cartas
                    
        # Imagem Tijolinho 
        self.atualizar_tijolos() # atualiza as cores dos tijolos
        self.image_tijolinho = PhotoImage(file=self.back_end.tijolos_cor_atual) # Variável dinâmica
        self.img_tijolinho = self.canvas_abre.create_image(400, 25, image=self.image_tijolinho)
        
        print(f"Debug classe Tela Jogo: {self.back_end.personagem_escolhido_imagem}") 
        # Imagem Carinha Tela Jogo
        try:    
            imagem_original = Image.open(self.back_end.personagem_escolhido_imagem)
            imagem_redimensionada = imagem_original.resize((125, 125), Image.Resampling.LANCZOS)
            self.image_carinha_jogador = ImageTk.PhotoImage(imagem_redimensionada)       
            self.img_carinha = self.canvas_abre.create_image(80, 155, image=self.image_carinha_jogador)
            print(f"Personagem selecionado: {self.back_end.personagem_escolhido_imagem}") 
        except Exception as e:
            print(f"Erro ao carregar imagem selecionada do personagem: {e}")
            self.image_carinha_jogador = PhotoImage(file="images/carinha_default_menor.png")
            self.img_carinha = self.canvas_abre.create_image(80, 155, image=self.image_carinha_jogador)      
                
        # Nome do caboclinho              
        self.label_titulo_nome = ctk.CTkLabel(
            self.root,
            text= self.back_end.personagem_escolhido_nome, 
            text_color= "white",  
            bg_color="black",  
            font=("Gelio Fasolada", 21),)            
        self.label_titulo_nome.place(x=80, y=75, anchor="center")
        self.widgets_dinamicos.append(self.label_titulo_nome)                
         # VIDAS           
        self.label_xp = ctk.CTkLabel(
            self.root,
            text= f"Lives: {str(self.back_end.player_xp)}", 
            text_color=self.cor_Layout,  
            bg_color="black",  
            font=("Gelio Fasolada", 18),)            
        self.label_xp.place(x=335, y=60) 
        self.widgets_dinamicos.append(self.label_xp) 
                 
        # PONTOS            
        self.label_pontos = ctk.CTkLabel(
            self.root,
            text= f"POINTS: {self.back_end.player_pontos}", 
            text_color=self.cor_Layout, # self.cor_Layout
            bg_color="black",  
            font=("Gelio Fasolada", 18),)            
        self.label_pontos.place(x=430, y=60, )
        self.widgets_dinamicos.append(self.label_pontos)
                
        # Você está na CASA numero_X
        self.label_esta_na_casa = ctk.CTkLabel(
            self.root,
            text= f"You are\non space:",
            text_color=self.cor_Layout,  
            bg_color="black",  
            font=("Gelio Fasolada", 18), )            
        self.label_esta_na_casa .place(x=200, y=140, anchor='center') 
        self.widgets_dinamicos.append(self.label_esta_na_casa )
        # CASA ATUAL        
        self.label_numero_casa_atual = ctk.CTkLabel(
            self.root,
            text= f"{self.back_end.casa_atual}",
            text_color='white',  
            bg_color="black",  
            font=("Gelio Fasolada", 22),
            )            
        self.label_numero_casa_atual .place(x=200, y=180, anchor='center') 
        self.widgets_dinamicos.append(self.label_numero_casa_atual)
         #linha               
        self.canvas_abre.create_text(
            150,  
            230,  
            text="<><><><><><><><><><><><><><><><>", 
            fill='gray', 
            font=("Arial", 12), 
            anchor="center")  
           
        # CARTAS  # CARTAS  # CARTAS  # CARTAS # CARTAS # CARTAS # CARTAS # CARTAS  
                
        self.label_cartas = ctk.CTkLabel(
            self.root,
            text= "Your Cards:", 
            text_color="white", 
            bg_color="black",  
            font=("Gelio Fasolada", 16),
            )            
        self.label_cartas.place(x=10, y=240) 
        self.widgets_dinamicos.append(self.label_cartas)
                 
        # cartas pequenas
         # Carta 1
        if len(self.back_end.cartas_player) >= 1:
            self.image_carta_menu1 = PhotoImage(file=self.back_end.cartas_player[0]["imagem_pequena"])
            self.image_referencias_cartas.append(self.image_carta_menu1)  # Guarda referência
           
            self.label_carta_menu1 = ctk.CTkLabel(
            self.root,
            text= self.back_end.cartas_player[0]["action_p"], # Variável de sistema
            text_color= self.cor_Layout, #'white',  
            bg_color="black",  
            font=("cambria", 14) )            
            self.label_carta_menu1.place(x=50, y=395, anchor='n' ) # relx=0.5, y=10, anchor="n"
            self.widgets_dinamicos.append(self.label_carta_menu1)            
        else:
            self.image_carta_menu1 = PhotoImage(file="images/carta_menu.png")
        self.img_carta_id1 = self.canvas_abre.create_image(50, 330, image=self.image_carta_menu1)

        # Carta 2
        if len(self.back_end.cartas_player) >= 2:
            self.image_carta_menu2 = PhotoImage(file=self.back_end.cartas_player[1]["imagem_pequena"])        
            self.image_referencias_cartas.append(self.image_carta_menu2)   # Guarda referência
   
            self.label_carta_menu2 = ctk.CTkLabel(
            self.root,
            text= self.back_end.cartas_player[1]["action_p"], # Variável de sistema
            text_color= self.cor_Layout, #'white',  
            bg_color="black",  
            font=("cambria", 14),)            
            self.label_carta_menu2.place(x=150, y=395, anchor='n' ) # relx=0.5, y=10, anchor="n"
            self.widgets_dinamicos.append(self.label_carta_menu2)           
        else:
            self.image_carta_menu2 = PhotoImage(file="images/carta_menu.png")
        self.img_carta_id2 = self.canvas_abre.create_image(150, 330, image=self.image_carta_menu2)

        # Carta 3
        if len(self.back_end.cartas_player) == 3:
            self.image_carta_menu3 = PhotoImage(file=self.back_end.cartas_player[2]["imagem_pequena"])            
            self.image_referencias_cartas.append(self.image_carta_menu3) # Guarda a referencia
            
            self.label_carta_menu3 = ctk.CTkLabel(
            self.root,
            text= self.back_end.cartas_player[2]["action_p"], # Variável de sistema
            text_color= self.cor_Layout, #'white',  
            bg_color="black",  
            font=("cambria", 14))            
            self.label_carta_menu3.place(x=250, y=395, anchor='n' ) # relx=0.5, y=10, anchor="n"
            self.widgets_dinamicos.append(self.label_carta_menu3)            
        else:
            self.image_carta_menu3 = PhotoImage(file="images/carta_menu.png")
        self.img_carta_id3 = self.canvas_abre.create_image(250, 330, image=self.image_carta_menu3)
 

        # CASAS TABULEIRO  # CASAS TABULEIRO  # CASAS TABULEIRO  # CASAS TABULEIRO  # CASAS TABULEIRO  # CASAS TABULEIRO
  
        # Chama a função exibir_casas do back_end para obter os 8 itens da lista de casas 
        self.casas_exibidas = self.exibir_casas(self.back_end.casas)        
        print(f'Lista de casas que a função retorna  {self.casas_exibidas}') # for debug
        
         # Imagem casa 1
        self.casa_1_lista = PhotoImage(file= self.casas_exibidas[0]["imagem"]) 
        self.img_casa_1_lista = self.canvas_abre.create_image(50, 520, image=self.casa_1_lista)       
         # Imagem casa 2
        self.casa_2_lista = PhotoImage(file=self.casas_exibidas[1]["imagem"])  
        self.img_casa_2_lista = self.canvas_abre.create_image(150, 520, image=self.casa_2_lista)
        # Imagem casa 3
        self.casa_3_lista = PhotoImage(file=self.casas_exibidas[2]["imagem"]) 
        self.img_casa_3_lista = self.canvas_abre.create_image(250, 520, image=self.casa_3_lista)       
        # Imagem casa 4
        self.casa_4_lista = PhotoImage(file=self.casas_exibidas[3]["imagem"])  
        self.img_casa_4_lista = self.canvas_abre.create_image(350, 520, image=self.casa_4_lista)
        # Imagem casa 5
        self.casa_5_lista = PhotoImage(file=self.casas_exibidas[4]["imagem"]) 
        self.img_casa_5_lista = self.canvas_abre.create_image(450, 520, image=self.casa_5_lista)
        # Imagem casa 6
        self.casa_6_lista = PhotoImage(file=self.casas_exibidas[5]["imagem"])  
        self.img_casa_6_lista = self.canvas_abre.create_image(550, 520, image=self.casa_6_lista)
        # Imagem casa 7
        self.casa_7_lista = PhotoImage(file=self.casas_exibidas[6]["imagem"])  
        self.img_casa_7_lista = self.canvas_abre.create_image(650, 520, image=self.casa_7_lista)      
        # Imagem casa 8
        self.casa_8_lista = PhotoImage(file=self.casas_exibidas[7]["imagem"])  
        self.img_casa_8_lista = self.canvas_abre.create_image(750, 520, image=self.casa_8_lista)

        # Lista de posições fixas no layout para as casas
        posicoes_x = [50, 150, 250, 350, 450, 550, 650, 750]  # As posições X para as 8 casas
        posicoes_y = 520  # Todas as casas têm a mesma posição Y fixada

        # Exibe cada uma das casas
        for i, casa in enumerate(self.casas_exibidas):
            # Cria o texto associado à casa
            label_nome_casa = ctk.CTkLabel(
                self.root,
                text=casa["texto"],  # Usando o texto da casa, que vem do dicionário
                text_color=self.cor_Layout,
                bg_color="black",  
                font=("Gelio Fasolada", 17),
            )
            label_nome_casa.place(x=posicoes_x[i], y=posicoes_y + 65, anchor="center")  # Posição fixa para o texto
            # Armazenando os widgets (imagem e label) para manipulação futura
            self.widgets_dinamicos.append(label_nome_casa)
        # Exibe para debug as casas que foram exibidas
        for casa in self.casas_exibidas:
            print(f"Casa {casa['numero']}: {casa['texto']} - {casa['imagem']}")
            

        # Botão de sair
        botao_sair = ctk.CTkButton(
        self.canvas_abre,
        width=40,
        height=20,
        fg_color='black',
        border_width= 1,
        text_color= "white",
        border_color= "white",
        hover_color="red",
        text="EXIT",
        font=("Gelio Fasolada", 14),
        command=lambda: self.interface_jogo.sair_jogo()
        )
        botao_sair.place(x=750, y=60)
        self.widgets_dinamicos.append(botao_sair)
                
        # Linhas
        self.canvas_abre.create_text(
            550,  
            100,  
            text="<><><><><><><><><><><><><><><><><><><><><><><><>", 
            fill='gray',  # #B8860B' dourado
            font=("Arial", 12), 
            anchor="center")  

        self.canvas_abre.create_text(
            550,  
            450,  
            text="<><><><><><><><><><><><><><><><><><><><><><><><>", 
            fill='gray', # self.cor_Layout
            font=("Arial", 12), 
            anchor="center")  
                
        # PRIMEIRA TELA EXIBIDA
        self.casa_evento_001()# Abre o jogo com a primeira casa   

          
    def exibir_casas(self, lista_maior): # O número sorteado define de onde os 8 itens devem começar        
        # Número esteja entre 1 e 128
        if self.back_end.casa_atual < 1 or self.back_end.casa_atual> 128:
            raise ValueError("O número deve estar entre 1 e 128.") # For DEBUG
        
        # Calcular o índice de início para a exibição de 8 itens
        inicio = self.back_end.casa_atual - 1  # O índice começa de 0, então subtrai 1
        
        # Garantir que o início não ultrapasse o limite de 120 elementos
        fim = inicio + 8
        
        # Se o fim ultrapassar 128, ajustamos para pegar até o fim da lista
        if fim > len(lista_maior):
            fim = len(lista_maior)
            
         # Calcular o início para garantir que sempre mostremos 8 elementos (se possível)
        if fim - inicio < 8:  # Se o número de elementos a ser exibido for menor que 8
            inicio = max(fim - 8, 0)  # Ajusta o início para que tenha 8 itens (ou menos no final)
        
        # Pega os 8 itens ou até o fim da lista
        lista_exibida = lista_maior[inicio:fim]
        
        # Retorna os 8 itens para serem exibidos
        return lista_exibida
    
       
    def atualizar_tijolos(self):
        if self.back_end.casa_atual <= 16:
            self.back_end.tijolos_cor_atual = self.back_end.tijolos_cor["azul"]
        elif self.back_end.casa_atual <= 31:
            self.back_end.tijolos_cor_atual = self.back_end.tijolos_cor["verde"]
        elif self.back_end.casa_atual <= 48:
            self.back_end.tijolos_cor_atual = self.back_end.tijolos_cor["amarelo"]
        elif self.back_end.casa_atual <= 63:
            self.back_end.tijolos_cor_atual = self.back_end.tijolos_cor["laranja"]
        elif self.back_end.casa_atual <= 80:
            self.back_end.tijolos_cor_atual = self.back_end.tijolos_cor["vermelho"]
        elif self.back_end.casa_atual <= 95:
            self.back_end.tijolos_cor_atual = self.back_end.tijolos_cor["rosa"]
        elif self.back_end.casa_atual <= 111:
            self.back_end.tijolos_cor_atual = self.back_end.tijolos_cor["roxo"]
        elif self.back_end.casa_atual <= 120:
            self.back_end.tijolos_cor_atual = self.back_end.tijolos_cor["agua"]

                    
    def atualizar_cor_layout(self):
        if self.back_end.casa_atual <= 16:
            self.back_end.cor_layout_atual = self.back_end.cores_layout["azul"]
        elif self.back_end.casa_atual <= 32:
            self.back_end.cor_layout_atual = self.back_end.cores_layout["verde"]
        elif self.back_end.casa_atual <= 48:
            self.back_end.cor_layout_atual = self.back_end.cores_layout["amarelo"]
        elif self.back_end.casa_atual <= 64:
            self.back_end.cor_layout_atual = self.back_end.cores_layout["laranja"]
        elif self.back_end.casa_atual <= 80:
            self.back_end.cor_layout_atual = self.back_end.cores_layout["vermelho"]
        elif self.back_end.casa_atual <= 95:
            self.back_end.cor_layout_atual = self.back_end.cores_layout["rosa"]
        elif self.back_end.casa_atual <= 112:
            self.back_end.cor_layout_atual = self.back_end.cores_layout["roxo"]
        elif self.back_end.casa_atual <= 120:
            self.back_end.cor_layout_atual = self.back_end.cores_layout["agua"]
            
        self.cor_Layout = self.back_end.cor_layout_atual


    # def rolar_dado_sem_delay(self):
    #         # Sorteia um número entre 1 e 6
    #         numero_sorteado = random.randint(1, 6) #
    #         print(f'Número sorteado: {numero_sorteado}')
            
    #         # atualiza a imagem em movimento por uma imagem estatica do resultado
    #         self.imagem_dado = f"images/dado{numero_sorteado}.png"
                                   
    #         # Atualiza o Canvas com a nova imagem
    #         nova_imagem = Image.open(self.imagem_dado).resize((80, 80), Image.Resampling.LANCZOS)
    #         self.imagem_estatica = ImageTk.PhotoImage(nova_imagem)
    #         self.canvas.itemconfig(self.image_on_canvas, image=self.imagem_estatica)
              
    #         # Atualiza os pontos e a posição do jogador         
    #         self.back_end.player_pontos +=  (15 * numero_sorteado)
    #         print(f'Pontos do jogador: {self.back_end.player_pontos}')           
    #         print(f'Casas do tabuleiro no momento:{self.casas_exibidas}')   
    #         self.back_end.casa_atual += numero_sorteado 
            
    #         self.interface_jogo.atualizar_estado_jogo() # verica o termino do jogo
            
                       
    #         print(f'Casa atual: {self.back_end.casa_atual}')
            
    #         # Introduz um atraso de 1 segundos antes de continuar
    #         self.root.after(1000, lambda: self._continuar_rolagem_dado())

    #         # Limpa widgets existentes antes de atualizar a tela
    #         self.limpar_widgets_casa_atual()
            
    #         self.atualizar_tela()# Atualiza outros elementos da tela 
            
    #         # Carrega os gadgets da nova casa
    #         self.carregar_casa(self.back_end.casa_atual)


    def atualizar_tela(self):
        """Atualiza os widgets e elementos gráficos baseados nas variáveis do backend."""  
        # Atualiza a cor do layout antes de usá-la
        self.atualizar_cor_layout()  # Atualiza a cor do layout com o valor do backend
        self.atualizar_tijolos()  # Atualiza a cor do tijolinho no  backend
        self.atualizar_imagem_tijolo()  # Atualiza a imagem no Canvas  
    
        
        # Atualizar a lista de casas exibidas
        self.casas_exibidas = self.exibir_casas(self.back_end.casas)
        if not self.casas_exibidas or len(self.casas_exibidas) < 8:
            print("Erro: A lista de casas exibidas está incompleta ou vazia.")
            return
        
       # Verificar se os widgets ainda existem antes de configurá-los
       # labels de texto
        if hasattr(self, 'label_titulo_nome') and self.label_titulo_nome.winfo_exists():
            self.label_titulo_nome.configure(text= (self.back_end.personagem_escolhido_nome), text_color="white")

        if hasattr(self, 'label_pontos') and self.label_pontos.winfo_exists():
            self.label_pontos.configure(text=f"POINTS: {self.back_end.player_pontos}", text_color=self.cor_Layout)

        if hasattr(self, 'label_xp') and self.label_xp.winfo_exists():
            self.label_xp.configure(text=f"Lives: {str(self.back_end.player_xp)}",text_color=self.cor_Layout)
            
        if hasattr(self, 'label_esta_na_casa') and self.label_esta_na_casa.winfo_exists():
            self.label_esta_na_casa.configure(text=f"You are\non space:",text_color=self.cor_Layout) 
            
        if hasattr(self, 'label_numero_casa_atual') and self.label_numero_casa_atual.winfo_exists():
            self.label_numero_casa_atual.configure(text=f"{self.back_end.casa_atual}",text_color="white")
            
        if hasattr(self, 'label_cartas') and self.label_cartas.winfo_exists():
            self.label_cartas.configure(text="Your Cards:",text_color="white")
            
         # Atualizar as cartas do jogador
        num_cartas = len(self.back_end.cartas_player)
        
            # Atualiza a carta 1
        if self.label_carta_menu1 and self.label_carta_menu1.winfo_exists():
            if num_cartas >= 1:
                self.label_carta_menu1.configure(
                    text=self.back_end.cartas_player[0]["action_p"],
                    text_color=self.cor_Layout
                )
            else:
                self.label_carta_menu1.configure(
                    text=" ",
                    text_color="black"
                )

        # Atualiza a carta 2
        if self.label_carta_menu2 and self.label_carta_menu2.winfo_exists():
            if num_cartas >= 2:
                self.label_carta_menu2.configure(
                    text=self.back_end.cartas_player[1]["action_p"],
                    text_color=self.cor_Layout
                )
            else:
                self.label_carta_menu2.configure(
                    text=" ",
                    text_color="black"
                )

        # Atualiza a carta 3
        if self.label_carta_menu3 and self.label_carta_menu3.winfo_exists():
            if num_cartas >= 3:
                self.label_carta_menu3.configure(
                    text=self.back_end.cartas_player[2]["action_p"],
                    text_color=self.cor_Layout
                )
            else:
                self.label_carta_menu3.configure(
                    text=" ",
                    text_color="black"
            )    
        # cartinhas
        # if self.label_carta_menu1 and self.label_carta_menu1.winfo_exists():
        #     self.label_carta_menu1.configure(text=self.back_end.cartas_player[0]["action_p"], text_color=self.cor_Layout) 
            
        # if self.label_carta_menu2 and self.label_carta_menu2.winfo_exists():
        #     self.label_carta_menu2.configure(text=self.back_end.cartas_player[1]["action_p"], text_color=self.cor_Layout)  
        
        # if self.label_carta_menu3 and self.label_carta_menu3.winfo_exists():
        #     self.label_carta_menu3.configure(text=self.back_end.cartas_player[2]["action_p"], text_color=self.cor_Layout)  
        

        # Atualizar a cor de fundo de todos os labels
        for widget in self.widgets_dinamicos:
            if isinstance(widget, ctk.CTkLabel):
                # Atualiza a cor do texto e do fundo de todos os labels
                widget.configure(bg_color="black",)  #text_color=self.cor_Layout
                               
        for widget in self.widgets_dinamicos:
            if isinstance(widget, ctk.CTkLabel) and widget not in [self.label_pontos, self.label_xp, self.label_titulo_nome,self.label_cartas,
                                                                   self.label_carta_menu1, self.label_carta_menu2, self.label_carta_menu3,
                                                                   self.label_esta_na_casa, self.label_numero_casa_atual]:
                widget.destroy()
                self.widgets_dinamicos = [self.label_pontos, self.label_xp, self.label_titulo_nome, self.label_cartas,
                                          self.label_carta_menu1, self.label_carta_menu2, self.label_carta_menu3,
                                          self.label_esta_na_casa, self.label_numero_casa_atual]  # Mantém as labels na lista

        # Atualiza as imagens das casas
        for i, casa in enumerate(self.casas_exibidas):
            nova_imagem = PhotoImage(file=casa["imagem"])
            try:
                if i == 0:
                    self.canvas_abre.itemconfig(self.img_casa_1_lista, image=nova_imagem)
                    self.casa_1_lista = nova_imagem
                elif i == 1:
                    self.canvas_abre.itemconfig(self.img_casa_2_lista, image=nova_imagem)
                    self.casa_2_lista = nova_imagem
                elif i == 2:
                    self.canvas_abre.itemconfig(self.img_casa_3_lista, image=nova_imagem)
                    self.casa_3_lista = nova_imagem
                elif i == 3:
                    self.canvas_abre.itemconfig(self.img_casa_4_lista, image=nova_imagem)
                    self.casa_4_lista = nova_imagem
                elif i == 4:
                    self.canvas_abre.itemconfig(self.img_casa_5_lista, image=nova_imagem)
                    self.casa_5_lista = nova_imagem
                elif i == 5:
                    self.canvas_abre.itemconfig(self.img_casa_6_lista, image=nova_imagem)
                    self.casa_6_lista = nova_imagem
                elif i == 6:
                    self.canvas_abre.itemconfig(self.img_casa_7_lista, image=nova_imagem)
                    self.casa_7_lista = nova_imagem
                elif i == 7:
                    self.canvas_abre.itemconfig(self.img_casa_8_lista, image=nova_imagem)
                    self.casa_8_lista = nova_imagem
            except Exception as e:
                print(f"Erro ao atualizar imagem da casa {i + 1}: {e}")

        # Lista de posições fixas no layout para as casas
        posicoes_x = [50, 150, 250, 350, 450, 550, 650, 750]  # As posições X para as 8 casas
        posicoes_y = 520  # Todas as casas têm a mesma posição Y fixada

        # Criando e posicionando manualmente cada label
        for i, casa in enumerate(self.casas_exibidas):
            if casa["texto"]:  # Apenas cria labels para casas com texto
                try:
                    label_nome_casa = ctk.CTkLabel(
                        self.root,
                        text=casa["texto"],  # Usando o texto da casa
                        text_color=self.cor_Layout,  # Cor do texto layout
                        bg_color="black",  
                        font=("Gelio Fasolada", 17),
                    )
                    label_nome_casa.place(x=posicoes_x[i], y=posicoes_y + 65, anchor="center")  # Posição fixa para o texto
                    self.widgets_dinamicos.append(label_nome_casa)  # Adiciona o label para controle futuro
                except Exception as e:
                    print(f"Erro ao criar label para a casa {i + 1}: {e}")


    def atualizar_imagem_tijolo(self):
        """Atualiza dinamicamente a imagem do tijolinho no Canvas baseado no valor de tijolos_cor_atual."""
        try:
            # Atualiza as cores dos tijolos com base no backend
            self.atualizar_tijolos()  # Chama a função que ajusta a cor atual dos tijolos no backend
            
            # Cria a nova imagem para o tijolinho com a cor definida
            self.image_tijolinho = PhotoImage(file=self.back_end.tijolos_cor_atual)  # Foto da cor atual dos tijolos
            
            # Se a imagem do tijolinho já existe no canvas, apenas a atualiza
            if hasattr(self, 'img_tijolinho') and self.canvas_abre.find_withtag("tijolinho"):
                self.canvas_abre.itemconfig(self.img_tijolinho, image=self.image_tijolinho)
            else:
                # Caso não exista, cria a imagem do tijolinho no canvas
                self.img_tijolinho = self.canvas_abre.create_image(400, 25, image=self.image_tijolinho, tags="tijolinho")
        
        except Exception as e:
            print(f"Erro ao atualizar a imagem dos tijolinhos: {e}")
      
    # Jogo até a casa 120, depois disso é função de back...
    def carregar_casa(self, casa_atual):# Carrega os widgets da casa especificada.
        
        self.limpar_widgets_casa_atual() # Limpa os widgets da casa anterior

        # Carrega os widgets específicos para a nova casa
        if casa_atual == 1:
            self.casa_evento_001()
        elif casa_atual == 2:
            self.casa_evento_002()
        elif casa_atual == 3:
            self.casa_evento_003()
        elif casa_atual == 4:
            self.casa_evento_004()
        elif casa_atual == 5:
            self.casa_evento_005()
        elif casa_atual == 6:
            self.casa_evento_006()
        elif casa_atual == 7:
            self.casa_evento_007()
        elif casa_atual == 8:
            self.casa_evento_008()
        elif casa_atual == 9:
            self.casa_evento_009()
        elif casa_atual == 10:
            self.casa_evento_010()
        elif casa_atual == 11:
            self.casa_evento_011()
        elif casa_atual == 12:
            self.casa_evento_012()
        elif casa_atual == 13:
            self.casa_evento_013()
        elif casa_atual == 14:
            self.casa_evento_014()
        elif casa_atual == 15:
            self.casa_evento_015()
        elif casa_atual == 16:
            self.casa_evento_016()
        elif casa_atual == 17:
            self.casa_evento_017()
        elif casa_atual == 18:
            self.casa_evento_018()
        elif casa_atual == 19:
            self.casa_evento_019()
        elif casa_atual == 20:
            self.casa_evento_020()
        elif casa_atual == 21:
            self.casa_evento_021()
        elif casa_atual == 22:
            self.casa_evento_022()
        elif casa_atual == 23:
            self.casa_evento_023()
        elif casa_atual == 24:
            self.casa_evento_024()
        elif casa_atual == 25:
            self.casa_evento_025()
        elif casa_atual == 26:
            self.casa_evento_026()
        elif casa_atual == 27:
            self.casa_evento_027()
        elif casa_atual == 28:
            self.casa_evento_028()
        elif casa_atual == 29:
            self.casa_evento_029()
        elif casa_atual == 30:
            self.casa_evento_030()
        elif casa_atual == 31:
            self.casa_evento_031()
        elif casa_atual == 32:
            self.casa_evento_032()
        elif casa_atual == 33:
            self.casa_evento_033()
        elif casa_atual == 34:
            self.casa_evento_034()
        elif casa_atual == 35:
            self.casa_evento_035()
        elif casa_atual == 36:
            self.casa_evento_036()
        elif casa_atual == 37:
            self.casa_evento_037()
        elif casa_atual == 38:
            self.casa_evento_038()
        elif casa_atual == 39:
            self.casa_evento_039()
        elif casa_atual == 40:
            self.casa_evento_040()
        elif casa_atual == 41:
            self.casa_evento_041()
        elif casa_atual == 42:
            self.casa_evento_042()
        elif casa_atual == 43:
            self.casa_evento_043()
        elif casa_atual == 44:
            self.casa_evento_044()
        elif casa_atual == 45:
            self.casa_evento_045()
        elif casa_atual == 46:
            self.casa_evento_046()
        elif casa_atual == 47:
            self.casa_evento_047()
        elif casa_atual == 48:
            self.casa_evento_048()
        elif casa_atual == 49:
            self.casa_evento_049()
        elif casa_atual == 50:
            self.casa_evento_050()
        elif casa_atual == 51:
            self.casa_evento_051()
        elif casa_atual == 52:
            self.casa_evento_052()
        elif casa_atual == 53:
            self.casa_evento_053()
        elif casa_atual == 54:
            self.casa_evento_054()
        elif casa_atual == 55:
            self.casa_evento_055()
        elif casa_atual == 56:
            self.casa_evento_056()
        elif casa_atual == 57:
            self.casa_evento_057()
        elif casa_atual == 58:
            self.casa_evento_058()
        elif casa_atual == 59:
            self.casa_evento_059()
        elif casa_atual == 60:
            self.casa_evento_060()
        elif casa_atual == 61:
            self.casa_evento_061()
        elif casa_atual == 62:
            self.casa_evento_062()
        elif casa_atual == 63:
            self.casa_evento_063()
        elif casa_atual == 64:
            self.casa_evento_064()
        elif casa_atual == 65:
            self.casa_evento_065()
        elif casa_atual == 66:
            self.casa_evento_066()
        elif casa_atual == 67:
            self.casa_evento_067()
        elif casa_atual == 68:
            self.casa_evento_068()
        elif casa_atual == 69:
            self.casa_evento_069()
        elif casa_atual == 70:
            self.casa_evento_070()
        elif casa_atual == 71:
            self.casa_evento_071()
        elif casa_atual == 72:
            self.casa_evento_072()
        elif casa_atual == 73:
            self.casa_evento_073()
        elif casa_atual == 74:
            self.casa_evento_074()
        elif casa_atual == 75:
            self.casa_evento_075()
        elif casa_atual == 76:
            self.casa_evento_076()
        elif casa_atual == 77:
            self.casa_evento_077()
        elif casa_atual == 78:
            self.casa_evento_078()
        elif casa_atual == 79:
            self.casa_evento_079()
        elif casa_atual == 80:
            self.casa_evento_080()
        elif casa_atual == 81:
            self.casa_evento_081()
        elif casa_atual == 82:
            self.casa_evento_082()
        elif casa_atual == 83:
            self.casa_evento_083()
        elif casa_atual == 84:
            self.casa_evento_084()
        elif casa_atual == 85:
            self.casa_evento_085()
        elif casa_atual == 86:
            self.casa_evento_086()
        elif casa_atual == 87:
            self.casa_evento_087()
        elif casa_atual == 88:
            self.casa_evento_088()
        elif casa_atual == 89:
            self.casa_evento_089()
        elif casa_atual == 90:
            self.casa_evento_090()
        elif casa_atual == 91:
            self.casa_evento_091()
        elif casa_atual == 92:
            self.casa_evento_092()
        elif casa_atual == 93:
            self.casa_evento_093()
        elif casa_atual == 94:
            self.casa_evento_094()
        elif casa_atual == 95:
            self.casa_evento_095()
        elif casa_atual == 96:
            self.casa_evento_096()
        elif casa_atual == 97:
            self.casa_evento_097()
        elif casa_atual == 98:
            self.casa_evento_098()
        elif casa_atual == 99:
            self.casa_evento_099()
        elif casa_atual == 100:
            self.casa_evento_100()
        elif casa_atual == 101:
            self.casa_evento_101()
        elif casa_atual == 102:
            self.casa_evento_102()
        elif casa_atual == 103:
            self.casa_evento_103()
        elif casa_atual == 104:
            self.casa_evento_104()
        elif casa_atual == 105:
            self.casa_evento_105()
        elif casa_atual == 106:
            self.casa_evento_106()
        elif casa_atual == 107:
            self.casa_evento_107()
        elif casa_atual == 108:
            self.casa_evento_108()
        elif casa_atual == 109:
            self.casa_evento_109()
        elif casa_atual == 110:
            self.casa_evento_110()
        elif casa_atual == 111:
            self.casa_evento_111()
        elif casa_atual == 112:
            self.casa_evento_112()
        elif casa_atual == 113:
            self.casa_evento_113()
        elif casa_atual == 114:
            self.casa_evento_114()
        elif casa_atual == 115:
            self.casa_evento_115()
        elif casa_atual == 116:
            self.casa_evento_116()
        elif casa_atual == 117:
            self.casa_evento_117()
        elif casa_atual == 118:
            self.casa_evento_118()
        elif casa_atual == 119:
            self.casa_evento_119()
        elif casa_atual == 120:
            self.casa_evento_120()
        elif casa_atual == 121:
            self.casa_evento_121()
        elif casa_atual == 122:
            self.casa_evento_122()
        elif casa_atual == 123:
            self.casa_evento_123()
        elif casa_atual == 124:
            self.casa_evento_124()
        elif casa_atual == 125:
            self.casa_evento_125()
        elif casa_atual == 126:
            self.casa_evento_126()

        else:
            print(f"Nenhum evento configurado para a casa {casa_atual}.")


    def atualizar_cartas(self): # atualiza a referencia das cartinhas
        self.limpar_referencias_cartas()
        self.tela_game()  # Rechama a lógica para redesenhar as cartas
        

# ROLAR DADOS ANDAR  CASAS NO TABULEIRO
    def rolar_dado(self):
        # Para a animação do GIF
        self.animacao_ativa = False
        
        # Sorteia um número entre 1 e 6
        numero_sorteado = random.randint(1, 6) # random.choice([4]) # random.randint(1, 6)
        print(f'Número sorteado: {numero_sorteado}')
        
        # Atualiza a imagem em movimento por uma imagem estática do resultado
        self.imagem_dado = f"images/dado{numero_sorteado}.png"
        nova_imagem = Image.open(self.imagem_dado).resize((80, 80), Image.Resampling.LANCZOS)
        self.imagem_estatica = ImageTk.PhotoImage(nova_imagem)
        self.canvas.itemconfig(self.image_on_canvas, image=self.imagem_estatica)  # Exibe a imagem estática imediatamente
        
        # Introduz um atraso de 1.5 segundos antes de continuar
        self.root.after(1500, lambda: self._continuar_rolagem_dado(numero_sorteado))

        
    def _continuar_rolagem_dado(self, numero_sorteado): # """Continua as ações após exibir a imagem estática por 1.5 segundos."""
        # Atualiza os pontos e a posição do jogador
        self.back_end.player_pontos += (15 * numero_sorteado)
        print(f'Pontos do jogador: {self.back_end.player_pontos}') # debug
        print(f'Casas do tabuleiro no momento: {self.casas_exibidas}') # debug
        self.back_end.casa_atual += numero_sorteado       
        print(f'Casa atual: {self.back_end.casa_atual}') # debug
                
        self.limpar_widgets_casa_atual() # Limpa widgets existentes antes de atualizar a tela
        self.atualizar_tela()  # Atualiza outros elementos da tela
        self.carregar_casa(self.back_end.casa_atual)  # Carrega os gadgets da nova casa        
        self.atualizar_estado_jogo() # verica o termino do jogo


# FUNÇÕES DADOS DE BATALHAS E EVENTOS
    def rolar_dado_de_batalha(self, casas_avanco=0, casas_retrocesso=0, vida=0):
#        Lógica da batalha: sorteia o número do dado, exibe o resultado e processa a batalha.
        self.animacao_ativa = False # Para a animação do GIF
        print(f'Pontos do jogador antes da batalha: {self.back_end.player_pontos}')  # Debug
        # Sorteia um número entre 1 e 6
        numero_sorteado = random.randint(1, 6)
        print(f'Número sorteado em batalha: {numero_sorteado}')
        # Verifica vitória ou derrota
        vitoria = numero_sorteado > 3
        print(f'Resultado: {numero_sorteado}, vitória: {vitoria}')  # Debug
        # Atualiza a imagem em movimento por uma imagem estática do resultado
        self.imagem_dado = f"images/dado{numero_sorteado}.png"
        nova_imagem = Image.open(self.imagem_dado).resize((80, 80), Image.Resampling.LANCZOS)
        self.imagem_estatica = ImageTk.PhotoImage(nova_imagem)
        self.canvas.itemconfig(self.image_on_canvas, image=self.imagem_estatica)  # Exibe a imagem estática imediatamente
        # Introduz um atraso de 1.5 segundos antes de processar o resultado
        self.root.after(1500, lambda: self._processar_resultado_batalha(numero_sorteado, casas_avanco, casas_retrocesso, vida))
        

    def mostrar_mensagem_vitoria_ou_derrota(self, titulo, mensagem, duracao): # abre a janelinha GANHOU! / PERDEU!
        """Exibe uma janela de mensagem temporária."""
        janela_mensagem = tk.Toplevel()
        janela_mensagem.title(titulo)
        janela_mensagem.geometry("250x150")
        janela_mensagem.configure(bg="black")
        janela_mensagem.wm_attributes("-topmost", True)  # Mantém a janela no topo
        
        # Texto da mensagem
        label = tk.Label(
            janela_mensagem, 
            text=mensagem, 
            fg= self.cor_Layout, # white
            bg="black", 
            font=("Gelio Fasolada", 13), 
            justify="center"
        )
        label.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Fecha automaticamente após `duracao` milissegundos
        janela_mensagem.after(duracao, janela_mensagem.destroy)



    def _processar_resultado_batalha(self, numero_sorteado, casas_avanco, casas_retrocesso, vida):
    # Processa o resultado da batalha após exibir a imagem do dado.
        vitoria = numero_sorteado > 3
        # Pontos, avanço ou retrocesso de acordo com o resultado da batalha
        if vitoria:
            self.back_end.player_pontos += (15 * casas_avanco) + 30  # Vitória
            self.back_end.casa_atual += casas_avanco
            print('Você VENCEU!') # debug back_end
            # messagebox implantar aqui 
            # You win!
            # 'go to space {casa_atual}'! fica aberta 1 segundo e fecha
            
        else:
            self.back_end.player_pontos -= ((15 * casas_retrocesso) + 30)  # Derrota
            self.back_end.casa_atual -= casas_retrocesso
            self.back_end.player_xp -= vida  # Perde vida se aplicável
            print('Você PERDEU!') # debug back_end
            # messagebox implantar aqui! fica aberta 1 segundo e fecha
            # You Lose!
            # Go back to space {casa_atual} 
            # if self.back_end.player_xp -= vida == True: # Perde vida se aplicável
            # You lose 1 life, restam {self.back_end.player_xp}

        print(f'Pontos do jogador depois da batalha: {self.back_end.player_pontos}')  # Debug
        print(f'Casa atual depois da batalha: {self.back_end.casa_atual}')
        
        
        # Uso dentro da função _processar_resultado_batalha
        if vitoria:
            self.mostrar_mensagem_vitoria_ou_derrota(
                "Victory!", 
                f"""You won!
                
Advance to
space {self.back_end.casa_atual}.""", 
                duracao=2000  # 2 segundos
            )
        else:
            mensagem = (
                f"You lost!"
                f"\nGo back to\nspace {self.back_end.casa_atual}.\n"
            )
            if self.back_end.player_xp > 0:
                mensagem += f"\nYou lost 1 life.\n{self.back_end.player_xp} lives remaining."
            else:
                mensagem += "\nYou lost all your lives."
            
            self.mostrar_mensagem_vitoria_ou_derrota(
                "Defeat!\n", 
                mensagem, 
                duracao=3000  # 3 segundos
            )

        # Atualiza a interface
        self.limpar_widgets_casa_atual()
        self.atualizar_tela()
        self.carregar_casa(self.back_end.casa_atual)        
        self.atualizar_estado_jogo() # verica o termino do jogo
             






    def chamada_do_dado_batalha(self, casas_avanco=0, casas_retrocesso=0, vida=0):
        # Ganha +4
        self.label_4_mais = ctk.CTkLabel(
            self.root,
            text= "+4", 
            text_color= 'green',  
            bg_color= "black",  
            font=("Gelio Fasolada", 18),
            )          
        self.label_4_mais.place(x=460, y=330, anchor="n") # relx=0.5, y=10, anchor="n"
        self.widgets_casa_atual.append(self.label_4_mais)
       # Perde -3
        self.label_4_mais = ctk.CTkLabel(
            self.root,
            text= "-3", 
            text_color= 'red',  
            bg_color= "black",  
            font=("Gelio Fasolada", 18),
            )          
        self.label_4_mais.place(x=460, y=355, anchor="n") # relx=0.5, y=10, anchor="n"
        self.widgets_casa_atual.append(self.label_4_mais)
        
        # OU...             
        self.label_ou = ctk.CTkLabel(
                    self.root,
                    text= "OR", 
                    text_color= self.back_end.cor_layout_atual,  
                    bg_color= "black",  
                    font=("Gelio Fasolada", 22),
                    )          
        self.label_ou.place(x=520, y=405, anchor="n") # relx=0.5, y=10, anchor="n"
        self.widgets_casa_atual.append(self.label_ou)
               
    # Configura o dado no canvas e exibe o botão de rolar.
        self.animacao_ativa = True
        # Canvas para o dado
        self.canvas = tk.Canvas(self.root, width=80, height=80, bg="black", highlightthickness=0)
        self.canvas.place(x=400, y=320, anchor='n')  # Posição do dado
        self.widgets_casa_atual.append(self.canvas)  # Adiciona o canvas à lista
        # Carrega o GIF com PIL
        self.gif = Image.open(self.imagem_dado)
        self.frames = []
        # Extrai os quadros do GIF
        try:
            while True:
                frame = self.gif.copy()
                frame = frame.convert("RGBA")  # Certificar-se de que está em RGBA
                # Adicionar fundo preto onde há transparência
                black_bg = Image.new("RGBA", frame.size, "black")
                frame = Image.alpha_composite(black_bg, frame)
                # Redimensionar o quadro
                frame = frame.resize((80, 80), Image.Resampling.LANCZOS)
                # Converter para PhotoImage
                self.frames.append(ImageTk.PhotoImage(frame))
                self.gif.seek(len(self.frames))  # Avançar para o próximo quadro
        except EOFError:
            pass  # Final do GIF
        # Configuração inicial do Canvas
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor="nw", image=self.frames[0])
        self.current_frame = 0       
        self.play_gif()# Exibe a animação
        # Botão de rolagem de dados
        botao_rolar_dados = ctk.CTkButton(
            self.canvas_abre,
            fg_color='black',
            width=100,
            border_width=1,
            border_color="white",
            hover_color=self.back_end.cor_layout_atual,
            text="Roll a die!",
            font=("Gelio Greek Diner", 18),
            command=lambda: (self.rolar_dado_de_batalha(casas_avanco, casas_retrocesso, vida)) # determina o que dado faz
        )
        botao_rolar_dados.place(x=400, y=405, anchor='n')
        self.widgets_casa_atual.append(botao_rolar_dados)


    def chamada_do_dado_batalha_troia(self, casas_avanco=0, casas_retrocesso=0, vida=0):
        # Ganha +4
        self.label_4_mais = ctk.CTkLabel(
            self.root,
            text= "+4", 
            text_color= 'green',  
            bg_color= "black",  
            font=("Gelio Fasolada", 18),
            )          
        self.label_4_mais.place(x=710, y=330, anchor="n") # relx=0.5, y=10, anchor="n"
        self.widgets_casa_atual.append(self.label_4_mais)
       # Perde -3
        self.label_4_mais = ctk.CTkLabel(
            self.root,
            text= "-3", 
            text_color= 'red',  
            bg_color= "black",  
            font=("Gelio Fasolada", 18),
            )          
        self.label_4_mais.place(x=710, y=355, anchor="n") # relx=0.5, y=10, anchor="n"
        self.widgets_casa_atual.append(self.label_4_mais)
           
    # Configura o dado no canvas e exibe o botão de rolar.
        self.animacao_ativa = True
        # Canvas para o dado
        self.canvas = tk.Canvas(self.root, width=80, height=80, bg="black", highlightthickness=0)
        self.canvas.place(x=650, y=320, anchor='n')  # Posição do dado
        self.widgets_casa_atual.append(self.canvas)  # Adiciona o canvas à lista
        # Carrega o GIF com PIL
        self.gif = Image.open(self.imagem_dado)
        self.frames = []
        # Extrai os quadros do GIF
        try:
            while True:
                frame = self.gif.copy()
                frame = frame.convert("RGBA")  # Certificar-se de que está em RGBA
                # Adicionar fundo preto onde há transparência
                black_bg = Image.new("RGBA", frame.size, "black")
                frame = Image.alpha_composite(black_bg, frame)
                # Redimensionar o quadro
                frame = frame.resize((80, 80), Image.Resampling.LANCZOS)
                # Converter para PhotoImage
                self.frames.append(ImageTk.PhotoImage(frame))
                self.gif.seek(len(self.frames))  # Avançar para o próximo quadro
        except EOFError:
            pass  # Final do GIF
        # Configuração inicial do Canvas
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor="nw", image=self.frames[0])
        self.current_frame = 0       
        self.play_gif()# Exibe a animação
        # Botão de rolagem de dados
        botao_rolar_dados = ctk.CTkButton(
            self.canvas_abre,
            fg_color='black',
            width=100,
            border_width=1,
            border_color="white",
            hover_color=self.back_end.cor_layout_atual,
            text="Roll a die!",
            font=("Gelio Greek Diner", 18),
            command=lambda: (self.rolar_dado_de_batalha(casas_avanco, casas_retrocesso, vida)) # determina o que dado faz
        )
        botao_rolar_dados.place(x=650, y=405, anchor='n')
        self.widgets_casa_atual.append(botao_rolar_dados)


    # FUNÇÃO VONTADE DOS DEUSES
    def vontade_dos_deuses(self, casas_avanco, casas_retrocesso, vida_mais, vida_menos, pontos_mais, pontos_menos):
        # pro bem
        self.back_end.casa_atual += casas_avanco 
        self.back_end.player_pontos += pontos_mais  
        self.back_end.player_xp += vida_mais
        # pro mal
        if self.back_end.casa_atual > 1:
            self.back_end.casa_atual -= casas_retrocesso
        self.back_end.player_pontos -= pontos_menos 
        self.back_end.player_xp -= vida_menos
        
        
        # TESTE DENTRO DESSA FUNÇÃO!!
        if casas_avanco  >= 1:
            self.mostrar_mensagem_vitoria_ou_derrota(
                "Advance!", 
                f"""The gods command:
                
Advance to
space {self.back_end.casa_atual}.""", 
                duracao=2000  # 2 segundos
            )

        elif casas_retrocesso >=1:
            mensagem = (
                f"The gods command:"
                f"\nGo back to\nspace {self.back_end.casa_atual}.\n"
            )
            if vida_menos >= 1:
                mensagem += f"\nYou lost 1 life.\n{self.back_end.player_xp} lives remaining."
            elif self.back_end.player_xp <= 0:
                mensagem += "\nYou lost all your lives."
                
            if vida_mais == 1:  
                mensagem += f"\nYou gain 1 life.\n{self.back_end.player_xp} lives remaining."  
            
            self.mostrar_mensagem_vitoria_ou_derrota(
                "Defeat!\n", 
                mensagem, 
                duracao=3000  # 3 segundos
            )
            
        # TESTE ATÉ AQUI!!!
          
        # Debug for Back end
        print(f'Pontos do jogador depois da vontade dos deuses: {self.back_end.player_pontos}') # Debug
        print(f'Casa atual depois da vontade dos deuses: {self.back_end.casa_atual}')# Debug
        # Atualiza a interface
        self.limpar_widgets_casa_atual()
        self.atualizar_tela()
        self.carregar_casa(self.back_end.casa_atual)       
        self.atualizar_estado_jogo() # verifica o termino do jogo
        
           
    def botao_vontade_dos_deuses(self, casas_avanco=0, casas_retrocesso=0, vida_mais=0, vida_menos=0, pontos_mais= 0, pontos_menos=0):
        # OU...             
        self.label_ou = ctk.CTkLabel(
                    self.root,
                    text= "OR", 
                    text_color= self.back_end.cor_layout_atual,  
                    bg_color= "black",  
                    font=("Gelio Fasolada", 22),
                    )          
        self.label_ou.place(x=540, y=370, anchor="n") 
        self.widgets_casa_atual.append(self.label_ou)
        
        botao_vontade_deuses = ctk.CTkButton(
            self.canvas_abre,
            fg_color='black',
            width=100,
            border_width=1,
            border_color="white",
            hover_color=self.back_end.cor_layout_atual,
            text="Submit to the\nwill of the gods",
            font=("Gelio Greek Diner", 18),
            command=lambda: (self.vontade_dos_deuses(casas_avanco, casas_retrocesso, vida_mais, vida_menos, pontos_mais, pontos_menos))
        )
        botao_vontade_deuses.place(x=420, y=360, anchor='n')
        self.widgets_casa_atual.append(botao_vontade_deuses)
    
        
    def usar_carta_da_mao(self, carta_numero=1):
        cartas_mao = self.back_end.cartas_player
        try:
             # Verifica se a carta existe na mão (índice válido)
            if carta_numero < 1 or carta_numero > len(cartas_mao):
                # Exibe uma mensagem de alerta caso o índice seja inválido
                messagebox.showerror("Error", "This position does not have any cards!")
                return
            
            nome_carta_escolhida = cartas_mao[carta_numero -1]['nome']
            print(f'Carta na posição str({carta_numero} -1): {nome_carta_escolhida}') # for debug
            
            if nome_carta_escolhida == "Aphrodite":
                self.use_carta_Aphrodite()
            elif nome_carta_escolhida == "Apollo":
                self.use_carta_Apollo()
            elif nome_carta_escolhida == "Artemis":
                self.use_carta_Artemis()
            elif nome_carta_escolhida == "Ares":
                self.use_carta_Ares()
            elif nome_carta_escolhida == "Hades":
                self.use_carta_Hades()                
            elif nome_carta_escolhida == "Hephaestus":
                self.use_carta_Hephaestus()
            elif nome_carta_escolhida == "Hera":
                self.use_carta_Hera()
            elif nome_carta_escolhida == "Hermes":
                self.use_carta_Hermes()
            elif nome_carta_escolhida == "Persephone":
                self.use_carta_Persephone()                 
            elif nome_carta_escolhida == "Poseidon":
                self.use_carta_Poseidon()       
            elif nome_carta_escolhida == "Zeus":
                self.use_carta_Zeus()
            elif nome_carta_escolhida == "Athena":
                self.use_carta_Athena()
            else:
                print(f"Carta {nome_carta_escolhida} não reconhecida.")  # For debug
                print(f"Não há cartas para usar...Lista vazia") # for backend Debug
        except Exception as e:
            print(f'Erro: {e}')
            messagebox.showerror("Erro", f"Ocorreu um erro ao tentar usar a carta: {e}")
                  
    # Menu fixo com o dado de rolagem mais escolha de cartas           
    def chamada_cartas_eventos(self):
        label_text_linha = ctk.CTkLabel(
        self.root,
        text="<><><><><><><><><><><><><><><><><><><><><><><><>",
        text_color="gray",
        font=("Arial", 16),
        bg_color= "black"
        )
        label_text_linha.place(x=550, y=310, anchor="center")
        self.widgets_casa_atual.append(label_text_linha)
                
        # Escolher carta
        self.botao_choose_card = ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 100,
        border_width= 1,
        border_color= "white",
        hover_color='black',
        text="Choose a card!",
        font=("Gelio Greek Diner", 18)
        )
        self.botao_choose_card.place(x=670, y=405, anchor='n')
        self.widgets_casa_atual.append(self.botao_choose_card) 
        
         # Botão carta 1
        botao_carta_1 = ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 48,
        height= 65,
        border_width= 1,
        border_color= "white",
        hover_color=self.back_end.cor_layout_atual,
        text="I",
        font=("Gelio Greek Diner", 24),
        command=lambda: self.usar_carta_da_mao(1) # função de abrir a carta do indice 0
        )
        botao_carta_1 .place(x=610, y=330, anchor='n')
        self.widgets_casa_atual.append(botao_carta_1 ) 
            
         # Botão carta 2
        botao_carta_2 = ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 48,
        height= 65,
        border_width= 1,
        border_color= "white",
        hover_color=self.back_end.cor_layout_atual,
        text="I I",
        font=("Gelio Greek Diner", 24),
        command=lambda: self.usar_carta_da_mao(2) # função de abrir a carta do indice 1
        )
        botao_carta_2 .place(x=670, y=330, anchor='n')
        self.widgets_casa_atual.append(botao_carta_2) 
        
         # Botão carta 3
        botao_carta_3 = ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 48,
        height= 65,
        border_width= 1,
        border_color= "white",
        hover_color=self.back_end.cor_layout_atual,
        text="I I I",
        font=("Gelio Greek Diner", 24),
        command=lambda: self.usar_carta_da_mao(3) # função de abrir a carta do indice 2
        )
        botao_carta_3 .place(x=730, y=330, anchor='n')
        self.widgets_casa_atual.append(botao_carta_3)


     

 # !!!!! EVENTOS DAS CASAS COMEÇAM AQUI !!!!!!!
 
    def casa_evento_001(self): # casa da abertura DADOS + CARTAS
         # Canvas para o dado
        self.canvas = tk.Canvas(self.root, width=80, height=80, bg="black", highlightthickness=0)
        self.canvas.place(x=550, y=120, anchor='n') # posição do dado
        self.widgets_casa_atual.append(self.canvas)  # Adiciona o canvas à lista
        # Carrega o GIF com PIL
        self.gif = Image.open(self.imagem_dado)
        self.frames = []
        # Extrai os quadros do GIF
        try:
            while True:
                frame = self.gif.copy()
                frame = frame.convert("RGBA")  # Certificar-se de que está em RGBA
                # Adicionar fundo preto onde há transparência
                black_bg = Image.new("RGBA", frame.size, "black")
                frame = Image.alpha_composite(black_bg, frame)
                # Redimensionar o quadro
                frame = frame.resize((80, 80), Image.Resampling.LANCZOS) # reduz a imagem pra 80 X 80
                # Converter para PhotoImage
                self.frames.append(ImageTk.PhotoImage(frame))
                self.gif.seek(len(self.frames))  # Avançar para o próximo quadro
        except EOFError:
            pass  # Final do GIF
          
        # Exibir o primeiro quadro
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor="nw", image=self.frames[0])        
        # Inicializa o índice do quadro
        self.current_frame = 0  
         # Ativa a animação
        self.animacao_ativa = True    
        # Exibe a animação
        self.play_gif()
         
        # Botão de rolagem de dados
        botao_rolar_dados = ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 100,
        border_width= 1,
        border_color= "white",
        hover_color=self.back_end.cor_layout_atual,
        text="Roll a die to move!",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.rolar_dado(), self.atualizar_tela()) # ROLAR DADO!!!
        )
        botao_rolar_dados.place(x=550, y=205, anchor='n')
        self.widgets_casa_atual.append(botao_rolar_dados)  # Adiciona o botão à lista
        
            #     # OU...             
        self.label_ou = ctk.CTkLabel(
                    self.root,
                    text= "OR", 
                    text_color= self.back_end.cor_layout_atual,  
                    bg_color= "black",  
                    font=("Gelio Fasolada", 22),
                    )          
        self.label_ou.place(x=550, y=260, anchor="n") # relx=0.5, y=10, anchor="n"
        self.widgets_casa_atual.append(self.label_ou)
        
         # Botão carta 1
        botao_carta_1 = ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 50,
        height= 80,
        border_width= 1,
        border_color= "white",
        hover_color=self.back_end.cor_layout_atual,
        text="I",
        font=("Gelio Greek Diner", 24),
        command=lambda: self.usar_carta_da_mao(1) # função de abrir a carta do indice 0
        )
        botao_carta_1 .place(x=480, y=305, anchor='n')
        self.widgets_casa_atual.append(botao_carta_1 )  # Adiciona o botão à lista 
            
         # Botão carta 2
        botao_carta_2 = ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 50,
        height= 80,
        border_width= 1,
        border_color= "white",
        hover_color=self.back_end.cor_layout_atual,
        text="I I",
        font=("Gelio Greek Diner", 24),
        command=lambda: self.usar_carta_da_mao(2) # função de abrir a carta do indice 0
        )
        botao_carta_2 .place(x=550, y=305, anchor='n')
        self.widgets_casa_atual.append(botao_carta_2)  # Adiciona o botão à lista 
        
         # Botão carta 3
        botao_carta_3 = ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 50,
        height= 80,
        border_width= 1,
        border_color= "white",
        hover_color=self.back_end.cor_layout_atual,
        text="I I I",
        font=("Gelio Greek Diner", 24),
        command=lambda: self.usar_carta_da_mao(3) # função de abrir a carta do indice 0
        )
        botao_carta_3 .place(x=620, y=305, anchor='n')
        self.widgets_casa_atual.append(botao_carta_3)  # Adiciona o botão à lista 
        
         # Escolher carta
        self.botao_choose_card = ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 100,
        border_width= 1,
        border_color= "white",
        hover_color='black',
        text="Choose a card!",
        font=("Gelio Greek Diner", 18)# ROLAR DADO!!!
        )
        self.botao_choose_card.place(x=550, y=400, anchor='n')
        self.widgets_casa_atual.append(self.botao_choose_card)  # Adiciona o botão à lista
        
                
    def casa_evento_002(self): # Carta HERMES
        self.limpar_widgets_casa_atual()
        
        try:
            # Carrega a imagem usando PIL
            img = Image.open(self.back_end.cartas_deuses[7]['imagem']) 
            # Converte a imagem para PhotoImage
            self.image_carta_exibida = ImageTk.PhotoImage(img)
            # Cria um Label para exibir a imagem no Canvas
            self.label_imagem_carta = tk.Label(self.canvas_abre, image=self.image_carta_exibida, bg="black")
            self.label_imagem_carta.place(x=440, y=130, anchor="n")
            # Adiciona o Label à lista de widgets dinâmicos
            self.widgets_casa_atual.append(self.label_imagem_carta)

        except Exception as e:
            print(f'Sem imagens nessa carta, usando a imagem default -> {e}')
               
        # label do nome da casa exibida
        label_descricao_carta1 = ctk.CTkLabel(
            self.root,
            text= 'Card abilities:',  # Substituir pelo texto dinâmico, 
            text_color=self.back_end.cor_layout_atual,  
            fg_color="black",  # Cor de fundo
            font=("Gelio Fasolada", 18), 
        )
        label_descricao_carta1.place(x=650, y=130, anchor ="n")
        self.widgets_casa_atual.append(label_descricao_carta1)
        
        """Exibe os widgets para o evento da Casa 002."""
        label_casa = ctk.CTkLabel(
            self.root,
            text= self.back_end.cartas_deuses[7]['action_p'],
            text_color="white",
            bg_color="black",
            font=("cambria", 18),
        )
        label_casa.place(x=650, y=160, anchor='n')
        self.widgets_casa_atual.append(label_casa)
        

        label_guardar_card_exibido = ctk.CTkLabel(
            self.root,
            text= "Do you keep the card?",  # Substituir pelo texto dinâmico, 
            text_color= self.back_end.cor_layout_atual,  
            fg_color="black",  # Cor de fundo
            font=("Gelio Fasolada", 17), # Gelio Fasolada
        )
        label_guardar_card_exibido.place(x=650, y=320, anchor ="center")
        self.widgets_casa_atual.append(label_guardar_card_exibido)
               
        # Botão SIM
        botao_sim_card = ctk.CTkButton(
        self.root,
        fg_color='black',
        width= 16,
        border_color= "white",
        border_width= 1,
        hover_color=self.back_end.cor_layout_atual,
        text="yes",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.back_end.adicionar_carta_a_cartas_player("Hermes"),
                         self.atualizar_cartas(),  # Atualiza imagens das cartas
                         self.limpar_widgets_casa_atual(),
                         self.casa_evento_001()) # acrescenta Hermes
        )
        botao_sim_card.place(x=600, y=360, anchor="center")
        self.widgets_casa_atual.append(botao_sim_card)
        
        # Botão NÃO
        botao_naum_card = ctk.CTkButton(
        self.root,
        fg_color='black',
        width= 16,
        border_color= "white",
        border_width= 1,
        hover_color="red",
        text="no",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.limpar_widgets_casa_atual(), self.casa_evento_001()) # abre pra jogar dado ou carta
        )
        botao_naum_card.place(x=700, y=360, anchor="center")
        self.widgets_casa_atual.append(botao_naum_card)    
        
      
    def casa_evento_003(self): # casa em branco
        self.limpar_widgets_casa_atual()        
        self.casa_evento_001()
               
    def casa_evento_004(self): # casa em branco
       self.limpar_widgets_casa_atual()        
       self.casa_evento_001()
       
    
    def casa_evento_005(self): # ESFINGE
        self.limpar_widgets_casa_atual()       
         # label do nome da casa exibida
        label_nome_casa_evento = ctk.CTkLabel(
            self.root,
            text= "Sphinx",  # Substituir pelo texto dinâmico, 
            text_color="white",  
            fg_color="black",  # Cor de fundo
            font=("Olympus", 24), 
        )
        label_nome_casa_evento.place(x=450, y=110, anchor ="n")
        self.widgets_casa_atual.append(label_nome_casa_evento)
        #IMAGEM DA CASA
        self.image_evento_exibido = PhotoImage(file="images/casa_005_esfinge.png")
        self.label_evento_exibido = tk.Label(
            self.root, 
            image=self.image_evento_exibido,
            bg="black"  
        )
        self.label_evento_exibido.place(x=450, y=140, anchor='n') 
        self.widgets_casa_atual.append(self.label_evento_exibido)

        texto_evento = ("""She asked you a question.
Solve the riddle and roll a die.
If you win,
move forward 2 spaces.
If you lose,
move back 2 spaces
and lose 1 life"""
        )
        # label de descrição do evento
        label_descricao_evento = ctk.CTkLabel(
            self.root,
            text=texto_evento, 
            text_color="white",  
            fg_color="black", 
            font=("Cambria", 17), 
        )
        label_descricao_evento.place(x=650, y=140, anchor ="n")
        self.widgets_casa_atual.append(label_descricao_evento)
        
        self.chamada_do_dado_batalha(casas_avanco=2, casas_retrocesso=2, vida=1)
        self.chamada_cartas_eventos()
        
      
    def casa_evento_006(self): # casa em branco
        self.limpar_widgets_casa_atual()        
        self.casa_evento_001()
               
    def casa_evento_007(self): # casa em branco
        self.limpar_widgets_casa_atual()        
        self.casa_evento_001() 
    
        
    def casa_evento_008(self): # PROMETEUS
        self.limpar_widgets_casa_atual()       
        # label do nome da casa exibida
        label_nome_casa_evento = ctk.CTkLabel(
            self.root,
            text= "Prometeus",  # Substituir pelo texto dinâmico, 
            text_color="white",  
            fg_color="black",  # Cor de fundo
            font=("Olympus", 24), 
        )
        label_nome_casa_evento.place(x=450, y=110, anchor ="n")
        self.widgets_casa_atual.append(label_nome_casa_evento)
        
        #IMAGEM DA CASA
        self.image_evento_exibido = PhotoImage(file="images/casa_008_prometeu.png")
        self.label_evento_exibido = tk.Label(
            self.root,  # Substitua por self.canvas_abre se quiser que o Label seja um filho do Canvas
            image=self.image_evento_exibido,
            bg="black"  # Define a cor de fundo do Label
        )
        self.label_evento_exibido.place(x=450, y=140, anchor='n')  # Posiciona o Label
        self.widgets_casa_atual.append(self.label_evento_exibido)

        texto_evento = ("""Watch the condemned Titan
in his punishment 
return 
2 spaces.
And lose
1 life"""
        )
        # label de descrição do evento
        label_descricao_evento = ctk.CTkLabel(
            self.root,
            text=texto_evento,  # Substituir pelo texto dinâmico, se necessário
            text_color="white",  
            fg_color="black",  # Cor de fundo
            font=("Cambria", 17), # "Gelio Fasolada"
        )
        label_descricao_evento.place(x=650, y=140, anchor ="n")
        self.widgets_casa_atual.append(label_descricao_evento)
        
        # evento da casa       
        # self.back_end.retornar_casas(numero_casas_retornar=2)

        self.botao_vontade_dos_deuses(casas_avanco=0, casas_retrocesso=2, vida_mais=0, vida_menos=1, pontos_mais= 0, pontos_menos=30)
        self.chamada_cartas_eventos()

                 
    def casa_evento_009(self): # casa em branco
        self.limpar_widgets_casa_atual()        
        self.casa_evento_001()   
     
        
    def casa_evento_010(self): # ESPARTA
        self.limpar_widgets_casa_atual()       
            # label do nome da casa exibida
        label_nome_casa_evento = ctk.CTkLabel(
            self.root,
            text= "Sparta",  # Substituir pelo texto dinâmico, 
            text_color="white",  
            fg_color="black",  # Cor de fundo
            font=("Olympus", 24), 
            )
        label_nome_casa_evento.place(x=450, y=110, anchor ="n")
        self.widgets_casa_atual.append(label_nome_casa_evento)
            
            #IMAGEM DA CASA
        self.image_evento_exibido = PhotoImage(file="images/casa_010_esparta.png")
        self.label_evento_exibido = tk.Label(
                self.root,  # Substitua por self.canvas_abre se quiser que o Label seja um filho do Canvas
                image=self.image_evento_exibido,
                bg="black"  # Define a cor de fundo do Label
            )
        self.label_evento_exibido.place(x=450, y=140, anchor='n')  # Posiciona o Label
        self.widgets_casa_atual.append(self.label_evento_exibido)

        texto_evento = ("""The Spartans
don't like strangers!
Fight for your life.

If you win,
advance 2 spaces.
If you lose,
lose 1 life."""
        )
        # label de descrição do evento
        label_descricao_evento = ctk.CTkLabel(
            self.root,
            text=texto_evento,  # Substituir pelo texto dinâmico, se necessário
            text_color="white",  
            fg_color="black",  # Cor de fundo
            font=("Cambria", 17), # "Gelio Fasolada"
        )
        label_descricao_evento.place(x=650, y=140, anchor ="n")
        self.widgets_casa_atual.append(label_descricao_evento)
        
        self.chamada_do_dado_batalha(casas_avanco=2, casas_retrocesso=1, vida=1)
        self.chamada_cartas_eventos()

     
    def casa_evento_011(self): # casa em branco
        self.limpar_widgets_casa_atual()        
        self.casa_evento_001() 
        
    def casa_evento_012(self): # casa em branco
        self.limpar_widgets_casa_atual()        
        self.casa_evento_001() 
        
        
    def casa_evento_013(self): # HESTIA
        self.limpar_widgets_casa_atual()       
            # label do nome da casa exibida
        label_nome_casa_evento = ctk.CTkLabel(
            self.root,
            text= "Hestia",  # Substituir pelo texto dinâmico, 
            text_color="white",  
            fg_color="black",  # Cor de fundo
            font=("Olympus", 24), 
            )
        label_nome_casa_evento.place(x=450, y=110, anchor ="n")
        self.widgets_casa_atual.append(label_nome_casa_evento)
            
            #IMAGEM DA CASA
        self.image_evento_exibido = PhotoImage(file="images/casa_013_hestia.png")
        self.label_evento_exibido = tk.Label(
                self.root,  # Substitua por self.canvas_abre se quiser que o Label seja um filho do Canvas
                image=self.image_evento_exibido,
                bg="black"  # Define a cor de fundo do Label
            )
        self.label_evento_exibido.place(x=450, y=140, anchor='n')  # Posiciona o Label
        self.widgets_casa_atual.append(self.label_evento_exibido)

        texto_evento = ("""Back 1 space

and assist
the Goddess
with her hearth."""
        )
        # label de descrição do evento
        label_descricao_evento = ctk.CTkLabel(
            self.root,
            text=texto_evento,  # Substituir pelo texto dinâmico, se necessário
            text_color="white",  
            fg_color="black",  # Cor de fundo
            font=("Cambria", 17), # "Gelio Fasolada"
        )
        label_descricao_evento.place(x=650, y=140, anchor ="n")
        self.widgets_casa_atual.append(label_descricao_evento)
        
        self.botao_vontade_dos_deuses(casas_avanco=0, casas_retrocesso=1, vida_mais=0, vida_menos=0, pontos_mais= 0, pontos_menos=15)
        self.chamada_cartas_eventos()
          
            
    def casa_evento_014(self): # casa em branco
        self.limpar_widgets_casa_atual()        
        self.casa_evento_001() 

    def casa_evento_015(self): # casa em branco
        self.limpar_widgets_casa_atual()        
        self.casa_evento_001() 
        
    def casa_evento_016(self): # casa em branco
        self.limpar_widgets_casa_atual()        
        self.casa_evento_001() 
        
                    
    def casa_evento_017(self): # QUIMERA
        self.limpar_widgets_casa_atual()       
            # label do nome da casa exibida
        label_nome_casa_evento = ctk.CTkLabel(
            self.root,
            text= "Chimera",  # Substituir pelo texto dinâmico, 
            text_color="white",  
            fg_color="black",  # Cor de fundo
            font=("Olympus", 24), 
            )
        label_nome_casa_evento.place(x=450, y=110, anchor ="n")
        self.widgets_casa_atual.append(label_nome_casa_evento)
            
            #IMAGEM DA CASA
        self.image_evento_exibido = PhotoImage(file="images/casa_017_quimera.png")
        self.label_evento_exibido = tk.Label(
                self.root,  # Substitua por self.canvas_abre se quiser que o Label seja um filho do Canvas
                image=self.image_evento_exibido,
                bg="black"  # Define a cor de fundo do Label
            )
        self.label_evento_exibido.place(x=450, y=140, anchor='n')  # Posiciona o Label
        self.widgets_casa_atual.append(self.label_evento_exibido)

        texto_evento = ("""Fight against the monster.

If you lose,
move back 3 spaces.
and lose 1 life
If you win,
move forward 3 spaces."""
        )
        # label de descrição do evento
        label_descricao_evento = ctk.CTkLabel(
            self.root,
            text=texto_evento,  # Substituir pelo texto dinâmico, se necessário
            text_color="white",  
            fg_color="black",  # Cor de fundo
            font=("Cambria", 17), # "Gelio Fasolada"
        )
        label_descricao_evento.place(x=650, y=140, anchor ="n")
        self.widgets_casa_atual.append(label_descricao_evento)

        self.chamada_do_dado_batalha(casas_avanco=3, casas_retrocesso=3, vida=1)
        self.chamada_cartas_eventos()
        
                
    def casa_evento_018(self): # casa em branco
        self.limpar_widgets_casa_atual()        
        self.casa_evento_001()  
        
    def casa_evento_019(self): # casa em branco
        self.limpar_widgets_casa_atual()        
        self.casa_evento_001()
        
    def casa_evento_020(self): # casa em branco
        self.limpar_widgets_casa_atual()        
        self.casa_evento_001() 
        
        
    def casa_evento_021(self): # casa da carta POSEIDON
        self.limpar_widgets_casa_atual()
        
        try:
            # Carrega a imagem usando PIL
            img = Image.open(self.back_end.cartas_deuses[9]['imagem']) 
            # Converte a imagem para PhotoImage
            self.image_carta_exibida = ImageTk.PhotoImage(img)
            # Cria um Label para exibir a imagem no Canvas
            self.label_imagem_carta = tk.Label(self.canvas_abre, image=self.image_carta_exibida, bg="black")
            self.label_imagem_carta.place(x=440, y=130, anchor="n")
            # Adiciona o Label à lista de widgets dinâmicos
            self.widgets_casa_atual.append(self.label_imagem_carta)

        except Exception as e:
            print(f'Sem imagens nessa carta, usando a imagem default -> {e}')
               
        # label do nome da casa exibida
        label_descricao_carta1 = ctk.CTkLabel(
            self.root,
            text= 'Card abilities:',  # Substituir pelo texto dinâmico, 
            text_color=self.back_end.cor_layout_atual,  
            fg_color="black",  # Cor de fundo
            font=("Gelio Fasolada", 18), 
        )
        label_descricao_carta1.place(x=650, y=130, anchor ="n")
        self.widgets_casa_atual.append(label_descricao_carta1)
        
        """Exibe os widgets para o evento da Casa 002."""
        label_casa = ctk.CTkLabel(
            self.root,
            text= self.back_end.cartas_deuses[9]['action_p'],
            text_color="white",
            bg_color="black",
            font=("cambria", 18),
        )
        label_casa.place(x=650, y=160, anchor='n')
        self.widgets_casa_atual.append(label_casa)
        

        label_guardar_card_exibido = ctk.CTkLabel(
            self.root,
            text= "Do you keep the card?",  # Substituir pelo texto dinâmico, 
            text_color= self.back_end.cor_layout_atual,  
            fg_color="black",  # Cor de fundo
            font=("Gelio Fasolada", 17), # Gelio Fasolada
        )
        label_guardar_card_exibido.place(x=650, y=320, anchor ="center")
        self.widgets_casa_atual.append(label_guardar_card_exibido)
               
        # Botão SIM
        botao_sim_card = ctk.CTkButton(
        self.root,
        fg_color='black',
        width= 16,
        border_color= "white",
        border_width= 1,
        hover_color=self.back_end.cor_layout_atual,
        text="yes",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.back_end.adicionar_carta_a_cartas_player("Poseidon"),
                         self.atualizar_cartas(),  # Atualiza imagens das cartas
                         #self.atualizar_tela(),
                         self.limpar_widgets_casa_atual(),
                         self.casa_evento_001()) # acrescenta Hermes
        )
        botao_sim_card.place(x=600, y=360, anchor="center")
        self.widgets_casa_atual.append(botao_sim_card)
        
        # Botão NÃO
        botao_naum_card = ctk.CTkButton(
        self.root,
        fg_color='black',
        width= 16,
        border_color= "white",
        border_width= 1,
        hover_color="red",
        text="no",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.limpar_widgets_casa_atual(), self.casa_evento_001()) # abre pra jogar dado ou carta
        )
        botao_naum_card.place(x=700, y=360, anchor="center")
        self.widgets_casa_atual.append(botao_naum_card) 


    def casa_evento_022(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001()
            
    def casa_evento_023(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001()


    def casa_evento_024(self): # CICLOPES
            self.limpar_widgets_casa_atual()       
            # label do nome da casa exibida
            label_nome_casa_evento = ctk.CTkLabel(
                self.root,
                text= "Ciclops",
                text_color="white",  
                fg_color="black", 
                font=("Olympus", 24), 
                )
            label_nome_casa_evento.place(x=450, y=110, anchor ="n")
            self.widgets_casa_atual.append(label_nome_casa_evento)
           #IMAGEM DA CASA
            self.image_evento_exibido = PhotoImage(file="images/casa_024_ciclope.png")
            self.label_evento_exibido = tk.Label(
                    self.root,  
                    image=self.image_evento_exibido,
                    bg="black"  
                )
            self.label_evento_exibido.place(x=450, y=140, anchor='n')  # Posiciona o Label
            self.widgets_casa_atual.append(self.label_evento_exibido)

            texto_evento = ("""Engage in battle
against the Cyclops.    
If you win, 
move forward
2 space.
If you lose,
lose 1 life."""
            )
            # label de descrição do evento
            label_descricao_evento = ctk.CTkLabel(
                self.root,
                text=texto_evento,  # Substituir pelo texto dinâmico, se necessário
                text_color="white",  
                fg_color="black",  # Cor de fundo
                font=("Cambria", 17), # "Gelio Fasolada"
            )
            label_descricao_evento.place(x=650, y=140, anchor ="n")
            self.widgets_casa_atual.append(label_descricao_evento)

            self.chamada_do_dado_batalha(casas_avanco=2, casas_retrocesso=1, vida=1)
            self.chamada_cartas_eventos()


    def casa_evento_025(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001()
            
    def casa_evento_026(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001()
            
    def casa_evento_027(self): # casa em branco
                self.limpar_widgets_casa_atual()        
                self.casa_evento_001()
                

    def casa_evento_028(self): # HARPIAS
            self.limpar_widgets_casa_atual()       
            # label do nome da casa exibida
            label_nome_casa_evento = ctk.CTkLabel(
                self.root,
                text= "Harpies",  # Substituir pelo texto dinâmico, 
                text_color="white",  
                fg_color="black",  # Cor de fundo
                font=("Olympus", 24), 
                )
            label_nome_casa_evento.place(x=450, y=110, anchor ="n")
            self.widgets_casa_atual.append(label_nome_casa_evento)
                
            #IMAGEM DA CASA
            self.image_evento_exibido = PhotoImage(file="images/casa_028_harpias.png")
            self.label_evento_exibido = tk.Label(
                    self.root,  # Substitua por self.canvas_abre se quiser que o Label seja um filho do Canvas
                    image=self.image_evento_exibido,
                    bg="black"  # Define a cor de fundo do Label
                )
            self.label_evento_exibido.place(x=450, y=140, anchor='n')  # Posiciona o Label
            self.widgets_casa_atual.append(self.label_evento_exibido)

            texto_evento = ("""Face the 
bronze-feathered monsters.
If you win,
move forward
1 space.
or lose
1 life"""
            )
            # label de descrição do evento
            label_descricao_evento = ctk.CTkLabel(
                self.root,
                text=texto_evento,  # Substituir pelo texto dinâmico, se necessário
                text_color="white",  
                fg_color="black",  # Cor de fundo
                font=("Cambria", 17), # "Gelio Fasolada"
            )
            label_descricao_evento.place(x=650, y=140, anchor ="n")
            self.widgets_casa_atual.append(label_descricao_evento)

            self.chamada_do_dado_batalha(casas_avanco=1, casas_retrocesso=1, vida=1)
            self.chamada_cartas_eventos()


    def casa_evento_029(self): # casa em branco
                self.limpar_widgets_casa_atual()        
                self.casa_evento_001()

        
    def casa_evento_030(self): # casa da carta ATHENA
        self.limpar_widgets_casa_atual()
        
        try:
            # Carrega a imagem usando PIL
            img = Image.open(self.back_end.cartas_deuses[11]['imagem']) 
            # Converte a imagem para PhotoImage
            self.image_carta_exibida = ImageTk.PhotoImage(img)
            # Cria um Label para exibir a imagem no Canvas
            self.label_imagem_carta = tk.Label(self.canvas_abre, image=self.image_carta_exibida, bg="black")
            self.label_imagem_carta.place(x=440, y=130, anchor="n")
            # Adiciona o Label à lista de widgets dinâmicos
            self.widgets_casa_atual.append(self.label_imagem_carta)

        except Exception as e:
            print(f'Sem imagens nessa carta, usando a imagem default -> {e}')
               
        # label do nome da casa exibida
        label_descricao_carta1 = ctk.CTkLabel(
            self.root,
            text= 'Card abilities:',  # Substituir pelo texto dinâmico, 
            text_color=self.back_end.cor_layout_atual,  
            fg_color="black",  # Cor de fundo
            font=("Gelio Fasolada", 18), 
        )
        label_descricao_carta1.place(x=650, y=130, anchor ="n")
        self.widgets_casa_atual.append(label_descricao_carta1)
        
        """Exibe os widgets para o evento da Casa 002."""
        label_casa = ctk.CTkLabel(
            self.root,
            text= self.back_end.cartas_deuses[11]['action_p'],
            text_color="white",
            bg_color="black",
            font=("cambria", 18),
        )
        label_casa.place(x=650, y=160, anchor='n')
        self.widgets_casa_atual.append(label_casa)
        

        label_guardar_card_exibido = ctk.CTkLabel(
            self.root,
            text= "Do you keep the card?",  # Substituir pelo texto dinâmico, 
            text_color= self.back_end.cor_layout_atual,  
            fg_color="black",  # Cor de fundo
            font=("Gelio Fasolada", 17), # Gelio Fasolada
        )
        label_guardar_card_exibido.place(x=650, y=320, anchor ="center")
        self.widgets_casa_atual.append(label_guardar_card_exibido)
               
        # Botão SIM
        botao_sim_card = ctk.CTkButton(
        self.root,
        fg_color='black',
        width= 16,
        border_color= "white",
        border_width= 1,
        hover_color=self.back_end.cor_layout_atual,
        text="yes",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.back_end.adicionar_carta_a_cartas_player("Athena"),
                         self.atualizar_cartas(),  # Atualiza imagens das cartas
                         #self.atualizar_tela(),
                         self.limpar_widgets_casa_atual(),
                         self.casa_evento_001()) # acrescenta Hermes
        )
        botao_sim_card.place(x=600, y=360, anchor="center")
        self.widgets_casa_atual.append(botao_sim_card)
        
        # Botão NÃO
        botao_naum_card = ctk.CTkButton(
        self.root,
        fg_color='black',
        width= 16,
        border_color= "white",
        border_width= 1,
        hover_color="red",
        text="no",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.limpar_widgets_casa_atual(), self.casa_evento_001()) # abre pra jogar dado ou carta
        )
        botao_naum_card.place(x=700, y=360, anchor="center")
        self.widgets_casa_atual.append(botao_naum_card) 


    def casa_evento_031(self): # casa em branco
                self.limpar_widgets_casa_atual()        
                self.casa_evento_001()
                
                
    def casa_evento_032(self): # TANATOS
            self.limpar_widgets_casa_atual()       
                # label do nome da casa exibida
            label_nome_casa_evento = ctk.CTkLabel(
                self.root,
                text= "Thanatos",  # Substituir pelo texto dinâmico, 
                text_color="white",  
                fg_color="black",  # Cor de fundo
                font=("Olympus", 24), 
                )
            label_nome_casa_evento.place(x=450, y=110, anchor ="n")
            self.widgets_casa_atual.append(label_nome_casa_evento)
                
                #IMAGEM DA CASA
            self.image_evento_exibido = PhotoImage(file="images/casa_032_tanatos.png")
            self.label_evento_exibido = tk.Label(
                    self.root,  # Substitua por self.canvas_abre se quiser que o Label seja um filho do Canvas
                    image=self.image_evento_exibido,
                    bg="black"  
                )
            self.label_evento_exibido.place(x=450, y=140, anchor='n')  # Posiciona o Label
            self.widgets_casa_atual.append(self.label_evento_exibido)

            texto_evento = ("""Thanatos 
will take you
to meet Charon.
Lose 1 life and
Advance to 
space 39."""
            )
            # label de descrição do evento
            label_descricao_evento = ctk.CTkLabel(
                self.root,
                text=texto_evento,  
                text_color="white",  
                fg_color="black", 
                font=("Cambria", 17), 
            )
            label_descricao_evento.place(x=650, y=140, anchor ="n")
            self.widgets_casa_atual.append(label_descricao_evento)
            
            self.botao_vontade_dos_deuses(casas_avanco=7, casas_retrocesso=0, vida_mais=0, vida_menos=1, pontos_mais= 30, pontos_menos=60)
            self.chamada_cartas_eventos()


    def casa_evento_033(self): # casa em branco
                self.limpar_widgets_casa_atual()        
                self.casa_evento_001()
                
                
    def casa_evento_034(self): # MINOTAURO
            self.limpar_widgets_casa_atual()       
                # label do nome da casa exibida
            label_nome_casa_evento = ctk.CTkLabel(
                self.root,
                text= "Minotaur",  # Substituir pelo texto dinâmico, 
                text_color="white",  
                fg_color="black",  # Cor de fundo
                font=("Olympus", 24), 
                )
            label_nome_casa_evento.place(x=450, y=110, anchor ="n")
            self.widgets_casa_atual.append(label_nome_casa_evento)
                
                #IMAGEM DA CASA
            self.image_evento_exibido = PhotoImage(file="images/casa_034_minotauro.png")
            self.label_evento_exibido = tk.Label(
                    self.root,  # Substitua por self.canvas_abre se quiser que o Label seja um filho do Canvas
                    image=self.image_evento_exibido,
                    bg="black"  # Define a cor de fundo do Label
                )
            self.label_evento_exibido.place(x=450, y=140, anchor='n')  # Posiciona o Label
            self.widgets_casa_atual.append(self.label_evento_exibido)

            texto_evento = ("""Welcome to the 
Labyrinth of Crete.
Face the Minotaur! 
Fight the beast.

Win and advance
2 spaces.
or lose 1 life"""
            )
            # label de descrição do evento
            label_descricao_evento = ctk.CTkLabel(
                self.root,
                text=texto_evento,  # Substituir pelo texto dinâmico, se necessário
                text_color="white",  
                fg_color="black",  # Cor de fundo
                font=("Cambria", 17), # "Gelio Fasolada"
            )
            label_descricao_evento.place(x=650, y=140, anchor ="n")
            self.widgets_casa_atual.append(label_descricao_evento)
            
            self.chamada_do_dado_batalha(casas_avanco=2, casas_retrocesso=1, vida=1)
            self.chamada_cartas_eventos()


    def casa_evento_035(self): # casa em branco
                self.limpar_widgets_casa_atual()        
                self.casa_evento_001()

                
    def casa_evento_036(self): # LABIRINTO
            self.limpar_widgets_casa_atual()       
                # label do nome da casa exibida
            label_nome_casa_evento = ctk.CTkLabel(
                self.root,
                text= "Labyrinth",  # Substituir pelo texto dinâmico, 
                text_color="white",  
                fg_color="black",  # Cor de fundo
                font=("Olympus", 24), 
                )
            label_nome_casa_evento.place(x=450, y=110, anchor ="n")
            self.widgets_casa_atual.append(label_nome_casa_evento)
                
                #IMAGEM DA CASA
            self.image_evento_exibido = PhotoImage(file="images/casa_036_labirinto.png")
            self.label_evento_exibido = tk.Label(
                    self.root,  # Substitua por self.canvas_abre se quiser que o Label seja um filho do Canvas
                    image=self.image_evento_exibido,
                    bg="black"  # Define a cor de fundo do Label
                )
            self.label_evento_exibido.place(x=450, y=140, anchor='n')  # Posiciona o Label
            self.widgets_casa_atual.append(self.label_evento_exibido)

            texto_evento = ("""You are lost 
in the Labyrinth.
Seek Ariadne's thread.

Try to escape, 
or lose 1 life"""
            )
            # label de descrição do evento
            label_descricao_evento = ctk.CTkLabel(
                self.root,
                text=texto_evento,  # Substituir pelo texto dinâmico, se necessário
                text_color="white",  
                fg_color="black",  # Cor de fundo
                font=("Cambria", 17), # "Gelio Fasolada"
            )
            label_descricao_evento.place(x=650, y=140, anchor ="n")
            self.widgets_casa_atual.append(label_descricao_evento)
            
            # DADO E CARTAS
            self.chamada_do_dado_batalha(casas_avanco=1, casas_retrocesso=1, vida=1)
            self.chamada_cartas_eventos()
                
            
    def casa_evento_037(self): # casa em branco
                self.limpar_widgets_casa_atual()        
                self.casa_evento_001()

      
    def casa_evento_038(self): # casa da carta HADES
        self.limpar_widgets_casa_atual()
        
        try:
            # Carrega a imagem usando PIL
            img = Image.open(self.back_end.cartas_deuses[4]['imagem']) 
            # Converte a imagem para PhotoImage
            self.image_carta_exibida = ImageTk.PhotoImage(img)
            # Cria um Label para exibir a imagem no Canvas
            self.label_imagem_carta = tk.Label(self.canvas_abre, image=self.image_carta_exibida, bg="black")
            self.label_imagem_carta.place(x=440, y=130, anchor="n")
            # Adiciona o Label à lista de widgets dinâmicos
            self.widgets_casa_atual.append(self.label_imagem_carta)

        except Exception as e:
            print(f'Sem imagens nessa carta, usando a imagem default -> {e}')
               
        # label do nome da casa exibida
        label_descricao_carta1 = ctk.CTkLabel(
            self.root,
            text= 'Card abilities:',  # Substituir pelo texto dinâmico, 
            text_color=self.back_end.cor_layout_atual,  
            fg_color="black",  # Cor de fundo
            font=("Gelio Fasolada", 18), 
        )
        label_descricao_carta1.place(x=650, y=130, anchor ="n")
        self.widgets_casa_atual.append(label_descricao_carta1)
        
        """Exibe os widgets para o evento da Casa 002."""
        label_casa = ctk.CTkLabel(
            self.root,
            text= self.back_end.cartas_deuses[4]['action_p'],
            text_color="white",
            bg_color="black",
            font=("cambria", 18),
        )
        label_casa.place(x=650, y=160, anchor='n')
        self.widgets_casa_atual.append(label_casa)
        

        label_guardar_card_exibido = ctk.CTkLabel(
            self.root,
            text= "Do you keep the card?",  # Substituir pelo texto dinâmico, 
            text_color= self.back_end.cor_layout_atual,  
            fg_color="black",  # Cor de fundo
            font=("Gelio Fasolada", 17), # Gelio Fasolada
        )
        label_guardar_card_exibido.place(x=650, y=320, anchor ="center")
        self.widgets_casa_atual.append(label_guardar_card_exibido)
               
        # Botão SIM
        botao_sim_card = ctk.CTkButton(
        self.root,
        fg_color='black',
        width= 16,
        border_color= "white",
        border_width= 1,
        hover_color=self.back_end.cor_layout_atual,
        text="yes",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.back_end.adicionar_carta_a_cartas_player("Hades"),
                         self.atualizar_cartas(),  # Atualiza imagens das cartas
                         #self.atualizar_tela(),
                         self.limpar_widgets_casa_atual(),
                         self.casa_evento_001()) # acrescenta Hermes
        )
        botao_sim_card.place(x=600, y=360, anchor="center")
        self.widgets_casa_atual.append(botao_sim_card)
        
        # Botão NÃO
        botao_naum_card = ctk.CTkButton(
        self.root,
        fg_color='black',
        width= 16,
        border_color= "white",
        border_width= 1,
        hover_color="red",
        text="no",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.limpar_widgets_casa_atual(), self.casa_evento_001()) # abre pra jogar dado ou carta
        )
        botao_naum_card.place(x=700, y=360, anchor="center")
        self.widgets_casa_atual.append(botao_naum_card) 

               
    def casa_evento_039(self): # CARONTE
            self.limpar_widgets_casa_atual()       
                # label do nome da casa exibida
            label_nome_casa_evento = ctk.CTkLabel(
                self.root,
                text= "Charon",  # Substituir pelo texto dinâmico, 
                text_color="white",  
                fg_color="black",  # Cor de fundo
                font=("Olympus", 24), 
                )
            label_nome_casa_evento.place(x=450, y=110, anchor ="n")
            self.widgets_casa_atual.append(label_nome_casa_evento)
                
                #IMAGEM DA CASA
            self.image_evento_exibido = PhotoImage(file="images/casa_039_caronte.png")
            self.label_evento_exibido = tk.Label(
                    self.root,  # Substitua por self.canvas_abre se quiser que o Label seja um filho do Canvas
                    image=self.image_evento_exibido,
                    bg="black"  # Define a cor de fundo do Label
                )
            self.label_evento_exibido.place(x=450, y=140, anchor='n')  # Posiciona o Label
            self.widgets_casa_atual.append(self.label_evento_exibido)

            texto_evento = ("""Roll a die and
negotiate your life 
with the ferryman 
of the River Styx.."""
            )
            # label de descrição do evento
            label_descricao_evento = ctk.CTkLabel(
                self.root,
                text=texto_evento,  # Substituir pelo texto dinâmico, se necessário
                text_color="white",  
                fg_color="black",  # Cor de fundo
                font=("Cambria", 17), # "Gelio Fasolada"
            )
            label_descricao_evento.place(x=650, y=140, anchor ="n")
            self.widgets_casa_atual.append(label_descricao_evento)
            
            self.chamada_do_dado_batalha(casas_avanco=1, casas_retrocesso=2, vida=1)
            self.chamada_cartas_eventos()
  

    def casa_evento_040(self): # casa em branco
                self.limpar_widgets_casa_atual()        
                self.casa_evento_001()
                    
    def casa_evento_041(self): # casa em branco
                self.limpar_widgets_casa_atual()        
                self.casa_evento_001()

              
    def casa_evento_042(self): # JULGAMENTO
            self.limpar_widgets_casa_atual()       
                # label do nome da casa exibida
            label_nome_casa_evento = ctk.CTkLabel(
                self.root,
                text= "Judgment",  # Substituir pelo texto dinâmico, 
                text_color="white",  
                fg_color="black",  # Cor de fundo
                font=("Olympus", 24), 
                )
            label_nome_casa_evento.place(x=450, y=110, anchor ="n")
            self.widgets_casa_atual.append(label_nome_casa_evento)   
                #IMAGEM DA CASA
            self.image_evento_exibido = PhotoImage(file="images/casa_042_juizes.png")
            self.label_evento_exibido = tk.Label(
                    self.root,  # Substitua por self.canvas_abre se quiser que o Label seja um filho do Canvas
                    image=self.image_evento_exibido,
                    bg="black"  # Define a cor de fundo do Label
                )
            self.label_evento_exibido.place(x=450, y=140, anchor='n')  # Posiciona o Label
            self.widgets_casa_atual.append(self.label_evento_exibido)

            texto_evento = ("""Be judged by 
the three judges:
Rhadamanthus, Minos and Aeacus.
If you pass, advance
to space 47.
Or lose 
1 life"""
            )
            label_descricao_evento = ctk.CTkLabel(
                self.root,
                text=texto_evento,  
                text_color="white",  
                fg_color="black",
                font=("Cambria", 17), 
            )
            label_descricao_evento.place(x=660, y=140, anchor ="n")
            self.widgets_casa_atual.append(label_descricao_evento)
            
            self.chamada_do_dado_batalha(casas_avanco=5, casas_retrocesso=1, vida=1)
            self.chamada_cartas_eventos()
  

    def casa_evento_043(self): # casa em branco
                self.limpar_widgets_casa_atual()        
                self.casa_evento_001()

              
    def casa_evento_044(self): # ORFEU
            self.limpar_widgets_casa_atual()       
                # label do nome da casa exibida
            label_nome_casa_evento = ctk.CTkLabel(
                self.root,
                text= "Orpheus",  # Substituir pelo texto dinâmico, 
                text_color="white",  
                fg_color="black",  # Cor de fundo
                font=("Olympus", 24), 
                )
            label_nome_casa_evento.place(x=450, y=110, anchor ="n")
            self.widgets_casa_atual.append(label_nome_casa_evento)
                
                #IMAGEM DA CASA
            self.image_evento_exibido = PhotoImage(file="images/casa_044_orfeu.png")
            self.label_evento_exibido = tk.Label(
                    self.root,  # Substitua por self.canvas_abre se quiser que o Label seja um filho do Canvas
                    image=self.image_evento_exibido,
                    bg="black"  # Define a cor de fundo do Label
                )
            self.label_evento_exibido.place(x=450, y=140, anchor='n')  # Posiciona o Label
            self.widgets_casa_atual.append(self.label_evento_exibido)

            texto_evento = ("""You are enchanted 
by Orpheus's sorrowful song.

Move back
1 space
and lose 
1 life."""
            )
            # label de descrição do evento
            label_descricao_evento = ctk.CTkLabel(
                self.root,
                text=texto_evento,  # Substituir pelo texto dinâmico, se necessário
                text_color="white",  
                fg_color="black",  # Cor de fundo
                font=("Cambria", 17), # "Gelio Fasolada"
            )
            label_descricao_evento.place(x=650, y=140, anchor ="n")
            self.widgets_casa_atual.append(label_descricao_evento)
            
            self.botao_vontade_dos_deuses(casas_avanco=0, casas_retrocesso=1, vida_mais=0, vida_menos=1, pontos_mais= 0, pontos_menos=30)
            self.chamada_cartas_eventos()
            

    def casa_evento_045(self): # casa em branco
                self.limpar_widgets_casa_atual()        
                self.casa_evento_001()

    def casa_evento_046(self): # casa em branco
                self.limpar_widgets_casa_atual()        
                self.casa_evento_001()

    def casa_evento_047(self): # casa em branco
                self.limpar_widgets_casa_atual()        
                self.casa_evento_001()

    def casa_evento_048(self): # casa em branco
                self.limpar_widgets_casa_atual()        
                self.casa_evento_001()
                
      
    def casa_evento_049(self): # casa da carta HEFESTO
        self.limpar_widgets_casa_atual()
        
        try:
            # Carrega a imagem usando PIL
            img = Image.open(self.back_end.cartas_deuses[5]['imagem']) 
            # Converte a imagem para PhotoImage
            self.image_carta_exibida = ImageTk.PhotoImage(img)
            # Cria um Label para exibir a imagem no Canvas
            self.label_imagem_carta = tk.Label(self.canvas_abre, image=self.image_carta_exibida, bg="black")
            self.label_imagem_carta.place(x=440, y=130, anchor="n")
            # Adiciona o Label à lista de widgets dinâmicos
            self.widgets_casa_atual.append(self.label_imagem_carta)

        except Exception as e:
            print(f'Sem imagens nessa carta, usando a imagem default -> {e}')
               
        # label do nome da casa exibida
        label_descricao_carta1 = ctk.CTkLabel(
            self.root,
            text= 'Card abilities:',  # Substituir pelo texto dinâmico, 
            text_color=self.back_end.cor_layout_atual,  
            fg_color="black",  # Cor de fundo
            font=("Gelio Fasolada", 18), 
        )
        label_descricao_carta1.place(x=650, y=130, anchor ="n")
        self.widgets_casa_atual.append(label_descricao_carta1)
        
        """Exibe os widgets para o evento da Casa 002."""
        label_casa = ctk.CTkLabel(
            self.root,
            text= self.back_end.cartas_deuses[5]['action_p'],
            text_color="white",
            bg_color="black",
            font=("cambria", 18),
        )
        label_casa.place(x=650, y=160, anchor='n')
        self.widgets_casa_atual.append(label_casa)
        

        label_guardar_card_exibido = ctk.CTkLabel(
            self.root,
            text= "Do you keep the card?",  # Substituir pelo texto dinâmico, 
            text_color= self.back_end.cor_layout_atual,  
            fg_color="black",  # Cor de fundo
            font=("Gelio Fasolada", 17), # Gelio Fasolada
        )
        label_guardar_card_exibido.place(x=650, y=320, anchor ="center")
        self.widgets_casa_atual.append(label_guardar_card_exibido)
               
        # Botão SIM
        botao_sim_card = ctk.CTkButton(
        self.root,
        fg_color='black',
        width= 16,
        border_color= "white",
        border_width= 1,
        hover_color=self.back_end.cor_layout_atual,
        text="yes",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.back_end.adicionar_carta_a_cartas_player("Hephaestus"),
                         self.atualizar_cartas(),  # Atualiza imagens das cartas
                         #self.atualizar_tela(),
                         self.limpar_widgets_casa_atual(),
                         self.casa_evento_001()) # acrescenta Hermes
        )
        botao_sim_card.place(x=600, y=360, anchor="center")
        self.widgets_casa_atual.append(botao_sim_card)
        
        # Botão NÃO
        botao_naum_card = ctk.CTkButton(
        self.root,
        fg_color='black',
        width= 16,
        border_color= "white",
        border_width= 1,
        hover_color="red",
        text="no",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.limpar_widgets_casa_atual(), self.casa_evento_001()) # abre pra jogar dado ou carta
        )
        botao_naum_card.place(x=700, y=360, anchor="center")
        self.widgets_casa_atual.append(botao_naum_card) 

               
    def casa_evento_050(self): # casa em branco
                self.limpar_widgets_casa_atual()        
                self.casa_evento_001()
                
    def casa_evento_051(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001()
            
                  
    def casa_evento_052(self): # ERINIAS
            self.limpar_widgets_casa_atual()       
                # label do nome da casa exibida
            label_nome_casa_evento = ctk.CTkLabel(
                self.root,
                text= "Erinyes",  # Substituir pelo texto dinâmico, 
                text_color="white",  
                fg_color="black",  # Cor de fundo
                font=("Olympus", 24), 
                )
            label_nome_casa_evento.place(x=450, y=110, anchor ="n")
            self.widgets_casa_atual.append(label_nome_casa_evento)
                
            #IMAGEM DA CASA
            self.image_evento_exibido = PhotoImage(file="images/casa_052_erinias.png")
            self.label_evento_exibido = tk.Label(
                    self.root,  # Substitua por self.canvas_abre se quiser que o Label seja um filho do Canvas
                    image=self.image_evento_exibido,
                    bg="black"  # Define a cor de fundo do Label
                )
            self.label_evento_exibido.place(x=450, y=140, anchor='n')  # Posiciona o Label
            self.widgets_casa_atual.append(self.label_evento_exibido)

            texto_evento_1=("""Face the Furies.
move forward 
2 spaces.
Or lose 
1 life"""
            )
            # label de descrição do evento
            label_descricao_evento = ctk.CTkLabel(
                self.root,
                text=texto_evento_1,  # Substituir pelo texto dinâmico, se necessário
                text_color="white",  
                fg_color="black",  # Cor de fundo
                font=("Cambria", 17), # "Gelio Fasolada"
            )
            label_descricao_evento.place(x=650, y=140, anchor ="n")
            self.widgets_casa_atual.append(label_descricao_evento)
            
            #rolagem de dados
            self.chamada_do_dado_batalha(casas_avanco=2, casas_retrocesso=2, vida=1)
            self.chamada_cartas_eventos()

  
    def casa_evento_053(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001()
            
    def casa_evento_054(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001()
            
      
    def casa_evento_055(self): # casa da carta PERSEFONE
        self.limpar_widgets_casa_atual()        
        try:
            img = Image.open(self.back_end.cartas_deuses[8]['imagem']) 
            self.image_carta_exibida = ImageTk.PhotoImage(img)
            self.label_imagem_carta = tk.Label(self.canvas_abre, image=self.image_carta_exibida, bg="black")
            self.label_imagem_carta.place(x=440, y=130, anchor="n")
            self.widgets_casa_atual.append(self.label_imagem_carta)
        except Exception as e:
            print(f'Sem imagens nessa carta, usando a imagem default -> {e}')
               
        label_descricao_carta1 = ctk.CTkLabel(
            self.root,
            text= 'Card abilities:', 
            text_color=self.back_end.cor_layout_atual,  
            fg_color="black",
            font=("Gelio Fasolada", 18), 
        )
        label_descricao_carta1.place(x=650, y=130, anchor ="n")
        self.widgets_casa_atual.append(label_descricao_carta1)
        
        label_casa = ctk.CTkLabel(
            self.root,
            text= self.back_end.cartas_deuses[8]['action_p'], # texto descritivo da carta
            text_color="white",
            bg_color="black",
            font=("cambria", 18),
        )
        label_casa.place(x=650, y=160, anchor='n')
        self.widgets_casa_atual.append(label_casa)
        
        # Quer guardar a carta?
        label_guardar_card_exibido = ctk.CTkLabel(
            self.root,
            text= "Do you keep the card?",
            text_color= self.back_end.cor_layout_atual,  
            fg_color="black",  
            font=("Gelio Fasolada", 17), 
        )
        label_guardar_card_exibido.place(x=650, y=320, anchor ="center")
        self.widgets_casa_atual.append(label_guardar_card_exibido)               
        # Botão SIM
        botao_sim_card = ctk.CTkButton(
        self.root,
        fg_color='black',
        width= 16,
        border_color= "white",
        border_width= 1,
        hover_color=self.back_end.cor_layout_atual,
        text="yes",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.back_end.adicionar_carta_a_cartas_player("Persephone"),
                         self.atualizar_cartas(), 
                         self.limpar_widgets_casa_atual(),
                         self.casa_evento_001()) # volta para o menu inicial, usar dado ou carta
                        )
        botao_sim_card.place(x=600, y=360, anchor="center")
        self.widgets_casa_atual.append(botao_sim_card)
        # Botão NÃO
        botao_naum_card = ctk.CTkButton(
        self.root,
        fg_color='black',
        width= 16,
        border_color= "white",
        border_width= 1,
        hover_color="red",
        text="no",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.limpar_widgets_casa_atual(), self.casa_evento_001()) # abre pra jogar dado ou carta
        )
        botao_naum_card.place(x=700, y=360, anchor="center")
        self.widgets_casa_atual.append(botao_naum_card) 


    def casa_evento_056(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001()

    def casa_evento_057(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001()

    def casa_evento_058(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001()

    def casa_evento_059(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001()

    def casa_evento_060(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001()
 
                      
    def casa_evento_061(self): # HIDRA
            self.limpar_widgets_casa_atual()       
            # label do nome da casa exibida
            label_nome_casa_evento = ctk.CTkLabel(
                self.root,
                text= "Hydra", 
                text_color="white",  
                fg_color="black",
                font=("Olympus", 24), 
                )
            label_nome_casa_evento.place(x=450, y=110, anchor ="n")
            self.widgets_casa_atual.append(label_nome_casa_evento)                
            #IMAGEM DA CASA
            self.image_evento_exibido = PhotoImage(file="images/casa_061_hidra.png")
            self.label_evento_exibido = tk.Label(
                    self.root,
                    image=self.image_evento_exibido,
                    bg="black"
                )
            self.label_evento_exibido.place(x=450, y=140, anchor='n')
            self.widgets_casa_atual.append(self.label_evento_exibido)
            texto_evento = ("""Cutting off just 
one head won't be 
your salvation.
If you win,
advance
2 spaces.
Or lose 1 life"""
            )
            # label de descrição do evento
            label_descricao_evento = ctk.CTkLabel(
                self.root,
                text=texto_evento,  
                text_color="white",  
                fg_color="black",
                font=("Cambria", 17), 
            )
            label_descricao_evento.place(x=650, y=140, anchor ="n")
            self.widgets_casa_atual.append(label_descricao_evento)
            
            #rolagem de dados
            self.chamada_do_dado_batalha(casas_avanco=2, casas_retrocesso=2, vida=1)
            self.chamada_cartas_eventos()


    def casa_evento_062(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001()
  
    def casa_evento_063(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001()
      
      
    def casa_evento_064(self): # casa da carta APOLO
        self.limpar_widgets_casa_atual()        
        try:
            img = Image.open(self.back_end.cartas_deuses[1]['imagem']) # caminho imagem da carta
            self.image_carta_exibida = ImageTk.PhotoImage(img)
            self.label_imagem_carta = tk.Label(self.canvas_abre, image=self.image_carta_exibida, bg="black")
            self.label_imagem_carta.place(x=440, y=130, anchor="n")
            self.widgets_casa_atual.append(self.label_imagem_carta)
        except Exception as e:
            print(f'Sem imagens nessa carta, usando a imagem default -> {e}')
               
        label_descricao_carta1 = ctk.CTkLabel(
            self.root,
            text= 'Card abilities:', 
            text_color=self.back_end.cor_layout_atual,  
            fg_color="black",
            font=("Gelio Fasolada", 18), 
        )
        label_descricao_carta1.place(x=650, y=130, anchor ="n")
        self.widgets_casa_atual.append(label_descricao_carta1)
        
        label_casa = ctk.CTkLabel(
            self.root,
            text= self.back_end.cartas_deuses[1]['action_p'], # texto descritivo da carta
            text_color="white",
            bg_color="black",
            font=("cambria", 18),
        )
        label_casa.place(x=650, y=160, anchor='n')
        self.widgets_casa_atual.append(label_casa)
        
        # Quer guardar a carta?
        label_guardar_card_exibido = ctk.CTkLabel(
            self.root,
            text= "Do you keep the card?",
            text_color= self.back_end.cor_layout_atual,  
            fg_color="black",  
            font=("Gelio Fasolada", 17), 
        )
        label_guardar_card_exibido.place(x=650, y=320, anchor ="center")
        self.widgets_casa_atual.append(label_guardar_card_exibido)               
        # Botão SIM
        botao_sim_card = ctk.CTkButton(
        self.root,
        fg_color='black',
        width= 16,
        border_color= "white",
        border_width= 1,
        hover_color=self.back_end.cor_layout_atual,
        text="yes",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.back_end.adicionar_carta_a_cartas_player("Apollo"),
                         self.atualizar_cartas(), 
                         self.limpar_widgets_casa_atual(),
                         self.casa_evento_001()) # volta para o menu inicial, usar dado ou carta
                        )
        botao_sim_card.place(x=600, y=360, anchor="center")
        self.widgets_casa_atual.append(botao_sim_card)
        # Botão NÃO
        botao_naum_card = ctk.CTkButton(
        self.root,
        fg_color='black',
        width= 16,
        border_color= "white",
        border_width= 1,
        hover_color="red",
        text="no",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.limpar_widgets_casa_atual(), self.casa_evento_001()) # abre pra jogar dado ou carta
        )
        botao_naum_card.place(x=700, y=360, anchor="center")
        self.widgets_casa_atual.append(botao_naum_card) 


    def casa_evento_065(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001()

                     
    def casa_evento_066(self): # SISIFO
            self.limpar_widgets_casa_atual()       
            # label do nome da casa exibida
            label_nome_casa_evento = ctk.CTkLabel(
                self.root,
                text= "Sisyphus", 
                text_color="white",  
                fg_color="black",
                font=("Olympus", 24), 
                )
            label_nome_casa_evento.place(x=450, y=110, anchor ="n")
            self.widgets_casa_atual.append(label_nome_casa_evento)                
            #IMAGEM DA CASA
            self.image_evento_exibido = PhotoImage(file="images/casa_066_sisifo.png")
            self.label_evento_exibido = tk.Label(
                    self.root,
                    image=self.image_evento_exibido,
                    bg="black"
                )
            self.label_evento_exibido.place(x=450, y=140, anchor='n')
            self.widgets_casa_atual.append(self.label_evento_exibido)
            texto_evento = ("""Help the condemned king
push his stone.

Lose one life,
and return to 
space 57"""
            )
            # label de descrição do evento
            label_descricao_evento = ctk.CTkLabel(
                self.root,
                text=texto_evento,  
                text_color="white",  
                fg_color="black",
                font=("Cambria", 17), 
            )
            label_descricao_evento.place(x=650, y=140, anchor ="n")
            self.widgets_casa_atual.append(label_descricao_evento)
            
            self.botao_vontade_dos_deuses(casas_avanco=0, casas_retrocesso=9, vida_mais=0, vida_menos=1, pontos_mais= 0, pontos_menos=30)
            self.chamada_cartas_eventos()


    def casa_evento_067(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001()

    def casa_evento_068(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001()

                     
    def casa_evento_069(self): # CENTAUROS
            self.limpar_widgets_casa_atual()       
            # label do nome da casa exibida
            label_nome_casa_evento = ctk.CTkLabel(
                self.root,
                text= "Centaurs", 
                text_color="white",  
                fg_color="black",
                font=("Olympus", 24), 
                )
            label_nome_casa_evento.place(x=450, y=110, anchor ="n")
            self.widgets_casa_atual.append(label_nome_casa_evento)                
            #IMAGEM DA CASA
            self.image_evento_exibido = PhotoImage(file="images/casa_069_centauros.png")
            self.label_evento_exibido = tk.Label(
                    self.root,
                    image=self.image_evento_exibido,
                    bg="black"
                )
            self.label_evento_exibido.place(x=450, y=140, anchor='n')
            self.widgets_casa_atual.append(self.label_evento_exibido)
            texto_evento = ("""The centaurs have drunk
too much wine and 
have become violent.

Try to defeat them.
Or lose 1 life"""
            )
            # label de descrição do evento
            label_descricao_evento = ctk.CTkLabel(
                self.root,
                text=texto_evento,  
                text_color="white",  
                fg_color="black",
                font=("Cambria", 17), 
            )
            label_descricao_evento.place(x=650, y=140, anchor ="n")
            self.widgets_casa_atual.append(label_descricao_evento)
            
            #rolagem de dados
            self.chamada_do_dado_batalha(casas_avanco=1, casas_retrocesso=1, vida=1)
            self.chamada_cartas_eventos()

   
    def casa_evento_070(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001()
            
                         
    def casa_evento_071(self): # SATIROS
            self.limpar_widgets_casa_atual()       
            # label do nome da casa exibida
            label_nome_casa_evento = ctk.CTkLabel(
                self.root,
                text= "Satyrs", 
                text_color="white",  
                fg_color="black",
                font=("Olympus", 24), 
                )
            label_nome_casa_evento.place(x=450, y=110, anchor ="n")
            self.widgets_casa_atual.append(label_nome_casa_evento)                
            #IMAGEM DA CASA
            self.image_evento_exibido = PhotoImage(file="images/casa_071_satiros.png")
            self.label_evento_exibido = tk.Label(
                    self.root,
                    image=self.image_evento_exibido,
                    bg="black"
                )
            self.label_evento_exibido.place(x=450, y=140, anchor='n')
            self.widgets_casa_atual.append(self.label_evento_exibido)
            texto_evento = ("""Some Satyrs from
Dionysus' army are returning
from their campaign in India.
And they won't let you pass.
Try to defeat them.
Or lose 1 life"""
            )
            # label de descrição do evento
            label_descricao_evento = ctk.CTkLabel(
                self.root,
                text=texto_evento,  
                text_color="white",  
                fg_color="black",
                font=("Cambria", 17), 
            )
            label_descricao_evento.place(x=650, y=140, anchor ="n")
            self.widgets_casa_atual.append(label_descricao_evento)
            
            #rolagem de dados
            self.chamada_do_dado_batalha(casas_avanco=1, casas_retrocesso=1, vida=1)
            self.chamada_cartas_eventos()

   
    def casa_evento_072(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001()
            
      
    def casa_evento_073(self): # casa da carta HERA
        self.limpar_widgets_casa_atual()        
        try:
            img = Image.open(self.back_end.cartas_deuses[6]['imagem']) 
            self.image_carta_exibida = ImageTk.PhotoImage(img)
            self.label_imagem_carta = tk.Label(self.canvas_abre, image=self.image_carta_exibida, bg="black")
            self.label_imagem_carta.place(x=440, y=130, anchor="n")
            self.widgets_casa_atual.append(self.label_imagem_carta)
        except Exception as e:
            print(f'Sem imagens nessa carta, usando a imagem default -> {e}')
               
        label_descricao_carta1 = ctk.CTkLabel(
            self.root,
            text= 'Card abilities:', 
            text_color=self.back_end.cor_layout_atual,  
            fg_color="black",
            font=("Gelio Fasolada", 18), 
        )
        label_descricao_carta1.place(x=650, y=130, anchor ="n")
        self.widgets_casa_atual.append(label_descricao_carta1)
        
        label_casa = ctk.CTkLabel(
            self.root,
            text= self.back_end.cartas_deuses[6]['action_p'], # texto descritivo da carta
            text_color="white",
            bg_color="black",
            font=("cambria", 18),
        )
        label_casa.place(x=650, y=160, anchor='n')
        self.widgets_casa_atual.append(label_casa)
        
        # Quer guardar a carta?
        label_guardar_card_exibido = ctk.CTkLabel(
            self.root,
            text= "Do you keep the card?",
            text_color= self.back_end.cor_layout_atual,  
            fg_color="black",  
            font=("Gelio Fasolada", 17), 
        )
        label_guardar_card_exibido.place(x=650, y=320, anchor ="center")
        self.widgets_casa_atual.append(label_guardar_card_exibido)               
        # Botão SIM
        botao_sim_card = ctk.CTkButton(
        self.root,
        fg_color='black',
        width= 16,
        border_color= "white",
        border_width= 1,
        hover_color=self.back_end.cor_layout_atual,
        text="yes",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.back_end.adicionar_carta_a_cartas_player("Hera"),
                         self.atualizar_cartas(), 
                         self.limpar_widgets_casa_atual(),
                         self.casa_evento_001()) # volta para o menu inicial, usar dado ou carta
                        )
        botao_sim_card.place(x=600, y=360, anchor="center")
        self.widgets_casa_atual.append(botao_sim_card)
        # Botão NÃO
        botao_naum_card = ctk.CTkButton(
        self.root,
        fg_color='black',
        width= 16,
        border_color= "white",
        border_width= 1,
        hover_color="red",
        text="no",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.limpar_widgets_casa_atual(), self.casa_evento_001()) # abre pra jogar dado ou carta
        )
        botao_naum_card.place(x=700, y=360, anchor="center")
        self.widgets_casa_atual.append(botao_naum_card) 

   
    def casa_evento_074(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001()

                         
    def casa_evento_075(self): # SEREIAS
            self.limpar_widgets_casa_atual()       
            # label do nome da casa exibida
            label_nome_casa_evento = ctk.CTkLabel(
                self.root,
                text= "Sirens", 
                text_color="white",  
                fg_color="black",
                font=("Olympus", 24), 
                )
            label_nome_casa_evento.place(x=450, y=110, anchor ="n")
            self.widgets_casa_atual.append(label_nome_casa_evento)                
            #IMAGEM DA CASA
            self.image_evento_exibido = PhotoImage(file="images/casa_075_sirenes.png")
            self.label_evento_exibido = tk.Label(
                    self.root,
                    image=self.image_evento_exibido,
                    bg="black"
                )
            self.label_evento_exibido.place(x=450, y=140, anchor='n')
            self.widgets_casa_atual.append(self.label_evento_exibido)
            texto_evento = ("""Sirens! try to escape 
their terrible singing.
Atalanta and Hippolyta
are immune 
to their song 
and advance 
2 spaces."""
            )
            # label de descrição do evento
            label_descricao_evento = ctk.CTkLabel(
                self.root,
                text=texto_evento,  
                text_color="white",  
                fg_color="black",
                font=("Cambria", 17), 
            )
            label_descricao_evento.place(x=650, y=140, anchor ="n")
            self.widgets_casa_atual.append(label_descricao_evento)
            
            print(f'Casa das Sirenes - personagem é: {self.back_end.personagem_escolhido_nome}') # For debug
            
            # Se atalanta ou Hipolita avança 2 casas
            if self.back_end.personagem_escolhido_nome == "Atalanta" or self.back_end.personagem_escolhido_nome == "Hippolyta" or self.back_end.personagem_escolhido_nome == "Helena of Troy":
                self.botao_vontade_dos_deuses(casas_avanco=2, casas_retrocesso=0, vida_mais=0, vida_menos=0, pontos_mais= 60, pontos_menos=0)
                print(f'Mulher não é afetada pelo canto das sereias - ESCAPOU!!')
            else:
                 self.chamada_do_dado_batalha(casas_avanco=2, casas_retrocesso=1, vida=1)
            self.chamada_cartas_eventos()

     
    def casa_evento_076(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001()

    def casa_evento_077(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001()

    def casa_evento_078(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001() 

      
    def casa_evento_079(self): # casa da carta ARES
        self.limpar_widgets_casa_atual()        
        try:
            img = Image.open(self.back_end.cartas_deuses[3]['imagem']) 
            self.image_carta_exibida = ImageTk.PhotoImage(img)
            self.label_imagem_carta = tk.Label(self.canvas_abre, image=self.image_carta_exibida, bg="black")
            self.label_imagem_carta.place(x=440, y=130, anchor="n")
            self.widgets_casa_atual.append(self.label_imagem_carta)
        except Exception as e:
            print(f'Sem imagens nessa carta, usando a imagem default -> {e}')
               
        label_descricao_carta1 = ctk.CTkLabel(
            self.root,
            text= 'Card abilities:', 
            text_color=self.back_end.cor_layout_atual,  
            fg_color="black",
            font=("Gelio Fasolada", 18), 
        )
        label_descricao_carta1.place(x=650, y=130, anchor ="n")
        self.widgets_casa_atual.append(label_descricao_carta1)
        
        label_casa = ctk.CTkLabel(
            self.root,
            text= self.back_end.cartas_deuses[3]['action_p'], # texto descritivo da carta
            text_color="white",
            bg_color="black",
            font=("cambria", 18),
        )
        label_casa.place(x=650, y=160, anchor='n')
        self.widgets_casa_atual.append(label_casa)
        
        # Quer guardar a carta?
        label_guardar_card_exibido = ctk.CTkLabel(
            self.root,
            text= "Do you keep the card?",
            text_color= self.back_end.cor_layout_atual,  
            fg_color="black",  
            font=("Gelio Fasolada", 17), 
        )
        label_guardar_card_exibido.place(x=650, y=320, anchor ="center")
        self.widgets_casa_atual.append(label_guardar_card_exibido)               
        # Botão SIM
        botao_sim_card = ctk.CTkButton(
        self.root,
        fg_color='black',
        width= 16,
        border_color= "white",
        border_width= 1,
        hover_color=self.back_end.cor_layout_atual,
        text="yes",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.back_end.adicionar_carta_a_cartas_player("Ares"),
                         self.atualizar_cartas(), 
                         self.limpar_widgets_casa_atual(),
                         self.casa_evento_001()) # volta para o menu inicial, usar dado ou carta
                        )
        botao_sim_card.place(x=600, y=360, anchor="center")
        self.widgets_casa_atual.append(botao_sim_card)
        # Botão NÃO
        botao_naum_card = ctk.CTkButton(
        self.root,
        fg_color='black',
        width= 16,
        border_color= "white",
        border_width= 1,
        hover_color="red",
        text="no",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.limpar_widgets_casa_atual(), self.casa_evento_001()) # abre pra jogar dado ou carta
        )
        botao_naum_card.place(x=700, y=360, anchor="center")
        self.widgets_casa_atual.append(botao_naum_card) 
          
               
    def casa_evento_080(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001()     
    
    def casa_evento_081(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001()     
    
                           
    def casa_evento_082(self): # NINFAS
            self.limpar_widgets_casa_atual()       
            # label do nome da casa exibida
            label_nome_casa_evento = ctk.CTkLabel(
                self.root,
                text= "Nymphs", 
                text_color="white",  
                fg_color="black",
                font=("Olympus", 24), 
                )
            label_nome_casa_evento.place(x=450, y=110, anchor ="n")
            self.widgets_casa_atual.append(label_nome_casa_evento)                
            #IMAGEM DA CASA
            self.image_evento_exibido = PhotoImage(file="images/casa_082_ninfas.png")
            self.label_evento_exibido = tk.Label(
                    self.root,
                    image=self.image_evento_exibido,
                    bg="black"
                )
            self.label_evento_exibido.place(x=450, y=140, anchor='n')
            self.widgets_casa_atual.append(self.label_evento_exibido)
            texto_evento = ("""They have fallen in love 
with you and have decided 
to show you a shortcut.

Advance 
2 spaces."""
            )
            # label de descrição do evento
            label_descricao_evento = ctk.CTkLabel(
                self.root,
                text=texto_evento,  
                text_color="white",  
                fg_color="black",
                font=("Cambria", 17), 
            )
            label_descricao_evento.place(x=650, y=140, anchor ="n")
            self.widgets_casa_atual.append(label_descricao_evento)
            
            # vontade dos deuses
            self.botao_vontade_dos_deuses(casas_avanco=2, casas_retrocesso=0, vida_mais=0, vida_menos=0, pontos_mais= 60, pontos_menos=0)
            self.chamada_cartas_eventos()



    def casa_evento_083(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001()   
                        
    def casa_evento_084(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001()  
    
                           
    def casa_evento_085(self): # TROIA
            self.limpar_widgets_casa_atual()       
            # label do nome da casa exibida
            label_nome_casa_evento = ctk.CTkLabel(
                self.root,
                text= "Troy", 
                text_color="white",  
                fg_color="black",
                font=("Olympus", 24), 
                )
            label_nome_casa_evento.place(x=450, y=110, anchor ="n")
            self.widgets_casa_atual.append(label_nome_casa_evento)                
            #IMAGEM DA CASA
            self.image_evento_exibido = PhotoImage(file="images/casa_085_troia.png")
            self.label_evento_exibido = tk.Label(
                    self.root,
                    image=self.image_evento_exibido,
                    bg="black"
                )
            self.label_evento_exibido.place(x=450, y=140, anchor='n')
            self.widgets_casa_atual.append(self.label_evento_exibido)
            texto_evento = ("""The great enemies
of the Greeks will not 
let you pass without a fight.
In this battle, the Gods
will not be able to help you, 
you cannot use cards,
if you win, advance 2 spaces.
Or lose 1 life."""
            )
            # label de descrição do evento
            label_descricao_evento = ctk.CTkLabel(
                self.root,
                text=texto_evento,  
                text_color="white",  
                fg_color="black",
                font=("Cambria", 17), 
            )
            label_descricao_evento.place(x=650, y=140, anchor ="n")
            self.widgets_casa_atual.append(label_descricao_evento)
            
            # Dados
            self.chamada_do_dado_batalha_troia(casas_avanco=2, casas_retrocesso=2, vida=1)
            #self.chamada_cartas_eventos()

    def casa_evento_086(self): # casa em branco
        self.limpar_widgets_casa_atual()        
        self.casa_evento_001()     

    def casa_evento_087(self): # casa em branco
        self.limpar_widgets_casa_atual()        
        self.casa_evento_001()        
    
      
    def casa_evento_088(self): # casa da carta AFRODITE
        self.limpar_widgets_casa_atual()        
        try:
            img = Image.open(self.back_end.cartas_deuses[0]['imagem']) 
            self.image_carta_exibida = ImageTk.PhotoImage(img)
            self.label_imagem_carta = tk.Label(self.canvas_abre, image=self.image_carta_exibida, bg="black")
            self.label_imagem_carta.place(x=440, y=130, anchor="n")
            self.widgets_casa_atual.append(self.label_imagem_carta)
        except Exception as e:
            print(f'Sem imagens nessa carta, usando a imagem default -> {e}')
               
        label_descricao_carta1 = ctk.CTkLabel(
            self.root,
            text= 'Card abilities:', 
            text_color=self.back_end.cor_layout_atual,  
            fg_color="black",
            font=("Gelio Fasolada", 18), 
        )
        label_descricao_carta1.place(x=650, y=130, anchor ="n")
        self.widgets_casa_atual.append(label_descricao_carta1)
        
        label_casa = ctk.CTkLabel(
            self.root,
            text= self.back_end.cartas_deuses[0]['action_p'], # texto descritivo da carta
            text_color="white",
            bg_color="black",
            font=("cambria", 18),
        )
        label_casa.place(x=650, y=160, anchor='n')
        self.widgets_casa_atual.append(label_casa)
        
        # Quer guardar a carta?
        label_guardar_card_exibido = ctk.CTkLabel(
            self.root,
            text= "Do you keep the card?",
            text_color= self.back_end.cor_layout_atual,  
            fg_color="black",  
            font=("Gelio Fasolada", 17), 
        )
        label_guardar_card_exibido.place(x=650, y=320, anchor ="center")
        self.widgets_casa_atual.append(label_guardar_card_exibido)               
        # Botão SIM
        botao_sim_card = ctk.CTkButton(
        self.root,
        fg_color='black',
        width= 16,
        border_color= "white",
        border_width= 1,
        hover_color=self.back_end.cor_layout_atual,
        text="yes",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.back_end.adicionar_carta_a_cartas_player("Aphrodite"),
                         self.atualizar_cartas(), 
                         self.limpar_widgets_casa_atual(),
                         self.casa_evento_001()) # volta para o menu inicial, usar dado ou carta
                        )
        botao_sim_card.place(x=600, y=360, anchor="center")
        self.widgets_casa_atual.append(botao_sim_card)
        # Botão NÃO
        botao_naum_card = ctk.CTkButton(
        self.root,
        fg_color='black',
        width= 16,
        border_color= "white",
        border_width= 1,
        hover_color="red",
        text="no",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.limpar_widgets_casa_atual(), self.casa_evento_001()) # abre pra jogar dado ou carta
        )
        botao_naum_card.place(x=700, y=360, anchor="center")
        self.widgets_casa_atual.append(botao_naum_card) 


    def casa_evento_089(self): # casa em branco
        self.limpar_widgets_casa_atual()        
        self.casa_evento_001()     
   
                             
    def casa_evento_090(self): # EROS
            self.limpar_widgets_casa_atual()       
            # label do nome da casa exibida
            label_nome_casa_evento = ctk.CTkLabel(
                self.root,
                text= "Eros", 
                text_color="white",  
                fg_color="black",
                font=("Olympus", 24), 
                )
            label_nome_casa_evento.place(x=450, y=110, anchor ="n")
            self.widgets_casa_atual.append(label_nome_casa_evento)                
            #IMAGEM DA CASA
            self.image_evento_exibido = PhotoImage(file="images/casa_090_eros.png")
            self.label_evento_exibido = tk.Label(
                    self.root,
                    image=self.image_evento_exibido,
                    bg="black"
                )
            self.label_evento_exibido.place(x=450, y=140, anchor='n')
            self.widgets_casa_atual.append(self.label_evento_exibido)
            texto_evento = ("""You met Eros and 
were struck by love's arrow.

Return to the house 
of Aphrodite,
the Goddess of 
beauty and Love."""
            )
            # label de descrição do evento
            label_descricao_evento = ctk.CTkLabel(
                self.root,
                text=texto_evento,  
                text_color="white",  
                fg_color="black",
                font=("Cambria", 17), 
            )
            label_descricao_evento.place(x=650, y=140, anchor ="n")
            self.widgets_casa_atual.append(label_descricao_evento)
            
            # vontade dos deuses
            self.botao_vontade_dos_deuses(casas_avanco=0, casas_retrocesso=2, vida_mais=0, vida_menos=0, pontos_mais= 60, pontos_menos=60)
            self.chamada_cartas_eventos()


    def casa_evento_091(self): # casa em branco
        self.limpar_widgets_casa_atual()        
        self.casa_evento_001()     
   
    def casa_evento_092(self): # casa em branco
        self.limpar_widgets_casa_atual()        
        self.casa_evento_001()     
   
                             
    def casa_evento_093(self): # PEGASO
            self.limpar_widgets_casa_atual()       
            # label do nome da casa exibida
            label_nome_casa_evento = ctk.CTkLabel(
                self.root,
                text= "Pegasus", 
                text_color="white",  
                fg_color="black",
                font=("Olympus", 24), 
                )
            label_nome_casa_evento.place(x=450, y=110, anchor ="n")
            self.widgets_casa_atual.append(label_nome_casa_evento)                
            #IMAGEM DA CASA
            self.image_evento_exibido = PhotoImage(file="images/casa_093_pegaso.png")
            self.label_evento_exibido = tk.Label(
                    self.root,
                    image=self.image_evento_exibido,
                    bg="black"
                )
            self.label_evento_exibido.place(x=450, y=140, anchor='n')
            self.widgets_casa_atual.append(self.label_evento_exibido)
            texto_evento = ("""Hop on the
winged horse 
and advance 
6 spaces"""
            )
            # label de descrição do evento
            label_descricao_evento = ctk.CTkLabel(
                self.root,
                text=texto_evento,  
                text_color="white",  
                fg_color="black",
                font=("Cambria", 17), 
            )
            label_descricao_evento.place(x=650, y=140, anchor ="n")
            self.widgets_casa_atual.append(label_descricao_evento)
            
            # vontade dos deuses
            self.botao_vontade_dos_deuses(casas_avanco=6, casas_retrocesso=0, vida_mais=0, vida_menos=0, pontos_mais= 180, pontos_menos=0)
            self.chamada_cartas_eventos()


    def casa_evento_094(self): # casa em branco
        self.limpar_widgets_casa_atual()        
        self.casa_evento_001()  

    def casa_evento_095(self): # casa em branco
        self.limpar_widgets_casa_atual()        
        self.casa_evento_001()  
   
                            
    def casa_evento_096(self): # DIONISIO
            self.limpar_widgets_casa_atual()       
            # label do nome da casa exibida
            label_nome_casa_evento = ctk.CTkLabel(
                self.root,
                text= "Dionisius", 
                text_color="white",  
                fg_color="black",
                font=("Olympus", 24), 
                )
            label_nome_casa_evento.place(x=450, y=110, anchor ="n")
            self.widgets_casa_atual.append(label_nome_casa_evento)                
            #IMAGEM DA CASA
            self.image_evento_exibido = PhotoImage(file="images/casa_096_dionisio.png")
            self.label_evento_exibido = tk.Label(
                    self.root,
                    image=self.image_evento_exibido,
                    bg="black"
                )
            self.label_evento_exibido.place(x=450, y=140, anchor='n')
            self.widgets_casa_atual.append(self.label_evento_exibido)
            
            texto_evento = ("""Gain 300 points
and advance
1 space
or
move forward
3 spaces."""
            )
            # label de descrição do evento
            label_descricao_evento = ctk.CTkLabel(
                self.root,
                text=texto_evento,  
                text_color="white",  
                fg_color="black",
                font=("Cambria", 17), 
            )
            label_descricao_evento.place(x=650, y=140, anchor ="n")
            self.widgets_casa_atual.append(label_descricao_evento)
            
            botao_avance= ctk.CTkButton(
            self.canvas_abre,
            fg_color='black',
            width= 70,
            border_color= "white",
            border_width= 1,
            hover_color=self.cor_Layout,
            text="Advance 3 spaces",
            font=("Gelio Greek Diner", 18),
            command=lambda: (self.vontade_dos_deuses(casas_avanco=3, casas_retrocesso=0, vida_mais=0, vida_menos=0, pontos_mais=45, pontos_menos=0),
                            self.atualizar_cartas(),
                            self.carregar_casa(self.back_end.casa_atual)))
            botao_avance.place(x=650, y=320, anchor="n")
            self.widgets_casa_atual.append(botao_avance)
        
            # Botão carta 1
            botao_carta_dioni = ctk.CTkButton(
            self.canvas_abre,
            fg_color='black',
            width= 70,
            border_width= 1,
            border_color= "white",
            hover_color=self.back_end.cor_layout_atual,
            text="Gain 300 points",
            font=("Gelio Greek Diner", 18),
            command=lambda: (self.vontade_dos_deuses(casas_avanco=1, casas_retrocesso=0, vida_mais=0, vida_menos=0, pontos_mais=300, pontos_menos=0),
                             self.atualizar_tela(),
                             self.carregar_casa(self.back_end.casa_atual)) #
            )
            botao_carta_dioni.place(x=650, y=400, anchor='n')
            self.widgets_casa_atual.append(botao_carta_dioni)  
            

    def casa_evento_097(self): # casa em branco
        self.limpar_widgets_casa_atual()        
        self.casa_evento_001() 
        
                                    
    def casa_evento_098(self): # BACANTES
            self.limpar_widgets_casa_atual()       
            # label do nome da casa exibida
            label_nome_casa_evento = ctk.CTkLabel(
                self.root,
                text= "Bacchaes", 
                text_color="white",  
                fg_color="black",
                font=("Olympus", 24), 
                )
            label_nome_casa_evento.place(x=450, y=110, anchor ="n")
            self.widgets_casa_atual.append(label_nome_casa_evento)                
            #IMAGEM DA CASA
            self.image_evento_exibido = PhotoImage(file="images/casa_098_bacantes.png")
            self.label_evento_exibido = tk.Label(
                    self.root,
                    image=self.image_evento_exibido,
                    bg="black"
                )
            self.label_evento_exibido.place(x=450, y=140, anchor='n')
            self.widgets_casa_atual.append(self.label_evento_exibido)
            texto_evento = ("""You fell into the
Bacchae's orgy and drank
too much wine during the party.
Move back
5 spaces 
and
lose 1 life"""
            )
            # label de descrição do evento
            label_descricao_evento = ctk.CTkLabel(
                self.root,
                text=texto_evento,  
                text_color="white",  
                fg_color="black",
                font=("Cambria", 17), 
            )
            label_descricao_evento.place(x=650, y=140, anchor ="n")
            self.widgets_casa_atual.append(label_descricao_evento)
            
            # vonatde dos deuses
            self.botao_vontade_dos_deuses(casas_avanco=0, casas_retrocesso=5, vida_mais=0, vida_menos=1, pontos_mais= 0, pontos_menos=60)
            self.chamada_cartas_eventos()


    def casa_evento_099(self): # casa em branco
        self.limpar_widgets_casa_atual()        
        self.casa_evento_001()    
   
                                    
    def casa_evento_100(self): # PAN
            self.limpar_widgets_casa_atual()       
            # label do nome da casa exibida
            label_nome_casa_evento = ctk.CTkLabel(
                self.root,
                text= "Pan", 
                text_color="white",  
                fg_color="black",
                font=("Olympus", 24), 
                )
            label_nome_casa_evento.place(x=450, y=110, anchor ="n")
            self.widgets_casa_atual.append(label_nome_casa_evento)                
            #IMAGEM DA CASA
            self.image_evento_exibido = PhotoImage(file="images/casa_100_pan.png")
            self.label_evento_exibido = tk.Label(
                    self.root,
                    image=self.image_evento_exibido,
                    bg="black"
                )
            self.label_evento_exibido.place(x=450, y=140, anchor='n')
            self.widgets_casa_atual.append(self.label_evento_exibido)
            texto_evento = ("""Upon hearing his chilling scream,
you were so scared that you
almost gave up on
reaching Olympus.
Go back to space 94
and
lost 1 life"""
            )
            # label de descrição do evento
            label_descricao_evento = ctk.CTkLabel(
                self.root,
                text=texto_evento,  
                text_color="white",  
                fg_color="black",
                font=("Cambria", 17), 
            )
            label_descricao_evento.place(x=660, y=140, anchor ="n")
            self.widgets_casa_atual.append(label_descricao_evento)
            
          # vontade dos deuses
            self.botao_vontade_dos_deuses(casas_avanco=0, casas_retrocesso=6, vida_mais=0, vida_menos=1, pontos_mais= 0, pontos_menos=60)
            self.chamada_cartas_eventos()


    def casa_evento_101(self): # casa em branco
        self.limpar_widgets_casa_atual()        
        self.casa_evento_001()    
      
    def casa_evento_102(self): # casa em branco
        self.limpar_widgets_casa_atual()        
        self.casa_evento_001()    
      
    def casa_evento_103(self): # casa em branco
        self.limpar_widgets_casa_atual()        
        self.casa_evento_001()    
     
      
    def casa_evento_104(self): # casa da carta ARTEMIS
        self.limpar_widgets_casa_atual()        
        try:
            img = Image.open(self.back_end.cartas_deuses[2]['imagem']) 
            self.image_carta_exibida = ImageTk.PhotoImage(img)
            self.label_imagem_carta = tk.Label(self.canvas_abre, image=self.image_carta_exibida, bg="black")
            self.label_imagem_carta.place(x=440, y=130, anchor="n")
            self.widgets_casa_atual.append(self.label_imagem_carta)
        except Exception as e:
            print(f'Sem imagens nessa carta, usando a imagem default -> {e}')
               
        label_descricao_carta1 = ctk.CTkLabel(
            self.root,
            text= 'Card abilities:', 
            text_color=self.back_end.cor_layout_atual,  
            fg_color="black",
            font=("Gelio Fasolada", 18), 
        )
        label_descricao_carta1.place(x=650, y=130, anchor ="n")
        self.widgets_casa_atual.append(label_descricao_carta1)
        
        label_casa = ctk.CTkLabel(
            self.root,
            text= self.back_end.cartas_deuses[2]['action_p'], # texto descritivo da carta
            text_color="white",
            bg_color="black",
            font=("cambria", 18),
        )
        label_casa.place(x=650, y=160, anchor='n')
        self.widgets_casa_atual.append(label_casa)
        
        # Quer guardar a carta?
        label_guardar_card_exibido = ctk.CTkLabel(
            self.root,
            text= "Do you keep the card?",
            text_color= self.back_end.cor_layout_atual,  
            fg_color="black",  
            font=("Gelio Fasolada", 17), 
        )
        label_guardar_card_exibido.place(x=650, y=320, anchor ="center")
        self.widgets_casa_atual.append(label_guardar_card_exibido)               
        # Botão SIM
        botao_sim_card = ctk.CTkButton(
        self.root,
        fg_color='black',
        width= 16,
        border_color= "white",
        border_width= 1,
        hover_color=self.back_end.cor_layout_atual,
        text="yes",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.back_end.adicionar_carta_a_cartas_player("Artemis"),
                         self.atualizar_cartas(), 
                         self.limpar_widgets_casa_atual(),
                         self.casa_evento_001()) # volta para o menu inicial, usar dado ou carta
                        )
        botao_sim_card.place(x=600, y=360, anchor="center")
        self.widgets_casa_atual.append(botao_sim_card)
        # Botão NÃO
        botao_naum_card = ctk.CTkButton(
        self.root,
        fg_color='black',
        width= 16,
        border_color= "white",
        border_width= 1,
        hover_color="red",
        text="no",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.limpar_widgets_casa_atual(), self.casa_evento_001()) # abre pra jogar dado ou carta
        )
        botao_naum_card.place(x=700, y=360, anchor="center")
        self.widgets_casa_atual.append(botao_naum_card) 
 
  
    def casa_evento_105(self): # casa em branco
        self.limpar_widgets_casa_atual()        
        self.casa_evento_001()    
         
    def casa_evento_106(self): # casa em branco
        self.limpar_widgets_casa_atual()        
        self.casa_evento_001()  

                                            
    def casa_evento_107(self): # ORION
            self.limpar_widgets_casa_atual()       
            # label do nome da casa exibida
            label_nome_casa_evento = ctk.CTkLabel(
                self.root,
                text= "Orion", 
                text_color="white",  
                fg_color="black",
                font=("Olympus", 24), 
                )
            label_nome_casa_evento.place(x=450, y=110, anchor ="n")
            self.widgets_casa_atual.append(label_nome_casa_evento)                
            #IMAGEM DA CASA
            self.image_evento_exibido = PhotoImage(file="images/casa_107_orion.png")
            self.label_evento_exibido = tk.Label(
                    self.root,
                    image=self.image_evento_exibido,
                    bg="black"
                )
            self.label_evento_exibido.place(x=450, y=140, anchor='n')
            self.widgets_casa_atual.append(self.label_evento_exibido)
            texto_evento = ("""The son of Poseidon
was furious that you crossed 
his hunting grounds.
Face the hunter.
If you lose, 
you lose a life"""
            )
            # label de descrição do evento
            label_descricao_evento = ctk.CTkLabel(
                self.root,
                text=texto_evento,  
                text_color="white",  
                fg_color="black",
                font=("Cambria", 17), 
            )
            label_descricao_evento.place(x=650, y=140, anchor ="n")
            self.widgets_casa_atual.append(label_descricao_evento)
            
            self.chamada_do_dado_batalha(casas_avanco=2, casas_retrocesso=2, vida=1)
            self.chamada_cartas_eventos()

     
    def casa_evento_108(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001()    
      
    def casa_evento_109(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001() 
            
                                            
    def casa_evento_110(self): # MIDAS
            self.limpar_widgets_casa_atual()       
            # label do nome da casa exibida
            label_nome_casa_evento = ctk.CTkLabel(
                self.root,
                text= "Midas", 
                text_color="white",  
                fg_color="black",
                font=("Olympus", 24), 
                )
            label_nome_casa_evento.place(x=450, y=110, anchor ="n")
            self.widgets_casa_atual.append(label_nome_casa_evento)                
            #IMAGEM DA CASA
            self.image_evento_exibido = PhotoImage(file="images/casa_110_midas.png")
            self.label_evento_exibido = tk.Label(
                    self.root,
                    image=self.image_evento_exibido,
                    bg="black"
                )
            self.label_evento_exibido.place(x=450, y=140, anchor='n')
            self.widgets_casa_atual.append(self.label_evento_exibido)
            texto_evento = ("""The greedy king embraced you 
and you turned into a gold statue.
To reverse the transformation, 
return to Dionysus' house 
and seek the god's help.."""
            )
            # label de descrição do evento
            label_descricao_evento = ctk.CTkLabel(
                self.root,
                text=texto_evento,  
                text_color="white",  
                fg_color="black",
                font=("Cambria", 17), 
            )
            label_descricao_evento.place(x=660, y=140, anchor ="n")
            self.widgets_casa_atual.append(label_descricao_evento)
            
            # vontade dos deuses
            self.botao_vontade_dos_deuses(casas_avanco=0, casas_retrocesso=14, vida_mais=0, vida_menos=0, pontos_mais= 0, pontos_menos=300)
            self.chamada_cartas_eventos()

   
    def casa_evento_111(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001()    
    
        
    def casa_evento_112(self): # casa da carta ZEUS
        self.limpar_widgets_casa_atual()        
        try:
            img = Image.open(self.back_end.cartas_deuses[10]['imagem']) 
            self.image_carta_exibida = ImageTk.PhotoImage(img)
            self.label_imagem_carta = tk.Label(self.canvas_abre, image=self.image_carta_exibida, bg="black")
            self.label_imagem_carta.place(x=440, y=130, anchor="n")
            self.widgets_casa_atual.append(self.label_imagem_carta)
        except Exception as e:
            print(f'Sem imagens nessa carta, usando a imagem default -> {e}')
               
        label_descricao_carta1 = ctk.CTkLabel(
            self.root,
            text= 'Card abilities:', 
            text_color=self.back_end.cor_layout_atual,  
            fg_color="black",
            font=("Gelio Fasolada", 18), 
        )
        label_descricao_carta1.place(x=650, y=130, anchor ="n")
        self.widgets_casa_atual.append(label_descricao_carta1)
        
        label_casa = ctk.CTkLabel(
            self.root,
            text= self.back_end.cartas_deuses[10]['action_p'], # texto descritivo da carta
            text_color="white",
            bg_color="black",
            font=("cambria", 18),
        )
        label_casa.place(x=650, y=160, anchor='n')
        self.widgets_casa_atual.append(label_casa)
        
        # Quer guardar a carta?
        label_guardar_card_exibido = ctk.CTkLabel(
            self.root,
            text= "Do you keep the card?",
            text_color= self.back_end.cor_layout_atual,  
            fg_color="black",  
            font=("Gelio Fasolada", 17), 
        )
        label_guardar_card_exibido.place(x=650, y=320, anchor ="center")
        self.widgets_casa_atual.append(label_guardar_card_exibido)               
        # Botão SIM
        botao_sim_card = ctk.CTkButton(
        self.root,
        fg_color='black',
        width= 16,
        border_color= "white",
        border_width= 1,
        hover_color=self.back_end.cor_layout_atual,
        text="yes",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.back_end.adicionar_carta_a_cartas_player("Zeus"),
                         self.atualizar_cartas(), 
                         self.limpar_widgets_casa_atual(),
                         self.casa_evento_001()) # volta para o menu inicial, usar dado ou carta
                        )
        botao_sim_card.place(x=600, y=360, anchor="center")
        self.widgets_casa_atual.append(botao_sim_card)
        # Botão NÃO
        botao_naum_card = ctk.CTkButton(
        self.root,
        fg_color='black',
        width= 16,
        border_color= "white",
        border_width= 1,
        hover_color="red",
        text="no",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.limpar_widgets_casa_atual(), self.casa_evento_001()) # abre pra jogar dado ou carta
        )
        botao_naum_card.place(x=700, y=360, anchor="center")
        self.widgets_casa_atual.append(botao_naum_card) 
 
  
    def casa_evento_113(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001()      
  
    def casa_evento_114(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001()    

    def casa_evento_115(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001()    

                                           
    def casa_evento_116(self): # CRONOS
            self.limpar_widgets_casa_atual()       
            # label do nome da casa exibida
            label_nome_casa_evento = ctk.CTkLabel(
                self.root,
                text= "Chronos", 
                text_color="white",  
                fg_color="black",
                font=("Olympus", 24), 
                )
            label_nome_casa_evento.place(x=450, y=110, anchor ="n")
            self.widgets_casa_atual.append(label_nome_casa_evento)                
            #IMAGEM DA CASA
            self.image_evento_exibido = PhotoImage(file="images/casa_116_cronos.png")
            self.label_evento_exibido = tk.Label(
                    self.root,
                    image=self.image_evento_exibido,
                    bg="black"
                )
            self.label_evento_exibido.place(x=450, y=140, anchor='n')
            self.widgets_casa_atual.append(self.label_evento_exibido)
            texto_evento = ("""You have been 
trapped in time.

Go back 5 spaces
and 
lose 1 life.."""
            )
            # label de descrição do evento
            label_descricao_evento = ctk.CTkLabel(
                self.root,
                text=texto_evento,  
                text_color="white",  
                fg_color="black",
                font=("Cambria", 17), 
            )
            label_descricao_evento.place(x=650, y=140, anchor ="n")
            self.widgets_casa_atual.append(label_descricao_evento)
            # vontade dos deuses
            self.botao_vontade_dos_deuses(casas_avanco=0, casas_retrocesso=5, vida_mais=0, vida_menos=1, pontos_mais=0, pontos_menos=60)
            self.chamada_cartas_eventos()


    def casa_evento_117(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001() 
    
    def casa_evento_118(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_001() 
    
                                            
    def casa_evento_119(self): # GRIFOS
            self.limpar_widgets_casa_atual()       
            # label do nome da casa exibida
            label_nome_casa_evento = ctk.CTkLabel(
                self.root,
                text= "Griffins", 
                text_color="white",  
                fg_color="black",
                font=("Olympus", 24), 
                )
            label_nome_casa_evento.place(x=450, y=110, anchor ="n")
            self.widgets_casa_atual.append(label_nome_casa_evento)                
            #IMAGEM DA CASA
            self.image_evento_exibido = PhotoImage(file="images/casa_119_grifos.png")
            self.label_evento_exibido = tk.Label(
                    self.root,
                    image=self.image_evento_exibido,
                    bg="black"
                )
            self.label_evento_exibido.place(x=450, y=140, anchor='n')
            self.widgets_casa_atual.append(self.label_evento_exibido)
            texto_evento = ("""The entrance to Mount Olympus
is heavily guarded.
You cannot use any 
God's help cards.
Now, only your skill counts!
Try to pass its guardians."""
            )
            # label de descrição do evento
            label_descricao_evento = ctk.CTkLabel(
                self.root,
                text=texto_evento,  
                text_color="white",  
                fg_color="black",
                font=("Cambria", 17), 
            )
            label_descricao_evento.place(x=650, y=140, anchor ="n")
            self.widgets_casa_atual.append(label_descricao_evento)            
            # Dados
            self.chamada_do_dado_batalha_troia(casas_avanco=1, casas_retrocesso=2, vida=1)
            

     # CASA FINAL !!!!          


    def casa_evento_120(self): # casa em branco
            self.limpar_widgets_casa_atual() 
            
            
           #IMAGEM DA CASA # iMAGEM DO MONTE OLIMPO
            self.image_evento_exibido = PhotoImage(file="images/olimpo.png")
            self.label_evento_exibido = tk.Label(
                    self.root,
                    image=self.image_evento_exibido,
                    bg="black"
                )
            self.label_evento_exibido.place(x=330, y=120)
            self.widgets_casa_atual.append(self.label_evento_exibido)
            
            # titulo welcome to olimpo       
            label_nome_casa_evento = ctk.CTkLabel(
                    self.root,
                    text= "Welcome to\nOlympus", 
                    text_color= "#FFA500", # LARANJA - > self.cor_Layout,  
                    fg_color="black",
                    font=("Olympus", 24), 
                    )
            label_nome_casa_evento.place(x=680, y=130, anchor ="n")
            self.widgets_casa_atual.append(label_nome_casa_evento)                

            texto_evento = ("""You have won!"
"Now you can ask 
the Gods for 
your boon!"
"They will grant it 
to you, or maybe not,
who knows? "
"The Greek Gods 
are temperamental."""
    )
            # label de descrição do evento
            label_descricao_evento = ctk.CTkLabel(
                self.root,
                text=texto_evento,  
                text_color="white",  
                fg_color="black",
                font=("Cambria", 17), 
            )
            label_descricao_evento.place(x=680, y=190, anchor ="n")
            self.widgets_casa_atual.append(label_descricao_evento) 
            
            # Score
            botao_score = ctk.CTkButton(
            self.canvas_abre,
            width= 100,
            fg_color= "#4DC2F5", # AZUL     
            hover_color= "#FFA500", # Laranja
            text="View score",
            font= ("Gelio Fasolada", 18), # text_color="black",  
            command=lambda: (self.atualizar_cor_layout(),
                             self.casa_evento_126() )
        )
            botao_score.place(x=420, y=405, anchor="n")
            self.widgets_casa_atual.append(botao_score)
                        
            # registrar_vitoria
            botao_registrar_vitoria = ctk.CTkButton(
            self.canvas_abre,
            width= 100,
            fg_color= "#2DCD70", # VERDE      #'#FF0000', RED
            hover_color= "#FFA500", #self.back_end.cores_layout['laranja']  # "#FFA500"
            text="Record victory", 
            font= ("Gelio Fasolada", 18), # text_color="black", 
            command=lambda: (self.atualizar_cor_layout(),
                             self.casa_evento_126() )
        )
            botao_registrar_vitoria.place(x=550, y=405, anchor="n")
            self.widgets_casa_atual.append(botao_registrar_vitoria)    
            
             
            # Botao restart GAME
            botao_iniciar = ctk.CTkButton(
            self.canvas_abre,
            width= 100,
            fg_color= '#FF0000', #'#FF0000', RED
            hover_color="#FFA500", #self.back_end.cores_layout['laranja']  # "#FFA500"
            text="Restart Game", 
            font= ("Gelio Fasolada", 18),
            command=lambda: (self.back_end.restart_game(),
                             self.atualizar_cor_layout(),
                             self.telas_iniciais.tela_02())
        )
            botao_iniciar.place(x=690, y=405, anchor="n")
            self.widgets_casa_atual.append(botao_iniciar)    
                
                        



    def casa_evento_121(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_120()
            
    def casa_evento_122(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_120()
                       
    def casa_evento_123(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_120()
                
    def casa_evento_124(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_120()
        
    def casa_evento_125(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            self.casa_evento_120()
            
            
    def casa_evento_126(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            print('implementar placar!!')






# CARTAS DE AÇÃO  # FUNÇÕES # CARTAS DE AÇÃO  # FUNÇÕES  # CARTAS DE AÇÃO

    def chama_foto_carta(self, index_dicionario_deuses): # insere a foto da carta do deus
        try:
            # Carrega a imagem usando PIL
            img = Image.open(self.back_end.cartas_deuses[index_dicionario_deuses]['imagem']) 
            # Converte a imagem para PhotoImage
            self.image_carta_exibida = ImageTk.PhotoImage(img)
            # Cria um Label para exibir a imagem no Canvas
            self.label_imagem_carta = tk.Label(self.canvas_abre, image=self.image_carta_exibida, bg="black")
            self.label_imagem_carta.place(x=440, y=275, anchor="center")
            
            self.widgets_casa_atual.append(self.label_imagem_carta)
            # Adiciona o Label à lista de widgets dinâmicos
            #self.widgets_dinamicos.append(self.label_imagem_carta)
        except Exception as e:
            print(f'Sem imagens nessa carta, usando a imagem default -> {e}')
  
    def chamar_casa_evento(self):# cria uma referencia pra casa atual, pra carta voltar pra ela se não for usada
        # Obtém o número da casa atual
        casa_atual = self.back_end.casa_atual  
        # Formata o nome do método correspondente
        nome_metodo = f"casa_evento_{str(casa_atual).zfill(3)}"
        # Verifica se o método existe na classe
        if hasattr(self, nome_metodo):
            metodo = getattr(self, nome_metodo)
            # Chama o método correspondente
            metodo()
        else:
            print(f"Erro: O método '{nome_metodo}' não existe.")

    def remover_carta(self, nome):# Remove uma carta usada da lista de cartas_player pelo nome.
        # Verifica se a carta existe na lista
        carta_encontrada = next((carta for carta in self.back_end.cartas_player if carta["nome"] == nome), None) 
        if carta_encontrada:
            self.back_end.cartas_player.remove(carta_encontrada) # apaga a carta encontrada
            print(f"Carta '{nome}' removida com sucesso.")
        else:
            print(f"Carta '{nome}' não encontrada na lista.")
        # atualiza a tela apos a remoção
        self.atualizar_tela()
        
    def chamada_do_dado_batalha_carta_deuses(self, casas_avanco=0, casas_retrocesso=0, vida=0, nome_deus=None):  
        # Vitoria
        self.label_vitoria= ctk.CTkLabel(
            self.root,
            text= "Victory => advance 1 space", 
            text_color= 'gray',  
            bg_color= "black",  
            font=("Gelio Fasolada", 13),
            )          
        self.label_vitoria.place(x=650, y=190, anchor="n")
        self.widgets_casa_atual.append(self.label_vitoria)
        # Ganha +4
        self.label_4_mais = ctk.CTkLabel(
            self.root,
            text= "+4", 
            text_color= 'green',  
            bg_color= "black",  
            font=("Gelio Fasolada", 18),
            )          
        self.label_4_mais.place(x=710, y=225, anchor="n") 
        self.widgets_casa_atual.append(self.label_4_mais)
       # Perde -3
        self.label_4_mais = ctk.CTkLabel(
            self.root,
            text= "-3", 
            text_color= 'red',  
            bg_color= "black",  
            font=("Gelio Fasolada", 18),
            )          
        self.label_4_mais.place(x=710, y=250, anchor="n") 
        self.widgets_casa_atual.append(self.label_4_mais)
           
    # Configura o dado no canvas e exibe o botão de rolar.
        self.animacao_ativa = True
        # Canvas para o dado
        self.canvas = tk.Canvas(self.root, width=80, height=80, bg="black", highlightthickness=0)
        self.canvas.place(x=650, y=210, anchor='n')  # Posição do dado
        self.widgets_casa_atual.append(self.canvas)  # Adiciona o canvas à lista
        # Carrega o GIF com PIL
        self.gif = Image.open(self.imagem_dado)
        self.frames = []
        # Extrai os quadros do GIF
        try:
            while True:
                frame = self.gif.copy()
                frame = frame.convert("RGBA")  # Certificar-se de que está em RGBA
                # Adicionar fundo preto onde há transparência
                black_bg = Image.new("RGBA", frame.size, "black")
                frame = Image.alpha_composite(black_bg, frame)
                # Redimensionar o quadro
                frame = frame.resize((80, 80), Image.Resampling.LANCZOS)
                # Converter para PhotoImage
                self.frames.append(ImageTk.PhotoImage(frame))
                self.gif.seek(len(self.frames))  # Avançar para o próximo quadro
        except EOFError:
            pass  # Final do GIF
        # Configuração inicial do Canvas
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor="nw", image=self.frames[0])
        self.current_frame = 0       
        self.play_gif()# Exibe a animação
        # Botão de rolagem de dados
        botao_rolar_dados = ctk.CTkButton(
            self.canvas_abre,
            fg_color='black',
            width=100,
            border_width=1,
            border_color="white",
            hover_color=self.back_end.cor_layout_atual,
            text="Roll a die!",
            font=("Gelio Greek Diner", 18),
            command=lambda: (self.rolar_dado_de_batalha(casas_avanco, casas_retrocesso, vida),
                             self.remover_carta(nome_deus),
                             self.atualizar_cartas()) 
        )
        botao_rolar_dados.place(x=650, y=295, anchor='n')
        self.widgets_casa_atual.append(botao_rolar_dados)
        
        # for battles
        self.label_battles= ctk.CTkLabel(
            self.root,
            text= "For battles only", 
            text_color= 'gray',  
            bg_color= "black",  
            font=("Gelio Fasolada", 13),
            )          
        self.label_battles.place(x=650, y=325, anchor="n")
        self.widgets_casa_atual.append(self.label_battles)
        
        
              
    def botao_nao_usar_carta(self):
        botao_naum = ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 50,
        border_color= "white",
        border_width= 1,
        hover_color="red",
        text="NO",
        font=("Gelio Greek Diner", 18),
        command= lambda:(self.chamar_casa_evento(),
                         self.atualizar_tela(),
                         self.carregar_casa(self.back_end.casa_atual))
        )
        botao_naum.place(x=650, y=405, anchor="center")
        self.widgets_casa_atual.append(botao_naum)


 # CARTAS DE AÇÃO   # CARTAS DE AÇÃO  # CARTAS DE AÇÃO  # CARTAS DE AÇÃO  # CARTAS DE AÇÃO
   
    def use_carta_Aphrodite(self):
        self.limpar_widgets_casa_atual()  
        
        self.chama_foto_carta(0) # index afrodite  
        
        botao_avance= ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 70,
        border_color= "white",
        border_width= 1,
        hover_color=self.cor_Layout,
        text="Advance 6 spaces",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.vontade_dos_deuses(casas_avanco=6, casas_retrocesso=0, vida_mais=0, vida_menos=0, pontos_mais=90, pontos_menos=0),
                         self.remover_carta('Aphrodite'),
                         self.atualizar_cartas(),
                         self.carregar_casa(self.back_end.casa_atual)))
        botao_avance.place(x=650, y=200, anchor="center")
        self.widgets_casa_atual.append(botao_avance)
        
        
        botao_skip= ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 70,
        border_color= "white",
        border_width= 1,
        hover_color=self.cor_Layout,
        text="Go back 1 space",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.vontade_dos_deuses(casas_avanco=0, casas_retrocesso=1, vida_mais=0, vida_menos=0, pontos_mais=0, pontos_menos=0),
                         self.remover_carta('Aphrodite'),
                         self.atualizar_cartas(),
                         self.carregar_casa(self.back_end.casa_atual)))
        botao_skip.place(x=650, y=300, anchor="center")
        self.widgets_casa_atual.append(botao_skip)  
        
        self.botao_nao_usar_carta()
        
        
        # self.limpar_widgets_casa_atual()
        # self.atualizar_tela()
        # self.carregar_casa(self.back_end.casa_atual)
        
        # Título
        # label_nome_actions = ctk.CTkLabel(
        #     self.root,
        #     text= "Advance\n6 spaces", 
        #     text_color="white",  
        #     fg_color="black",
        #     font=("cambria", 21), # "Olympus"
        #     )
        # label_nome_actions.place(x=650, y=200, anchor ="n")
        # self.widgets_dinamicos.append(label_nome_actions)        
        # # Botão SIM
        # botao_sim = ctk.CTkButton(
        # self.canvas_abre,
        # fg_color='black',
        # width= 70,
        # border_color= "white",
        # border_width= 1,
        # hover_color=self.cor_Layout,
        # text="YES",
        # font=("Gelio Greek Diner", 22),
        # command=lambda: (self.vontade_dos_deuses(casas_avanco=6, casas_retrocesso=0, vida_mais=0, vida_menos=0, pontos_mais=90, pontos_menos=0),
        #                  self.remover_carta('Aphrodite'),
        #                  self.atualizar_cartas())
        # )
        # botao_sim.place(x=600, y=350, anchor="center")
        # self.widgets_casa_atual.append(botao_sim)
        
        
        # Botão NÃO
        # botao_naum = ctk.CTkButton(
        # self.canvas_abre,
        # fg_color='black',
        # width= 70,
        # border_color= "white",
        # border_width= 1,
        # hover_color="red",
        # text="NO",
        # font=("Gelio Greek Diner", 22),
        # command= lambda:(self.chamar_casa_evento(),
        #                  self.atualizar_tela(),
        #                  self.carregar_casa(self.back_end.casa_atual))
        # )
        # botao_naum.place(x=700, y=350, anchor="center")
        # self.widgets_casa_atual.append(botao_naum)
        

    def use_carta_Apollo(self):
        self.limpar_widgets_casa_atual()  
        
        self.chama_foto_carta(1) # index Apolo 
         
        self.chamada_do_dado_batalha_carta_deuses(1,0,0,"Apollo")  
        
         # SKIP
        botao_skip= ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 70,
        border_color= "white",
        border_width= 1,
        hover_color=self.cor_Layout,
        text="Skip 1 space",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.vontade_dos_deuses(casas_avanco=1, casas_retrocesso=0, vida_mais=0, vida_menos=0, pontos_mais=15, pontos_menos=0),
                         self.remover_carta('Apollo'),
                         self.atualizar_cartas(),
                         self.carregar_casa(self.back_end.casa_atual)))
        botao_skip.place(x=650, y=140, anchor="center")
        self.widgets_casa_atual.append(botao_skip)   
        self.botao_nao_usar_carta()
             
        
    def use_carta_Artemis(self):
        self.limpar_widgets_casa_atual()  
        self.chama_foto_carta(2) # index Artemis 
        
        self.chamada_do_dado_batalha_carta_deuses(1,0,0,nome_deus="Artemis")  
                
        botao_avance= ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 70,
        border_color= "white",
        border_width= 1,
        hover_color=self.cor_Layout,
        text="Advance 3 spaces",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.vontade_dos_deuses(casas_avanco=3, casas_retrocesso=0, vida_mais=0, vida_menos=0, pontos_mais=45, pontos_menos=0),
                         self.remover_carta('Artemis'),
                         self.atualizar_cartas(),
                         self.carregar_casa(self.back_end.casa_atual))
        )
        botao_avance.place(x=650, y=150, anchor="center")
        self.widgets_casa_atual.append(botao_avance)
        
        self.botao_nao_usar_carta()
           
                 
    def use_carta_Ares(self):
        self.limpar_widgets_casa_atual()  
        
        self.chama_foto_carta(3) # index Ares
        
        self.chamada_do_dado_batalha_carta_deuses(1,0,0,nome_deus="Ares")  
                
        botao_avance= ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 70,
        border_color= "white",
        border_width= 1,
        hover_color=self.cor_Layout,
        text="Win 1 battle",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.vontade_dos_deuses(casas_avanco=1, casas_retrocesso=0, vida_mais=0, vida_menos=0, pontos_mais=100, pontos_menos=0),
                         self.remover_carta('Ares'),
                         self.atualizar_cartas(),
                         self.carregar_casa(self.back_end.casa_atual))
        )
        botao_avance.place(x=650, y=150, anchor="center")
        self.widgets_casa_atual.append(botao_avance)
        
        self.botao_nao_usar_carta()
           

    def use_carta_Hades(self): 
        self.limpar_widgets_casa_atual() 
         
        self.chama_foto_carta(4) # index Hades
                
        botao_avance= ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 70,
        border_color= "white",
        border_width= 1,
        hover_color=self.cor_Layout,
        text="Gain one life",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.vontade_dos_deuses(casas_avanco=1, casas_retrocesso=0, vida_mais=1, vida_menos=0, pontos_mais=15, pontos_menos=0),
                         self.remover_carta('Hades'),
                         self.atualizar_cartas(),
                         self.carregar_casa(self.back_end.casa_atual))
        )
        botao_avance.place(x=650, y=200, anchor="center")
        self.widgets_casa_atual.append(botao_avance)
        
        # SKIP
        botao_skip= ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 70,
        border_color= "white",
        border_width= 1,
        hover_color=self.cor_Layout,
        text="Skip 1 space",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.vontade_dos_deuses(casas_avanco=1, casas_retrocesso=0, vida_mais=0, vida_menos=0, pontos_mais=15, pontos_menos=0),
                         self.remover_carta('Hades'),
                         self.atualizar_cartas(),
                         self.carregar_casa(self.back_end.casa_atual)))
        botao_skip.place(x=650, y=300, anchor="center")
        self.widgets_casa_atual.append(botao_skip)

        
        self.botao_nao_usar_carta()
    

    def use_carta_Hephaestus(self):
        self.limpar_widgets_casa_atual()  
        
        self.chama_foto_carta(5) # index Hefesto 
        
        self.chamada_do_dado_batalha_carta_deuses(1,0,0,"Hephaestus")   
        
        # SKIP
        botao_skip= ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 70,
        border_color= "white",
        border_width= 1,
        hover_color=self.cor_Layout,
        text="Go back 1 space",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.vontade_dos_deuses(casas_avanco=0, casas_retrocesso=1, vida_mais=0, vida_menos=0, pontos_mais=0, pontos_menos=0),
                         self.remover_carta('Hephaestus'),
                         self.atualizar_cartas(),
                         self.carregar_casa(self.back_end.casa_atual)))
        botao_skip.place(x=650, y=140, anchor="center")
        self.widgets_casa_atual.append(botao_skip)     
        
        self.botao_nao_usar_carta()
         

    def use_carta_Hera(self):
        self.limpar_widgets_casa_atual()  
        
        self.chama_foto_carta(6) # index Hera
        
        botao_avance= ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 70,
        border_color= "white",
        border_width= 1,
        hover_color=self.cor_Layout,
        text="Gain one life",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.vontade_dos_deuses(casas_avanco=1, casas_retrocesso=0, vida_mais=1, vida_menos=0, pontos_mais=15, pontos_menos=0),
                         self.remover_carta('Hera'),
                         self.atualizar_cartas(),
                         self.carregar_casa(self.back_end.casa_atual))
        )
        botao_avance.place(x=650, y=150, anchor="center")
        self.widgets_casa_atual.append(botao_avance)
        
        self.chamada_do_dado_batalha_carta_deuses(1,0,0,nome_deus="Hera")
        
        self.botao_nao_usar_carta()
                   

    def use_carta_Hermes(self):
        self.limpar_widgets_casa_atual()  
        
        self.chama_foto_carta(7) # index Hermes 
        
        botao_avance= ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 70,
        border_color= "white",
        border_width= 1,
        hover_color=self.cor_Layout,
        text="Advance 5 spaces",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.vontade_dos_deuses(casas_avanco=5, casas_retrocesso=0, vida_mais=0, vida_menos=0, pontos_mais=75, pontos_menos=0),
                         self.remover_carta('Hermes'),
                         self.atualizar_cartas(),
                         self.carregar_casa(self.back_end.casa_atual)))
        botao_avance.place(x=650, y=200, anchor="center")
        self.widgets_casa_atual.append(botao_avance)
        
        # SKIP
        botao_skip= ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 70,
        border_color= "white",
        border_width= 1,
        hover_color=self.cor_Layout,
        text="Skip 1 space",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.vontade_dos_deuses(casas_avanco=2, casas_retrocesso=0, vida_mais=0, vida_menos=0, pontos_mais=75, pontos_menos=0),
                         self.remover_carta('Hermes'),
                         self.atualizar_cartas(),
                         self.carregar_casa(self.back_end.casa_atual)))
        botao_skip.place(x=650, y=300, anchor="center")
        self.widgets_casa_atual.append(botao_skip)

        self.botao_nao_usar_carta()
        

    def use_carta_Persephone(self):  
        self.limpar_widgets_casa_atual()
          
        self.chama_foto_carta(8) # index Persefone 
         # Título
        label_nome_actions = ctk.CTkLabel(
            self.root,
            text= "Move back spaces", 
            text_color="white",  
            fg_color="black",
            font=("Gelio Greek Diner", 21), # "Olympus"
            )
        label_nome_actions.place(x=650, y=200, anchor ="n")
        self.widgets_dinamicos.append(label_nome_actions)  
        
        botao_back1= ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 50,
        border_color= "white",
        border_width= 1,
        hover_color=self.cor_Layout,
        text="I",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.vontade_dos_deuses(casas_avanco=0, casas_retrocesso=1, vida_mais=0, vida_menos=0, pontos_mais=0, pontos_menos=0),
                         self.remover_carta('Persephone'),
                         self.atualizar_cartas(),
                         self.carregar_casa(self.back_end.casa_atual)))
        botao_back1.place(x=580, y=250, anchor="center")
        self.widgets_casa_atual.append(botao_back1)
        
        botao_back2= ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 50,
        border_color= "white",
        border_width= 1,
        hover_color=self.cor_Layout,
        text="I I",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.vontade_dos_deuses(casas_avanco=0, casas_retrocesso=2, vida_mais=0, vida_menos=0, pontos_mais=0, pontos_menos=0),
                         self.remover_carta('Persephone'),
                         self.atualizar_cartas(),
                         self.carregar_casa(self.back_end.casa_atual)))
        botao_back2.place(x=650, y=250, anchor="center")
        self.widgets_casa_atual.append(botao_back2)
        
        botao_back3= ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 50,
        border_color= "white",
        border_width= 1,
        hover_color=self.cor_Layout,
        text="I I I",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.vontade_dos_deuses(casas_avanco=0, casas_retrocesso=3, vida_mais=0, vida_menos=0, pontos_mais=0, pontos_menos=0),
                         self.remover_carta('Persephone'),
                         self.atualizar_cartas(),
                         self.carregar_casa(self.back_end.casa_atual)))
        botao_back3.place(x=720, y=250, anchor="center")
        self.widgets_casa_atual.append(botao_back3)
  
        self.botao_nao_usar_carta()
        

    def use_carta_Poseidon(self):
        self.limpar_widgets_casa_atual()  
        
        self.chama_foto_carta(9) # index Poseidon  
        
        self.chamada_do_dado_batalha_carta_deuses(1,0,0,nome_deus="Poseidon")  
                
        botao_avance= ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 70,
        border_color= "white",
        border_width= 1,
        hover_color=self.cor_Layout,
        text="Advance 4 spaces",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.vontade_dos_deuses(casas_avanco=4, casas_retrocesso=0, vida_mais=0, vida_menos=0, pontos_mais=60, pontos_menos=0),
                         self.remover_carta('Poseidon'),
                         self.atualizar_cartas(),
                         self.carregar_casa(self.back_end.casa_atual))
        )
        botao_avance.place(x=650, y=150, anchor="center")
        self.widgets_casa_atual.append(botao_avance)
        
        self.botao_nao_usar_carta()
           
               
    def use_carta_Zeus(self):
        self.limpar_widgets_casa_atual()  
        
        self.chama_foto_carta(10) # index Zeus 
        
        self.chamada_do_dado_batalha_carta_deuses(1,0,0,nome_deus="Zeus")  
                
        botao_avance= ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 70,
        border_color= "white",
        border_width= 1,
        hover_color=self.cor_Layout,
        text="Advance 6 spaces",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.vontade_dos_deuses(casas_avanco=6, casas_retrocesso=0, vida_mais=0, vida_menos=0, pontos_mais=60, pontos_menos=0),
                         self.remover_carta('Zeus'),
                         self.atualizar_cartas(),
                         self.carregar_casa(self.back_end.casa_atual))
        )
        botao_avance.place(x=650, y=150, anchor="center")
        self.widgets_casa_atual.append(botao_avance)
        
        self.botao_nao_usar_carta()
        
   
    def use_carta_Athena(self):
        self.limpar_widgets_casa_atual()  
        
        self.chama_foto_carta(11) # index Atena 
        
        botao_win= ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 70,
        border_color= "white",
        border_width= 1,
        hover_color=self.cor_Layout,
        text="Win 1 battle",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.vontade_dos_deuses(casas_avanco=1, casas_retrocesso=0, vida_mais=0, vida_menos=0, pontos_mais=100, pontos_menos=0),
                         self.remover_carta('Athena'),
                         self.atualizar_cartas(),
                         self.carregar_casa(self.back_end.casa_atual))
        )
        botao_win.place(x=650, y=150, anchor="center")
        self.widgets_casa_atual.append(botao_win)
        
        
        botao_avance= ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 70,
        border_color= "white",
        border_width= 1,
        hover_color=self.cor_Layout,
        text="Advance 2 spaces",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.vontade_dos_deuses(casas_avanco=2, casas_retrocesso=0, vida_mais=0, vida_menos=0, pontos_mais=60, pontos_menos=0),
                         self.remover_carta('Athena'),
                         self.atualizar_cartas(),
                         self.carregar_casa(self.back_end.casa_atual))
        )
        botao_avance.place(x=650, y=250, anchor="center")
        self.widgets_casa_atual.append(botao_avance)
        
        self.botao_nao_usar_carta()
        
