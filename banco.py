import sqlite3
import os

class BancoDados:
    def __init__(self):
  

        self.conexao = sqlite3.connect("worldgame.db")
        self.cursor = self.conexao.cursor()
        self.criar_tabela()

    def criar_tabela(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ranking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                jogador TEXT NOT NULL,
                pontuacao REAL NOT NULL,
                data_hora DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conexao.commit()

    def salvar_recorde(self, nome, pontos):
        self.cursor.execute(
            "INSERT INTO ranking (jogador, pontuacao) VALUES (?, ?)", 
            (nome, pontos)
        )
        self.conexao.commit()

    def obter_top_5(self):
        self.cursor.execute("SELECT jogador, pontuacao FROM ranking ORDER BY pontuacao DESC LIMIT 5")
        return self.cursor.fetchall()
