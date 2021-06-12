from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image
import pyaudio
from playsound import playsound
import time

pomodoros = n_pomodoros = 1
loop = True
ativo = False
icones = ["icon_v.png", "icon_a.png", "icon_c.png"]
tempo_acao = 1
tempo_pausa = 1


def acao_inicia():
    global ativo
    ativo = True


def acao_para():
    global pomodoros
    pomodoros = 0


def atualiza_menu(icone, status):
    if status == "inicio":
        icone.menu = menu(
            item(
                "Pomodoros",
                menu(
                    item("1", acao_escolha, radio=True),
                    item("2", acao_escolha, radio=True),
                    item("3", acao_escolha, radio=True),
                    item("4", acao_escolha, radio=True),
                    item("5", acao_escolha, radio=True),
                    item("6", acao_escolha, radio=True),
                    item("7", acao_escolha, radio=True),
                    item("8", acao_escolha, radio=True),
                    item("9", acao_escolha, radio=True),
                    item("10", acao_escolha, radio=True),
                ),
            ),
            item("Inicia", acao_inicia),
            item("sai", acao_sai),
        )
    else:
        icone.menu = menu(
            item(
                "Pomodoros",
                menu(
                    item("1", acao_escolha, radio=True),
                    item("2", acao_escolha, radio=True),
                    item("3", acao_escolha, radio=True),
                    item("4", acao_escolha, radio=True),
                    item("5", acao_escolha, radio=True),
                    item("6", acao_escolha, radio=True),
                    item("7", acao_escolha, radio=True),
                    item("8", acao_escolha, radio=True),
                    item("9", acao_escolha, radio=True),
                    item("10", acao_escolha, radio=True),
                ),
            ),
            item("Inicia", acao_inicia),
            item("Sai", acao_sai),
            item("Para", acao_para),
            item(status, atualiza),
        )
    icone.update_menu()


def atualiza(icone):
    icone.update_menu()


def acao_sai(icon, item):
    global loop
    loop = False
    icon.stop()


def acao_escolha(icon, item):
    global pomodoros
    global n_pomodoros
    n_pomodoros = pomodoros = int(item.text)


def em_exec(icone):
    global pomodoros
    global ativo
    global loop
    primeira_vez = True
    pausa = False
    while loop:
        if ativo:
            if pomodoros > 0:
                if primeira_vez:
                    playsound("alarm.wav")
                    inicio_contagem = time.time()
                    primeira_vez = False
                    if pausa:
                        fim = temporizador = tempo_pausa * 60
                        image = Image.open(icones[1])
                    else:
                        fim = temporizador = tempo_acao * 60
                        image = Image.open(icones[0])
                    icone.icon = image
                else:
                    fim = temporizador - (time.time() - inicio_contagem)
                    if fim < 0:
                        primeira_vez = True
                        if pausa:
                            pomodoros -= 1
                        pausa = not pausa
                    else:
                        fim = (tempo_pausa * 60) - (time.time() - inicio_contagem)
                        if fim < 0:
                            pausa = False
                            primeira_vez = True
                            pomodoros -= 1

                texto_icone = "Resta(m) " + (
                    str(pomodoros)
                    + "/"
                    + str(n_pomodoros)
                    + " "
                    + "{:02d}:{:02d}".format((int(fim / 60)), (int(fim) % 60))
                    + "\n"
                    + "Status: "
                    + ("Pausa" if pausa else "Ao Trabalho")
                )
                atualiza_menu(icone, texto_icone)
            else:
                image = Image.open(icones[2])
                icone.icon = image
                ativo = False
                pomodoros = 1
                primeira_vez = True
                playsound("alarm.wav")
                atualiza_menu(icone, "inicio")
        time.sleep(2)


if __name__ == "__main__":
    icone = icon("Pomodoro")
    atualiza_menu(icone, "inicio")
    image = Image.open(icones[2])
    icone.icon = image
    icone.visible = True
    icone.run(setup=em_exec)
