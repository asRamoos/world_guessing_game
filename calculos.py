import math
from datetime import datetime

def calcular_pontos(tempo_inicio, populacao):
    tempo_fim = datetime.now()
    tempo_gasto = (tempo_fim - tempo_inicio).total_seconds()
    tempo_gasto = max(tempo_gasto, 1) 

    pontos_base = 1000 / tempo_gasto
    divisor_bonus = math.log10(populacao + 10) 
    bonus_dificuldade = 500 / divisor_bonus
    
    pontuacao_final = round(pontos_base + bonus_dificuldade, 2)
    return pontuacao_final, round(tempo_gasto, 2)
