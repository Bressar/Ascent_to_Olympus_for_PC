from cx_Freeze import setup, Executable

build_options = {
    'packages': ['pygame', 'customtkinter', 'tkinter', 'PIL', 'webbrowser', 'random', 'sqlite3', 'os', 'ctypes', 'sys' ],  # Adicione aqui as bibliotecas necessárias
    'include_files': [
        'fonts/',  # Incluir a pasta fonts
        'images/',  # Incluir a pasta images
        'imagens_casas/',  # Incluir a pasta imagens_casas
        'music/'  # Incluir a pasta music
    ]
}

setup(
    name="AscentToOlympus",
    version="1.0",
    description="Jogo Grécia Antiga",
    options={"build_exe": build_options},
    executables=[Executable("app.py", base="Win32GUI")]
)

# bash: »»   python setup.py build
