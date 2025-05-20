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

DATA_FILE = "data.json"

def read_data():
    if not os.path.exists(DATA_FILE):
        return {"comptes": [], "commentaires": []}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/register", methods=["POST"])
def register():
    data = read_data()
    infos = request.get_json()
    pseudo = infos.get("pseudo", "").strip()
    password = infos.get("password", "").strip()

    if not pseudo or not password:
        return jsonify({"error": "Champs vides"}), 400

    if any(compte["pseudo"] == pseudo for compte in data["comptes"]):
        return jsonify({"error": "Pseudo déjà utilisé"}), 409

    data["comptes"].append({"pseudo": pseudo, "password": password})
    write_data(data)
    return jsonify({"message": "Compte créé"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = read_data()
    infos = request.get_json()
    pseudo = infos.get("pseudo", "").strip()
    password = infos.get("password", "").strip()

    if any(compte["pseudo"] == pseudo and compte["password"] == password for compte in data["comptes"]):
        return jsonify({"message": "Connexion réussie"})
    return jsonify({"error": "Identifiants invalides"}), 401

@app.route("/comments", methods=["GET"])
def get_comments():
    data = read_data()
    type_graphique = request.args.get("type")
    grand_prix = request.args.get("gp")
    cible = request.args.get("cible")

    comments = [
        c for c in data["commentaires"]
        if c["type_graphique"] == type_graphique and c["grand_prix"] == grand_prix and str(c["cible"]) == str(cible)
    ]
    return jsonify(comments)

@app.route("/comments", methods=["POST"])
def post_comment():
    data = read_data()
    infos = request.get_json()
    auteur = infos.get("auteur")
    contenu = infos.get("contenu")
    type_graphique = infos.get("type_graphique")
    grand_prix = infos.get("grand_prix")
    cible = infos.get("cible")
    timestamp = datetime.utcnow().isoformat()

    if not all([auteur, contenu, type_graphique, grand_prix, cible]):
        return jsonify({"error": "Champs manquants"}), 400

    data["commentaires"].append({
        "auteur": auteur,
        "contenu": contenu,
        "type_graphique": type_graphique,
        "grand_prix": grand_prix,
        "cible": cible,
        "timestamp": timestamp
    })
    write_data(data)
    return jsonify({"message": "Commentaire ajouté"}), 201

@app.route("/", methods=["GET"])
def index():
    return "Serveur F1 actif", 200

if __name__ == "__main__":
    app.run(debug=True)
