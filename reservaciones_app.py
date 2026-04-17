import streamlit as st
import uuid
from datetime import date, datetime
from db import (
    get_db, get_disponibilidad,
    count_reservations, insert_reservation,
)

# ── Config ────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Reserva tu Mesa",
    page_icon="🪑",
    layout="centered",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=Outfit:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }
h1, h2, h3 { font-family: 'Cormorant Garamond', serif !important; }

/* ── Fondo general ── */
.stApp {
    background: linear-gradient(135deg, #1f1f1f 0%, #2b2b2b 50%, #1f1f1f 100%);
    color: #e6f7f7;
}

/* ── Hero principal ── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    background: linear-gradient(180deg, #181818 0%, #242424 100%);
    border: 1px solid rgba(0, 207, 209, 0.30);
    border-radius: 16px;
    margin-bottom: 2rem;
    color: #e6f7f7;
    box-shadow: 0 6px 24px rgba(0,0,0,0.25);
}
.hero h1 {
    font-size: 2.8rem !important;
    font-weight: 700;
    color: #00e5e7 !important;
    margin-bottom: 0.3rem;
}
.hero p {
    color: #9adfe0;
    font-size: 1rem;
    font-weight: 300;
}

/* ── Tarjetas ── */
.step-card {
    background: #242424;
    border: 1px solid rgba(0, 207, 209, 0.25);
    border-radius: 14px;
    padding: 1.8rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.18);
}
.step-label {
    font-size: 0.7rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #00cfd1;
    margin-bottom: 0.4rem;
}

/* ── Estados de disponibilidad ── */
.avail-ok {
    display: inline-block;
    background: rgba(0, 207, 209, 0.12);
    border: 1px solid rgba(0, 207, 209, 0.45);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.82rem;
    color: #aef6f7;
    font-weight: 500;
}
.avail-none {
    display: inline-block;
    background: rgba(120, 120, 120, 0.18);
    border: 1px solid rgba(180, 180, 180, 0.35);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.82rem;
    color: #d0d0d0;
    font-weight: 500;
}

/* ── Resumen ── */
.summary {
    background: linear-gradient(135deg, #181818, #252525);
    border: 1px solid rgba(0, 207, 209, 0.25);
    border-radius: 14px;
    padding: 1.5rem 2rem;
    color: #e6f7f7;
    margin: 1rem 0;
}
.summary .row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.4rem;
    font-size: 0.92rem;
}
.summary .row .lbl { color: #91d7d8; }
.summary .row .val {
    font-weight: 500;
    color: #00e5e7;
}

/* ── Confirmación ── */
.confirm-box {
    background: linear-gradient(135deg, #181818, #252525);
    border: 1px solid rgba(0, 207, 209, 0.35);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    color: #e6f7f7;
    box-shadow: 0 6px 24px rgba(0,0,0,0.20);
}
.confirm-box .check {
    font-size: 3rem;
    margin-bottom: 0.5rem;
}
.confirm-box h2 {
    color: #00e5e7 !important;
    font-size: 1.8rem !important;
}
.confirm-box .code {
    font-family: monospace;
    font-size: 1.1rem;
    color: #00e5e7;
    background: rgba(0, 207, 209, 0.10);
    border: 1px solid rgba(0, 207, 209, 0.30);
    padding: 6px 16px;
    border-radius: 8px;
    display: inline-block;
    margin-top: 0.5rem;
}

/* ── Inputs ── */
.stTextInput input, .stNumberInput input {
    background: rgba(255,255,255,0.04) !important;
    border: 1.5px solid rgba(0, 207, 209, 0.35) !important;
    border-radius: 10px !important;
    color: #e6f7f7 !important;
}

/* ── Selects ── */
.stSelectbox > div > div {
    background: #242424 !important;
    border: 1px solid rgba(0, 207, 209, 0.30) !important;
    border-radius: 10px !important;
    color: #e6f7f7 !important;
}

/* ── Botones ── */
.stButton > button {
    background: linear-gradient(135deg, #00cfd1, #00a8aa) !important;
    color: #0f0f0f !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 10px !important;
    font-size: 1rem !important;
    padding: 0.6rem 2rem !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
    width: 100% !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0, 207, 209, 0.35) !important;
}

/* ── Divider ── */
.divider {
    border: none;
    border-top: 1px solid rgba(0, 207, 209, 0.20);
    margin: 1.2rem 0;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ──────────────────────────────────────────────────────────────────
def date_label(date_str: str) -> str:
    d = date.fromisoformat(date_str)
    dias  = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
    meses = ["","enero","febrero","marzo","abril","mayo","junio",
             "julio","agosto","septiembre","octubre","noviembre","diciembre"]
    return f"{dias[d.weekday()]} {d.day} de {meses[d.month]}"


# ── Connect ──────────────────────────────────────────────────────────────────
try:
    db = get_db()
except Exception as e:
    st.error(f"❌ No se pudo conectar a MongoDB: {e}")
    st.stop()

# ── State ────────────────────────────────────────────────────────────────────
if "step"    not in st.session_state: st.session_state.step    = 1
if "booking" not in st.session_state: st.session_state.booking = {}

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🪑 Reserva tu Mesa</h1>
    <p>Elige el día y horario que más te convenga</p>
</div>
""", unsafe_allow_html=True)

# ── Load availability ─────────────────────────────────────────────────────────
disponibilidad = get_disponibilidad(db)
today_str      = date.today().isoformat()
future_dates   = {k: v for k, v in disponibilidad.items() if k >= today_str}

if not future_dates:
    st.info("⏳ Aún no hay disponibilidad publicada. Por favor vuelve pronto.")
    st.stop()


# ═══ STEP 1 – Elegir fecha y horario ═════════════════════════════════════════
if st.session_state.step == 1:

    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-label">Paso 1 · Elige cuándo</div>', unsafe_allow_html=True)

    date_options    = {date_label(k): k for k in sorted(future_dates.keys())}
    chosen_label    = st.selectbox("📅 Selecciona la fecha", list(date_options.keys()))
    chosen_date_str = date_options[chosen_label]
    cfg             = future_dates[chosen_date_str]

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("**🕐 Horarios disponibles**")

    slots_info = [
        (slot, cfg["mesas"] - count_reservations(db, chosen_date_str, slot))
        for slot in sorted(cfg["horarios"])
    ]

    pills_html = "".join(
        f'<span class="avail-ok">🟢 {s} &nbsp;·&nbsp; {av} mesa{"s" if av!=1 else ""} libre{"s" if av!=1 else ""}</span> '
        if av > 0 else
        f'<span class="avail-none">🔴 {s} &nbsp;·&nbsp; Lleno</span> '
        for s, av in slots_info
    )
    st.markdown(pills_html + "<br><br>", unsafe_allow_html=True)

    available_slots = [s for s, av in slots_info if av > 0]
    if not available_slots:
        st.error("😔 No hay mesas disponibles en esta fecha. Elige otra.")
    else:
        slot_labels   = {f"{s} ({av} {'mesa' if av==1 else 'mesas'} libre{'s' if av!=1 else ''})": s
                         for s, av in slots_info if av > 0}
        chosen_slot_l = st.selectbox("Horario", list(slot_labels.keys()))
        chosen_slot   = slot_labels[chosen_slot_l]

        st.markdown("</div>", unsafe_allow_html=True)
        if st.button("Continuar →"):
            st.session_state.booking = {
                "fecha":       chosen_date_str,
                "fecha_label": date_label(chosen_date_str),
                "horario":     chosen_slot,
            }
            st.session_state.step = 2
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ═══ STEP 2 – Datos del cliente ═══════════════════════════════════════════════
elif st.session_state.step == 2:
    b = st.session_state.booking

    st.markdown(f"""
    <div class="summary">
        <div class="row"><span class="lbl">Fecha</span><span class="val">{b['fecha_label']}</span></div>
        <div class="row"><span class="lbl">Horario</span><span class="val">{b['horario']} hrs</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-label">Paso 2 · Tus datos</div>', unsafe_allow_html=True)

    nombre   = st.text_input("👤 Nombre",   placeholder="Comisario Yarrick")
    notas    = st.text_input("📝 Juego",
                              placeholder="40k, kill team, legion....")

    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("← Regresar"):
            st.session_state.step = 1
            st.rerun()
    with c2:
        if st.button("Confirmar reservación ✓"):
            if not nombre.strip():
                st.error("Por favor ingresa tu nombre.")
            else:
                # Race-condition check
                cfg  = get_disponibilidad(db).get(b["fecha"], {})
                used = count_reservations(db, b["fecha"], b["horario"])
                if used >= cfg.get("mesas", 0):
                    st.error("😔 Esta mesa acaba de ser reservada. Por favor elige otro horario.")
                    st.session_state.step = 1
                    st.rerun()
                else:
                    booking_id = uuid.uuid4().hex[:8].upper()
                    insert_reservation(db, {
                        "id":         booking_id,
                        "fecha":      b["fecha"],
                        "horario":    b["horario"],
                        "nombre":     nombre.strip(),
                        "notas":      notas.strip(),
                        "estado":     "confirmada",
                        "creada_en":  datetime.now().isoformat(),
                    })
                    st.session_state.booking.update({
                        "id":       booking_id,
                        "nombre":   nombre.strip(),
                    })
                    st.session_state.step = 3
                    st.rerun()


# ═══ STEP 3 – Confirmación ════════════════════════════════════════════════════
elif st.session_state.step == 3:
    b = st.session_state.booking
    st.markdown(f"""
    <div class="confirm-box">
        <div class="check">🎉</div>
        <h2>¡Reservación confirmada!</h2>
        <p style="color:#b7e4c7;margin-top:0.5rem">
            Hola <strong>{b['nombre']}</strong>, te esperamos el<br>
            <strong style="color:#95d5b2">{b['fecha_label']}</strong> a las
            <strong style="color:#95d5b2">{b['horario']} hrs</strong>.
        </p>
        <div style="margin-top:1rem;color:#74c69d;font-size:0.85rem">Tu código de reserva:</div>
        <div class="code">{b['id']}</div>
        <p style="font-size:0.78rem;color:#74c69d;margin-top:1rem">
            Guarda este código — te lo pediremos al llegar.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Hacer otra reservación"):
        st.session_state.step    = 1
        st.session_state.booking = {}
        st.rerun()

st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.caption("🪑 Sistema de Reservaciones · ¿Preguntas? Contáctanos directamente.")