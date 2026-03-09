import os
import subprocess
import time
import sys
import pyautogui
import winreg


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


def desinstalar_forticlient_wmic():
    """Desinstala o FortiClient usando WMIC."""
    comando_wmic = 'wmic product where "name like \'%FortiClient%\'" call uninstall'
    returncode = subprocess.call(comando_wmic, shell=True)
    return returncode


# Caminhos do registro para buscar programas instalados
REG_PATHS = [
    r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
    r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
]


def get_forticlient_uninstall():
    """Busca o comando de desinstalação do FortiClient no registro do Windows."""
    for reg_path in REG_PATHS:
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)

            for i in range(0, winreg.QueryInfoKey(key)[0]):
                subkey_name = winreg.EnumKey(key, i)

                try:
                    subkey = winreg.OpenKey(key, subkey_name)
                    display_name = winreg.QueryValueEx(
                        subkey, "DisplayName")[0]

                    if "FortiClient" in display_name:
                        uninstall_string = winreg.QueryValueEx(
                            subkey, "UninstallString")[0]
                        return uninstall_string

                except:
                    continue

        except:
            continue

    return None


def desinstalar_forticlient_registro():
    """Desinstala o FortiClient usando o comando encontrado no registro."""
    uninstall_cmd = get_forticlient_uninstall()

    if not uninstall_cmd:
        print("❌ FortiClient não encontrado no registro.")
        return False

    print("✅ FortiClient encontrado no registro.")
    print(f"📋 Comando: {uninstall_cmd}")

    # Ajusta o comando para desinstalação silenciosa
    if "msiexec" in uninstall_cmd.lower():
        uninstall_cmd = uninstall_cmd.replace("/I", "/X")
        cmd = f'{uninstall_cmd} /qn /norestart'
    else:
        cmd = f'{uninstall_cmd} /quiet /norestart'

    print("🔄 Executando desinstalação via registro...")
    subprocess.run(cmd, shell=True)
    print("✅ Processo de desinstalação via registro finalizado.")
    return True


def main():
    """Função principal que coordena todo o processo de desinstalação."""
    print("=" * 60)
    print("SCRIPT DE DESINSTALAÇÃO DO FORTICLIENT")
    print("=" * 60)

    # Verifica privilégios de administrador
    if not verificar_admin():
        print("❌ Este script precisa ser executado como Administrador!")
        input("Pressione ENTER para sair...")
        sys.exit(1)

    print("✅ Executando como Administrador\n")

    # Etapa 1: Tentar desbloquear com FortiESNAC
    print("=" * 60)
    print("ETAPA 1: Desbloqueando FortiClient com FortiESNAC")
    print("=" * 60)

    senhas = ["7eS*n[Q47A2!", "Cor5Rml@as!x"]

    for idx, senha in enumerate(senhas, 1):
        print(f"🔑 Tentando senha {idx}...")
        try:
            executar_fortiesnac(senha)
            time.sleep(10)  # Aguarda o FortiESNAC processar
            print(f"✅ Senha {idx} processada.")
        except Exception as e:
            print(f"⚠️ Erro ao processar senha {idx}: {e}")

    print("\n" + "=" * 60)
    print("ETAPA 2: Desinstalando FortiClient via Registro")
    print("=" * 60)

    # Etapa 2: Desinstalar via registro
    sucesso_registro = desinstalar_forticlient_registro()

    # Etapa 3: Fallback para WMIC se necessário
    if not sucesso_registro:
        print("\n" + "=" * 60)
        print("ETAPA 3: Tentando desinstalação via WMIC (fallback)")
        print("=" * 60)
        print("🔄 Executando desinstalação via WMIC...")
        desinstalar_forticlient_wmic()
        print("✅ Processo de desinstalação via WMIC finalizado.")

    print("\n" + "=" * 60)
    print("✅ PROCESSO COMPLETO FINALIZADO")
    print("=" * 60)
    input("\nPressione ENTER para sair...")


if __name__ == "__main__":
    main()
