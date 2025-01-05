# Versão do Jogo Grécia Antiga, para desktop - By Bressar
# Implementação do jogo
# criado:  18/12/24
# atualizado: 04/01/25

# Publicada versão 1.0 Beta para download em:
# https://bressar.itch.io/ascent-to-olympus 


import pygame
import customtkinter as ctk
from telas_iniciais import Telas
from back_end import Back_End

pygame.mixer.init() # Inicializar pygame mixer

class Interface_Jogo:
    def __init__(self, root):
        self.janela = root
        self.janela.title("Hermes&BressarGames©")
        self.janela.geometry("800x600")
        ctk.set_appearance_mode("dark")    
        self.janela.resizable(False, False)
        self.janela.configure(bg="black")
       
        self.Telas_iniciais = Telas(root, self) # Passa a referência da própria instância para Telas        
        self.tela_jogo = self.Telas_iniciais.tela_jogo # Tela de jogo agora já recebe Telas        
        self.back_end = Back_End()
        
        self.widgets_dinamicos = self.Telas_iniciais.widgets_dinamicos # traz de telas a Lista para armazenar widgets dinâmicos        
        self.janelas_abertas = [] # para a função sair(main)
      
        self.Telas_iniciais.tela_01() # Interface de incialização 
        self.iniciar_musica()# Iniciar música em loop
               
    def iniciar_musica(self):
        try:
            pygame.mixer.music.load("music/mars.mp3")  #  música do G. Holst
            pygame.mixer.music.play(-1, start=9)  # -1 para tocar em loop infinito
            print("Música iniciada em loop.")
        except pygame.error as e:
            print(f"Erro ao carregar a música: {e}")
        
        
    def sair_jogo(self):
        print("Função sair_jogo chamada")  # Verificação Debug
        janela_confirmacao = ctk.CTkToplevel(self.janela)
        janela_confirmacao.title("EXIT")
        janela_confirmacao.geometry("250x150")
        janela_confirmacao.configure(fg_color="black")  
        janela_confirmacao.wm_attributes("-topmost", True)    
        self.janelas_abertas.append(janela_confirmacao) # Armazenar a janela Toplevel em uma lista
        
        # Texto de confirmação
        texto = ctk.CTkLabel(
            janela_confirmacao, 
            text="Exit Game?", 
            fg_color=None,  # Transparente
            text_color="white",  # Texto branco
            font=("Gelio Fasolada", 20)
        )
        texto.place(relx=0.5, rely=0.3, anchor="center") 

        # Botões de Sim e Não
        botao_sim = ctk.CTkButton(
            janela_confirmacao,
            width= 40,
            text="Yes",
            font=("Gelio Fasolada", 16),
            fg_color="green", 
            text_color="white",
            hover_color="darkgreen",
            command=lambda: self.confirmar_saida(janela_confirmacao)
        )
        botao_sim.place(relx=0.4, rely=0.6, anchor="center")

        botao_nao = ctk.CTkButton(
            janela_confirmacao,
            width= 40,
            text="No",
            font=("Gelio Fasolada", 16),
            fg_color="red", 
            text_color="white",
            hover_color="darkred",
            command=janela_confirmacao.destroy
        )
        botao_nao.place(relx=0.6, rely=0.6, anchor="center")

    
    def confirmar_saida(self, janela_confirmacao):# Função auxiliar para confirmar saída
        print("Encerrando o programa...")
        janela_confirmacao.destroy()
        self.janela.destroy()  # Fecha a janela principal e encerra o programa

            
if __name__ == "__main__":
    root = ctk.CTk()
    app = Interface_Jogo(root)
    root.mainloop() 
    
