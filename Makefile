N ?=
A ?=
WAVE ?=

instalar_dependencias:
	pip install matplotlib
	pip install numpy
	pip install pyinstaller
	pip install PyQt5

libcalculo.so: calculo.c
	gcc -shared -fPIC -lm -o libcalculo.so calculo.c

libcalculo.dll: calculo.c
	gcc -shared -lm -o libcalculo.dll calculo.c

fourier.exe: interface.py
	pyinstaller --onefile --noconsole --name "fourier.exe" --distpath . interface.py

run_windows: fourier.exe
	.\fourier.exe $(N) $(A) $(WAVE)

fourier.out: interface.py
	pyinstaller --onefile --noconsole --name "fourier.out" --distpath . interface.py

run_linux: fourier.out
	./fourier.out $(N) $(A) $(WAVE)

limpar_windows:
	-cmd /c del /Q libcalculo.dll fourier.exe *.spec
	-cmd /c rmdir /S /Q build __pycache__ 
	@echo "Limpeza do Windows Concluida"

limpar_linux:
	rm -rf libcalculo.so fourier.out build/ __pycache__/ *.spec
	@echo "Limpeza do Linux concluida"
