import PySimpleGUI as sg
from PySimpleGUI import theme_previewer
from playwright.sync_api import sync_playwright
import time

theme_previewer()
layout = [
    [sg.Text("Robô Instagram 1.0 / Curtidas")],
    [sg.Text("")],
    [sg.Text("Login do Instagram:  "), sg.InputText(key="login")],
    [sg.Text("Senha do Instagram: "), sg.InputText(key="senha", password_char="*")],
    [sg.Text("Hashtag para busca: "), sg.InputText(key="hashtag")],
    [sg.Text("Digite o número de páginas para buscar: ")],
    [sg.InputText(key="paginas")],
    [sg.Text("")],
    [sg.Button("COMEÇAR"), sg.Button("SAIR")],
    [sg.Text("")],
    [sg.Multiline("", key="prints1", size=(55,5))],
    [sg.Multiline("", key="prints2", size=(55,5))],
    [sg.Text("", key="printsreferencia")],
    [sg.Text("", key="prints3")],
    [sg.Multiline("", key="prints4", size=(70,8))]

]

janela = sg.Window("Robô Instagram 1.0 / Curtidas", layout)

while True:
    evento, valores = janela.read()

    if evento == sg.WIN_CLOSED or evento == "SAIR":
        break

    if evento == "COMEÇAR":
        login = valores["login"]
        senha = valores["senha"]
        hashtag = valores["hashtag"]
        paginas = int(valores["paginas"])
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
            # navegador = p.chromium.launch_persistent_context('user_data_dir', headless=False)
            navegador = p.chromium.launch(headless=False)
            pagina = navegador.new_page()
            links_sem_tratamento = []
            link_da_foto_tratado = []

            login_automatico()

            pagina.goto(f"https://www.instagram.com/explore/tags/{hashtag}/")
            pagina.wait_for_selector('a')
            rolar_pagina_para_baixo(paginas)
            time.sleep(5)

            index = pagina.locator('a')

            for i in range(index.count()):
                hrefs = pagina.locator('a').nth(i)
                # hrefs = pagina.query_selector("a").get_attribute('href')
                links_sem_tratamento.append(hrefs.get_attribute("href"))
                janela["prints1"].update(f"Adicionando as {index.count()} referências encontradas em uma lista... {i + 1}")

            # janela["printsreferencia"].update("##########Tratando as referências encontradas...##########")

            for pic in (links_sem_tratamento):
                if "/p/" in pic:
                    link_da_foto_tratado.append(pic)
                    janela["prints2"].update(f"Referência correta adicionada a lista... {pic}")

            janela["prints3"].update(f"{len(link_da_foto_tratado)} referências encontradas e tratadas...")

            for i, link in enumerate(link_da_foto_tratado):
                pagina.goto('https://www.instagram.com{}'.format(link_da_foto_tratado[i]))
                time.sleep(1)
                pagina.locator('//*[@class="_abm0 _abl_"]').nth(0).click()
                janela["prints4"].update("foto {} curtida com sucesso, segue link: https://www.instagram.com{}".format(i + 1, link_da_foto_tratado[i]))





janela.close()