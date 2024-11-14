import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import sys
from suaBibSignal import signalMeu
import soundfile as sf
from scipy import signal
from math import *

import numpy as np
from scipy import signal

def demodulacaoAM(dados, fs):
    f_c = 14000 
    A_c = 1
    duration = 6  

    lista_tempo = np.linspace(0, duration, len(dados), endpoint=False)

    C = A_c * np.cos(2 * np.pi * f_c * lista_tempo)

    S = dados * C

    # ----------------- Filtro passa baixa ------------------
    cutoff_hz = 3000  # Frequência de corte
    nyq_rate = fs / 2  # Frequência de Nyquist
    normal_cutoff = cutoff_hz / nyq_rate  # Normalizar a frequência de corte

    # Definir ordem e frequências do filtro Butterworth
    ordem = 8  # Ordem do filtro (ajustável para obter a resposta desejada)
    b, a = signal.butter(ordem, normal_cutoff, btype='low', analog=False)

    # Filtrar o sinal demodulado
    sinal_demodulado = signal.filtfilt(b, a, S)  # filtfilt aplica o filtro sem atrasos de fase

    return sinal_demodulado



def main():

    signal2 = signalMeu()

    data, fs = sf.read('Projeto 8/gravacao_modulada.wav')

    duration = 6

    sd.wait()
    sd.play(data, samplerate=fs)
    sd.wait()

    # Plota o FFT do sinal modulado
    # signal2.plotFFT(data, fs)
    # plt.legend(["Sinal Modulado"])
    # plt.show()

    # Demodula o sinal
    sinal_demodulado = demodulacaoAM(data, fs)

    # ------- Normalizando o sinal filtrado ----------------

    max_value = np.abs(sinal_demodulado).max()

    audioNormalizado = sinal_demodulado / max_value

    sf.write('Projeto 8/gravacao_demodulada.wav', audioNormalizado, fs)
    print("Arquivo demodulado salvo com sucesso!")

    # Gráfico 6: Sinal de áudio demodulado – domínio do tempo
    # plt.figure()
    plt.plot(sinal_demodulado)
    plt.title("Gráfico 6: Sinal de Áudio Demodulado - Domínio do Tempo")
    plt.xlabel("Amostras")
    plt.ylabel("Amplitude")

    # Gráfico 7: Sinal de áudio demodulado – domínio da frequência
    # plt.figure()
    signal2.plotFFT(sinal_demodulado, fs)
    plt.legend(["Sinal Demodulado"])
    plt.title("Gráfico 7: Sinal de Áudio Demodulado - Domínio da Frequência")

    # Gráfico 8: Sinal de áudio demodulado e filtrado – domínio da frequência
    # Este gráfico é o mesmo que o Gráfico 2, pois `sinal_demodulado` já está filtrado.
    # plt.figure()
    signal2.plotFFT(sinal_demodulado, fs)
    plt.legend(["Sinal Demodulado e Filtrado"])
    plt.title("Gráfico 8: Sinal de Áudio Demodulado e Filtrado - Domínio da Frequência")

    plt.show()

    sd.wait()
    sd.play(audioNormalizado, samplerate=fs)
    sd.wait()




if __name__ == "__main__":
    main()



# Estou com duvida nos gráficos f, g, h