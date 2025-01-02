# Funcionalidades do jogo
# criado:  18/12/24
# atualizado: 02/01/25

import ctypes
import tkinter as tk
from tkinter import font
from tkinter import filedialog, messagebox, Label, Tk, Canvas, PhotoImage
import random
from random import randint

class Back_End:
    def __init__(self):
        print(f"Instância de Back_End criada: {id(self)}") # for debug
        self.personagem_escolhido_nome = "No Name"
        self.personagem_escolhido_about = "Return and select a player\nto start"
        self.personagem_escolhido_imagem = None       
        self.player_xp = 10 # tá como XP mas são as vidas do player o certo seria: HP
        self.player_pontos = 0    
        self.casa_atual = 1 # Inicializando com a casa 1
  
        self.carta_inicial = [{
            "nome": "No name",
            "action": "Return and select a card to start",
            "action_p": """Return and select
a card to start""",
            "imagem": "images/carta_default.png",
            "imagem_pequena": "images/carta_menu.png"
        }]
        
        self.carta_casa_deus = [ {
            "nome": "Persephone",
            "action": "Go back 1, 2, or 3 spaces",
            "action_p": """Return and select
a card to start""",
            "imagem": "images/carta_persephone.png",
            "imagem_pequena": "images/carta_persephone_p.png"
        }]
        
        # Só pode ter 1 carta no inicio
        self.cartas_player = [ {
            "nome": "Persephone",
            "action": "Go back 1, 2, or 3 spaces",
            "action_p": """Return and 
select a card
to start""",
            "imagem": "images/carta_persephone.png",
            "imagem_pequena": "images/carta_persephone_p.png"
        }  ] # cartas do jogador na partida, máximo 3 cartas
                                        
        self.cores_layout = {
            'branco': "#FFFFFF", # branco
            'azul': "#4DC2F5",   # (0.3, 0.76, 0.96, 1)
            'verde': "#2DCD70",  # (0.18, 0.8, 0.44)
            'amarelo': "#F1C20D",  # (0.94, 0.76, 0.05)
            'laranja': "#FF8A65",  # (255/255, 138/255, 101/255)
            'vermelho': "#D32F2F",  # (211/255, 47/255, 47/255)
            'rosa': "#F48FB1",  # (244/255, 143/255, 177/255)
            'roxo': "#9575CD",   # (149/255, 117/255, 205/255)
            'agua': "#5FD3C1",
        }
        # deixar no default quando terminar o layout
        
        self.cor_layout_atual = self.cores_layout['azul'] #"default de layout texto azul
        
        # dicionário dos personagens em jogo
        self.personagens_jogo = [
            {
            "nome" : "Hippolyta",
            "about":  """Queen of the Amazons: A powerful warrior 
and ruler of a legendary race of female warriors.
She wants to reach Olympus to attain 
the status of a demigoddess.""",
            "imagem": "images/hipolita.png"},
            
            {"nome" : "Odysseus",
             "about":  """King of Ithaca, outsmarts monsters and gods
on his epic journey home after the Trojan War.
He wants to reach Olympus to attain
the status of a demigod.""",
             "imagem": "images/odisseu.png"},
            
            {"nome" : "Achilles",
             "about": """The greatest Greek warrior,
possesses invulnerability (except for a heel).
He wants to reach Olympus to attain
the status of a demigod.""",
             "imagem": "images/aquiles.png"},
            
            {"nome" : "Atalanta",
             "about": """The Unbeatable Huntress: A Timeless 
Symbol of Female Strength and Independence.
He wants to reach Olympus to attain
the status of a demigod.""",
             "imagem": "images/atalanta.png"},
            
            {"nome" : "Theseus",
             "about": """The hero who conquered the Minotaur,
united the lands of Attica, and became king.
He wants to reach Olympus to attain
the status of a demigod.""",
             "imagem": "images/teseu.png"}
        ]
            
        # Todas as cartas do jogo
        self.cartas_deuses = [
        {
            "nome": "Aphrodite",
            "action": "Advance 6 spaces",
            "action_p": """Advance
6 spaces""",
            "imagem": "images/carta_aphrodite.png",
            "imagem_pequena": "images/carta_aphrodite_p.png"
        },
        {
            "nome": "Apollo",
            "action": "Roll 1 dice",
            "action_p": """Roll
1 dice""",
            "imagem": "images/carta_apollo.png",
            "imagem_pequena": "images/carta_apollo_p.png"
        },
        {
            "nome": "Artemis",
            "action": "Advance 3 spaces, or roll 1 die",
            "action_p": """Advance
3 spaces,
or roll
1 die""",
            "imagem": "images/carta_artemis.png",
            "imagem_pequena": "images/carta_artemis_p.png"
        },
        {
            "nome": "Ares",
            "action": "Win 1 battle, or roll 1 die",
            "action_p": """Win
1 battle,
or roll
1 die""",
            "imagem": "images/carta_ares.png",
            "imagem_pequena": "images/carta_ares_p.png"
        },
        {
            "nome": "Hades",
            "action": "Gain one life",
            "action_p": """Gain
1 life""",
            "imagem": "images/carta_hades.png",
            "imagem_pequena": "images/carta_hades_p.png"
        },
        {
            "nome": "Hephaestus",
            "action": "Roll 1 dice",
            "action_p": """Roll
1 dice""",
            "imagem": "images/carta_hephaestus.png",
            "imagem_pequena": "images/carta_hephaestus_p.png"
        },
        {
            "nome": "Hera",
            "action": "Gain one life, or roll 1 die",
            "action_p": """Gain
1 life,
or roll 
1 die""",
            "imagem": "images/carta_hera.png",
            "imagem_pequena": "images/carta_hera_p.png"
        },
        {
            "nome": "Hermes",
            "action": "Advance 5 spaces, or skip 1 space",
            "action_p": """Advance 
5 spaces,
or skip
1 space""",
            "imagem": "images/carta_hermes.png",
            "imagem_pequena": "images/carta_hermes_p.png"
        },
        {
            "nome": "Persephone",
            "action": "Go back 1, 2, or 3 spaces",
            "action_p": """Go back
1, 2, or
3 spaces""",
            "imagem": "images/carta_persephone.png",
            "imagem_pequena": "images/carta_persephone_p.png"
        },
        {
            "nome": "Poseidon",
            "action": "Advance 4 spaces, or roll 1 die",
            "action_p": """Advance
4 spaces,
or roll
1 die""",
            "imagem": "images/carta_poseidon.png",
            "imagem_pequena": "images/carta_poseidon_p.png"
        },
        {
            "nome": "Zeus",
            "action": "Advance 6 spaces, or roll 1 dice",
            "action_p": """Advance
6 spaces,
or roll
1 dice""",
            "imagem": "images/carta_zeus.png",
            "imagem_pequena": "images/carta_zeus_p.png"
        },
         {
            "nome": "Athena",
            "action": "Win 1 battle, or advance 2 spaces",
            "action_p": """Win
1 battle,
or advance
2 spaces""",
            "imagem": "images/carta_athena.png",
            "imagem_pequena": "images/carta_athena_p.png"
        }
    ]
      
        self.tijolos_cor = {
            "azul": "images/tijolos_azuis.png",
            "verde": "images/tijolos_verde.png",
            "amarelo": "images/tijolos_amarelo.png",
            "laranja": "images/tijolos_laranja.png",
            "vermelho": "images/tijolos_vermelho.png",
            "rosa": "images/tijolos_rosa.png",
            "roxo": "images/tijolos_roxo.png",
            "agua": "images/tijolos_agua.png",
        }
        
        # Tijolo grnade que vai em cima da tela
        self.tijolos_cor_atual = "images/tijolos_azuis.png" # default
        
        self.dic_cards = {
            "1": self.cartas_deuses[0],   # Aphrodite
            "2": self.cartas_deuses[1],   # Apollo
            "3": self.cartas_deuses[2],   # Artemis
            "4": self.cartas_deuses[3],   # Ares
            "5": self.cartas_deuses[4],   # Hades
            "6": self.cartas_deuses[5],   # Hephaestus
            "7": self.cartas_deuses[6],   # Hera
            "8": self.cartas_deuses[7],   # Hermes
            "9": self.cartas_deuses[8],   # Persephone
            "10": self.cartas_deuses[9],  # Poseidon
            "11": self.cartas_deuses[10],  # Zeus
            "12": self.cartas_deuses[11]  # Atena
        }
        
        self.casas = [
    {"numero": 1, "texto": "", "imagem": "imagens_casas/casa_001.png"},
    {"numero": 2, "texto": "Hermes", "imagem": "imagens_casas/casa_002.png"},
    {"numero": 3, "texto": "", "imagem": "imagens_casas/casa_003.png"},
    {"numero": 4, "texto": "", "imagem": "imagens_casas/casa_004.png"},
    {"numero": 5, "texto": "Sphinx", "imagem": "imagens_casas/casa_005.png"},
    {"numero": 6, "texto": "", "imagem": "imagens_casas/casa_006.png"},
    {"numero": 7, "texto": "", "imagem": "imagens_casas/casa_007.png"},
    {"numero": 8, "texto": "Prometheus", "imagem": "imagens_casas/casa_008.png"},
    {"numero": 9, "texto": "", "imagem": "imagens_casas/casa_009.png"},
    {"numero": 10, "texto": "Sparta", "imagem": "imagens_casas/casa_010.png"},
    {"numero": 11, "texto": "", "imagem": "imagens_casas/casa_011.png"},
    {"numero": 12, "texto": "", "imagem": "imagens_casas/casa_012.png"},
    {"numero": 13, "texto": "Hestia", "imagem": "imagens_casas/casa_013.png"},
    {"numero": 14, "texto": "", "imagem": "imagens_casas/casa_014.png"},
    {"numero": 15, "texto": "", "imagem": "imagens_casas/casa_015.png"},
    {"numero": 16, "texto": "", "imagem": "imagens_casas/casa_016.png"},
    {"numero": 17, "texto": "Chimera", "imagem": "imagens_casas/casa_017.png"},
    {"numero": 18, "texto": "", "imagem": "imagens_casas/casa_018.png"},
    {"numero": 19, "texto": "", "imagem": "imagens_casas/casa_019.png"},
    {"numero": 20, "texto": "", "imagem": "imagens_casas/casa_020.png"},
    {"numero": 21, "texto": "Poseidon", "imagem": "imagens_casas/casa_021.png"},
    {"numero": 22, "texto": "", "imagem": "imagens_casas/casa_022.png"},
    {"numero": 23, "texto": "", "imagem": "imagens_casas/casa_023.png"},
    {"numero": 24, "texto": "Ciclops", "imagem": "imagens_casas/casa_024.png"},
    {"numero": 25, "texto": "", "imagem": "imagens_casas/casa_025.png"},
    {"numero": 26, "texto": "", "imagem": "imagens_casas/casa_026.png"},
    {"numero": 27, "texto": "", "imagem": "imagens_casas/casa_027.png"},
    {"numero": 28, "texto": "Harpies", "imagem": "imagens_casas/casa_028.png"},
    {"numero": 29, "texto": "", "imagem": "imagens_casas/casa_029.png"},
    {"numero": 30, "texto": "Athena", "imagem": "imagens_casas/casa_030.png"},
    {"numero": 31, "texto": "", "imagem": "imagens_casas/casa_031.png"},
    {"numero": 32, "texto": "Thanatos", "imagem": "imagens_casas/casa_032.png"},
    {"numero": 33, "texto": "", "imagem": "imagens_casas/casa_033.png"},
    {"numero": 34, "texto": "Minotaur", "imagem": "imagens_casas/casa_034.png"},
    {"numero": 35, "texto": "", "imagem": "imagens_casas/casa_035.png"},
    {"numero": 36, "texto": "Labyrinth", "imagem": "imagens_casas/casa_036.png"},
    {"numero": 37, "texto": "", "imagem": "imagens_casas/casa_037.png"},
    {"numero": 38, "texto": "Hades", "imagem": "imagens_casas/casa_038.png"},
    {"numero": 39, "texto": "Charon", "imagem": "imagens_casas/casa_039.png"},
    {"numero": 40, "texto": "", "imagem": "imagens_casas/casa_040.png"},
    {"numero": 41, "texto": "", "imagem": "imagens_casas/casa_041.png"},
    {"numero": 42, "texto": "Judgment", "imagem": "imagens_casas/casa_042.png"},
    {"numero": 43, "texto": "", "imagem": "imagens_casas/casa_043.png"},
    {"numero": 44, "texto": "Orpheus", "imagem": "imagens_casas/casa_044.png"},
    {"numero": 45, "texto": "", "imagem": "imagens_casas/casa_045.png"},
    {"numero": 46, "texto": "", "imagem": "imagens_casas/casa_046.png"},
    {"numero": 47, "texto": "", "imagem": "imagens_casas/casa_047.png"},
    {"numero": 48, "texto": "", "imagem": "imagens_casas/casa_048.png"},
    {"numero": 49, "texto": "Hephaestus", "imagem": "imagens_casas/casa_049.png"},
    {"numero": 50, "texto": "", "imagem": "imagens_casas/casa_050.png"},
    {"numero": 51, "texto": "", "imagem": "imagens_casas/casa_051.png"},
    {"numero": 52, "texto": "Erinyes", "imagem": "imagens_casas/casa_052.png"},
    {"numero": 53, "texto": "", "imagem": "imagens_casas/casa_053.png"},
    {"numero": 54, "texto": "", "imagem": "imagens_casas/casa_054.png"},
    {"numero": 55, "texto": "Persephone", "imagem": "imagens_casas/casa_055.png"},
    {"numero": 56, "texto": "", "imagem": "imagens_casas/casa_056.png"},
    {"numero": 57, "texto": "", "imagem": "imagens_casas/casa_057.png"},
    {"numero": 58, "texto": "", "imagem": "imagens_casas/casa_058.png"},
    {"numero": 59, "texto": "", "imagem": "imagens_casas/casa_059.png"},
    {"numero": 60, "texto": "", "imagem": "imagens_casas/casa_060.png"},
    {"numero": 61, "texto": "Hydra", "imagem": "imagens_casas/casa_061.png"},
    {"numero": 62, "texto": "", "imagem": "imagens_casas/casa_062.png"},
    {"numero": 63, "texto": "", "imagem": "imagens_casas/casa_063.png"},
    {"numero": 64, "texto": "Apollo", "imagem": "imagens_casas/casa_064.png"},
    {"numero": 65, "texto": "", "imagem": "imagens_casas/casa_065.png"},
    {"numero": 66, "texto": "Sisyphus", "imagem": "imagens_casas/casa_066.png"},
    {"numero": 67, "texto": "", "imagem": "imagens_casas/casa_067.png"},
    {"numero": 68, "texto": "", "imagem": "imagens_casas/casa_068.png"},
    {"numero": 69, "texto": "Centaurs", "imagem": "imagens_casas/casa_069.png"},
    {"numero": 70, "texto": "", "imagem": "imagens_casas/casa_070.png"},
    {"numero": 71, "texto": "Satyrs", "imagem": "imagens_casas/casa_071.png"},
    {"numero": 72, "texto": "", "imagem": "imagens_casas/casa_072.png"},
    {"numero": 73, "texto": "Hera", "imagem": "imagens_casas/casa_073.png"},
    {"numero": 74, "texto": "", "imagem": "imagens_casas/casa_074.png"},
    {"numero": 75, "texto": "Sirens", "imagem": "imagens_casas/casa_075.png"},
    {"numero": 76, "texto": "", "imagem": "imagens_casas/casa_076.png"},
    {"numero": 77, "texto": "", "imagem": "imagens_casas/casa_077.png"},
    {"numero": 78, "texto": "", "imagem": "imagens_casas/casa_078.png"},
    {"numero": 79, "texto": "Ares", "imagem": "imagens_casas/casa_079.png"},
    {"numero": 80, "texto": "", "imagem": "imagens_casas/casa_080.png"},
    {"numero": 81, "texto": "", "imagem": "imagens_casas/casa_081.png"},
    {"numero": 82, "texto": "Nymphs", "imagem": "imagens_casas/casa_082.png"},
    {"numero": 83, "texto": "", "imagem": "imagens_casas/casa_083.png"},
    {"numero": 84, "texto": "", "imagem": "imagens_casas/casa_084.png"},
    {"numero": 85, "texto": "Troy", "imagem": "imagens_casas/casa_085.png"},
    {"numero": 86, "texto": "", "imagem": "imagens_casas/casa_086.png"},
    {"numero": 87, "texto": "", "imagem": "imagens_casas/casa_087.png"},
    {"numero": 88, "texto": "Aphrodite", "imagem": "imagens_casas/casa_088.png"},
    {"numero": 89, "texto": "", "imagem": "imagens_casas/casa_089.png"},
    {"numero": 90, "texto": "Eros", "imagem": "imagens_casas/casa_090.png"},
    {"numero": 91, "texto": "", "imagem": "imagens_casas/casa_091.png"},
    {"numero": 92, "texto": "", "imagem": "imagens_casas/casa_092.png"},
    {"numero": 93, "texto": "Pegasus", "imagem": "imagens_casas/casa_093.png"},
    {"numero": 94, "texto": "", "imagem": "imagens_casas/casa_094.png"},
    {"numero": 95, "texto": "", "imagem": "imagens_casas/casa_095.png"},
    {"numero": 96, "texto": "Dionisius", "imagem": "imagens_casas/casa_096.png"},
    {"numero": 97, "texto": "", "imagem": "imagens_casas/casa_097.png"},
    {"numero": 98, "texto": "Bacchaes", "imagem": "imagens_casas/casa_098.png"},
    {"numero": 99, "texto": "", "imagem": "imagens_casas/casa_099.png"},
    {"numero": 100, "texto": "Pan", "imagem": "imagens_casas/casa_100.png"},
    {"numero": 101, "texto": "", "imagem": "imagens_casas/casa_101.png"},
    {"numero": 102, "texto": "", "imagem": "imagens_casas/casa_102.png"},
    {"numero": 103, "texto": "", "imagem": "imagens_casas/casa_103.png"},
    {"numero": 104, "texto": "Artemis", "imagem": "imagens_casas/casa_104.png"},
    {"numero": 105, "texto": "", "imagem": "imagens_casas/casa_105.png"},
    {"numero": 106, "texto": "", "imagem": "imagens_casas/casa_106.png"},
    {"numero": 107, "texto": "Orion", "imagem": "imagens_casas/casa_107.png"},
    {"numero": 108, "texto": "", "imagem": "imagens_casas/casa_108.png"},
    {"numero": 109, "texto": "", "imagem": "imagens_casas/casa_109.png"},
    {"numero": 110, "texto": "Midas", "imagem": "imagens_casas/casa_110.png"},
    {"numero": 111, "texto": "", "imagem": "imagens_casas/casa_111.png"},
    {"numero": 112, "texto": "Zeus", "imagem": "imagens_casas/casa_112.png"},
    {"numero": 113, "texto": "", "imagem": "imagens_casas/casa_113.png"},
    {"numero": 114, "texto": "", "imagem": "imagens_casas/casa_114.png"},
    {"numero": 115, "texto": "", "imagem": "imagens_casas/casa_115.png"},
    {"numero": 116, "texto": "Chronos", "imagem": "imagens_casas/casa_116.png"},
    {"numero": 117, "texto": "", "imagem": "imagens_casas/casa_117.png"},
    {"numero": 118, "texto": "", "imagem": "imagens_casas/casa_118.png"},
    {"numero": 119, "texto": "Griffins", "imagem": "imagens_casas/casa_119.png"},
    {"numero": 120, "texto": "", "imagem": "imagens_casas/casa_120.png"}
]
 
       
    # escolha a carta inicial
    def escolher_carta(self):
        # Sorteia um número aleatório entre 1 e 12
        numero_sorteado = str(random.randint(1, 12))  # Convertido para string, pois as chaves no dic_cards são strings

        # Atualiza a carta inicial com a carta sorteada
        self.carta_inicial[0] = self.dic_cards[numero_sorteado]

        # Substitui a carta que está no índice 0 da lista cartas_player
        if not self.cartas_player:
            # Se a lista estiver vazia, inicializa com a carta sorteada
            self.cartas_player.append(self.carta_inicial[0])
        else:
            # Se já existir uma carta no índice 0, substitui a carta
            self.cartas_player[0] = self.carta_inicial[0]

        # Garante que a lista de cartas do jogador não exceda o limite de 3
        if len(self.cartas_player) > 3:
            self.cartas_player = self.cartas_player[:3]  # Mantém apenas os primeiros 3 elementos

        # Exibe as informações da carta sorteada
        carta_sorteada = self.carta_inicial[0]
        print(f"**Carta Sorteada:** {carta_sorteada['nome']}")
        print(f"Ação: {carta_sorteada['action']}")
        print(f"Imagem: {carta_sorteada['imagem']}")

        # Debug: Exibe todas as cartas do jogador
        print("**Cartas do Jogador:**")
        for carta in self.cartas_player:
            print(f"- {carta['nome']}: {carta['action']}")
            print(f"- {carta['imagem']}: {carta['imagem_pequena']}")


        
        # Garante que a lista de cartas do jogador não exceda o limite de 3
        if len(self.cartas_player) > 3:
            self.cartas_player = self.cartas_player[:3]  # Mantém apenas os primeiros 3 elementos

        # Exibe as informações da carta sorteada
        carta_sorteada = self.carta_inicial[0]
        print(f"**Carta Sorteada:** {carta_sorteada['nome']}")
        print(f"Ação: {carta_sorteada['action']}")
        print(f"Imagem: {carta_sorteada['imagem']}")

        # Debug: Exibe todas as cartas do jogador
        print("**Cartas do Jogador:**")
        for carta in self.cartas_player:
            print(f"- {carta['nome']}: {carta['action']}")
            print(f"- {carta['imagem']}: {carta['imagem_pequena']}")
      
    # Falta testar!
    def escolher_carta_dionisio(self):
        # Sorteia um número aleatório entre 1 e 12
        numero_sorteado = str(random.randint(1, 12))  # Convertido para string, pois as chaves no dic_cards são strings        
         # Se a lista estiver vazia, inicializa com a carta sorteada
        self.cartas_player.append(self.dic_cards[numero_sorteado])
        
        # Garante que a lista de cartas do jogador não exceda o limite de 3
        if len(self.cartas_player) > 3:
            self.cartas_player = self.cartas_player[:3]  # Mantém apenas os primeiros 3 elementos

       
    def load_font(self, font_path):  # Método para carregar fontes personalizadas
        FR_PRIVATE = 0x10
        FR_NOT_ENUM = 0x20
        pathbuf = ctypes.create_unicode_buffer(font_path)
        ctypes.windll.gdi32.AddFontResourceExW(pathbuf, FR_PRIVATE | FR_NOT_ENUM, 0)


    def load_fonts(self):  # Método para inicializar e verificar fontes
        self.load_font("fonts/Gelio Fasolada.ttf")
        self.load_font("fonts/OlympusBold.ttf")        
        # Verifica as fontes carregadas
        #print("Fontes disponíveis:", font.families())  # Opcional: listar todas as fontes disponíveis 
        

    def escolher_personagem(self, nome_personagem):
        # Busca os dados do personagem no dicionário
        personagem = next(
            (p for p in self.personagens_jogo if p["nome"].lower() == nome_personagem.lower()), None
        )
        if personagem:
            self.personagem_escolhido_nome = personagem["nome"]
            self.personagem_escolhido_about = personagem["about"]
            self.personagem_escolhido_imagem = personagem["imagem"]
            print(f"Personagem escolhido foi {self.personagem_escolhido_nome}\n"
                  f"Texto personagem: {self.personagem_escolhido_about}\n"
                  f"Imagem do personagem: {self.personagem_escolhido_imagem}")
        else:
            print(f"Personagem {nome_personagem} não encontrado!")
     
         
    def remove_carta_usada(self, nome_carta):
        # Itera sobre as cartas do jogador para encontrar a carta com o nome fornecido
        print(f'Cartas do player antes de usar a carta: {self.cartas_player}') #Debug
        for carta in self.cartas_player:
            if carta['nome'] == nome_carta:
                self.cartas_player.remove(carta)  # Remove a carta do jogador
                print(f"Carta '{nome_carta}' removida com sucesso!")
                return self.cartas_player  # Retorna a lista de cartas atualizada
        print(f"Carta '{nome_carta}' não encontrada!")
        print(f'Cartas do player depois de usar a carta: {self.cartas_player}') #Debug
        return self.cartas_player  # Retorna a lista de cartas sem alterações
    
    
    def avanca_casa_cartas(self, numero_de_avanco=0, numero_retorna=0):
        print(f'Casa atual antes de usar a carta: {self.casa_atual}')#Debug
        # Atualiza a casa atual com base nos avanços e retornos
        self.casa_atual += numero_de_avanco  # Avança a casa
        self.casa_atual -= numero_retorna   # Retorna a casa (subtração)
        # Para que a casa nunca seja negativa
        if self.casa_atual < 1:
            self.casa_atual = 1  # Garantir que a casa atual nunca seja menor que 1
        print(f'Casa atual depois de usar a carta: {self.casa_atual}')#Debug
        return self.casa_atual  # Retorna a casa atualizada


    def adicionar_carta_a_cartas_player(self, nome_carta):
        # Localiza a carta correspondente pelo nome
        carta_selecionada = next((carta for carta in self.cartas_deuses if carta["nome"] == nome_carta), None)
        
        if not carta_selecionada:
            print(f"Erro: Carta com nome '{nome_carta}' não encontrada.")
            return
        
        # Verifica se a carta já está na lista
        if any(carta["nome"] == nome_carta for carta in self.cartas_player):
            print(f"Erro: A carta '{nome_carta}' já está na lista.")
            return

        # Verifica se a lista está cheia
        if len(self.cartas_player) >= 3:
            # Remove o primeiro item (substituição)
            carta_removida = self.cartas_player.pop(0)
            print(f"A lista está cheia. Substituindo a carta '{carta_removida['nome']}' pela nova carta '{nome_carta}'.")

        # Adiciona a nova carta à lista
        self.cartas_player.append(carta_selecionada)
        print(f"Carta '{nome_carta}' adicionada com sucesso. Lista atual:")
        for carta in self.cartas_player:
            print(f"- {carta['nome']}: {carta['action']}")
  
    
    # PARA SABER SE O JOGO ACABOU!!
    def verificar_condicoes(self):
        """Verifica as condições de game over ou vitória."""
        if self.player_xp <= 0:
            return "game_over"
        elif self.casa_atual >= 120:
            return "game_win"
        return None
    
    
    def restart_game(self): # reinicializa as variaveis do jogo
        self.personagem_escolhido_nome = "No Name"
        self.personagem_escolhido_about = "Return and select a player\nto start"
        self.personagem_escolhido_imagem = None    
        self.player_xp = 3 
        self.player_pontos = 0    
        self.casa_atual = 1 
  
        self.carta_inicial = [{
            "nome": "No name",
            "action": "Return and select a card to start",
            "action_p": """Return and select
a card to start""",
            "imagem": "images/carta_default.png",
            "imagem_pequena": "images/carta_menu.png"
        }]
        
        self.carta_casa_deus = [ {
            "nome": "Persephone",
            "action": "Go back 1, 2, or 3 spaces",
            "action_p": """Return and select
a card to start""",
            "imagem": "images/carta_persephone.png",
            "imagem_pequena": "images/carta_persephone_p.png"
        }]
        
        self.cartas_player = [ {
            "nome": "Persephone",
            "action": "Go back 1, 2, or 3 spaces",
            "action_p": """Return and 
select a card
to start""",
            "imagem": "images/carta_persephone.png",
            "imagem_pequena": "images/carta_persephone_p.png"
        }  ] # cartas do jogador na partida, máximo 3 cartas
        
        # self.cor_layout_atual = "#4DC2F5" # ['azul'] #"default de layout texto azul
        
        
