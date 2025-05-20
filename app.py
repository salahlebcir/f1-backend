#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 20 17:28:31 2025

@author: slebcir
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

USERS_FILE = "users.json"
COMMENTS_FILE = "comments.json"

# Charger les utilisateurs
if os.path.exists(USERS_FILE):
    with open(USERS_FILE, "r") as f:
        users = json.load(f)
else:
    users = {}
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

# Charger les commentaires
if os.path.exists(COMMENTS_FILE):
    with open(COMMENTS_FILE, "r") as f:
        commentaires = json.load(f)
else:
    commentaires = []
    with open(COMMENTS_FILE, "w") as f:
        json.dump(commentaires, f)


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    pseudo = data.get("pseudo")
    password = data.get("password")

    if not pseudo or not password:
        return jsonify({"error": "Champs manquants"}), 400

    if pseudo in users:
        return jsonify({"error": "Pseudo déjà pris"}), 409

    users[pseudo] = password
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

    return jsonify({"message": "Compte créé"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    pseudo = data.get("pseudo")
    password = data.get("password")

    if users.get(pseudo) != password:
        return jsonify({"error": "Identifiants incorrects"}), 401

    return jsonify({"message": "Connexion réussie"}), 200


@app.route("/comments", methods=["GET", "POST"])
def comments():
    if request.method == "GET":
        type_graphique = request.args.get("type")
        gp = request.args.get("gp")
        cible = request.args.get("cible")

        results = [c for c in commentaires if c["type_graphique"] == type_graphique and c["grand_prix"] == gp and str(c["cible"]) == str(cible)]
        return jsonify(results)

    elif request.method == "POST":
        data = request.get_json()
        commentaire = {
            "auteur": data.get("auteur"),
            "contenu": data.get("contenu"),
            "type_graphique": data.get("type_graphique"),
            "grand_prix": data.get("grand_prix"),
            "cible": data.get("cible"),
            "timestamp": datetime.utcnow().isoformat()
        }
        commentaires.append(commentaire)
        with open(COMMENTS_FILE, "w") as f:
            json.dump(commentaires, f, indent=2)
        return jsonify({"message": "Commentaire ajouté"}), 201


@app.route("/", methods=["GET"])
def home():
    return "✅ Backend F1 commentaires actif."


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
