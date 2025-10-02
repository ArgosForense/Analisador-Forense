from flask import Flask, request, jsonify
from flask_cors import CORS
from elasticsearch import Elasticsearch, ConnectionError
import time
import sys

app = Flask(__name__)
CORS(app)

es = None
MAX_RETRIES = 50
RETRY_DELAY_SECONDS = 5

for attempt in range(MAX_RETRIES):
    try:
        print(f"Tentando conectar ao Elasticsearch (tentativa {attempt + 1}/{MAX_RETRIES})...")
        client = Elasticsearch(
            hosts=[{'host': 'elasticsearch', 'port': 9200, 'scheme': 'http'}],
            request_timeout=30
        )
        if client.ping():
            es = client
            print("Backend conectado ao Elasticsearch com sucesso!")
            break
    except ConnectionError:
        print(f"Conexão falhou! Tentando novamente em {RETRY_DELAY_SECONDS} segundos...")
        time.sleep(RETRY_DELAY_SECONDS)

if es is None:
    print("Não foi possível conectar ao Elasticsearch.")
    sys.exit(1)

def process_hits(hits):
    """Função auxiliar para adicionar o _id do Elasticsearch ao corpo do documento."""
    results = []
    for hit in hits:
        source = hit['_source']
        source['id'] = hit['_id']
        results.append(source)
    return results

@app.route('/search', methods=['GET'])
def search():
    query_term = request.args.get('q', '').strip()

    if not query_term:
        query_body = {"query": {"match_all": {}}}
    else:
        query_body = {
            "query": {
                "multi_match": {
                    "query": query_term,
                    "fields": ["mensagem", "nome", "ip_origem", "evento"]
                }
            }
        }
    
    query_body["size"] = 50
    query_body["sort"] = [{"@timestamp": "desc"}]

    try:
        response = es.search(index="filebeat-*", body=query_body)
        return jsonify(process_hits(response['hits']['hits']))
    except Exception as e:
        return jsonify({f"Erro durante a busca: {e}"}), 500

@app.route('/alertas', methods=['GET'])
def get_alertas():
    try:
        response = es.search(
            index="alertas",
            body={"size": 50, "sort": [{"@timestamp": "desc"}]}
        )
        return jsonify(process_hits(response['hits']['hits']))
    except Exception as e:
        if "index_not_found_exception" in str(e):
            return jsonify([])
        return jsonify({f"Erro durante a busca de alertas: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)