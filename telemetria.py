import os
import subprocess
import time
import sys
import pyautogui


def verificar_admin():
    """Verifica se o script está rodando como administrador."""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def executar_fortiesnac(senha):
    """Executa o FortiESNAC com a senha fornecida."""
    caminho_forticlient = r"C:\Program Files\Fortinet\FortiClient"
    executavel_snac = os.path.join(caminho_forticlient, "FortiESNAC.exe")

    # Executa o FortiESNAC
    subprocess.Popen([executavel_snac, '-u'])
    time.sleep(5)  # Aguarda um pouco para a janela aparecer

    # Digita a senha
    pyautogui.typewrite(senha)
    pyautogui.press('enter')


def desinstalar_forticlient():
    """Desinstala o FortiClient usando WMIC."""
    comando_wmic = 'wmic product where "name like \'%FortiClient%\'" call uninstall'
    returncode = subprocess.call(comando_wmic, shell=True)
    return returncode


def main():
    if not verificar_admin():
        print("❌ Este script precisa ser executado como Administrador!")
        input("Pressione ENTER para sair...")
        sys.exit(1)

    print("✅ Executando como Administrador")

    # Senhas possíveis
    senhas = ["7eS*n[Q47A2!", "Cor5Rml@as!x"]

    for senha in senhas:
        executar_fortiesnac(senha)
        time.sleep(10)  # Aguarda o FortiESNAC processar

    print("Processo concluído.")
    input("Pressione ENTER para sair...")


if __name__ == "__main__":
    main()
    