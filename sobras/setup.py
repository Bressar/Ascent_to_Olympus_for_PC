from distutils.core import setup
import py2exe

setup(
    console=['app.py'],  # Arquivo Python principal
    data_files=[('fonts', ['fonts/']),  # Pasta fonts
                ('images', ['images/']),  # Pasta images
                ('imagens_casas', ['imagens_casas/']),  # Pasta imagens_casas
                ('music', ['music/'])]  # Pasta music
)
pyinstaller --onefile --add-data "fonts;fonts" app.py
