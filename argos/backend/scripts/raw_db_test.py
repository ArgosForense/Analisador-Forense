import os
import random
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env da api_gestao para manter consistência
# Ajuste o caminho conforme onde você rodar o script
load_dotenv(dotenv_path="../api_gestao/.env")

# --- 1. CONFIGURAÇÃO ADAPTADA ---
# Se não houver variável, usa o padrão do Docker Local
MONGO_URI = os.getenv("MONGODB_URL", "mongodb://localhost:27017/argos_db")
DB_NAME = "argos_db" # Nome padronizado do seu banco no projeto

def connect_to_db():
    """Conecta ao MongoDB Local e retorna o objeto do DB."""
    print(f"--- CONECTANDO AO BANCO: {MONGO_URI} ---")
    try:
        client = MongoClient(MONGO_URI)
        # O comando 'ping' verifica se o servidor está ativo
        client.admin.command('ping')
        db = client[DB_NAME]
        print("✅ Conexão estabelecida com sucesso!")
        return db
    except Exception as e:
        print(f"❌ Erro de Conexão: {e}")
        return None

def run_crud_simulation(db):
    print("\n--- INICIANDO SIMULAÇÃO CRUD (DIRETO NO BANCO) ---")

    # --- C R U D: CREATE ---
    print("-> Criando dados...")
    
    # Inserir Empresa
    nova_empresa = db['empresas'].insert_one({
        "nome": "Simulacao Script Direto",
        "cnpj": "88.888.888/0001-88"
    })
    print(f"   - Empresa criada: {nova_empresa.inserted_id}")

    # Inserir Usuário (Note que usamos 'usuarios' minusculo, padrão do Beanie)
    novo_usuario = db['usuarios'].insert_one({
        "nome": f"User Script {random.randint(10, 99)}",
        "email": f"script{random.randint(100, 999)}@teste.com",
        "senha": "hash_simulado_direto",
        "status": "ATIVO",
        "empresa": nova_empresa.inserted_id # Link direto
    })
    print(f"   - Usuário criado: {novo_usuario.inserted_id}")

    # --- C R U D: READ ---
    print("\n-> Lendo dados...")
    user_found = db['usuarios'].find_one({"_id": novo_usuario.inserted_id})
    print(f"   - Usuário encontrado: {user_found['nome']}")

    # --- C R U D: DELETE (Limpeza) ---
    print("\n-> Limpando sujeira de teste...")
    db['usuarios'].delete_one({"_id": novo_usuario.inserted_id})
    db['empresas'].delete_one({"_id": nova_empresa.inserted_id})
    print("✅ Limpeza concluída.")

if __name__ == "__main__":
    db_conn = connect_to_db()
    if db_conn is not None:
        run_crud_simulation(db_conn)