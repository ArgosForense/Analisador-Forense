import pprint
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
import random


# --- 1. CONFIGURAÇÃO DE ACESSO ---
# SUBSTITUA 'SUA_SENHA_AQUI' PELA SENHA REAL DO SEU USUÁRIO 'analistaforense'
MONGO_URI = "mongodb://localhost:27017/ArgosDB"
DB_NAME = "ArgosDB"

def connect_to_db(uri, db_name):
    """Conecta ao MongoDB Atlas e retorna o objeto do DB."""
    print("--- 1. CONECTANDO AO BANCO DE DADOS ---")
    try:
        client = MongoClient(uri, server_api=ServerApi('1'))
        client.admin.command('ping')
        db = client[db_name]
        print("✅ Conexão estabelecida com sucesso!")
        return db
    except Exception as e:
        print(f"❌ Erro de Conexão: Verifique sua URI e acesso à rede. Detalhe: {e}")
        return None

def run_crud_simulation(db):
    """Executa as operacoes CRUD e BI para demonstracao."""
    print("\n--- 2. INICIANDO SIMULAÇÃO CRUD ---")

    # IDs Reais (Assumindo que já existem no DB)
    PERFIL_ANALISTA_ID = ObjectId("68b63631f85f1b9248a90d07") # ID de um Perfil Analista existente
    PERFIL_FUNCIONARIO_ID = ObjectId("68b6363bf85f1b9248a90d09") # ID de um Perfil Funcionario existente

    # Armazenamento de IDs criados durante a simulação
    temp_ids = []

    # --- C R U D: CREATE (Criação de Entidades de Teste) ---

    # 2.1 Criar uma Empresa Temporária
    nova_empresa = db['EMPRESA'].insert_one({
        "nome_empresa": "Simulacao Teste",
        "cnpj": "99.999.999/0001-00"
    })
    temp_ids.append(('EMPRESA', nova_empresa.inserted_id))
    print(f"   - EMPRESA criada. ID: {nova_empresa.inserted_id}")

    # 2.2 Criar um Usuário Analista (Para gerar Logs)
    novo_usuario = db['USUARIOS'].insert_one({
        "nome": "User Teste " + str(random.randint(10, 99)),
        "email": "teste" + str(random.randint(100, 999)) + "@simulacao.com",
        "senha": "hash_teste",
        "empresa_id": nova_empresa.inserted_id,
        "perfil_id": PERFIL_ANALISTA_ID,
        "status": True
    })
    temp_ids.append(('USUARIOS', novo_usuario.inserted_id))
    print(f"   - USUARIO criado. ID: {novo_usuario.inserted_id}")

    # 2.3 Criar um Log Simulado
    novo_log = db['LOG'].insert_one({
        "tipo_evento": "deteccao_malware",
        "timestamp": "2025-10-02T16:30:00Z",
        "detalhes": {"ameaca": "Trojan.Fake", "caminho": "/caminho/teste.exe"},
        "usuario_id": novo_usuario.inserted_id
    })
    temp_ids.append(('LOG', novo_log.inserted_id))
    print(f"   - LOG criado. ID: {novo_log.inserted_id}")

    # --- C R U D: READ (Leitura e Busca) ---
    print("\n--- C R U D: READ (Lendo Dados) ---")

    # 2.4 Buscar o Log Recem-Criado
    log_lido = db['LOG'].find_one({"_id": novo_log.inserted_id})
    print(f"   - Log lido com sucesso (Tipo: {log_lido['tipo_evento']})")

    # --- C R U D: UPDATE (Atualização de Dados) ---
    print("\n--- C R U D: UPDATE (Atualizando Dados) ---")

    # 2.5 Mudar o Status do Usuario (Simulando desativação)
    db['USUARIOS'].update_one(
        {"_id": novo_usuario.inserted_id},
        {"$set": {"status": False, "comentario_status": "Desativado para teste"}}
    )
    usuario_atualizado = db['USUARIOS'].find_one({"_id": novo_usuario.inserted_id})
    print(f"   - Status do Usuário Atualizado para: {usuario_atualizado['status']}")

    # --- 3. SIMULAÇÃO BI (Business Intelligence) ---
    print("\n--- 3. SIMULAÇÃO BI (Contagem de Usuários) ---")

    # Contagem de Analistas
    total_analistas = db['USUARIOS'].count_documents({"perfil_id": PERFIL_ANALISTA_ID})
    print(f"   - Total de Analistas no DB: {total_analistas}")

    # Contagem de Funcionarios
    total_funcionarios = db['USUARIOS'].count_documents({"perfil_id": PERFIL_FUNCIONARIO_ID})
    print(f"   - Total de Funcionários no DB: {total_funcionarios}")


    # --- C R U D: DELETE (Limpeza dos Dados de Teste) ---
    print("\n--- 4. LIMPEZA (DELETANDO DADOS DE TESTE) ---")
    for collection_name, doc_id in temp_ids:
        db[collection_name].delete_one({"_id": doc_id})
        print(f"   - Documento deletado na coleção {collection_name} (ID: {doc_id})")
    print("✅ Simulação concluída e dados de teste removidos.")


# --- Execução Principal ---
if __name__ == "__main__":
    db_conn = connect_to_db(MONGO_URI, DB_NAME)

    if db_conn is not None:
        print("\nINICIANDO O TESTE DE CONEXÃO E SIMULAÇÃO...")
        run_crud_simulation(db_conn)