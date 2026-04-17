import streamlit as st
import uuid
from datetime import date, datetime
from db import (
    get_db, get_disponibilidad,
    count_reservations, insert_reservation,
    get_all_reservations,
)
from ui import set_page, render_brand_header

# ── Config ────────────────────────────────────────────────────────────────────
set_page(
    page_title="Reserva tu Mesa",
    layout="centered",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=Outfit:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }
h1, h2, h3 { font-family: 'Cormorant Garamond', serif !important; }

.stApp {
    background: linear-gradient(135deg, #1f1f1f 0%, #2b2b2b 50%, #1f1f1f 100%);
    color: #e6f7f7;
}

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

.confirm-box {
    background: linear-gradient(135deg, #181818, #252525);
    border: 1px solid rgba(0, 207, 209, 0.35);
    border-radius: 16px;
    padding: 1.6rem;
    text-align: center;
    color: #e6f7f7;
    box-shadow: 0 6px 24px rgba(0,0,0,0.20);
    max-width: 100%;
}
.confirm-box .check {
    font-size: 3rem;
    margin-bottom: 0.4rem;
}
.confirm-box h2 {
    color: #00e5e7 !important;
    font-size: 1.7rem !important;
    margin-bottom: 0.6rem;
}

.agenda-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(0, 207, 209, 0.22);
    border-radius: 12px;
    padding: 0.9rem 1rem;
    margin-bottom: 0.7rem;
}
.agenda-title {
    font-weight: 700;
    font-size: 1rem;
    color: #00e5e7;
    margin-bottom: 0.25rem;
}
.agenda-meta {
    font-size: 0.88rem;
    color: #d8f4f4;
    line-height: 1.6;
}
.agenda-extra {
    font-size: 0.78rem;
    color: #8fdfe0;
    margin-top: 0.35rem;
}

.stTextInput input, .stNumberInput input {
    background: rgba(255,255,255,0.04) !important;
    border: 1.5px solid rgba(0, 207, 209, 0.35) !important;
    border-radius: 10px !important;
    color: #e6f7f7 !important;
}

.stSelectbox > div > div {
    background: #242424 !important;
    border: 1px solid rgba(0, 207, 209, 0.30) !important;
    border-radius: 10px !important;
    color: #e6f7f7 !important;
}

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

.divider {
    border: none;
    border-top: 1px solid rgba(0, 207, 209, 0.20);
    margin: 1.2rem 0;
}

@media (max-width: 640px) {
    .confirm-box {
        padding: 1.2rem;
        border-radius: 12px;
    }

    .confirm-box .check {
        font-size: 2.2rem;
    }

    .confirm-box h2 {
        font-size: 1.3rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

# ── Helpers ──────────────────────────────────────────────────────────────────
def date_label(date_str: str) -> str:
    d = date.fromisoformat(date_str)
    dias = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
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
if "step" not in st.session_state:
    st.session_state.step = 1
if "booking" not in st.session_state:
    st.session_state.booking = {}

# ── Header ───────────────────────────────────────────────────────────────────
render_brand_header(
    title="The Guild",
    subtitle="Reserva tu mesa y consulta partidas agendadas",
)

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>♟ Reserva tu Mesa</h1>
    <p>Elige el día y horario que más te convenga</p>
</div>
""", unsafe_allow_html=True)

# ── Load availability ─────────────────────────────────────────────────────────
disponibilidad = get_disponibilidad(db)
todas_reservas = get_all_reservations(db)
today_str = date.today().isoformat()
future_dates = {k: v for k, v in disponibilidad.items() if k >= today_str}

if not future_dates:
    st.info("⏳ Aún no hay disponibilidad publicada. Por favor vuelve pronto.")
    st.stop()

tab1, tab2 = st.tabs(["🪑 Reservar mesa", "🎲 Partidas agendadas"])

# ═══ TAB 1 – Reservar ════════════════════════════════════════════════════════
with tab1:
    if st.session_state.step == 1:

        st.markdown('<div class="step-card">', unsafe_allow_html=True)
        st.markdown('<div class="step-label">Paso 1 · Elige cuándo</div>', unsafe_allow_html=True)

        date_options = {date_label(k): k for k in sorted(future_dates.keys())}
        chosen_label = st.selectbox("📅 Selecciona la fecha", list(date_options.keys()))
        chosen_date_str = date_options[chosen_label]
        cfg = future_dates[chosen_date_str]

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
            slot_labels = {
                f"{s} ({av} {'mesa' if av==1 else 'mesas'} libre{'s' if av!=1 else ''})": s
                for s, av in slots_info if av > 0
            }
            chosen_slot_l = st.selectbox("Horario", list(slot_labels.keys()))
            chosen_slot = slot_labels[chosen_slot_l]

            st.markdown("</div>", unsafe_allow_html=True)
            if st.button("Continuar →"):
                st.session_state.booking = {
                    "fecha": chosen_date_str,
                    "fecha_label": date_label(chosen_date_str),
                    "horario": chosen_slot,
                }
                st.session_state.step = 2
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

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

        nombre = st.text_input("👤 Nombre", placeholder="Comisario Yarrick")
        rival = st.text_input("⚔️ Rival", placeholder="Ghazghkull")
        notas = st.text_input("📝 Juego", placeholder="40k, Kill Team, Legion...")

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
                    cfg = get_disponibilidad(db).get(b["fecha"], {})
                    used = count_reservations(db, b["fecha"], b["horario"])
                    if used >= cfg.get("mesas", 0):
                        st.error("😔 Esta mesa acaba de ser reservada. Por favor elige otro horario.")
                        st.session_state.step = 1
                        st.rerun()
                    else:
                        booking_id = uuid.uuid4().hex[:8].upper()
                        insert_reservation(db, {
                            "id": booking_id,
                            "fecha": b["fecha"],
                            "horario": b["horario"],
                            "nombre": nombre.strip(),
                            "rival": rival.strip(),
                            "notas": notas.strip(),
                            "estado": "confirmada",
                            "creada_en": datetime.now().isoformat(),
                        })
                        st.session_state.booking.update({
                            "id": booking_id,
                            "nombre": nombre.strip(),
                            "rival": rival.strip(),
                            "notas": notas.strip(),
                        })
                        st.session_state.step = 3
                        st.rerun()

    elif st.session_state.step == 3:
        b = st.session_state.booking

        st.markdown('<div class="confirm-box">', unsafe_allow_html=True)
        st.markdown('<div class="check">🎉</div>', unsafe_allow_html=True)
        st.markdown('<h2>¡Reservación confirmada!</h2>', unsafe_allow_html=True)

        st.markdown(
            f"""
            <div style="margin-top:0.5rem; line-height:1.6; font-size:1rem;">
                Hola <strong>{b['nombre']}</strong>,<br>
                te esperamos el<br>
                <strong style="color:#00e5e7">{b['fecha_label']}</strong><br>
                a las <strong style="color:#00e5e7">{b['horario']} hrs</strong>.
            </div>
            """,
            unsafe_allow_html=True,
        )

        if b.get("notas") or b.get("rival"):
            extras = []
            if b.get("notas"):
                extras.append(f"🎲 Juego: <strong>{b['notas']}</strong>")
            if b.get("rival"):
                extras.append(f"⚔️ Rival: <strong>{b['rival']}</strong>")

            st.markdown(
                f"""
                <div style="
                    margin-top:0.8rem;
                    padding:0.6rem 0.8rem;
                    background: rgba(0,207,209,0.08);
                    border:1px solid rgba(0,207,209,0.25);
                    border-radius:10px;
                    font-size:0.95rem;
                    line-height:1.7;
                ">
                    {'<br>'.join(extras)}
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            """
            <div style="
                margin-top:1rem;
                font-size:0.85rem;
                color:#8fdfe0;
            ">
                💬 Solo da tu nombre al llegar y listo.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Hacer otra reservación"):
            st.session_state.step = 1
            st.session_state.booking = {}
            st.rerun()

# ═══ TAB 2 – Partidas agendadas ══════════════════════════════════════════════
with tab2:
    st.markdown("### 🎲 Partidas agendadas")
    st.caption("Consulta qué enfrentamientos ya están organizados y cuántas mesas quedan disponibles por horario.")

    reservas_activas = [
        r for r in todas_reservas
        if r.get("estado") != "cancelada" and r.get("fecha", "") >= today_str
    ]

    if not reservas_activas:
        st.info("Aún no hay partidas agendadas para las próximas fechas.")
    else:
        for date_str in sorted(future_dates.keys()):
            cfg = future_dates[date_str]
            reservas_dia = sorted(
                [r for r in reservas_activas if r.get("fecha") == date_str],
                key=lambda x: x.get("horario", "")
            )

            total_res = sum(count_reservations(db, date_str, s) for s in cfg["horarios"])

            with st.expander(
                f"📅 {date_label(date_str)}  —  {len(cfg['horarios'])} turnos  |  {total_res} reservaciones",
                expanded=False,
            ):
                st.markdown("#### Disponibilidad por horario")
                slot_cols = st.columns(min(max(len(cfg["horarios"]), 1), 3))

                for i, slot in enumerate(sorted(cfg["horarios"])):
                    res_count = count_reservations(db, date_str, slot)
                    available = cfg["mesas"] - res_count

                    with slot_cols[i % 3]:
                        st.markdown(f"""
                        <div class="agenda-card">
                            <div class="agenda-title">{slot}</div>
                            <div class="agenda-meta">
                                🪑 Mesas totales: <strong>{cfg['mesas']}</strong><br>
                                ✅ Libres: <strong>{available}</strong><br>
                                🎟 Reservadas: <strong>{res_count}</strong>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                st.markdown('<hr class="divider">', unsafe_allow_html=True)
                st.markdown("#### Enfrentamientos registrados")

                if not reservas_dia:
                    st.caption("No hay partidas registradas para este día todavía.")
                else:
                    for r in reservas_dia:
                        nombre = r.get("nombre", "Jugador")
                        rival = r.get("rival", "").strip()
                        horario = r.get("horario", "Sin horario")
                        juego = r.get("notas", "").strip()

                        juego_texto = juego if juego else "Juego por definir"
                        rival_texto = rival if rival else "Rival por definir"

                        st.markdown(f"""
                        <div class="agenda-card">
                            <div class="agenda-title">🎲 {juego_texto}</div>
                            <div class="agenda-meta">
                                👤 Jugador: <strong>{nombre}</strong><br>
                                ⚔️ Rival: <strong>{rival_texto}</strong><br>
                                🕐 Horario: <strong>{horario}</strong>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.caption("♟ The Guild · ¿Preguntas? Contáctanos directamente.")