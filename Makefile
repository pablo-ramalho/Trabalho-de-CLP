N ?=
A ?=

instalar_dependencias:
	pip install matplotlib
	pip install numpy
	pip install pyinstaller

gerar_windows: interface.py
	pyinstaller --onefile --noconsole --name "fourier.exe" --distpath . interface.py

executar_windows: fourier.exe
	.\fourier.exe $(N) $(A)

gerar_linux: interface.py
	pyinstaller --onefile --noconsole --name "fourier.out" --distpath . interface.py

executar_linux: fourier
	./fourier $(N) $(A)