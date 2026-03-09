import winreg
import subprocess

REG_PATHS = [
    r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
    r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
]


def get_forticlient_uninstall():
    for reg_path in REG_PATHS:

        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)

            for i in range(0, winreg.QueryInfoKey(key)[0]):
                subkey_name = winreg.EnumKey(key, i)

                try:
                    subkey = winreg.OpenKey(key, subkey_name)

                    display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]

                    if "FortiClient" in display_name:

                        uninstall_string = winreg.QueryValueEx(subkey, "UninstallString")[0]

                        return uninstall_string

                except:
                    continue

        except:
            continue

    return None


def uninstall_forticlient():

    uninstall_cmd = get_forticlient_uninstall()

    if not uninstall_cmd:
        print("FortiClient não encontrado.")
        return

    print("FortiClient encontrado.")
    print("Comando:", uninstall_cmd)

    if "msiexec" in uninstall_cmd.lower():
        uninstall_cmd = uninstall_cmd.replace("/I", "/X")
        cmd = f'{uninstall_cmd} /qn /norestart'
    else:
        cmd = f'{uninstall_cmd} /quiet /norestart'

    print("Executando desinstalação...")

    subprocess.run(cmd, shell=True)

    print("Processo finalizado.")


if __name__ == "__main__":
    uninstall_forticlient()