import time
import datetime
import random
import pytz
import json
import argparse
import socket
import threading

LOG_FILE_PATH = "/var/log/gerador.log"
TIMEZONE = pytz.timezone('America/Sao_Paulo')

FUNCIONARIOS = [
    {"usuario": "ana.silva", "equipe": "financeiro", "ip_normal": "187.15.22.10", "cargo": "analista"},
    {"usuario": "roberto.gomes", "equipe": "financeiro", "ip_normal": "187.15.22.11", "cargo": "gerente"},
    {"usuario": "carla.monteiro", "equipe": "rh", "ip_normal": "187.15.23.20", "cargo": "recrutadora"},
    {"usuario": "julio.cesar", "equipe": "rh", "ip_normal": "187.15.23.21", "cargo": "coordenador"},
    {"usuario": "fernanda.lima", "equipe": "comercial", "ip_normal": "187.15.24.30", "cargo": "corretora"},
    {"usuario": "marcos.almeida", "equipe": "comercial", "ip_normal": "187.15.24.31", "cargo": "corretor"},
    {"usuario": "lucas.pereira", "equipe": "operacional", "ip_normal": "187.15.25.40", "cargo": "auxiliar"},
    {"usuario": "patricia.freitas", "equipe": "operacional", "ip_normal": "187.15.25.41", "cargo": "suporte"},
    {"usuario": "ricardo.mendes", "equipe": "compliance", "ip_normal": "187.15.26.50", "cargo": "auditor"},
    {"usuario": "sandra.nunes", "equipe": "compliance", "ip_normal": "187.15.26.51", "cargo": "diretora"},
]

IPS_SUSPEITOS = {
    "tentativas_falhas": "201.45.112.88",
    "localidade_incomum": "103.77.200.15"
}

def listen_tcp(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"TCP: Escutando na porta {port}")
    while True:
        client_socket, addr = server.accept()
        print(f"TCP: Conexão aceita de {addr}")
        client_socket.close()

def listen_udp(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('0.0.0.0', port))
    print(f"UDP: Escutando na porta {port}")
    while True:
        data, addr = server.recvfrom(1024)
        print(f"UDP: Recebido {data} de {addr}")

def gerar_timestamp_aleatorio():
    now = datetime.datetime.now(TIMEZONE)
    if random.random() <= 0.80:
        hora = random.randint(8, 17)
    else:
        hora = random.choice([random.randint(0, 7), random.randint(19, 23)])
    minuto = random.randint(0, 59)
    segundo = random.randint(0, 59)
    return now.replace(hour=hora, minute=minuto, second=segundo, microsecond=0)

def escrever_log_no_arquivo(f, entrada_log):
    f.write(json.dumps(entrada_log) + '\n')

def gerar_log_normal(f):
    funcionario = random.choice(FUNCIONARIOS)
    timestamp = gerar_timestamp_aleatorio()
    entrada_log = {
        "@timestamp": timestamp.isoformat(),
        "evento": "entrada_efetuada",
        "nome": funcionario["usuario"],
        "equipe": funcionario["equipe"],
        "cargo": funcionario["cargo"],
        "ip_origem": funcionario["ip_normal"],
        "mensagem": f"Usuario '{funcionario['usuario']}' logou com sucesso do IP {funcionario['ip_normal']}"
    }
    escrever_log_no_arquivo(f, entrada_log)
    print(f"Log Normal Gerado: Entrada efetuada para {funcionario['usuario']}.")

def gerar_log_falha_multipla(f):
    ip_ataque = IPS_SUSPEITOS["tentativas_falhas"]
    usuario_alvo = random.choice(FUNCIONARIOS)["usuario"]
    num_tentativas = random.randint(5, 12)
    print(f"ALERTA: Gerando {num_tentativas} tentativas de login falhas do IP {ip_ataque}...")
    timestamp_base = gerar_timestamp_aleatorio()
    for i in range(num_tentativas):
        timestamp = timestamp_base + datetime.timedelta(seconds=i*2)
        entrada_log = {
            "@timestamp": timestamp.isoformat(),
            "evento": "entrada_falhou",
            "nome": usuario_alvo,
            "ip_origem": ip_ataque,
            "mensagem": f"Tentativa de login falha para o '{usuario_alvo}' do IP {ip_ataque}. Motivo: Credenciais invalidas."
        }
        escrever_log_no_arquivo(f, entrada_log)

def gerar_log_acesso_ip_incomum(f):
    funcionario = random.choice(FUNCIONARIOS)
    ip_incomum = IPS_SUSPEITOS["localidade_incomum"]
    timestamp = gerar_timestamp_aleatorio()
    entrada_log = {
        "@timestamp": timestamp.isoformat(),
        "evento": "entrada_efetuada",
        "categoria": "suspeito",
        "nome": funcionario["usuario"],
        "equipe": funcionario["equipe"],
        "ip_origem": ip_incomum,
        "nome_pais_origem": "Londres",
        "mensagem": f"SUSPEITO: Entrada efetuada do usuario '{funcionario['usuario']}' de um IP incomum {ip_incomum}"
    }
    escrever_log_no_arquivo(f, entrada_log)
    print(f"ALERTA: Gerado acesso de IP incomum para {funcionario['usuario']}.")

def gerar_log_fora_de_horario(f):
    funcionario = random.choice(FUNCIONARIOS)
    now = datetime.datetime.now(TIMEZONE)
    hora = random.choice([random.randint(22, 23), random.randint(0, 5)])
    minuto = random.randint(0, 59)
    timestamp = now.replace(hour=hora, minute=minuto, microsecond=0)
    entrada_log = {
        "@timestamp": timestamp.isoformat(),
        "evento": "entrada_efetuada",
        "categoria": "suspeito",
        "nome": funcionario["usuario"],
        "equipe": funcionario["equipe"],
        "ip_origem": funcionario["ip_normal"],
        "mensagem": f"SUSPEITO: Entrada efetuada do usuario '{funcionario['usuario']}' fora do horario comercial."
    }
    escrever_log_no_arquivo(f, entrada_log)
    print(f"ALERTA: Gerado acesso fora de hora para {funcionario['usuario']}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gerador de Logs de Acesso com listeners de porta.")
    parser.add_argument("--tcp-port", type=int, help="Porta TCP para escutar.")
    parser.add_argument("--udp-port", type=int, help="Porta UDP para escutar.")
    args = parser.parse_args()

    if args.tcp_port:
        tcp_thread = threading.Thread(target=listen_tcp, args=(args.tcp_port,), daemon=True)
        tcp_thread.start()

    if args.udp_port:
        udp_thread = threading.Thread(target=listen_udp, args=(args.udp_port,), daemon=True)
        udp_thread.start()

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