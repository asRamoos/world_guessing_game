import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

from banco import BancoDados
from web import ServicoAPI
from calculos import calcular_pontos

class JogoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("World Guessing Game")
        self.api = ServicoAPI()
        self.db = BancoDados()
        
        self.pais_atual = None
        self.tempo_inicio = None
        
        self.configurar_interface()
        self.nova_rodada()

    def configurar_interface(self):
        tk.Label(self.root, text="DICA (CAPITAL):", font=("Arial", 10, "bold")).pack(pady=5)
        self.lbl_dica = tk.Label(self.root, text="", font=("Arial", 14), fg="blue")
        self.lbl_dica.pack()

        tk.Label(self.root, text="Seu Palpite:").pack()
        self.ent_palpite = tk.Entry(self.root)
        self.ent_palpite.pack()

        tk.Label(self.root, text="Seu Nome:").pack()
        self.ent_nome = tk.Entry(self.root)
        self.ent_nome.pack()

        tk.Button(self.root, text="CHUTAR!", command=self.processar_palpite, bg="green", fg="white").pack(pady=10)

        self.tree = ttk.Treeview(self.root, columns=("Jogador", "Pontos"), show="headings", height=5)
        self.tree.heading("Jogador", text="Jogador")
        self.tree.heading("Pontos", text="Pontuação")
        self.tree.pack(pady=10)
        self.atualizar_ranking_visual()

    def nova_rodada(self):
        self.pais_atual = self.api.obter_pais_aleatorio()
        if self.pais_atual:
            cap = self.pais_atual['capital']
            dica = cap if isinstance(cap, str) else cap
            self.lbl_dica.config(text=dica)
            
            self.tempo_inicio = datetime.now()
            self.ent_palpite.delete(0, tk.END)

    def processar_palpite(self):
        if self.pais_atual is None:
            messagebox.showerror("Erro", "O jogo não carregou o país.")
            return

        palpite = self.ent_palpite.get().strip().lower()
        nome_jogador = self.ent_nome.get().strip() or "Anonimo"
        resposta_correta = str(self.pais_atual['nome']).strip().lower()
        
        if palpite == resposta_correta:
            pontos, tempo = calcular_pontos(self.tempo_inicio, self.pais_atual['populacao'])
            
            self.db.salvar_recorde(nome_jogador, pontos)
            
            messagebox.showinfo("Acertou!", f"Pontos: {pontos}\nTempo: {tempo}s")
            self.atualizar_ranking_visual()
            self.nova_rodada()
        else:
            messagebox.showerror("Erro", f"Tente novamente! Era: {resposta_correta}")

    def atualizar_ranking_visual(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for linha in self.db.obter_top_5(): 
            self.tree.insert("", tk.END, values=linha)

if __name__ == "__main__":
    root = tk.Tk()
    app = JogoApp(root)
    root.mainloop()
