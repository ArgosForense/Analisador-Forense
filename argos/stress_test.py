import threading
import requests
import time
import random

# Para realizar os testes desative as portas no docker-compose.yml
# Comentando as linhas 76-79 que expõem a porta 5140 do servio de gerador de logs.

API_URL = "http://localhost:5000/search"
TERMOS = ["Login", "Erro", "192.168", "Falha", "Admin"]
NUM_THREADS = 20  # 20 usuários pesquisando ao mesmo tempo
DURACAO_SEGUNDOS = 60 # Teste dura 1 minuto

def realizar_busca(id):
    start_time = time.time()
    while time.time() - start_time < DURACAO_SEGUNDOS:
        termo = random.choice(TERMOS)
        try:
            # Medir tempo de resposta
            t0 = time.time()
            resp = requests.get(f"{API_URL}?q={termo}")
            latencia = time.time() - t0
            
            status = "✅" if resp.status_code == 200 else f"❌ {resp.status_code}"
            print(f"[User {id}] Busca: '{termo}' | Status: {status} | Tempo: {latencia:.2f}s")
            
            # Pequena pausa humana
            time.sleep(random.uniform(0.5, 2.0))
        except Exception as e:
            print(f"[User {id}] 💥 Erro de conexão: {e}")

print(f"🔥 INICIANDO STRESS TEST ({NUM_THREADS} threads por {DURACAO_SEGUNDOS}s)...")

threads = []
for i in range(NUM_THREADS):
    t = threading.Thread(target=realizar_busca, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("🏁 Teste finalizado.")