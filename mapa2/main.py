class JogoDaForca():
    def __init__(self):
        self.forca = ['''
        _________
        |        |
        |        o
        |       /|\\
        |       / \\
        |
        |
        ______________''',
                      '''
        _________
        |        |
        |        o
        |       /|\\
        |       / 
        |
        |
        ______________''',
                      '''
        _________
        |        |
        |        o
        |       /|\\
        |       
        |
        |
        ______________''',
                      '''
        _________
        |        |
        |        o
        |       /|
        |       
        |
        |
        ______________''',
                      '''
        _________
        |        |
        |        o
        |        |
        |       
        |
        |
        ______________''',
                      '''
        _________
        |        |
        |        o
        |       
        |       
        |
        |
        ______________''',
                      '''
        _________
        |        |
        |        
        |       
        |       
        |
        |
        ______________'''
                      ]

        self.nomes = [nome.title() for nome in open('nomes.txt', 'r').read().split('\n')]
        self.frutas = [nome.title() for nome in open('frutas.txt', 'r').read().split('\n')]
        self.objetos = [nome.title() for nome in open('objetos.txt', 'r').read().split('\n')]
        self.animais = [nome.title() for nome in open('animais.txt', 'r').read().split('\n')]
        self.acertos = 0
        self.erros = 0
        self.tentativas = 0
        self.chute = ''
        self.letras_certas = []
        self.letras_erradas = []
        self.palavra_oculta = []
        self.tipo_palavra = ''
        self.palavra_chave = ''
        self.condenacao = False
        self.palavra = False
        self.vitoria = False
        self.derrota = False

    #-----------------------------------------------------------------------

    def f_palavra(self):
        print('Precione ENTER para continuar!')
        input()
        from random import randint, sample

        tipo = int(input("""
                            Escolha se a palavra sera uma fruta, um animal, um objeto ou o nome de uma pessoa.
                            Escolha entre:
                            1 - Frutas
                            2 - Animais
                            3 - Objetos
                            4 - Nomes de pessoas
                >>"""))

        while tipo not in [1,2,3,4]:
            tipo = int(input("""
                                Escolha se a palavra sera uma fruta, um animal, um objeto ou o nome de uma pessoa.
                                Escolha entre:
                                1 - Frutas
                                2 - Animais
                                3 - Objetos
                                4 - Nomes de pessoas
                >>"""))

        if tipo == 1:
            palavra = sample(self.frutas, 1)[0]
            self.tipo_palavra = 'fruta'
        elif tipo == 2:
            palavra = sample(self.animais, 1)[0]
            self.tipo_palavra = 'animal'
        elif tipo == 3:
            palavra = sample(self.objetos, 1)[0]
            self.tipo_palavra = 'objeto'
        else:
            qtd_nomes = sample([1, 2, 3], 1)[0]
            nome = sample(self.nomes, qtd_nomes)
            if qtd_nomes > 1:
                palavra = ' '.join(nome)
            else:
                palavra = nome[0]
            self.tipo_palavra = 'nome'

        self.palavra = True
        self.palavra_chave = palavra
        return

    #---------------------------------------------------------------------------------------------------------

    def auxilio(self,i=0,cased='lower'):
        if self.tipo_palavra.lower() == 'fruta':
            lst = ['esta', 'a']
        elif self.tipo_palavra.lower() in ['animal', 'objeto', 'nome']:
            lst = ['este', 'o']

        case = { 'lower': lst[i].lower(),
                 'upper': lst[i].upper(),
                 'title': lst[i].title(),
                 'capitalize': lst[i].capitalize()}

        return case[cased]

    #-----------------------------------------------------------------------------

    def f_status(self):
        print(f"""Voce tem que advinhar qual e {self.auxilio(1)} {self.tipo_palavra.upper()}!
              Letras acertadas: {self.letras_certas}
              Letras erradas: {self.letras_erradas}
              {self.f_display_forca()} {self.f_display_palavra_oculta()}
        """)

    #-----------------------------------------------------------------------------

    def f_condenacao(self):
        print(f"""
        Bem vindo ao Jogo da forca!!

        Você esta prestes a ser condenado a morte pelo metodo da forca.
        Para tentar escapar voce deve acertar a palavra que sera apresentada a voce.
        Pode ser tanto o nome de uma pessoa, fruta, objeto ou animal, voce escolhe!"
        
        Voce deve informar as letras desta palavra, letra por letra.
        Caso erre uma parte do seu corpo vai aparecer na forca. Quando seu corpo inteiro estiver la...
        VOCE SERA SENTENCIADO A MORTE!!!!
        {self.f_display_forca()} {self.f_display_palavra_oculta()}
        """)
        self.condenacao = True
        return

    #-----------------------------------------------------------------------------

    def f_display_forca(self):
        return self.forca[int(f'-{self.erros+1}')]

    #----------------------------------------------------------------------------

    def f_display_palavra_oculta(self):
        if not self.palavra_chave:
            palavra = '? ? ? ? ? ?'
        else:
            palavra = ' '.join(self.palavra_oculta)

        return palavra

    #-----------------------------------------------------------------------------

    def f_chutes(self):
        self.palavra_oculta = ['_' for letra in self.palavra_chave]
        for i, letra in enumerate(self.palavra_chave):
            if letra == ' ':
                self.palavra_oculta[i] = ' '

        while '_' in self.palavra_oculta:
            if self.erros+1 == len(self.forca):
                self.derrota = True
                break
            self.f_status()
            self.chute = input('Digite uma letra: >>  ').upper()
            self.tentativas += 1

            if self.chute in self.palavra_chave.upper():
                self.acertos += 1
                if self.chute not in self.letras_certas:
                    self.letras_certas.append(self.chute)
                for i, l in enumerate(self.palavra_chave):
                    if self.chute == l.upper():
                        self.palavra_oculta[i] = l.upper()
                print(f'''
------------------------------------------------------------------------
VOCE ACERTOU!!!
A letra '{self.chute.upper()}' foi adicionada na palavra oculta!!!
------------------------------------------------------------------------''')
            else:
                if self.chute not in self.letras_erradas:
                    self.letras_erradas.append(self.chute)
                print(f'''
------------------------------------------------------------------------
VOCE ERROU!!!! A letra '{self.chute.upper()}' nao pertence a '{self.auxilio()} {self.tipo_palavra.upper()}'
Como consequencia, uma parte de seu corpo sera adicionada na forca!!!
------------------------------------------------------------------------''')
                self.erros += 1
        if self.palavra_oculta.count('_') == 0:
            self.vitoria = True

    def f_vitoria(self):
        from time import sleep

        print(f'''
        Parabens! Voce esta livre.
        -------------------------------------------------------
        {self.acertos} acertos.
        {self.erros} erros.
        {self.tentativas} tentativas.
        -------------------------------------------------------
        {self.f_display_forca()}
        DESTA VEZ!''')
        sleep(5)
        print('''
        
        
        
        Pressione ENTER!''')
        input()
        print('Obrigado por Jogar!!!')
        print('finalizando....')
        sleep(5)

    def f_morte(self):
        from time import sleep
        print(f'''
        SUAS CHANCES ACABARAM!!!
        --------------------------------------------------------
        {self.acertos} acertos.
        {self.erros} erros.
        {self.tentativas} tentativas.
        -------------------------------------------------------
        {self.f_display_forca()}

        A Palavra era {self.palavra_chave.upper()}

        MORTE PELA FORCA!''')
        sleep(5)
        print('''



        Pressione ENTER!''')
        input()
        print('Obrigado por Jogar!!!')
        print('finalizando....')
        sleep(5)

    def f_play(self):
        from time import sleep

        print('>>>>>>>>>> JOGO DA FORCA <<<<<<<<<<')
        sleep(1)
        print('Pressione ENTER para iniciar.')
        input()
        self.f_condenacao()

        if self.condenacao == True:
            self.f_palavra()
        if self.palavra == True:
            self.f_chutes()
        if self.vitoria == True:
            self.f_vitoria()
        if self.derrota == True:
            self.f_morte()

def game():
    jogo = JogoDaForca()
    jogo.f_play()

game()
