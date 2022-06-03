import PySimpleGUI as sg
from playwright.sync_api import sync_playwright
import time

versao = "1.1"

sg.theme("Reddit")
layout = [
    # [sg.Text(f"Robô Instagram {versao} / Curtidas")],
    [sg.Text("Login do Instagram:  "), sg.InputText(key="login", size=(35,1))],
    [sg.Text("Senha do Instagram: "), sg.InputText(key="senha", password_char="*", size=(35,1))],
    [sg.Radio('Hashtag', "selecao", key="selecao1", default=True), sg.Radio('Página', "selecao", key="selecao2")],
    [sg.Text("Buscar: ")],
    [sg.InputText(key="buscar", size=(30,1))],
    [sg.Text("Digite o número de páginas para buscar: ")],
    [sg.InputText(key="paginas", size=(10,1))],
    [sg.Text("")],
    [sg.Button("COMEÇAR"), sg.Button("SAIR")],
    [sg.Text("")],
    # [sg.Multiline("", key="prints1", size=(55,5))],
    # [sg.Multiline("", key="prints2", size=(55,5))],
    # [sg.Text("", key="printsreferencia")],
    [sg.Text("", key="prints3")],
    [sg.Multiline("", key="prints4", size=(70,8))],
    [sg.Text("Feito por Thiago", font=('Helvetica', 8, 'underline italic'))]

]

janela = sg.Window(f"Robô Instagram {versao} / Curtidas", layout)

while True:
    evento, valores = janela.read()

    if evento == sg.WIN_CLOSED or evento == "SAIR":
        break

    if evento == "COMEÇAR":
        login = valores["login"]
        senha = valores["senha"]
        buscar = valores["buscar"]
        selec_hashtag = valores["selecao1"]
        selec_pagina = valores["selecao2"]
        quantidade_de_paginas = int(valores["paginas"])
        tempo = 30

        def login_automatico():
            # Abrir navegador na página pretendida
            pagina.goto("https://www.instagram.com/")
            # Selecionar o campo de login e clicar
            pagina.locator('//*[@name="username"]').click()
            # Preencher o campo de login com o LOGIN
            pagina.fill('//*[@name="username"]', login)
            # Selecionar o campo de senha e clicar
            pagina.locator('//*[@name="password"]').click()
            # Preencher o campo de senha com o SENHA
            pagina.fill('//*[@name="password"]', senha)
            # clicar em Entrar
            pagina.locator('//*[@type="submit"]').click()
            # Tempo para colocar o login de segunda etapa
            time.sleep(tempo)


        def rolar_pagina_para_baixo(quantidade_vezes_rolar_para_baixo):
            for i in range(quantidade_vezes_rolar_para_baixo):
                pagina.keyboard.down('PageDown')


        with sync_playwright() as p:
            #   variável    chamando o navegador do playwright   Cache de login   mostrar navegador
            #   navegador = p.chromium.launch_persistent_context('user_data_dir', headless=False)
            # Foma simples de inciar o navegar:
            # navegador = p.chromium.launch(channel="chrome", headless=False)
            # Abaixo relacionei o navegador de forma a compliar como .exe e utilziar o chrome no Pc do usuário
            navegador = p.chromium.launch(channel="chrome", headless=False)
            pagina = navegador.new_page()
            links_sem_tratamento = []
            link_da_foto_tratado = []

            login_automatico()
            if selec_hashtag == True:
                pagina.goto(f"https://www.instagram.com/explore/tags/{buscar}/")
            else:
                pagina.goto(f"https://www.instagram.com/{buscar}/")

            pagina.wait_for_selector('a')
            rolar_pagina_para_baixo(quantidade_de_paginas)
            time.sleep(5)

            index = pagina.locator('a')

            for i in range(index.count()):
                hrefs = pagina.locator('a').nth(i)
                # hrefs = pagina.query_selector("a").get_attribute('href')
                links_sem_tratamento.append(hrefs.get_attribute("href"))
                # janela["prints1"].update(f"Adicionando as {index.count()} referências encontradas em uma lista... {i + 1}")

            # janela["printsreferencia"].update("##########Tratando as referências encontradas...##########")

            for pic in (links_sem_tratamento):
                if "/p/" in pic:
                    link_da_foto_tratado.append(pic)
                    # janela["prints2"].update(f"Referência correta adicionada a lista... {pic}")

            janela["prints3"].update(f"{len(link_da_foto_tratado)} referências encontradas e tratadas...")

            for i, link in enumerate(link_da_foto_tratado):
                pagina.goto('https://www.instagram.com{}'.format(link_da_foto_tratado[i]))
                time.sleep(1)
                pagina.locator('//*[@class="_abm0 _abl_"]').nth(0).click()
                # janela["prints4"].update("foto {} curtida com sucesso, segue link: https://www.instagram.com{}".format(i + 1, link_da_foto_tratado[i]))
                janela["prints4"].print("foto {} curtida com sucesso, segue link: https://www.instagram.com{}".format(i + 1, link_da_foto_tratado[i]))




janela.close()