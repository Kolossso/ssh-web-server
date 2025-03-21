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
    if not request.is_json:
        return jsonify({"error": "Invalid JSON"}), 400
    
    command = request.json.get("command")
    if not command:
        return jsonify({"error": "No command provided"}), 400

    if not PRIVATE_KEY:
        return jsonify({"error": "SSH_PRIVATE_KEY is not set"}), 500

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
    
    except paramiko.ssh_exception.AuthenticationException:
        return jsonify({"error": "SSH authentication failed"}), 403
    except paramiko.ssh_exception.SSHException as e:
        return jsonify({"error": f"SSH error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
