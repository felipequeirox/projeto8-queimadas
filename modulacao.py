import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import sys
from suaBibSignal import signalMeu
import soundfile as sf
from scipy import signal
from math import *


def modulacaoAM(dados, fs):
    f_c = 14000
    A_c = 1
    A_m = 1

    duration = 6

    lista_tempo = np.linspace(0, duration, len(dados), endpoint=False)

    # m = np.zeros(len(dados))
    # C = np.zeros(len(dados))
    # S = np.zeros(len(dados))

    C = A_c * np.cos(2 * np.pi * f_c * lista_tempo)
    S = (dados) * (C)
    # for t in lista_tempo:
    #     C[t] = A_c * cos(2 * pi * f_c * t)
    #     S[t] = (dados[t])*(C[t]) #Não vamos mandar a portafora junto com o sinal ent será 0 a cosntante, ent some o C[t]
    
    return S



def main():

    signal2 = signalMeu()

    data, fs = sf.read('Projeto 8/gravacao.wav')

    duration = 6

    # Gerar Gráfico 1: Sinal de áudio original normalizado – domínio do tempo
    plt.figure()
    plt.plot(data)
    plt.title("Gráfico 1: Sinal de Áudio Original - Domínio do Tempo")
    plt.xlabel("Amostras")
    plt.ylabel("Amplitude")


    # ----------------- Aplicando filtro passa-baixa Butterworth ------------------
    cutoff_hz = 3000  # Frequência de corte do filtro passa-baixa
    nyq_rate = fs / 2  # Frequência de Nyquist
    normal_cutoff = cutoff_hz / nyq_rate  # Normaliza a frequência de corte em relação à Nyquist

    # Definir a ordem e os coeficientes do filtro Butterworth
    ordem = 8  # Ordem do filtro (ajustável)
    b, a = signal.butter(ordem, normal_cutoff, btype='low', analog=False)

    # Aplicar o filtro Butterworth ao áudio
    yFiltrado = signal.filtfilt(b, a, data)  # filtfilt aplica o filtro sem introduzir atraso de fase

    # Gráfico 2: Sinal de áudio filtrado – domínio do tempo
    plt.figure()
    plt.plot(yFiltrado)
    plt.title("Gráfico 2: Sinal de Áudio Filtrado – Domínio do Tempo")
    plt.xlabel("Amostras")
    plt.ylabel("Amplitude")

    # Gerar o vetor de tempo
    # t = np.linspace(0, duration, len(dados), endpoint=False)

    # ------- Normalizando o sinal filtrado ----------------

    max_value = np.abs(yFiltrado).max()

    audioNormalizado = yFiltrado / max_value

    sf.write('Projeto 8/gravacao_filtrada.wav', audioNormalizado, fs)
    print("Arquivo filtrado salvo com sucesso!")

    sd.wait()
    sd.play(yFiltrado, samplerate=fs)
    sd.wait()

    # ------------------------------ Modulação ----------------------------
    data_filtrado, fs_filtrado = sf.read('Projeto 8/gravacao_filtrada.wav')
    resultado_modulado = modulacaoAM(data_filtrado, fs_filtrado)

    # Gráfico 4: Sinal de áudio modulado – domínio do tempo
    plt.figure()
    plt.plot(resultado_modulado)
    plt.title("Gráfico 4: Sinal de Áudio Modulado – Domínio do Tempo")
    plt.xlabel("Amostras")
    plt.ylabel("Amplitude")

    # Normalizando o sinal modulado
    max_resultado = np.abs(resultado_modulado).max()
    audioModulado = resultado_modulado / max_resultado

    sf.write('Projeto 8/gravacao_modulada.wav', audioModulado, fs_filtrado)
    print("Arquivo Modulado salvo com sucesso!")

    sd.wait()
    sd.play(resultado_modulado, samplerate=fs_filtrado)
    sd.wait()



    # Plota o FFT do sinal original
    signal2.plotFFT(data, fs)
    plt.legend(["Sinal Original"])

    # Plota o FFT do sinal filtrado - Gráfico 3
    signal2.plotFFT(yFiltrado, fs)
    plt.legend(["Sinal Filtrado"])

    # Gráfico 5: Sinal de áudio modulado – domínio da frequência (Fourier)
    signal2.plotFFT(resultado_modulado, fs_filtrado)
    plt.legend(["Sinal Modulado"])

    plt.show()



if __name__ == "__main__":
    main()


# Estou com dúvida no tópico 8