"""
db.py — Capa de acceso a MongoDB compartida por ambas apps.
Las credenciales vienen de st.secrets (secrets.toml en local,
o Secrets en el panel de Streamlit Cloud).
"""
 
import streamlit as st
from pymongo import MongoClient
from pymongo import ReturnDocument
import certifi
 
 
@st.cache_resource
def get_db():
    """Conexión única y cacheada a MongoDB Atlas."""
    uri = st.secrets["mongodb"]["uri"]
    client = MongoClient(uri, tlsCAFile=certifi.where())
    db = client[st.secrets["mongodb"]["db_name"]]
    # Índices útiles (idempotente)
    db.disponibilidad.create_index("fecha", unique=True)
    db.reservaciones.create_index([("fecha", 1), ("horario", 1)])
    return db
 
 
# ── Disponibilidad ────────────────────────────────────────────────────────────
 
def get_disponibilidad(db) -> dict:
    """Devuelve {fecha_str: {mesas, horarios}} de todos los documentos."""
    return {
        doc["fecha"]: {"mesas": doc["mesas"], "horarios": doc["horarios"]}
        for doc in db.disponibilidad.find({}, {"_id": 0})
    }
 
 
def upsert_disponibilidad(db, fecha_str: str, mesas: int, horarios: list):
    db.disponibilidad.find_one_and_update(
        {"fecha": fecha_str},
        {"$set": {"mesas": mesas, "horarios": sorted(horarios)}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
 
 
def delete_disponibilidad(db, fecha_str: str):
    db.disponibilidad.delete_one({"fecha": fecha_str})
 
 
def delete_past_disponibilidad(db, today_str: str) -> int:
    result = db.disponibilidad.delete_many({"fecha": {"$lt": today_str}})
    return result.deleted_count
 
 
# ── Reservaciones ─────────────────────────────────────────────────────────────
 
def count_reservations(db, fecha_str: str, horario: str) -> int:
    return db.reservaciones.count_documents({
        "fecha": fecha_str,
        "horario": horario,
        "estado": {"$ne": "cancelada"},
    })
 
 
def get_all_reservations(db) -> list:
    return list(db.reservaciones.find({}, {"_id": 0}))
 
 
def insert_reservation(db, doc: dict):
    db.reservaciones.insert_one(doc)
 
 
def get_reservations_for_date(db, fecha_str: str) -> list:
    return list(db.reservaciones.find(
        {"fecha": fecha_str, "estado": {"$ne": "cancelada"}},
        {"_id": 0}
    ))