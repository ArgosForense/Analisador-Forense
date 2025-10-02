import time
from elasticsearch import Elasticsearch, ConnectionError
import sys

IPS_SUSPEITOS = {
    "tentativas_falhas": "201.45.112.88",
    "localidade_incomum": "103.77.200.15"
}

def connect_to_elasticsearch():
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

def create_alert(es, log_entry, reason):
    alert = {
        "@timestamp": log_entry["@timestamp"],
        "reason": reason,
        "suspicious_log": log_entry
    }
    try:
        es.index(index="alerts", document=alert)
        print(f"ALERTA GERADO: {reason} para o usuário {log_entry.get('user.name', 'N/A')}")
    except Exception as e:
        print(f"Erro ao criar alerta: {e}")

def analyze_logs(es):
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
                    log_entry = hit['_source']
                    
                    last_checked_timestamp = log_entry["@timestamp"]

                    source_ip = log_entry.get("source.ip")
                    if source_ip in IPS_SUSPEITOS.values():
                        reason = f"Atividade suspeita detectada do IP: {source_ip}"
                        create_alert(es, log_entry, reason)

                    if log_entry.get("event.category") == "suspicious":
                        reason = f"Evento categorizado como suspeito: {log_entry.get('message', '')}"
                        create_alert(es, log_entry, reason)
                
                last_checked_timestamp = hits[-1]['_source']['@timestamp']


        except Exception as e:
            print(f"Erro ao analisar logs: {e}")

        time.sleep(10)

if __name__ == "__main__":
    es_client = connect_to_elasticsearch()
    if es_client:
        if not es_client.indices.exists(index="alerts"):
            es_client.indices.create(index="alerts")
        analyze_logs(es_client)
    else:
        print("Analisador: Não foi possível conectar ao Elasticsearch. Encerrando.")
        sys.exit(1)