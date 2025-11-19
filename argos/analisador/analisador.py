import time
from elasticsearch import Elasticsearch, ConnectionError
import sys

IPS_SUSPEITOS = {
    "tentativas_falhas": "201.45.112.88",
    "localidade_incomum": "103.77.200.15"
}

def conenctando_elasticsearch():
    es = None
    MAX_RETRIES = 50
    RETRY_DELAY_SECONDS = 5
    for attempt in range(MAX_RETRIES):
        try:
            print(f"Analisador: Tentando conectar ao Elasticsearch (tentativa {attempt + 1}/{MAX_RETRIES})...")
            client = Elasticsearch(
                hosts=[{'host': 'elasticsearch', 'port': 9200, 'scheme': 'http'}],
                request_timeout=30
            )
            if client.ping():
                es = client
                print("Analisador conectado ao Elasticsearch com sucesso!")
                return es
        except ConnectionError:
            print(f"Analisador: Conexão falhou! Tentando novamente em {RETRY_DELAY_SECONDS} segundos...")
            time.sleep(RETRY_DELAY_SECONDS)
    return None

def criar_alertas(es, entrada_log, motivo):
    alertas = {
        "@timestamp": entrada_log["@timestamp"],
        "motivo": motivo,
        "log_suspeito": entrada_log
    }
    try:
        es.index(index="alertas", document=alertas)
        print(f"ALERTAS GERADO: {motivo} para o usuário {entrada_log.get('nome', 'N/A')}")
    except Exception as e:
        print(f"Erro ao criar alertas: {e}")

def analisando_logs(es):
    last_checked_timestamp = "now-1m"

    while True:
        try:
            query_body = {
                "query": {
                    "range": {
                        "@timestamp": {
                            "gt": last_checked_timestamp
                        }
                    }
                },
                "sort": [
                    {"@timestamp": "asc"}
                ]
            }

            response = es.search(index="filebeat-*", body=query_body)
            hits = response['hits']['hits']

            if hits:
                for hit in hits:
                    entrada_log = hit['_source']
                    
                    last_checked_timestamp = entrada_log["@timestamp"]

                    ip_origem = entrada_log.get("ip_origem")
                    if ip_origem in IPS_SUSPEITOS.values():
                        motivo = f"Atividade suspeita detectada do IP: {ip_origem}"
                        criar_alertas(es, entrada_log, motivo)

                    if entrada_log.get("categoria") == "suspeito":
                        motivo = f"Evento categorizado como suspeito: {entrada_log.get('mensagem', '')}"
                        criar_alertas(es, entrada_log, motivo)
                
                last_checked_timestamp = hits[-1]['_source']['@timestamp']


        except Exception as e:
            print(f"Erro ao analisar logs: {e}")

        time.sleep(10)

if __name__ == "__main__":
    es_client = conenctando_elasticsearch()
    if es_client:
        if not es_client.indices.exists(index="alertas"):
            es_client.indices.create(index="alertas")
        analisando_logs(es_client)
    else:
        print("Analisador: Não foi possível conectar ao Elasticsearch. Encerrando.")
        sys.exit(1)