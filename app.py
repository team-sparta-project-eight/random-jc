from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.pkdgkh7.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

