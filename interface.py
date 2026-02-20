from typing import Literal, Sequence, cast

import sys

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt

WaveType = Literal["square", "sawtooth", "triangle"]

def parse_args(argv: Sequence[str]) -> tuple[int, float, WaveType]:
	# Sem parametros: usar valores padrao pedidos pelo enunciado.
	if len(argv) == 1:
		return 10, 1.0, "square"

	# Com parametros, exigimos pelo menos N e A.
	if len(argv) < 3:
		raise ValueError("Uso: python interface.py N A [wave]")

	# sys.argv[1] -> N (numero de termos), sys.argv[2] -> A (amplitude).
	n_terms = int(argv[1])
	amplitude = float(argv[2])
	wave = argv[3].lower() if len(argv) >= 4 else "square"

	# O tipo de onda deve ser um dos valores aceitos.
	if wave not in {"square", "sawtooth", "triangle"}:
		raise ValueError("wave deve ser square, sawtooth, ou triangle")

	return n_terms, amplitude, cast(WaveType, wave)


def fourier_approximation(
	x_values: npt.NDArray[np.float64],
	n_terms: int,
	amplitude: float,
	wave: WaveType,
) -> npt.NDArray[np.float64]:
	# Cada tipo de onda usa a serie de Fourier correspondente.
	if wave == "square":
		# Onda quadrada: apenas harmonicos impares, amplitude 4/pi.
		n = np.arange(1, n_terms + 1, 2)
		terms = np.sin(np.outer(n, x_values)) / n[:, None]
		return (4 * amplitude / np.pi) * terms.sum(axis=0)

	if wave == "sawtooth":
		# Onda dente de serra: todos os harmonicos com sinal alternado.
		n = np.arange(1, n_terms + 1)
		signs = (-1) ** (n + 1)
		terms = signs[:, None] * np.sin(np.outer(n, x_values)) / n[:, None]
		return (2 * amplitude / np.pi) * terms.sum(axis=0)

	# Onda triangular: harmonicos impares com sinais alternados e 1/n^2.
	n = np.arange(1, n_terms + 1, 2)
	signs = (-1) ** ((n - 1) // 2)
	terms = signs[:, None] * np.sin(np.outer(n, x_values)) / (n[:, None] ** 2)
	return (8 * amplitude / (np.pi ** 2)) * terms.sum(axis=0)


def main() -> None:
	# Faz o parse da linha de comando e valida entradas.
	try:
		n_terms, amplitude, wave = parse_args(sys.argv)
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
	ax.set_title("Fourier", color="#ffffff", pad=8)  # type: ignore[reportUnknownMemberType]

	# Estilo claro para eixos e grade em fundo escuro.
	ax.tick_params(colors="#ffffff")  # type: ignore[reportUnknownMemberType]
	for spine in ax.spines.values():
		spine.set_color("#ffffff")

	ax.grid(color="#1a1a1a", linestyle="--", linewidth=0.6, alpha=0.8)  # type: ignore[reportUnknownMemberType]
	fig.subplots_adjust(left=0.04, right=0.99, top=0.92, bottom=0.08)

	plt.show()  # type: ignore[reportUnknownMemberType]


if __name__ == "__main__":
	main()

