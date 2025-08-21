from elasticsearch import Elasticsearch
from datetime import datetime, timedelta

#Conexão com o Elasticsearch
try:
    es = Elasticsearch(
        hosts=[{'host': 'localhost', 'port': 9200, 'scheme': 'http'}]
    )
    if not es.ping():
        raise ConnectionError("Não foi possível estabelecer a conexão.")
    print("Conexão estabelecida com sucesso!")
except ConnectionError as e:
    print(e)
    exit()

# Índice onde guardaremos nossos logs
INDEX_NAME = 'forensic_logs'

# Endpoint de API
def indexar_log(log_data):
    """Adiciona um documento de log."""
    try:
        response = es.index(index=INDEX_NAME, document=log_data)
        print(f"Log indexado com sucesso. ID: {response['_id']}")
    except Exception as e:
        print(f"Erro ao indexar log: {e}")


def buscar_tentativas_de_login_falhas(ip_suspeito, time_window_hours=24):
    """
    Busca por tentativas de login falhas de um IP específico
    em uma janela de tempo.
    """
    print(f"\n--- Iniciando análise: buscando falhas de login do IP {ip_suspeito} ---")

    start_time = datetime.utcnow() - timedelta(hours=time_window_hours)

    query = {
        "bool": {
            "must": [
                { "match": { "event.action": "authentication_failure" } },
                { "match": { "source.ip": ip_suspeito } }
            ],
            "filter": [
                { "range": { "@timestamp": { "gte": start_time.isoformat() } } }
            ]
        }
    }

    try:
        results = es.search(index=INDEX_NAME, query=query)
        
        hits = results['hits']['hits']
        num_hits = len(hits)

        if num_hits > 0:
            print(f"Resultados encontrados: {num_hits} tentativas de login falhas.")
            for hit in hits:
                log_entry = hit['_source']
                print(
                    f"  - Timestamp: {log_entry['@timestamp']} | "
                    f"Usuário: {log_entry.get('user.name', 'N/A')} | "
                    f"Mensagem: {log_entry['message']}"
                )
        else:
            print("Nenhuma atividade suspeita encontrada para os critérios informados.")

    except Exception as e:
        print(f"Erro durante a busca: {e}")

if __name__ == "__main__":
    
    print("\n--- Chegada de logs ---")
    log1 = {
        "@timestamp": datetime.utcnow().isoformat(),
        "message": "Failed password for invalid user admin from 185.191.171.13 port 22 ssh2",
        "event.action": "authentication_failure",
        "source.ip": "185.191.171.13",
        "user.name": "admin",
        "process.name": "sshd"
    }
    log2 = {
        "@timestamp": (datetime.utcnow() - timedelta(minutes=10)).isoformat(),
        "message": "Accepted password for user 'carlos' from 192.168.1.10",
        "event.action": "authentication_success",
        "source.ip": "192.168.1.10",
        "user.name": "carlos",
        "process.name": "sshd"
    }
    log3 = {
        "@timestamp": (datetime.utcnow() - timedelta(minutes=5)).isoformat(),
        "message": "Failed password for root from 185.191.171.13 port 22 ssh2",
        "event.action": "authentication_failure",
        "source.ip": "185.191.171.13",
        "user.name": "root",
        "process.name": "sshd"
    }
    
    indexar_log(log1)
    indexar_log(log2)
    indexar_log(log3)
    
    es.indices.refresh(index=INDEX_NAME)

    buscar_tentativas_de_login_falhas(ip_suspeito="185.191.171.13")
    
    buscar_tentativas_de_login_falhas(ip_suspeito="1.2.3.4")