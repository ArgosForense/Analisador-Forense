import json
import os
from pymongo import MongoClient
from bson import ObjectId
from bson.dbref import DBRef
from dotenv import load_dotenv

# Carrega config do ambiente
load_dotenv(dotenv_path="../api_gestao/.env")
MONGO_URI = os.getenv("MONGODB_URL", "mongodb://localhost:27017/argos_db")
DB_NAME = "argos_db"

# Caminho onde estão os JSONs
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        print(f"⚠️ Arquivo não encontrado: {filename}")
        return []
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # O Mongo exporta no formato {"_id": {"$oid": "..."}}, precisamos limpar isso
        for item in data:
            if "_id" in item and "$oid" in item["_id"]:
                item["_id"] = ObjectId(item["_id"]["$oid"])
        return data

def connect_db():
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]

def migrar():
    db = connect_db()
    print(f"🚀 Iniciando migração para o banco: {DB_NAME}")

    # 1. PERMISSÕES (Converter nome_permissao -> nome)
    print("\n🔄 Migrando Permissões...")
    raw_perms = load_json("ArgosBD.PERMISSAO.json")
    perm_map_name_to_id = {}
    
    for p in raw_perms:
        new_p = {
            "_id": p["_id"],
            "nome": p.get("nome_permissao", p.get("nome")) # Ajusta o campo
        }
        db["permissoes"].replace_one({"_id": new_p["_id"]}, new_p, upsert=True)
        perm_map_name_to_id[new_p["nome"]] = new_p["_id"]
    print(f"   ✅ {len(raw_perms)} permissões importadas.")

    # 2. EMPRESAS (Converter nome_empresa -> nome)
    print("\n🔄 Migrando Empresas...")
    raw_empresas = load_json("ArgosBD.EMPRESA.json")
    for e in raw_empresas:
        new_e = {
            "_id": e["_id"],
            "nome": e.get("nome_empresa", e.get("nome")),
            "cnpj": e["cnpj"]
        }
        db["empresas"].replace_one({"_id": new_e["_id"]}, new_e, upsert=True)
    print(f"   ✅ {len(raw_empresas)} empresas importadas.")

    # 3. PERFIS (Ajustar relacionamentos)
    print("\n🔄 Migrando Perfis...")
    raw_perfis = load_json("ArgosBD.PERFIL.json")
    for p in raw_perfis:
        # Converte lista de nomes de permissão para DBRefs (Links do Beanie)
        perm_refs = []
        if "permissoes" in p:
            for perm_name in p["permissoes"]:
                if perm_name in perm_map_name_to_id:
                    # Beanie usa DBRef para Links por padrão
                    perm_refs.append(DBRef("permissoes", perm_map_name_to_id[perm_name]))
        
        new_p = {
            "_id": p["_id"],
            "nome": p.get("nome_do_perfil", p.get("nome_perfil", p.get("nome"))),
            "permissoes": perm_refs
        }
        db["perfis"].replace_one({"_id": new_p["_id"]}, new_p, upsert=True)
    print(f"   ✅ {len(raw_perfis)} perfis importados.")

    # 4. GESTORES (Linkar com Empresa)
    print("\n🔄 Migrando Gestores...")
    raw_gestores = load_json("ArgosBD.GESTOR.json")
    for g in raw_gestores:
        # Converte empresa_id (string) para DBRef
        empresa_ref = None
        if "empresa_id" in g and g["empresa_id"]:
             # Se for string hexadecimal
             try:
                 e_id = ObjectId(g["empresa_id"])
                 empresa_ref = DBRef("empresas", e_id)
             except:
                 pass

        new_g = {
            "_id": g["_id"],
            "nome": g["nome"],
            "email": g["email"],
            "senha": g["senha"], # Assumindo que já está hash ou vai ser tratada
            "empresa": empresa_ref
        }
        db["gestores"].replace_one({"_id": new_g["_id"]}, new_g, upsert=True)
    print(f"   ✅ {len(raw_gestores)} gestores importados.")

    # 5. USUÁRIOS (Linkar com Perfil e Gestor)
    print("\n🔄 Migrando Usuários...")
    raw_users = load_json("ArgosBD.USUARIOS.json")
    for u in raw_users:
        # Criar Links (DBRefs)
        perfil_ref = None
        if "perfil_id" in u and u["perfil_id"]:
            perfil_ref = DBRef("perfis", ObjectId(u["perfil_id"]))
            
        gestor_ref = None
        if "gestor_id" in u and u["gestor_id"]:
            gestor_ref = DBRef("gestores", ObjectId(u["gestor_id"]))

        new_u = {
            "_id": u["_id"],
            "nome": u["nome"],
            "email": u["email"],
            "senha": u["senha"],
            "status": "ATIVO" if u.get("status") is True else "DESATIVADO", # Converter bool para str
            "perfil": perfil_ref,
            "gestor": gestor_ref
        }
        db["usuarios"].replace_one({"_id": new_u["_id"]}, new_u, upsert=True)
    print(f"   ✅ {len(raw_users)} usuários importados.")
    
    print("\n🏁 Migração Concluída com Sucesso!")

if __name__ == "__main__":
    migrar()