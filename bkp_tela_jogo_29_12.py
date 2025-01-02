# tela onde o jogo se desenrola..
#  criado:  20/12/24
# atualizado: 28/12/24
# 

import tkinter as tk
from tkinter import font
from tkinter import filedialog, messagebox, Label, Tk, Canvas, PhotoImage
import customtkinter as ctk
from customtkinter import CTkImage, CTkFont 
from PIL import Image, ImageDraw, ImageFont, ImageTk
import random
from back_end import Back_End

# Até aqui! 12H:56


class Tela_Jogo:
    def __init__(self, root, telas_iniciais, interface_jogo, back_end):
        self.root = root  # Referência à janela principal
        self.widgets_dinamicos = []  # Lista para armazenar widgets dinâmicos
        self.interface_jogo = interface_jogo  # Referência à instância de Interface_Jogo
        self.telas_iniciais = telas_iniciais   # Referência à instância de Telas    
        self.back_end = back_end  #  Back_End 
        # self.cartas = cartas  # Instância de Cartas passada para Tela_Jogo
        self.canvas_abre = None  # Inicialmente vazio
        self.back_end.load_fonts()
        # self.cor_Layout = self.back_end.cor_layout_atual # busca a cor do layout do backend        
        self.root.configure(bg="black")
        self.cor_Layout = self.back_end.cor_layout_atual # busca a cor do layout do 
        # para evitar erros na atualização das labels
        self.label_carta_menu1 = None
        self.label_carta_menu2 = None
        self.label_carta_menu3 = None
        self.imagem_dado = "images/dado_grego.gif"
        
        self.widgets_casa_atual = [] # widgets por casa
        
        self.image_referencias_cartas = []  # Lista para manter referências às imagens das cartas
        
        
    # Método de limpeza pode ser ajustado se necessário: PARA AS CARTINHAS QUE NÂO ATUALIZAVAM.....
    def limpar_referencias_cartas(self):
        self.image_referencias_cartas.clear()
        
                    
    def atualizar_cor(self, nova_cor):
        self.cor_Layout = nova_cor
        self.atualizar_tela()
   
    
    def play_gif(self):# Reproduz a animação do GIF no canvas
        if not hasattr(self, 'animacao_ativa') or self.animacao_ativa: # para exibor a imagem 'resultado' no final da rolagem
            if self.current_frame < len(self.frames):
                self.canvas.itemconfig(self.image_on_canvas, image=self.frames[self.current_frame])
                self.current_frame += 1
                self.root.after(500, self.play_gif)  # Controla a velocidade da animação
            else:
                self.current_frame = 0  # Reinicia o índice para repetir
    

    def limpar_widgets_casa_atual(self):
        """Limpa os widgets da casa atual, incluindo o canvas e a imagem do dado."""
        for widget in self.widgets_casa_atual:
            widget.destroy()

        # Se o canvas ainda estiver presente, é destruido
        if hasattr(self, 'canvas') and self.canvas:
            self.canvas.destroy()
            self.canvas = None

        # Certifica que nenhuma imagem estática ou GIF fique referenciada
        if hasattr(self, 'image_on_canvas') and self.image_on_canvas:
            self.image_on_canvas = None

        # Limpa a lista de widgets dinâmicos da casa atual
        self.widgets_casa_atual = []

     
    def tela_game(self):
        self.canvas_abre = Canvas(self.root, width=800, height=600, bg="black", bd=0, highlightthickness=0)
        self.canvas_abre.place(x=0, y=0) 
        self.widgets_dinamicos.append(self.canvas_abre)
        #  # Atualize a instância de `Cartas` com a referência do canvas
        # self.cartas.canvas_abre = self.canvas_abre
        
        
         # Limpa referências antigas de imagens de cartas
        self.limpar_referencias_cartas()
  
                   
        # Imagem Tijolinho 
        self.atualizar_tijolos()# atualiza as cores dos tijolos
        self.image_tijolinho = PhotoImage(file=self.back_end.tijolos_cor_atual) # Variável dinâmica
        self.img_tijolinho = self.canvas_abre.create_image(400, 25, image=self.image_tijolinho)
        
        
       # self.rolagem_de_dados() # rola o dado teste
        

       
        print(f"Debug classe Tela Jogo: {self.back_end.personagem_escolhido_imagem}") 
        # Imagem Carinha Tela Jogo
        try:
            print(f"Tentando carregar imagem: {self.back_end.personagem_escolhido_imagem}")       
            imagem_original = Image.open(self.back_end.personagem_escolhido_imagem)
            imagem_redimensionada = imagem_original.resize((125, 125), Image.Resampling.LANCZOS)
            self.image_carinha_jogador = ImageTk.PhotoImage(imagem_redimensionada)       
            self.img_carinha = self.canvas_abre.create_image(80, 155, image=self.image_carinha_jogador)
            print(f"Debug Tela Jogo, imagem selecionada: {self.back_end.personagem_escolhido_imagem}") 
        except Exception as e:
            print(f"Erro ao carregar imagem selecionada: {e}")
            self.image_carinha_jogador = PhotoImage(file="images/carinha_default_menor.png")
            self.img_carinha = self.canvas_abre.create_image(80, 155, image=self.image_carinha_jogador)      
                

        # Nome do caboclinho              
        self.label_titulo_nome = ctk.CTkLabel(
            self.root,
            text= self.back_end.personagem_escolhido_nome, # Variável de sistema
            text_color= "white",  
            bg_color="black",  
            font=("Gelio Fasolada", 21),
            )  # Alinha o texto à esquerda (west))            
        self.label_titulo_nome.place(x=70, y=75, anchor="center") # relx=0.5, y=10, anchor="n"
        self.widgets_dinamicos.append(self.label_titulo_nome)
                
         # XP            
        self.label_xp = ctk.CTkLabel(
            self.root,
            text= f"XP: {str(self.back_end.player_xp)}", # self.back_end.player_xp Variável de sistema
            text_color=self.cor_Layout,  
            bg_color="black",  
            font=("Gelio Fasolada", 18),
            )            
        self.label_xp.place(x=140, y=60) # relx=0.5, y=10, anchor="n" anchor="center"
        self.widgets_dinamicos.append(self.label_xp)
                
        # PONTOS            
        self.label_pontos = ctk.CTkLabel(
            self.root,
            text= f"POINTS: {self.back_end.player_pontos}", # Variável de sistema
            text_color=self.cor_Layout,  
            bg_color="black",  
            font=("Gelio Fasolada", 18),
            )            
        self.label_pontos.place(x=190, y=60, ) # relx=0.5, y=10, anchor="n"
        self.widgets_dinamicos.append(self.label_pontos)
        
        
        # Você está na CASA numero_X
        self.label_esta_na_casa = ctk.CTkLabel(
            self.root,
            text= f"You are\non space:",
            text_color=self.cor_Layout,  
            bg_color="black",  
            font=("Gelio Fasolada", 18),
            )            
        self.label_esta_na_casa .place(x=200, y=140, anchor='center') # relx=0.5, y=10, anchor="n"
        self.widgets_dinamicos.append(self.label_esta_na_casa )
        
        
        self.label_numero_casa_atual = ctk.CTkLabel(
            self.root,
            text= f"{self.back_end.casa_atual}",
            text_color='white',  
            bg_color="black",  
            font=("Gelio Fasolada", 22),
            )            
        self.label_numero_casa_atual .place(x=200, y=180, anchor='center') # relx=0.5, y=10, anchor="n"
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
            text_color= 'white',  
            bg_color="black",  
            font=("cambria", 14),
            )            
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
            text_color= 'white',  
            bg_color="black",  
            font=("cambria", 14),
            )            
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
            text_color= 'white',  
            bg_color="black",  
            font=("cambria", 14),
            )            
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
            # Cria o texto associado à casa, que pode ser o texto da casa ou outro
            label_nome_casa = ctk.CTkLabel(
                self.root,
                text=casa["texto"],  # Usando o texto da casa, que vem do dicionário
                text_color=self.cor_Layout,  # Cor do texto layout
                bg_color="black",  
                font=("Gelio Fasolada", 17),
            )
            label_nome_casa.place(x=posicoes_x[i], y=posicoes_y + 65, anchor="center")  # Posição fixa para o texto
            # Armazenando os widgets (imagem e label) para manipulação futura
            # self.widgets_dinamicos.append(img_casa)
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
        
        # self.canvas_abre.create_text(
        #     150,  
        #     450,
        #     text="<><><><><><><><><><><><><><><><>", 
        #     fill='gray',  # #B8860B' dourado
        #     font=("Arial", 12), 
        #     anchor="center")  
                
        # testando a função das cartas
        self.casa_evento_001()      
        # teste de evento de casa 
        #self.quadro_de_acao_evento()
        
  
    def exibir_casas(self, lista_maior):
        # O número sorteado define de onde os 8 itens devem começar
        # Vamos garantir que o número esteja entre 1 e 120
        if self.back_end.casa_atual < 1 or self.back_end.casa_atual> 120:
            raise ValueError("O número deve estar entre 1 e 120.")
        
        # Calcular o índice de início para a exibição de 8 itens
        inicio = self.back_end.casa_atual - 1  # O índice começa de 0, então subtrai 1
        
        # Garantir que o início não ultrapasse o limite de 120 elementos
        fim = inicio + 8
        
        # Se o fim ultrapassar 120, ajustamos para pegar até o fim da lista
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
        elif self.back_end.casa_atual <= 32:
            self.back_end.tijolos_cor_atual = self.back_end.tijolos_cor["verde"]
        elif self.back_end.casa_atual <= 48:
            self.back_end.tijolos_cor_atual = self.back_end.tijolos_cor["amarelo"]
        elif self.back_end.casa_atual <= 64:
            self.back_end.tijolos_cor_atual = self.back_end.tijolos_cor["laranja"]
        elif self.back_end.casa_atual <= 80:
            self.back_end.tijolos_cor_atual = self.back_end.tijolos_cor["vermelho"]
        elif self.back_end.casa_atual <= 96:
            self.back_end.tijolos_cor_atual = self.back_end.tijolos_cor["rosa"]
        elif self.back_end.casa_atual <= 112:
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
        elif self.back_end.casa_atual <= 96:
            self.back_end.cor_layout_atual = self.back_end.cores_layout["rosa"]
        elif self.back_end.casa_atual <= 112:
            self.back_end.cor_layout_atual = self.back_end.cores_layout["roxo"]
        elif self.back_end.casa_atual <= 120:
            self.back_end.cor_layout_atual = self.back_end.cores_layout["agua"]
            
          # Atualiza a variável de instância para o uso em outros widgets
        self.cor_Layout = self.back_end.cor_layout_atual
        #self.atualizar_layout_widgets()  # Atualiza os widgets com a nova cor


    def rolar_dado_sem_delay(self):
            # Sorteia um número entre 1 e 6
            numero_sorteado = random.randint(1, 6) #
            print(f'Número sorteado: {numero_sorteado}')
            
            # atualiza a imagem em movimento por uma imagem estatica do resultado
            self.imagem_dado = f"images/dado{numero_sorteado}.png"
                                   
            # Atualiza o Canvas com a nova imagem
            nova_imagem = Image.open(self.imagem_dado).resize((80, 80), Image.Resampling.LANCZOS)
            self.imagem_estatica = ImageTk.PhotoImage(nova_imagem)
            self.canvas.itemconfig(self.image_on_canvas, image=self.imagem_estatica)
              
            # Atualiza os pontos e a posição do jogador         
            self.back_end.player_pontos +=  (15 * numero_sorteado)
            print(f'Pontos do jogador: {self.back_end.player_pontos}')           
            print(f'Casas do tabuleiro no momento:{self.casas_exibidas}')   
            self.back_end.casa_atual += numero_sorteado            
            print(f'Casa atual: {self.back_end.casa_atual}')
            
            # Introduz um atraso de 2 segundos antes de continuar
            self.root.after(2000, lambda: self._continuar_rolagem_dado())

            # Limpa widgets existentes antes de atualizar a tela
            self.limpar_widgets_casa_atual()
            
            self.atualizar_tela()# Atualiza outros elementos da tela 
            
            # Carrega os gadgets da nova casa
            self.carregar_casa(self.back_end.casa_atual)


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
            self.label_xp.configure(text=f"XP: {str(self.back_end.player_xp)}",text_color=self.cor_Layout)
            
        if hasattr(self, 'label_esta_na_casa') and self.label_esta_na_casa.winfo_exists():
            self.label_esta_na_casa.configure(text=f"You are\non space:",text_color=self.cor_Layout) 
            
        if hasattr(self, 'label_numero_casa_atual') and self.label_numero_casa_atual.winfo_exists():
            self.label_numero_casa_atual.configure(text=f"{self.back_end.casa_atual}",text_color="white")
            
        if hasattr(self, 'label_cartas') and self.label_cartas.winfo_exists():
            self.label_cartas.configure(text="Your Cards:",text_color="white")
            
        # cartinhas
        if self.label_carta_menu1 and self.label_carta_menu1.winfo_exists():
            self.label_carta_menu1.configure(text=self.back_end.cartas_player[0]["action_p"], text_color="white") 
            
        if self.label_carta_menu2 and self.label_carta_menu2.winfo_exists():
            self.label_carta_menu2.configure(text=self.back_end.cartas_player[1]["action_p"], text_color="white")  
        
        if self.label_carta_menu3 and self.label_carta_menu3.winfo_exists():
            self.label_carta_menu3.configure(text=self.back_end.cartas_player[2]["action_p"], text_color="white")  
        

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


    def carregar_casa(self, casa_atual):# Carrega os widgets da casa especificada.
        # Limpa os widgets da casa anterior
        self.limpar_widgets_casa_atual()

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

        else:
            print(f"Nenhum evento configurado para a casa {casa_atual}.")


    def atualizar_cartas(self): # atualiza a referencia das cartinhas
        self.limpar_referencias_cartas()
        self.tela_game()  # Rechama a lógica para redesenhar as cartas
        

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
        
        # Introduz um atraso de 2 segundos antes de continuar
        self.root.after(2000, lambda: self._continuar_rolagem_dado(numero_sorteado))
        
    def _continuar_rolagem_dado(self, numero_sorteado):
        """Continua as ações após exibir a imagem estática por 2 segundos."""
        # Atualiza os pontos e a posição do jogador
        self.back_end.player_pontos += (15 * numero_sorteado)
        print(f'Pontos do jogador: {self.back_end.player_pontos}')
        print(f'Casas do tabuleiro no momento: {self.casas_exibidas}')
        self.back_end.casa_atual += numero_sorteado
        print(f'Casa atual: {self.back_end.casa_atual}')
        
        # Limpa widgets existentes antes de atualizar a tela
        self.limpar_widgets_casa_atual()
        self.atualizar_tela()  # Atualiza outros elementos da tela
        self.carregar_casa(self.back_end.casa_atual)  # Carrega os gadgets da nova casa

#tentativa 1
# NOVAS FUNÇÕES DADOS FUNCIONANDO
    def rolar_dado_de_batalha(self, casas_avanco=0, casas_retrocesso=0, vida=0):
#        Lógica da batalha: sorteia o número do dado, exibe o resultado e processa a batalha.
        # Para a animação do GIF
        self.animacao_ativa = False

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

        # Introduz um atraso de 2 segundos antes de processar o resultado
        self.root.after(2000, lambda: self._processar_resultado_batalha(numero_sorteado, casas_avanco, casas_retrocesso, vida))

    def _processar_resultado_batalha(self, numero_sorteado, casas_avanco, casas_retrocesso, vida):
    # Processa o resultado da batalha após exibir a imagem do dado.

        vitoria = numero_sorteado > 3

        # Pontos, avanço ou retrocesso de acordo com o resultado da batalha
        if vitoria:
            self.back_end.player_pontos += (15 * casas_avanco) + 30  # Vitória
            self.back_end.casa_atual += casas_avanco
            self.back_end.player_xp += vida  # Ganha vida se aplicável
            print('Você VENCEU!')
        else:
            self.back_end.player_pontos -= ((15 * casas_retrocesso) + 30)  # Derrota
            self.back_end.casa_atual -= casas_retrocesso
            self.back_end.player_xp -= vida  # Perde vida se aplicável
            print('Você PERDEU!')

        print(f'Pontos do jogador depois da batalha: {self.back_end.player_pontos}')  # Debug
        print(f'Casa atual depois da batalha: {self.back_end.casa_atual}')

        # Atualiza a interface
        self.limpar_widgets_casa_atual()
        self.atualizar_tela()
        self.carregar_casa(self.back_end.casa_atual)

    def chamada_do_dado_batalha(self):
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

        # Exibe a animação
        self.play_gif()

        # Botão de rolagem de dados
        botao_rolar_dados = ctk.CTkButton(
            self.canvas_abre,
            fg_color='black',
            width=100,
            border_width=1,
            border_color="white",
            hover_color='red',
            text="Roll a die!",
            font=("Gelio Greek Diner", 18),
            command=lambda: (self.rolar_dado_de_batalha(casas_avanco=2, casas_retrocesso=2, vida=0)) # determina o que dado faz
        )
        botao_rolar_dados.place(x=400, y=405, anchor='n')
        self.widgets_casa_atual.append(botao_rolar_dados)




    # somente para combates de dados   VELHOS VELHOS VELHOS
    def rolar_dado_de_batalha_1(self, casas_avanco=0, casas_retrocesso=0, vida=0):
        # Para a animação do GIF
        self.animacao_ativa = False   
        
        print(f'Pontos do jogador antes da batalha: {self.back_end.player_pontos}') # for Debug   
     
        # Sorteia um número entre 1 e 6
        numero_sorteado = random.randint(1, 6) #random.choice([4]) # random.randint(1, 6)
        print(f'Número sorteado em batalha: {numero_sorteado}')
        
        vitoria = False
        if numero_sorteado > 3:
            vitoria= True
        print(f'resultado: {numero_sorteado}, vitória: {vitoria} ')# for debug  
                  
        # Atualiza a imagem em movimento por uma imagem estática do resultado
        self.imagem_dado = f"images/dado{numero_sorteado}.png"
        nova_imagem = Image.open(self.imagem_dado).resize((80, 80), Image.Resampling.LANCZOS)
        self.imagem_estatica = ImageTk.PhotoImage(nova_imagem)
        self.canvas.itemconfig(self.image_on_canvas, image=self.imagem_estatica)  # Exibe a imagem estática imediatamente
        
        # Introduz um atraso de 2 segundos antes de processar o resultado
        self.root.after(2000, lambda: self._processar_resultado_batalha(numero_sorteado, casas_avanco, casas_retrocesso, vida))
    
    def _processar_resultado_batalha_1(self, numero_sorteado, casas_avanco, casas_retrocesso, vida):
        """Processa o resultado da batalha após exibir a imagem do dado."""
        vitoria = numero_sorteado > 3
        print(f'Resultado: {numero_sorteado}, vitória: {vitoria}')  # for debug  

        # Pontos, avanço ou retrocesso de acordo com o resultado da batalha
        if vitoria:
            self.back_end.player_pontos += (15 * casas_avanco) + 30  # Vitória
            self.back_end.casa_atual += casas_avanco
            self.back_end.player_xp += vida  # Ganha vida se aplicável
            print('Você VENCEU!')
        else:
            self.back_end.player_pontos -= ((15 * casas_retrocesso) + 30)  # Derrota
            self.back_end.casa_atual -= casas_retrocesso
            self.back_end.player_xp -= vida  # Perde vida se aplicável
            print('Você PERDEU!')

        print(f'Pontos do jogador depois da batalha: {self.back_end.player_pontos}')  # for Debug   
        print(f'Casa atual depois da batalha: {self.back_end.casa_atual}')

        # Atualiza a interface
        self.limpar_widgets_casa_atual()
        self.atualizar_tela()
        self.carregar_casa(self.back_end.casa_atual)
 
        # Pontos, avanço ou retorcesso de acordo com o resultado da batalha      
        # if vitoria == True:                
        #     self.back_end.player_pontos += ((15 * casas_avanco) + 30 )  # a cada vitória + 30 pontos e pontos de avanço
        #     self.back_end.casa_atual += casas_avanco
        #     self.back_end.player_xp += vida # se houver ganho de vidas na rolagem
        #     print('Você VENCEU!')
            
        # if vitoria == False:
        #     self.back_end.player_pontos -= ((15 * casas_avanco) - 30 ) # a cada derrota - 30 pontos e pontos de retorno 
        #     self.back_end.casa_atual -= casas_retrocesso 
        #     self.back_end.player_xp -= vida # se houver perda de vidas na rolagem  
        #     print('Você PERDEU!')
                            
        # print(f'Pontos do jogador depois da batalha: {self.back_end.player_pontos}') # for Debug   
        # print(f'Casa atual depois da batalha: {self.back_end.casa_atual}')
        
        #  # Limpa widgets existentes antes de atualizar a tela
        # self.limpar_widgets_casa_atual()
        # self.atualizar_tela()  # Atualiza outros elementos da tela
        # self.carregar_casa(self.back_end.casa_atual)  # Carrega os gadgets da nova casa
       
    def chamada_do_dado_batalha_1(self): # USADO NAS CASAS DE EVENTO
         # Para a animação do GIF
        self.animacao_ativa = False
                # Canvas para o dado
        self.canvas = tk.Canvas(self.root, width=80, height=80, bg="black", highlightthickness=0)
        self.canvas.place(x=400, y=320, anchor='n') # posição do dado
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
        # Configuraçºão do Canvas - tamanhao do Dado
        self.canvas = tk.Canvas(self.root, width=80, height=80, bg="black", highlightthickness=0)
        self.canvas.place(x=400, y=320, anchor='n')  # posição do dado     
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
        hover_color='red',
        text="Roll a die!",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.rolar_dado_de_batalha(casas_avanco=2,casas_retrocesso=2), self.atualizar_tela()) # ROLAR DADO!!!
        )
        botao_rolar_dados.place(x=400, y=405, anchor='n')
        self.widgets_casa_atual.append(botao_rolar_dados)   
    # somente para combates de dados   VELHOS VELHOS VELHOS




    # Acho que não está em uso... testar depois!!!!!!!!!!!  
    def usar_carta_inicial(self):
         # Limpar os widgets da casa atual para evitar sobreposição
        self.limpar_widgets_casa_atual()        
        try:
            # Carregar a imagem usando PIL
            img = Image.open(self.back_end.cartas_player[0]['imagem'])
            # Converter a imagem para PhotoImage
            self.image_carta_player = ImageTk.PhotoImage(img)
            # Criar o Label com a imagem
            self.label_imagem_carta = tk.Label(self.canvas_abre, image=self.image_carta_player, bg="black")
            self.label_imagem_carta.place(x=440, y=265, anchor="center")
            # Adicionar o Label à lista de widgets dinâmicos
            self.widgets_casa_atual.append(self.label_imagem_carta)
        except Exception as e:
            print(f"Erro ao carregar a imagem da carta: {e}")           
            self.label_imagem_carta = tk.Label(self.canvas_abre, image=self.back_end.cartas_player[0]['imagem'], bg="black")
            self.label_imagem_carta.place(x=440, y=265, anchor="center")
            self.widgets_casa_atual.append(self.label_imagem_carta)

         # label do nome da casa exibida
        label_descricao_carta_exibida = ctk.CTkLabel(
            self.root,
            text=self.back_end.cartas_player[0]['action_p'],  # Substitui pelo texto dinâmico, 
            text_color="white",  
            fg_color="black",  # Cor de fundo
            font=("Cambria", 17), 
        )
        label_descricao_carta_exibida.place(x=650, y=220, anchor ="center")
        self.widgets_casa_atual.append(label_descricao_carta_exibida)
        
        
    
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
        
            #     # OU...             
        self.label_ou = ctk.CTkLabel(
                    self.root,
                    text= "OR", 
                    text_color= self.back_end.cor_layout_atual,  
                    bg_color= "black",  
                    font=("Gelio Fasolada", 22),
                    )          
        self.label_ou.place(x=520, y=405, anchor="n") # relx=0.5, y=10, anchor="n"
        self.widgets_casa_atual.append(self.label_ou)
        
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
        self.widgets_casa_atual.append(self.botao_choose_card)  # Adiciona o botão à lista
        
         # Botão carta 1
        botao_carta_1 = ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 50,
        height= 50,
        border_width= 1,
        border_color= "white",
        hover_color=self.back_end.cor_layout_atual,
        text="I",
        font=("Gelio Greek Diner", 24),
        command=lambda: self.usar_carta_da_mao(1) # função de abrir a carta do indice 0
        )
        botao_carta_1 .place(x=610, y=340, anchor='n')
        self.widgets_casa_atual.append(botao_carta_1 )  # Adiciona o botão à lista 
            
         # Botão carta 2
        botao_carta_2 = ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 50,
        height= 50,
        border_width= 1,
        border_color= "white",
        hover_color=self.back_end.cor_layout_atual,
        text="I I",
        font=("Gelio Greek Diner", 24),
        command=lambda: self.usar_carta_da_mao(2) # função de abrir a carta do indice 0
        )
        botao_carta_2 .place(x=670, y=340, anchor='n')
        self.widgets_casa_atual.append(botao_carta_2)  # Adiciona o botão à lista 
        
         # Botão carta 3
        botao_carta_3 = ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 50,
        height= 50,
        border_width= 1,
        border_color= "white",
        hover_color=self.back_end.cor_layout_atual,
        text="I I I",
        font=("Gelio Greek Diner", 24),
        command=lambda: self.usar_carta_da_mao(3) # função de abrir a carta do indice 0
        )
        botao_carta_3 .place(x=730, y=340, anchor='n')
        self.widgets_casa_atual.append(botao_carta_3)  # Adiciona o botão à lista 


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
        # Configuraçºão do Canvas - tamanhao do Dado
        self.canvas = tk.Canvas(self.root, width=80, height=80, bg="black", highlightthickness=0)
        self.canvas.place(x=550, y=120, anchor='n')  # posição do dado     
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
        hover_color='red',
        text="Roll a die to move!",
        font=("Gelio Greek Diner", 18),
        command=lambda: (self.rolar_dado(), self.atualizar_tela()) # ROLAR DADO!!!
        )
        botao_rolar_dados.place(x=550, y=210, anchor='n')
        self.widgets_casa_atual.append(botao_rolar_dados)  # Adiciona o botão à lista
        
            #     # OU...             
        self.label_ou = ctk.CTkLabel(
                    self.root,
                    text= "OR", 
                    text_color= self.back_end.cor_layout_atual,  
                    bg_color= "black",  
                    font=("Gelio Fasolada", 22),
                    )          
        self.label_ou.place(x=550, y=270, anchor="n") # relx=0.5, y=10, anchor="n"
        self.widgets_casa_atual.append(self.label_ou)
        
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
        self.botao_choose_card.place(x=550, y=330, anchor='n')
        self.widgets_casa_atual.append(self.botao_choose_card)  # Adiciona o botão à lista
        
         # Botão carta 1
        botao_carta_1 = ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 50,
        height= 50,
        border_width= 1,
        border_color= "white",
        hover_color=self.back_end.cor_layout_atual,
        text="I",
        font=("Gelio Greek Diner", 24),
        command=lambda: self.usar_carta_da_mao(1) # função de abrir a carta do indice 0
        )
        botao_carta_1 .place(x=480, y=380, anchor='n')
        self.widgets_casa_atual.append(botao_carta_1 )  # Adiciona o botão à lista 
            
         # Botão carta 2
        botao_carta_2 = ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 50,
        height= 50,
        border_width= 1,
        border_color= "white",
        hover_color=self.back_end.cor_layout_atual,
        text="I I",
        font=("Gelio Greek Diner", 24),
        command=lambda: self.usar_carta_da_mao(2) # função de abrir a carta do indice 0
        )
        botao_carta_2 .place(x=550, y=380, anchor='n')
        self.widgets_casa_atual.append(botao_carta_2)  # Adiciona o botão à lista 
        
         # Botão carta 3
        botao_carta_3 = ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 50,
        height= 50,
        border_width= 1,
        border_color= "white",
        hover_color=self.back_end.cor_layout_atual,
        text="I I I",
        font=("Gelio Greek Diner", 24),
        command=lambda: self.usar_carta_da_mao(3) # função de abrir a carta do indice 0
        )
        botao_carta_3 .place(x=620, y=380, anchor='n')
        self.widgets_casa_atual.append(botao_carta_3)  # Adiciona o botão à lista 
         
       
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
        self.widgets_dinamicos.append(label_nome_casa_evento)
        
        #IMAGEM DA CASA
        self.image_evento_exibido = PhotoImage(file="images/casa_005_esfinge.png")
        self.label_evento_exibido = tk.Label(
            self.root,  # Substitua por self.canvas_abre se quiser que o Label seja um filho do Canvas
            image=self.image_evento_exibido,
            bg="black"  # Define a cor de fundo do Label
        )
        self.label_evento_exibido.place(x=450, y=140, anchor='n')  # Posiciona o Label
        self.widgets_casa_atual.append(self.label_evento_exibido)

        texto_evento = ("""She asked you a question.
Solve the riddle and roll a die.

If you get 3 or more,
move forward 2 spaces.
If you get 2 or less,
move back 2 spaces."""
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
        self.widgets_dinamicos.append(label_descricao_evento)
        
        # DADO E CARTAS
        self.chamada_do_dado_batalha()
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
        self.widgets_dinamicos.append(label_nome_casa_evento)
        
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

and return 
2 spaces."""
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
        self.widgets_dinamicos.append(label_descricao_evento)
        
        # evento da casa       
        self.back_end.retornar_casas(numero_casas_retornar=2)
        #self.atualizar_tela()
        
        # DADO E CARTAS
        self.chamada_do_dado_batalha()
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
        self.widgets_dinamicos.append(label_nome_casa_evento)
            
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
        self.widgets_dinamicos.append(label_descricao_evento)
        
        # evento da casa
        self.back_end.retornar_casas(numero_casas_retornar=2)
        
        # DADO E CARTAS
        self.chamada_do_dado_batalha()
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
        self.widgets_dinamicos.append(label_nome_casa_evento)
            
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
        self.widgets_dinamicos.append(label_descricao_evento)
        
                # DADO E CARTAS
        self.chamada_do_dado_batalha()
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
        self.widgets_dinamicos.append(label_nome_casa_evento)
            
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
        self.widgets_dinamicos.append(label_descricao_evento)
        
                # DADO E CARTAS
        self.chamada_do_dado_batalha()
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
                text= "Ciclops",  # Substituir pelo texto dinâmico, 
                text_color="white",  
                fg_color="black",  # Cor de fundo
                font=("Olympus", 24), 
                )
            label_nome_casa_evento.place(x=450, y=110, anchor ="n")
            self.widgets_dinamicos.append(label_nome_casa_evento)
                
                #IMAGEM DA CASA
            self.image_evento_exibido = PhotoImage(file="images/casa_024_ciclope.png")
            self.label_evento_exibido = tk.Label(
                    self.root,  # Substitua por self.canvas_abre se quiser que o Label seja um filho do Canvas
                    image=self.image_evento_exibido,
                    bg="black"  # Define a cor de fundo do Label
                )
            self.label_evento_exibido.place(x=450, y=140, anchor='n')  # Posiciona o Label
            self.widgets_casa_atual.append(self.label_evento_exibido)

            texto_evento = ("""Engage in battle
against the Cyclops.
    
If you win, 
move forward
1 space."""
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
            self.widgets_dinamicos.append(label_descricao_evento)
            
                        # DADO E CARTAS
            self.chamada_do_dado_batalha()
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
            self.widgets_dinamicos.append(label_nome_casa_evento)
                
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
1 space."""
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
            self.widgets_dinamicos.append(label_descricao_evento)
            
                    # DADO E CARTAS
            self.chamada_do_dado_batalha()
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
            self.widgets_dinamicos.append(label_nome_casa_evento)
                
                #IMAGEM DA CASA
            self.image_evento_exibido = PhotoImage(file="images/casa_032_tanatos.png")
            self.label_evento_exibido = tk.Label(
                    self.root,  # Substitua por self.canvas_abre se quiser que o Label seja um filho do Canvas
                    image=self.image_evento_exibido,
                    bg="black"  # Define a cor de fundo do Label
                )
            self.label_evento_exibido.place(x=450, y=140, anchor='n')  # Posiciona o Label
            self.widgets_casa_atual.append(self.label_evento_exibido)

            texto_evento = ("""Thanatos 
will take you
to meet Charon.

Advance to 
space 39."""
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
            self.widgets_dinamicos.append(label_descricao_evento)
            
                    # DADO E CARTAS
            self.chamada_do_dado_batalha()
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
            self.widgets_dinamicos.append(label_nome_casa_evento)
                
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

if you win,
advance 2 spaces."""
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
            self.widgets_dinamicos.append(label_descricao_evento)
            
            
                        # DADO E CARTAS
            self.chamada_do_dado_batalha()
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
            self.widgets_dinamicos.append(label_nome_casa_evento)
                
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
Seek Ariadne's thread,
to escape you must roll
the number
5 or 6."""
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
            self.widgets_dinamicos.append(label_descricao_evento)
            
                        # DADO E CARTAS
            self.chamada_do_dado_batalha()
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
            self.widgets_dinamicos.append(label_nome_casa_evento)
                
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
            self.widgets_dinamicos.append(label_descricao_evento)
            
                    # DADO E CARTAS
            self.chamada_do_dado_batalha()
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
            self.widgets_dinamicos.append(label_nome_casa_evento)   
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

Roll a die, and if 
you pass, advance to 
space 47."""
            )
            # label de descrição do evento
            label_descricao_evento = ctk.CTkLabel(
                self.root,
                text=texto_evento,  # Substituir pelo texto dinâmico, se necessário
                text_color="white",  
                fg_color="black",  # Cor de fundo
                font=("Cambria", 17), # "Gelio Fasolada"
            )
            label_descricao_evento.place(x=660, y=140, anchor ="n")
            self.widgets_dinamicos.append(label_descricao_evento)
  

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
            self.widgets_dinamicos.append(label_nome_casa_evento)
                
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
            self.widgets_dinamicos.append(label_descricao_evento)
  

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
            self.widgets_dinamicos.append(label_nome_casa_evento)
                
                #IMAGEM DA CASA
            self.image_evento_exibido = PhotoImage(file="images/casa_052_erinias.png")
            self.label_evento_exibido = tk.Label(
                    self.root,  # Substitua por self.canvas_abre se quiser que o Label seja um filho do Canvas
                    image=self.image_evento_exibido,
                    bg="black"  # Define a cor de fundo do Label
                )
            self.label_evento_exibido.place(x=450, y=140, anchor='n')  # Posiciona o Label
            self.widgets_casa_atual.append(self.label_evento_exibido)

            texto_evento = ("""Face the Furies.
                            
If you win, 
move forward 
2 spaces."""
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
            self.widgets_dinamicos.append(label_descricao_evento)

  
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
            self.widgets_dinamicos.append(label_nome_casa_evento)                
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
            self.widgets_dinamicos.append(label_descricao_evento)


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
            self.widgets_dinamicos.append(label_nome_casa_evento)                
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
            self.widgets_dinamicos.append(label_descricao_evento)


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
            self.widgets_dinamicos.append(label_nome_casa_evento)                
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

Try to defeat them."""
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
            self.widgets_dinamicos.append(label_descricao_evento)

   
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
            self.widgets_dinamicos.append(label_nome_casa_evento)                
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

Try to defeat them"""
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
            self.widgets_dinamicos.append(label_descricao_evento)

   
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
            self.widgets_dinamicos.append(label_nome_casa_evento)                
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

Atalanta and Hippolyta are immune 
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
            self.widgets_dinamicos.append(label_descricao_evento)

     
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
            self.widgets_dinamicos.append(label_nome_casa_evento)                
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
            self.widgets_dinamicos.append(label_descricao_evento)


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
            self.widgets_dinamicos.append(label_nome_casa_evento)                
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
if you win, advance 2 spaces."""
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
            self.widgets_dinamicos.append(label_descricao_evento)


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
            self.widgets_dinamicos.append(label_nome_casa_evento)                
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
            self.widgets_dinamicos.append(label_descricao_evento)


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
            self.widgets_dinamicos.append(label_nome_casa_evento)                
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
            self.widgets_dinamicos.append(label_descricao_evento)


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
            self.widgets_dinamicos.append(label_nome_casa_evento)                
            #IMAGEM DA CASA
            self.image_evento_exibido = PhotoImage(file="images/casa_096_dionisio.png")
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
            self.widgets_dinamicos.append(label_descricao_evento)


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
            self.widgets_dinamicos.append(label_nome_casa_evento)                
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
            self.widgets_dinamicos.append(label_descricao_evento)


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
            self.widgets_dinamicos.append(label_nome_casa_evento)                
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
almost gave up on reaching Olympus.
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
            self.widgets_dinamicos.append(label_descricao_evento)


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
            self.widgets_dinamicos.append(label_nome_casa_evento)                
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
                            
Face the hunter."""
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
            self.widgets_dinamicos.append(label_descricao_evento)

     
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
            self.widgets_dinamicos.append(label_nome_casa_evento)                
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
            self.widgets_dinamicos.append(label_descricao_evento)

   
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
            self.widgets_dinamicos.append(label_nome_casa_evento)                
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
            self.widgets_dinamicos.append(label_descricao_evento)


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
            self.widgets_dinamicos.append(label_nome_casa_evento)                
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
            self.widgets_dinamicos.append(label_descricao_evento)

               
    def casa_evento_120(self): # casa em branco
            self.limpar_widgets_casa_atual()        
            print('implementar tela de vitória + placar')


     






  
  
    
    
    def quadro_de_acao_evento(self):       
    # label do nome da casa exibida
        label_nome_casa_evento = ctk.CTkLabel(
            self.root,
            text= "Sphinx",  # Substituir pelo texto dinâmico, 
            text_color="white",  
            fg_color="black",  # Cor de fundo
            font=("Olympus", 28), 
        )
        label_nome_casa_evento.place(x=550, y=130, anchor ="center")
        self.widgets_dinamicos.append(label_nome_casa_evento)
               
        self.image_evento_exibido = PhotoImage(file="images/casa_evento_layout.png")
        # self.image_carta_escolha_hover1 = PhotoImage(file="images/carta_escolha_hover.png")
        # self.image_carta_escolha_click1 = PhotoImage(file="images/carta_escolha_click.png")
        self.img_evento_exibido= self.canvas_abre.create_image(550, 235, image=self.image_evento_exibido)
        
        texto_evento = (
"""She asked you a question.
Solve the riddle and roll a die.
If you get 3 or more, move forward 2 spaces.
If you get 2 or less, move back 2 spaces."""
        )
        # label de descrição do evento
        label_descricao_evento = ctk.CTkLabel(
            self.root,
            text=texto_evento,  # Substituir pelo texto dinâmico, se necessário
            text_color="white",  
            fg_color="black",  # Cor de fundo
            font=("Cambria", 17), # "Gelio Fasolada"
        )
        label_descricao_evento.place(x=550, y=380, anchor ="center")
        self.widgets_dinamicos.append(label_descricao_evento)
        

    def quadro_de_acao_carta(self):
        # Carta
        try:
             self.image_carta_exibida = PhotoImage(file=self.back_end.carta_casa_deus[0]['imagem']) 
             self.img_carta_exibida = self.canvas_abre.create_image(440, 265, image=self.image_carta_exibida)
        except Exception as e:
            print(f'Sem imagens nessa carta, usando a imagem default - > {e}')
            self.image_carta_exibida = PhotoImage(file="images/carta_aphrodite_layout.png")
            self.img_carta_exibida = self.canvas_abre.create_image(440, 265, image=self.image_carta_exibida)
        
        try:
            texto_descricao_carta = self.back_end.carta_casa_deus[0]['action']           
        except Exception as e: 
            print(f'Semtexto nessa carta, usando o texto default - > {e}')  
            texto_descricao_carta = """The Aphrodite card has
the power to move 
forward 6 spaces.

If you don´t keep
the card, move forward
3 spaces"""
        # label do nome da casa exibida
        label_descricao_carta_exibida = ctk.CTkLabel(
            self.root,
            text= texto_descricao_carta,  # Substituir pelo texto dinâmico, 
            text_color="white",  
            fg_color="black",  # Cor de fundo
            font=("Cambria", 17), 
        )
        label_descricao_carta_exibida.place(x=650, y=220, anchor ="center")
        self.widgets_dinamicos.append(label_descricao_carta_exibida)
        
        label_guardar_carta_exibida = ctk.CTkLabel(
            self.root,
            text= "Do you keep the card?",  # Substituir pelo texto dinâmico, 
            text_color=self.cor_Layout,  
            fg_color="black",  # Cor de fundo
            font=("Cambria Bold", 17), # Gelio Fasolada
        )
        label_guardar_carta_exibida.place(x=650, y=340, anchor ="center")
        self.widgets_dinamicos.append(label_guardar_carta_exibida)
               
        # Botão SIM
        botao_sim = ctk.CTkButton(
        self.canvas_abre,
        fg_color='black',
        width= 16,
        border_color= "white",
        border_width= 1,
        hover_color=self.cor_Layout,
        text="yes",
        font=("Gelio Greek Diner", 18),
        command=lambda: self.telas_iniciais.tela_03() # acrescentar função de saída!!!!
        )
        botao_sim.place(x=600, y=380, anchor="center")
        self.widgets_dinamicos.append(botao_sim)
        
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
        command=lambda: self.telas_iniciais.tela_03() # acrescentar função de saída!!!!
        )
        botao_naum.place(x=700, y=380, anchor="center")
        self.widgets_dinamicos.append(botao_naum)
        
      
  # até aqui!    
        
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
            self.widgets_dinamicos.append(self.label_imagem_carta)

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
            self.limpar_widgets_casa_atual(), # Limpa widgets existentes antes de atualizar a tela
            self.atualizar_tela(),  # Atualiza outros elementos da tela
            self.carregar_casa(self.back_end.casa_atual)  # Carrega os gadgets da nova casa# remove carta da lista
        )
        )
        
        botao_sim.place(x=600, y=380, anchor="center")
        self.widgets_dinamicos.append(botao_sim)
        
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
        command= self.casa_evento_001()
        )
        botao_naum.place(x=700, y=380, anchor="center")
        self.widgets_dinamicos.append(botao_naum)
        

    def use_carta_Apollo(self):
        pass

    def use_carta_Artemis(self):
        pass
    

    def use_carta_Ares(self):
        pass

    def use_carta_Hades(self): 
        pass             

    def use_carta_Hephaestus(self):
        pass

    def use_carta_Hera(self):
        pass

    def use_carta_Hermes(self):
        pass

    def use_carta_Persephone(self):  
        pass              
 
    def use_carta_Poseidon(self):
        pass    

    def use_carta_Zeus(self):
        pass
   
    def use_carta_Athena(self):
        pass