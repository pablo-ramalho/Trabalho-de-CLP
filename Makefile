N ?=
A ?=

instalar_dependencias:
	pip install matplotlib
	pip install numpy
	pip install pyinstaller
	pip install PyQt5

compilar_lib:
	gcc -shared -fPIC -lm -o libcalculo.so calculo.c

instalar_windows:
	gcc -shared -lm -o libcalculo.dll calculo.c

gerar_windows: interface.py
	pyinstaller --onefile --noconsole --name "fourier.exe" --distpath . interface.py

executar_windows: fourier.exe
	.\fourier.exe $(N) $(A)

gerar_linux: interface.py
	pyinstaller --onefile --noconsole --name "fourier.out" --distpath . interface.py

executar_linux: compilar_lib
	python interface.py $(N) $(A)
