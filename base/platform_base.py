import platform

def system_plat():
    "判断是wins还是ios,用于命令行差异"
    plat =platform.system()
    if plat == "Windows":
        pass
    else:
        pass