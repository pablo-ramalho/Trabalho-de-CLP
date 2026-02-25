N ?=
A ?=
WAVE ?=

instalar_dependencias:
	pip install matplotlib
	pip install numpy
	pip install pyinstaller
	pip install PyQt5

# --- Compilação C ---
libcalculo.so: calculo.c
	gcc -shared -fPIC -lm -o libcalculo.so calculo.c

libcalculo.dll: calculo.c
	gcc -shared -lm -o libcalculo.dll calculo.c

# --- Executáveis (Windows) ---
# --add-binary "src;dest" pega a DLL e coloca na raiz do executável
fourier.exe: interface.py libcalculo.dll
	pyinstaller --onefile --noconsole --name "fourier.exe" --add-binary "libcalculo.dll;." --distpath . interface.py

run_windows: fourier.exe
	.\fourier.exe $(N) $(A) $(WAVE)

# --- Executáveis (Linux) ---
# --add-binary "src:dest" (nota o dois pontos ao invés de ponto e vírgula)
fourier.out: interface.py libcalculo.so
	pyinstaller --onefile --noconsole --name "fourier.out" --add-binary "libcalculo.so:." --distpath . interface.py

run_linux: fourier.out
	./fourier.out $(N) $(A) $(WAVE)

# --- Limpeza ---
limpar_windows:
	-cmd /c del /Q libcalculo.dll fourier.exe *.spec
	-cmd /c rmdir /S /Q build __pycache__ 
	@echo "Limpeza do Windows Concluida"

limpar_linux:
	rm -rf libcalculo.so fourier.out build/ __pycache__/ *.spec
	@echo "Limpeza do Linux concluida"
