from typing import Literal, Sequence, cast
import ctypes
import os
import sys
import matplotlib
matplotlib.use('qt5agg')  # Backend interativo com PyQt5
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import numpy.typing as npt

WaveType = Literal["square", "sawtooth", "triangle"]

# Carregamento da Biblioteca (Mantendo a correção do Windows)
def load_fourier_library():
    """Load the compiled C library for Fourier calculations."""
    
    # Lógica para encontrar o caminho correto (seja rodando script ou executável)
    if getattr(sys, 'frozen', False):
        # Se estiver rodando como executável compilado pelo PyInstaller (--onefile)
        # Os arquivos são descompactados em sys._MEIPASS
        base_path = sys._MEIPASS
    else:
        # Se estiver rodando como script Python normal
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    if sys.platform == "win32":
        lib_name = "libcalculo.dll"
    else:
        lib_name = "libcalculo.so"
        
    lib_path = os.path.join(base_path, lib_name)
    
    try:
        lib = ctypes.CDLL(lib_path)
        return lib
    except OSError as e:
        print(f"Erro ao carregar biblioteca C em '{lib_path}': {e}")
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
        return 1, 1.2, "square", None

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
    phase_shift: float = 0.0 # Novo parâmetro para deslocar a onda
) -> npt.NDArray[np.float64]:
    """
	Compute Fourier approximation using the C library.
	
	For each time value t in x_values, calls the corresponding C function
	to compute f(t) and returns an array of results.
	"""
    
    output = np.zeros_like(x_values)
    
    # Seleção da função C com base no tipo de onda
    if wave == "square":
        c_func = fourier_lib.squareWave
    elif wave == "sawtooth":
        c_func = fourier_lib.sawtoothWave
    else: # triangle
        c_func = fourier_lib.triangleWave
    
    # Passamos (t + phase_shift) para a função C.
    # Isso calcula a onda como se ela estivesse deslocada no tempo.
    for i, t in enumerate(x_values):
        time_point = t + phase_shift
        output[i] = c_func(ctypes.c_int(n_terms), ctypes.c_int(int(amplitude)), ctypes.c_double(time_point))
    
    return output

def main() -> None:
    # Faz o parse da linha de comando e valida entradas.
    try:
        n_terms, amplitude, wave, save_path = parse_args(sys.argv)
    except ValueError as exc:
        print(exc)
        sys.exit(1)

    # Aumentei a resolução para 2000 pontos para ficar mais fluido
    x_values = np.linspace(0, 4 * np.pi, 2000) 

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor("#000000")
    ax.set_facecolor("#000000")
    ax.tick_params(colors="#ffffff")
    for spine in ax.spines.values():
        spine.set_color("#ffffff")
    ax.grid(color="#1a1a1a", linestyle="--", linewidth=0.6, alpha=0.8)
    
    # Ajusta limites Y com uma margem
    ax.set_ylim(-amplitude * 1.5, amplitude * 1.5)
    ax.set_xlim(0, 4 * np.pi) # Mostra 2 períodos da onda
    
    fig.subplots_adjust(left=0.05, right=0.99, top=0.90, bottom=0.08)

    if save_path:
        # Modo estático original
        y_values = fourier_approximation(x_values, n_terms, amplitude, wave)
        ax.plot(x_values, y_values, color="#00d2ff", linewidth=2.0)
        ax.set_title(f"Fourier - {wave.upper()} (N={n_terms}, A={amplitude})", color="#ffffff", pad=8)
        plt.savefig(save_path, facecolor="#000000", dpi=100)
        print(f"✓ Gráfico salvo em: {save_path}")
    else:
        # Modo Animação "Running"
        print("Iniciando animação... Pressione [ESPAÇO] para Pausar.")
        
        line, = ax.plot([], [], color="#00d2ff", linewidth=2.0)
        
        # Texto informativo sobre N e Velocidade
        info_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, color="#ffffff", fontsize=10)

        def init():
            line.set_data([], [])
            info_text.set_text('')
            return line, info_text

        def update(frame):
            # Lógica da Animação:
            # 1. Faz a onda correr (Phase Shift)
            # frame * 0.1 controla a velocidade do movimento
            phase = frame * 0.05
            
            # 2. Mantém o N constante
            current_n = n_terms
            
            # Calcula a onda com deslocamento
            y = fourier_approximation(x_values, current_n, amplitude, wave, phase_shift=phase)
            
            line.set_data(x_values, y)
            
            # Atualiza título e texto
            ax.set_title(f"Fourier - {wave.upper()}", color="#ffffff", pad=8, fontsize=14)
            info_text.set_text(f"Harmônicas (N): {current_n}\nDeslocamento: {phase:.1f}")
            
            return line, info_text

        # frames=None cria um loop infinito
        # interval=20 deixa a animação bem rápida (60fps approx)
        anim = FuncAnimation(fig, update, frames=None, init_func=init, interval=20, blit=False, cache_frame_data=False)

        # Controle de Pausa
        anim_running = True
        def on_key(event):
            nonlocal anim_running
            if event.key == ' ':
                if anim_running:
                    anim.event_source.stop()
                    anim_running = False
                else:
                    anim.event_source.start()
                    anim_running = True

        fig.canvas.mpl_connect('key_press_event', on_key)
        plt.show()

if __name__ == "__main__":
    main()
