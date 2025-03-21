from flask import Flask, request, jsonify
import paramiko
import os
import io

app = Flask(__name__)

# Настройки для подключения к VPS
VPS_HOST = "34.88.223.194"
VPS_PORT = 22
VPS_USER = "zokirjonovjavohir61"
PRIVATE_KEY = os.getenv("SSH_PRIVATE_KEY")  # Берем ключ из переменной окружения

@app.route("/ssh", methods=["POST"])
def ssh_command():
    command = request.json.get("command")
    if not command:
        return jsonify({"error": "No command provided"}), 400
    
    try:
        # Читаем ключ из строки
        key_file = io.StringIO(PRIVATE_KEY)
        key = paramiko.RSAKey.from_private_key(key_file)

        # Подключаемся к серверу
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(VPS_HOST, port=VPS_PORT, username=VPS_USER, pkey=key)
        
        # Выполняем команду
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        ssh.close()
        
        return jsonify({"output": output, "error": error})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
