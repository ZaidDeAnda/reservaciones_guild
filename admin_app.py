import streamlit as st
from datetime import datetime, date, timedelta
from db import (
    get_db, get_disponibilidad, upsert_disponibilidad,
    delete_disponibilidad, delete_past_disponibilidad,
    count_reservations, get_all_reservations,
    delete_reservation,
)

# ── Config ───────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Admin · Gestión de Mesas",
    page_icon="🍽️",
    layout="wide",
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
h1, h2, h3 { font-family: 'Playfair Display', serif !important; }

.stApp {
    background: linear-gradient(135deg, #1f1f1f 0%, #2b2b2b 50%, #1f1f1f 100%);
    color: #e6f7f7;
}

section[data-testid="stSidebar"] {
    background: #181818 !important;
    border-right: 1px solid #00cfd1;
}

.metric-box {
    background: rgba(0, 207, 209, 0.08);
    border: 1px solid rgba(0, 207, 209, 0.4);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    text-align: center;
    margin-bottom: 0.8rem;
}
.metric-box .num {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    color: #00e5e7;
    line-height: 1;
}
.metric-box .label {
    font-size: 0.75rem;
    color: #8fdfe0;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 0.3rem;
}

.stTextInput input, .stNumberInput input {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(0, 207, 209, 0.4) !important;
    color: #e6f7f7 !important;
    border-radius: 8px !important;
}

.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: #242424 !important;
    border: 1px solid rgba(0, 207, 209, 0.30) !important;
    color: #e6f7f7 !important;
    border-radius: 8px !important;
}

.stMultiSelect span {
    background: rgba(0, 207, 209, 0.2) !important;
    border-color: rgba(0, 207, 209, 0.5) !important;
    color: #aaf6f7 !important;
}

.stButton > button {
    background: linear-gradient(135deg, #00cfd1, #00a8aa) !important;
    color: #0d0d0d !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 8px !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0, 207, 209, 0.4) !important;
}

.divider {
    border: none;
    border-top: 1px solid rgba(0, 207, 209, 0.2);
    margin: 1.5rem 0;
}

.reservation-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(0, 207, 209, 0.22);
    border-radius: 12px;
    padding: 0.9rem 1rem;
    margin-bottom: 0.7rem;
}
.reservation-name {
    font-weight: 700;
    font-size: 1rem;
    color: #00e5e7;
    margin-bottom: 0.25rem;
}
.reservation-meta {
    font-size: 0.88rem;
    color: #d8f4f4;
    line-height: 1.6;
}
.reservation-extra {
    font-size: 0.78rem;
    color: #8fdfe0;
    margin-top: 0.35rem;
}
</style>
""", unsafe_allow_html=True)

# ── Helpers ──────────────────────────────────────────────────────────────────
def get_upcoming_weekends(n=6):
    today = date.today()
    weekends, d = [], today
    while len(weekends) < n * 2:
        if d.weekday() == 5:
            weekends += [d, d + timedelta(days=1)]
        d += timedelta(days=1)
    return weekends[:n * 2]

def date_label(d: date) -> str:
    dias = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]
    meses = ["", "ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
    return f"{dias[d.weekday()]} {d.day} {meses[d.month]}"

# ── Connect ──────────────────────────────────────────────────────────────────
try:
    db = get_db()
except Exception as e:
    st.error(f"❌ No se pudo conectar a MongoDB: {e}")
    st.stop()

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("## 🍽️ Panel de Administración")
st.markdown("Configura la disponibilidad de mesas para cada fin de semana y revisa quién ha reservado.")
st.markdown('<hr class="divider">', unsafe_allow_html=True)

disponibilidad = get_disponibilidad(db)
todas_reservas = get_all_reservations(db)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📊 Resumen")
    st.markdown(f"""
    <div class="metric-box">
        <div class="num">{len(disponibilidad)}</div>
        <div class="label">Días configurados</div>
    </div>
    <div class="metric-box">
        <div class="num">{len(todas_reservas)}</div>
        <div class="label">Reservaciones totales</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ⚙️ Acciones")
    if st.button("🔄 Recargar datos"):
        st.rerun()
    if st.button("🗑️ Limpiar días pasados"):
        n = delete_past_disponibilidad(db, date.today().isoformat())
        st.success(f"Se eliminaron {n} días pasados.")
        st.rerun()

# ── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["➕ Configurar disponibilidad", "📋 Ver configuración actual"])

with tab1:
    upcoming = get_upcoming_weekends()
    st.markdown("### Selecciona el día a configurar")
    col_left, col_right = st.columns([2, 3])

    with col_left:
        date_options = {date_label(d): d for d in upcoming}
        selected_label = st.selectbox("Fin de semana", list(date_options.keys()))
        selected_date = date_options[selected_label]
        selected_str = selected_date.isoformat()

        st.markdown("---")
        existing_mesas = disponibilidad.get(selected_str, {}).get("mesas", 10)
        num_mesas = st.number_input(
            "Número de mesas disponibles",
            min_value=1, max_value=50, value=existing_mesas, step=1,
        )

    with col_right:
        st.markdown("#### Horarios disponibles")
        st.caption("Define los turnos que estarán abiertos para reservar")

        slots = []
        for h in range(12, 23):
            slots.append(f"{h:02d}:00")
            if h < 22:
                slots.append(f"{h:02d}:30")

        default_slots = disponibilidad.get(selected_str, {}).get("horarios", [])
        selected_slots = st.multiselect(
            "Horarios", slots, default=default_slots,
            placeholder="Elige uno o más horarios...",
        )

        st.markdown("##### ➕ Agregar horario personalizado")
        c1, c2 = st.columns([2, 1])
        with c1:
            custom_time = st.text_input("Hora (HH:MM)", placeholder="ej. 13:45")
        with c2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Agregar"):
                try:
                    datetime.strptime(custom_time, "%H:%M")
                    if custom_time not in selected_slots:
                        selected_slots.append(custom_time)
                        st.success(f"Horario {custom_time} añadido.")
                except ValueError:
                    st.error("Formato inválido. Usa HH:MM")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    save_col, _ = st.columns([1, 3])
    with save_col:
        if st.button("💾 Guardar configuración", use_container_width=True):
            if not selected_slots:
                st.error("Selecciona al menos un horario.")
            else:
                upsert_disponibilidad(db, selected_str, int(num_mesas), selected_slots)
                st.success(
                    f"✅ Guardado para {selected_label}: "
                    f"{num_mesas} mesas en {len(selected_slots)} horarios."
                )
                st.rerun()

with tab2:
    st.markdown("### Disponibilidad configurada")
    disponibilidad = get_disponibilidad(db)
    todas_reservas = get_all_reservations(db)

    if not disponibilidad:
        st.info("Aún no has configurado ningún día.")
    else:
        today_str = date.today().isoformat()

        for date_str in sorted(disponibilidad.keys()):
            cfg = disponibilidad[date_str]
            d = date.fromisoformat(date_str)
            label = date_label(d)
            is_past = date_str < today_str
            total_res = sum(count_reservations(db, date_str, s) for s in cfg["horarios"])

            reservas_dia = [
                r for r in todas_reservas
                if r.get("fecha") == date_str
            ]
            reservas_dia = sorted(reservas_dia, key=lambda x: x.get("horario", ""))

            with st.expander(
                f"{'⏳' if is_past else '📅'} {label}  —  "
                f"{cfg['mesas']} mesas  |  {len(cfg['horarios'])} turnos  |  {total_res} reservas",
                expanded=not is_past,
            ):
                st.markdown("#### Disponibilidad por horario")
                slot_cols = st.columns(min(max(len(cfg["horarios"]), 1), 4))

                for i, slot in enumerate(sorted(cfg["horarios"])):
                    res_count = count_reservations(db, date_str, slot)
                    available = cfg["mesas"] - res_count
                    with slot_cols[i % 4]:
                        st.markdown(f"""
                        <div class="metric-box" style="margin-bottom:0.6rem">
                            <div style="font-size:1rem;color:#e6f7f7;font-weight:500">{slot}</div>
                            <div class="num" style="font-size:1.5rem">{available}</div>
                            <div class="label">mesas libres</div>
                            <div style="font-size:0.7rem;color:#8fdfe0;margin-top:2px">{res_count} reservadas</div>
                        </div>
                        """, unsafe_allow_html=True)

                st.markdown('<hr class="divider">', unsafe_allow_html=True)
                st.markdown("#### 👥 Reservaciones")

                if not reservas_dia:
                    st.caption("No hay reservaciones para este día.")
                else:
                    for r in reservas_dia:
                        nombre = r.get("nombre", "Sin nombre")
                        horario = r.get("horario", "Sin horario")
                        codigo = r.get("id", "—")
                        notas = r.get("notas", "")

                        notas_html = f"<br><strong>📝 Notas:</strong> {notas}" if notas else ""

                        col_info, col_action = st.columns([5, 1])

                        with col_info:
                            st.markdown(f"""
                            <div class="reservation-card">
                                <div class="reservation-name">{nombre}</div>
                                <div class="reservation-extra">
                                    Código: <strong>{codigo}</strong> &nbsp;|&nbsp;
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                        with col_action:
                            st.markdown("<br>", unsafe_allow_html=True)
                            if st.button("🗑️ Eliminar", key=f"delete_res_{codigo}", use_container_width=True):
                                delete_reservation(db, codigo)
                                st.success(f"Reservación {codigo} eliminada.")
                                st.rerun()

                a1, a2, _ = st.columns([1, 1, 3])
                with a1:
                    if st.button("✏️ Editar", key=f"edit_{date_str}"):
                        st.info(f"Ve a 'Configurar' y selecciona {label}.")
                with a2:
                    if st.button("🗑️ Eliminar día", key=f"del_{date_str}"):
                        delete_disponibilidad(db, date_str)
                        st.rerun()

st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.caption("🍽️ Sistema de Reservaciones · Panel Administrativo")