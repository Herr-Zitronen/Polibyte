import requests
import os
import streamlit as st

# Por defecto se conecta a la URL de Render, que es pública.
# Si configuramos un secreto o variable de entorno, lo usará en su lugar.
try:
    API_URL = st.secrets.get("API_URL", os.getenv("API_URL", "https://polibyte.onrender.com"))
except Exception:
    API_URL = "https://polibyte.onrender.com"

def check_health():
    try:
        response = requests.get(f"{API_URL}/")
        return response.status_code == 200
    except:
        return False

# --- CULTIVOS ---
def get_crops():
    res = requests.get(f"{API_URL}/crops/")
    return res.json() if res.status_code == 200 else []

def create_crop(data):
    res = requests.post(f"{API_URL}/crops/", json=data)
    return res.status_code == 200

def delete_crop(crop_id):
    res = requests.delete(f"{API_URL}/crops/{crop_id}")
    return res.status_code == 200

# --- ACTIVIDADES ---
def get_activities(crop_id):
    res = requests.get(f"{API_URL}/crops/{crop_id}/activities/")
    return res.json() if res.status_code == 200 else []

def create_activity(crop_id, data):
    res = requests.post(f"{API_URL}/crops/{crop_id}/activities/", json=data)
    return res.status_code == 200

# --- DASHBOARD STATS ---
def get_dashboard_stats():
    res = requests.get(f"{API_URL}/dashboard/stats")
    return res.json() if res.status_code == 200 else {}
