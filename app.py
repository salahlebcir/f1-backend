#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 20 17:28:31 2025

@author: slebcir
"""

# app.py
from flask import Flask, request, jsonify
import json
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

USERS_FILE = "users.json"
COMMENTS_FILE = "comments.json"

# Charger les utilisateurs
if os.path.exists(USERS_FILE):
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)
else:
    users = []

# Charger les commentaires
if os.path.exists(COMMENTS_FILE):
    with open(COMMENTS_FILE, "r", encoding="utf-8") as f:
        comments = json.load(f)
else:
    comments = []

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    pseudo = data.get("pseudo")
    password = data.get("password")
    if not pseudo or not password:
        return jsonify({"error": "Champs manquants"}), 400
    if any(u["pseudo"] == pseudo for u in users):
        return jsonify({"error": "Pseudo déjà pris"}), 409
    users.append({"pseudo": pseudo, "password": password})
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)
    return jsonify({"message": "Compte créé"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    pseudo = data.get("pseudo")
    password = data.get("password")
    if any(u["pseudo"] == pseudo and u["password"] == password for u in users):
        return jsonify({"message": "Connexion réussie"})
    return jsonify({"error": "Identifiants invalides"}), 401

@app.route("/comments", methods=["GET"])
def get_comments():
    type_graphique = request.args.get("type")
    grand_prix = request.args.get("gp")
    cible = request.args.get("cible")
    if not type_graphique or not grand_prix or cible is None:
        return jsonify({"error": "Paramètres manquants"}), 400
    filtres = [c for c in comments if c["type_graphique"] == type_graphique and c["grand_prix"] == grand_prix and c["cible"] == str(cible)]
    return jsonify(filtres)

@app.route("/comments", methods=["POST"])
def post_comment():
    data = request.json
    required = ["auteur", "contenu", "type_graphique", "grand_prix", "cible"]
    if not all(k in data for k in required):
        return jsonify({"error": "Champs requis manquants"}), 400

    from datetime import datetime
    data["timestamp"] = datetime.utcnow().isoformat()
    comments.append(data)
    with open(COMMENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(comments, f, indent=2)
    return jsonify({"message": "Commentaire enregistré"}), 201

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
