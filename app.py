from flask import Flask, request, jsonify
import paramiko
import os

app = Flask(__name__)

# Настройки для подключения к VPS
VPS_HOST = "34.88.223.194"
VPS_PORT = 22
VPS_USER = "zokirjonovjavohir61"
PRIVATE_KEY_PATH = "id_rsa"

@app.route("/ssh", methods=["POST"])
def ssh_command():
    command = request.json.get("command")
    if not command:
        return jsonify({"error": "No command provided"}), 400
    
    try:
        key = paramiko.RSAKey(filename=PRIVATE_KEY_PATH)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(VPS_HOST, port=VPS_PORT, username=VPS_USER, pkey=key)
        
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode()
        ssh.close()
        
        return jsonify({"output": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
