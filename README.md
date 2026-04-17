# 🍽️ Sistema de Reservaciones — Instrucciones

## Archivos incluidos

| Archivo | Descripción |
|---|---|
| `admin_app.py` | App para el dueño de la tienda |
| `reservaciones_app.py` | App para los clientes |
| `reservaciones_data.json` | Base de datos compartida (se crea automáticamente) |

---

## Requisitos

```bash
pip install streamlit
```

---

## Cómo correr las apps

Abre **dos terminales** en la misma carpeta:

### Terminal 1 — Panel admin (dueño)
```bash
streamlit run admin_app.py --server.port 8501
```
Accede en: http://localhost:8501

### Terminal 2 — Reservaciones (clientes)
```bash
streamlit run reservaciones_app.py --server.port 8502
```
Accede en: http://localhost:8502

---

## Flujo de uso

### El dueño (admin_app.py):
1. Selecciona el día del fin de semana a configurar
2. Define cuántas mesas estarán disponibles
3. Elige los horarios disponibles (12:00–22:00 cada 30 min, o personalizados)
4. Guarda la configuración
5. Puede ver en tiempo real cuántas mesas quedan por horario

### El cliente (reservaciones_app.py):
1. Elige la fecha disponible
2. Ve los horarios con mesas libres
3. Ingresa su nombre, teléfono y número de personas
4. Recibe un código de confirmación

---

## Notas
- Ambas apps comparten el archivo `reservaciones_data.json` — deben estar en la misma carpeta.
- Si corres las apps en servidores diferentes, asegúrate de que compartan el mismo sistema de archivos o reemplaza el JSON con una base de datos (SQLite, Supabase, etc.).
- Las reservas tienen protección básica contra doble-booking (verifica disponibilidad justo antes de confirmar).
