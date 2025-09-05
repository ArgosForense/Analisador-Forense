import time
import datetime
import random
import pytz
import json

LOG_FILE_PATH = "/var/log/gerador.log"
TIMEZONE = pytz.timezone('America/Sao_Paulo')

FUNCIONARIOS = [
    {"user": "ana.silva", "equipe": "financeiro", "ip_normal": "187.15.22.10", "role": "analyst"},
    {"user": "roberto.gomes", "equipe": "financeiro", "ip_normal": "187.15.22.11", "role": "manager"},
    {"user": "carla.monteiro", "equipe": "rh", "ip_normal": "187.15.23.20", "role": "recruiter"},
    {"user": "julio.cesar", "equipe": "rh", "ip_normal": "187.15.23.21", "role": "coordinator"},
    {"user": "fernanda.lima", "equipe": "comercial", "ip_normal": "187.15.24.30", "role": "broker"},
    {"user": "marcos.almeida", "equipe": "comercial", "ip_normal": "187.15.24.31", "role": "broker_lead"},
    {"user": "lucas.pereira", "equipe": "operacional", "ip_normal": "187.15.25.40", "role": "support"},
    {"user": "patricia.freitas", "equipe": "operacional", "ip_normal": "187.15.25.41", "role": "support"},
    {"user": "ricardo.mendes", "equipe": "compliance", "ip_normal": "187.15.26.50", "role": "auditor"},
    {"user": "sandra.nunes", "equipe": "compliance", "ip_normal": "187.15.26.51", "role": "officer"},
]

IPS_SUSPEITOS = {
    "tentativas_falhas": "201.45.112.88",
    "localidade_incomum": "103.77.200.15"
}

def gerar_timestamp_aleatorio():
    now = datetime.datetime.now(TIMEZONE)
    if random.random() <= 0.80:
        hora = random.randint(8, 17)
    else:
        hora = random.choice([random.randint(0, 7), random.randint(19, 23)])
    minuto = random.randint(0, 59)
    segundo = random.randint(0, 59)
    return now.replace(hour=hora, minute=minuto, second=segundo, microsecond=0)

def escrever_log_no_arquivo(f, log_entry):
    f.write(json.dumps(log_entry) + '\n')

def gerar_log_normal(f):
    funcionario = random.choice(FUNCIONARIOS)
    timestamp = gerar_timestamp_aleatorio()
    log_entry = {
        "@timestamp": timestamp.isoformat(),
        "event.action": "login_success",
        "user.name": funcionario["user"],
        "user.team": funcionario["equipe"],
        "user.role": funcionario["role"],
        "source.ip": funcionario["ip_normal"],
        "message": f"User '{funcionario['user']}' successfully logged in from IP {funcionario['ip_normal']}"
    }
    escrever_log_no_arquivo(f, log_entry)
    print(f"Log Normal Gerado: Login sucesso para {funcionario['user']}.")

def gerar_log_falha_multipla(f):
    ip_ataque = IPS_SUSPEITOS["tentativas_falhas"]
    usuario_alvo = random.choice(FUNCIONARIOS)["user"]
    num_tentativas = random.randint(5, 12)
    print(f"ALERTA: Gerando {num_tentativas} tentativas de login falhas do IP {ip_ataque}...")
    timestamp_base = gerar_timestamp_aleatorio()
    for i in range(num_tentativas):
        timestamp = timestamp_base + datetime.timedelta(seconds=i*2)
        log_entry = {
            "@timestamp": timestamp.isoformat(),
            "event.action": "login_failure",
            "user.name": usuario_alvo,
            "source.ip": ip_ataque,
            "message": f"Failed login attempt for user '{usuario_alvo}' from IP {ip_ataque}. Reason: Invalid credentials."
        }
        escrever_log_no_arquivo(f, log_entry)

def gerar_log_acesso_ip_incomum(f):
    funcionario = random.choice(FUNCIONARIOS)
    ip_incomum = IPS_SUSPEITOS["localidade_incomum"]
    timestamp = gerar_timestamp_aleatorio()
    log_entry = {
        "@timestamp": timestamp.isoformat(),
        "event.action": "login_success",
        "event.category": "suspicious",
        "user.name": funcionario["user"],
        "user.team": funcionario["equipe"],
        "source.ip": ip_incomum,
        "source.geo.country_name": "Russia",
        "message": f"SUSPICIOUS: Successful login for user '{funcionario['user']}' from an unusual IP {ip_incomum}"
    }
    escrever_log_no_arquivo(f, log_entry)
    print(f"ALERTA: Gerado acesso de IP incomum para {funcionario['user']}.")

def gerar_log_fora_de_horario(f):
    funcionario = random.choice(FUNCIONARIOS)
    now = datetime.datetime.now(TIMEZONE)
    hora = random.choice([random.randint(22, 23), random.randint(0, 5)])
    minuto = random.randint(0, 59)
    timestamp = now.replace(hour=hora, minute=minuto, microsecond=0)
    log_entry = {
        "@timestamp": timestamp.isoformat(),
        "event.action": "login_success",
        "event.category": "suspicious",
        "user.name": funcionario["user"],
        "user.team": funcionario["equipe"],
        "source.ip": funcionario["ip_normal"],
        "message": f"SUSPICIOUS: Successful login for user '{funcionario['user']}' outside of business hours."
    }
    escrever_log_no_arquivo(f, log_entry)
    print(f"ALERTA: Gerado acesso fora de hora para {funcionario['user']}.")

print("--- Gerador de Logs de Acesso iniciado. Escrevendo em:", LOG_FILE_PATH)
with open(LOG_FILE_PATH, "a") as f:
    while True:
        escolha = random.random()
        if escolha < 0.85:
            gerar_log_normal(f)
        elif escolha < 0.92:
            gerar_log_falha_multipla(f)
        elif escolha < 0.97:
            gerar_log_acesso_ip_incomum(f)
        else:
            gerar_log_fora_de_horario(f)
        f.flush()
        time.sleep(random.uniform(0.5, 3))
