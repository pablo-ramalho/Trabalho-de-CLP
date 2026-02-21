from typing import Literal, Sequence, cast
import ctypes
import sys
import matplotlib
matplotlib.use('qt5agg')  # Backend interativo com PyQt5
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt

WaveType = Literal["square", "sawtooth", "triangle"]

# Carrega a biblioteca C compartilhada
def load_fourier_library():
	"""Load the compiled C library for Fourier calculations."""
	if sys.platform == "win32":
		lib_name = "libcalculo.dll"
	else:
		lib_name = "./libcalculo.so"
	
	try:
		lib = ctypes.CDLL(lib_name)
		return lib
	except OSError as e:
		print(f"Erro ao carregar biblioteca C: {e}")
		print("Certifique-se de compilar com: make compilar_lib")
		sys.exit(1)

# Carrega a biblioteca C
fourier_lib = load_fourier_library()

# Define as assinaturas das funções C
fourier_lib.squareWave.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_double]
fourier_lib.squareWave.restype = ctypes.c_double

fourier_lib.sawtoothWave.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_double]
fourier_lib.sawtoothWave.restype = ctypes.c_double

fourier_lib.triangleWave.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_double]
fourier_lib.triangleWave.restype = ctypes.c_double

def parse_args(argv: Sequence[str]) -> tuple[int, float, WaveType, str | None]:
    # Sem parametros: usar valores padrao pedidos pelo enunciado.
    if len(argv) == 1:
        return 10, 1.0, "square", None

    # Com parametros, exigimos pelo menos N e A.
    if len(argv) < 3:
        raise ValueError("Uso: python interface.py N A [wave] [--save arquivo.png]")

    # sys.argv[1] -> N (numero de termos), sys.argv[2] -> A (amplitude).
    n_terms = int(argv[1])
    amplitude = float(argv[2])
    wave = argv[3].lower() if len(argv) >= 4 else "square"
    save_path = None

    # O tipo de onda deve ser um dos valores aceitos.
    if wave not in {"square", "sawtooth", "triangle"}:
        raise ValueError("wave deve ser square, sawtooth, ou triangle")

    # Verifica se há argumento --save
    if len(argv) >= 5 and argv[4] == "--save":
        if len(argv) >= 6:
            save_path = argv[5]
        else:
            raise ValueError("--save requer um caminho de arquivo")

    return n_terms, amplitude, cast(WaveType, wave), save_path


def fourier_approximation(
	x_values: npt.NDArray[np.float64],
	n_terms: int,
	amplitude: float,
	wave: WaveType,
) -> npt.NDArray[np.float64]:
	"""
	Compute Fourier approximation using the C library.
	
	For each time value t in x_values, calls the corresponding C function
	to compute f(t) and returns an array of results.
	"""
	output = np.zeros_like(x_values)
	
	# Select which C function to call based on wave type
	if wave == "square":
		c_func = fourier_lib.squareWave
	elif wave == "sawtooth":
		c_func = fourier_lib.sawtoothWave
	else:  # triangle
		c_func = fourier_lib.triangleWave
	
	# Call C function for each time value t
	for i, t in enumerate(x_values):
		output[i] = c_func(ctypes.c_int(n_terms), ctypes.c_int(int(amplitude)), ctypes.c_double(t))
	
	return output
def main() -> None:
	# Faz o parse da linha de comando e valida entradas.
	try:
		n_terms, amplitude, wave, save_path = parse_args(sys.argv)
	except ValueError as exc:
		print(exc)
		sys.exit(1)

	# Grade de x em 0..2pi para desenhar um periodo da onda.
	x_values = np.linspace(0, 2 * np.pi, 1000)
	y_values = fourier_approximation(x_values, n_terms, amplitude, wave)

	# Configura a figura com fundo preto e margem estreita.
	fig, ax = plt.subplots(figsize=(10, 5))  # type: ignore[reportUnknownMemberType]
	fig.patch.set_facecolor("#000000")
	ax.set_facecolor("#000000")

	# Linha da aproximacao: cor definida para bom contraste.
	ax.plot(x_values, y_values, color="#00d2ff", linewidth=2.0)  # type: ignore[reportUnknownMemberType]
	ax.set_title(f"Fourier - {wave.upper()} (N={n_terms}, A={amplitude})", color="#ffffff", pad=8)  # type: ignore[reportUnknownMemberType]

	# Estilo claro para eixos e grade em fundo escuro.
	ax.tick_params(colors="#ffffff")  # type: ignore[reportUnknownMemberType]
	for spine in ax.spines.values():
		spine.set_color("#ffffff")

	ax.grid(color="#1a1a1a", linestyle="--", linewidth=0.6, alpha=0.8)  # type: ignore[reportUnknownMemberType]
	fig.subplots_adjust(left=0.04, right=0.99, top=0.92, bottom=0.08)

	# Salva ou exibe
	if save_path:
		plt.savefig(save_path, facecolor="#000000", dpi=100)  # type: ignore[reportUnknownMemberType]
		print(f"✓ Gráfico salvo em: {save_path}")
	else:
		plt.show()  # type: ignore[reportUnknownMemberType]

if __name__ == "__main__":
    main()
