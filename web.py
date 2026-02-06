import requests
import random

class ServicoAPI:
    def __init__(self):
        self.url = "https://restcountries.com/v3.1/all?fields=name,capital"

    def obter_pais_aleatorio(self):
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(self.url, headers=headers, timeout=10)
            
            if res.status_code == 200:
                paises = res.json()
               
                pais = random.choice(paises)
                
                return {
                    "nome": str(pais['name']['common']),
                    "capital": str(pais.get('capital', ["Sem Capital"])[0]),
                    "populacao": int(pais.get('population', 1))
                }
        except Exception as e:
            print(f"Erro ao carregar API: {e}")
        return {
            "nome": "Brasil",
            "capital": "Brasilia",
            "populacao": 214000000
        }

if __name__ == "__main__":
    api = ServicoAPI()
    print(api.obter_pais_aleatorio())
