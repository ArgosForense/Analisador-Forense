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

@app.route('/search', methods=['GET'])
def search():
    query_term = request.args.get('q', '')

    query_body = {
        "query": {
            "multi_match": {
                "query": query_term,
                "fields": ["message", "log.level"]
            }
        },
        "size": 50,
        "sort": [
            {"@timestamp": "desc"}
        ]
    }

    try:
        response = es.search(index="filebeat-*", body=query_body)
        hits = [hit['_source'] for hit in response['hits']['hits']]
        return jsonify(hits)
    except Exception as e:
        return jsonify({"error": f"Erro durante a busca: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)