
import streamlit as st
import datetime

from main import (
    connect_calendar,
    get_today_events,
    get_timed_events,
    detect_free_time,
)

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Smart Calendar AI",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ================= PROFESSIONAL CSS =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #080d1b 0%, #101a32 55%, #11112b 100%);
    color: #f1f5f9;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.8rem;
    padding-bottom: 2rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #151b3b, #10172b);
    border-right: 1px solid #303b62;
}

[data-testid="stSidebar"] * {
    color: #e2e8f0;
}

h1, h2, h3 {
    color: #f8fafc !important;
}

p, label {
    color: #cbd5e1;
}

.hero {
    background: linear-gradient(120deg, #222b60, #38246f, #173c67);
    border: 1px solid #6257b9;
    border-radius: 22px;
    padding: 30px;
    margin-bottom: 25px;
    box-shadow: 0 10px 35px rgba(75, 65, 180, 0.18);
}

.hero-title {
    font-size: 35px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 8px;
}

.hero-subtitle {
    font-size: 15px;
    color: #d7ddff;
}

.hero-tag {
    display: inline-block;
    background: rgba(74, 222, 128, 0.13);
    border: 1px solid #4ade80;
    color: #86efac;
    padding: 7px 13px;
    border-radius: 25px;
    font-size: 13px;
    font-weight: 600;
}

div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #1b2946, #172039);
    border: 1px solid #34486d;
    border-radius: 17px;
    padding: 20px;
    box-shadow: 0 7px 20px rgba(0, 0, 0, 0.15);
}

div[data-testid="stMetricLabel"] {
    color: #bdc9e4;
}

div[data-testid="stMetricValue"] {
    color: #ffffff;
    font-size: 29px;
}

.panel {
    background: rgba(19, 30, 54, 0.94);
    border: 1px solid #2b3d60;
    border-radius: 17px;
    padding: 20px;
    margin-bottom: 15px;
}

.event-card {
    background: linear-gradient(100deg, #1c3159, #192644);
    border: 1px solid #35558b;
    border-left: 5px solid #60a5fa;
    border-radius: 12px;
    padding: 15px;
    margin: 12px 0;
}

.conflict-card {
    background: #321d30;
    border: 1px solid #87425c;
    border-left: 5px solid #fb7185;
    border-radius: 12px;
    padding: 15px;
    margin: 12px 0;
}

.free-card {
    background: #142e2d;
    border: 1px solid #2d6359;
    border-left: 5px solid #34d399;
    border-radius: 12px;
    padding: 13px;
    margin: 10px 0;
}

.event-title {
    font-size: 16px;
    font-weight: 700;
    color: #f8fafc;
}

.event-time {
    color: #b8c9e8;
    font-size: 13px;
    margin-top: 5px;
}

.muted {
    color: #9eafd0;
    font-size: 13px;
}

div.stButton > button {
    background: linear-gradient(100deg, #635bdf, #4778e8);
    color: white;
    border: 1px solid #7e83f5;
    border-radius: 11px;
    font-weight: 700;
    padding: 10px 15px;
    transition: 0.2s;
}

div.stButton > button:hover {
    background: linear-gradient(100deg, #7c73fa, #5b96ff);
    color: white;
    border-color: #a5b4fc;
}

hr {
    border-color: #2b3a58;
}

#MainMenu, footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("## 📅 Smart Calendar")
    st.caption("Your day. Your schedule. Your control.")
    st.divider()

    st.markdown("### 🧭 NAVIGATION")
    section = st.radio(
        "Go to",
        [
            "🏠 Dashboard",
            "📆 Today's Schedule",
            "⚠️ Conflicts",
            "⏰ Free Time",
        ],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("### ✨ PRODUCTIVITY")
    st.caption("Stay organized and keep track of your day.")

    refresh = st.button(
        "🔄 Refresh Calendar",
        use_container_width=True,
    )

    st.divider()
    st.markdown(
        "<div class='muted'>SMART CALENDAR AI<br>"
        "Work Smarter, Not Harder ✨</div>",
        unsafe_allow_html=True,
    )

if refresh:
    st.rerun()


# ================= HEADER =================
today = datetime.date.today()

st.markdown(
    f"""
    <div class="hero">
        <div class="hero-tag">● YOUR CALENDAR DASHBOARD</div>
        <div class="hero-title">📅 Smart Calendar AI</div>
        <div class="hero-subtitle">
            Your personal calendar and productivity assistant.
            <br><br>
            📍 {today.strftime("%A, %d %B %Y")}
            &nbsp; • &nbsp; Plan your day with clarity.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ================= GOOGLE CALENDAR DATA =================
try:
    service = connect_calendar()
    events = get_today_events(service)
    timed_events = get_timed_events(events)

    # Detect overlapping timed events
    conflicts = []

    for i, first in enumerate(timed_events):
        for second in timed_events[i + 1:]:
            if second["start"] >= first["end"]:
                break

            overlap_start = max(first["start"], second["start"])
            overlap_end = min(first["end"], second["end"])

            if overlap_start < overlap_end:
                conflicts.append({
                    "first": first["title"],
                    "second": second["title"],
                    "start": overlap_start,
                    "end": overlap_end,
                })

    # Free slots of at least 15 minutes
    free_slots = [
        (start, end)
        for start, end in detect_free_time(events)
        if (end - start).total_seconds() >= 15 * 60
    ]

    total_free_minutes = sum(
        int((end - start).total_seconds() / 60)
        for start, end in free_slots
    )

    # ================= METRIC CARDS =================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="📅 Today's Events",
            value=len(events),
        )

    with col2:
        st.metric(
            label="⚠️ Scheduling Conflicts",
            value=len(conflicts),
            delta="Needs attention" if conflicts else "All clear",
            delta_color="inverse" if conflicts else "normal",
        )

    with col3:
        st.metric(
            label="⏰ Available Free Time",
            value=f"{total_free_minutes // 60}h "
                  f"{total_free_minutes % 60}m",
        )

    st.divider()

    # ================= DASHBOARD VIEW =================
    if section == "🏠 Dashboard":
        left, right = st.columns([1.1, 0.9], gap="large")

        with left:
            st.markdown("### 📆 Today's Schedule")

            if events:
                for event in events:
                    title = event.get("summary", "Untitled Event")
                    start_data = event.get("start", {})
                    end_data = event.get("end", {})

                    if "dateTime" in start_data:
                        start_time = datetime.datetime.fromisoformat(
                            start_data["dateTime"].replace("Z", "+00:00")
                        ).astimezone()

                        time_text = start_time.strftime("%I:%M %p")

                        if "dateTime" in end_data:
                            end_time = datetime.datetime.fromisoformat(
                                end_data["dateTime"].replace("Z", "+00:00")
                            ).astimezone()
                            time_text += " – " + end_time.strftime("%I:%M %p")
                    else:
                        time_text = "All-day event"

                    st.markdown(
                        f"""
                        <div class="event-card">
                            <div class="event-title">📌 {title}</div>
                            <div class="event-time">🕒 {time_text}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                st.info("No events scheduled for today.")

        with right:
            st.markdown("### ⚠️ Conflict Monitor")

            if conflicts:
                for conflict in conflicts:
                    overlap_text = (
                        f"{conflict['start'].strftime('%I:%M %p')} – "
                        f"{conflict['end'].strftime('%I:%M %p')}"
                    )

                    st.markdown(
                        f"""
                        <div class="conflict-card">
                            <div class="event-title">
                                🚨 Scheduling Conflict
                            </div>
                            <div class="event-time">
                                {conflict['first']}<br>
                                overlaps with<br>
                                {conflict['second']}<br><br>
                                ⏱️ {overlap_text}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                st.success("✅ No scheduling conflicts found.")

            st.markdown("### ⏰ Available Free Time")

            if free_slots:
                for start, end in free_slots:
                    st.markdown(
                        f"""
                        <div class="free-card">
                            <div class="event-title">🌿 Free Time</div>
                            <div class="event-time">
                                {start.strftime('%I:%M %p')}
                                – {end.strftime('%I:%M %p')}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                st.info("No free slots of at least 15 minutes.")

    # ================= SCHEDULE VIEW =================
    elif section == "📆 Today's Schedule":
        st.markdown("### 📆 Your Complete Schedule")

        if events:
            for event in events:
                title = event.get("summary", "Untitled Event")
                start_data = event.get("start", {})
                end_data = event.get("end", {})

                if "dateTime" in start_data:
                    start_time = datetime.datetime.fromisoformat(
                        start_data["dateTime"].replace("Z", "+00:00")
                    ).astimezone()

                    time_text = start_time.strftime("%I:%M %p")

                    if "dateTime" in end_data:
                        end_time = datetime.datetime.fromisoformat(
                            end_data["dateTime"].replace("Z", "+00:00")
                        ).astimezone()
                        time_text += " – " + end_time.strftime("%I:%M %p")
                else:
                    time_text = "All-day event"

                st.markdown(
                    f"""
                    <div class="event-card">
                        <div class="event-title">📌 {title}</div>
                        <div class="event-time">🕒 {time_text}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("No events scheduled for today.")

    # ================= CONFLICT VIEW =================
    elif section == "⚠️ Conflicts":
        st.markdown("### ⚠️ Scheduling Conflict Report")

        if conflicts:
            st.warning(f"{len(conflicts)} scheduling conflict(s) detected.")

            for conflict in conflicts:
                overlap_text = (
                    f"{conflict['start'].strftime('%I:%M %p')} – "
                    f"{conflict['end'].strftime('%I:%M %p')}"
                )

                st.markdown(
                    f"""
                    <div class="conflict-card">
                        <div class="event-title">🚨 Overlapping Events</div>
                        <div class="event-time">
                            {conflict['first']}<br>
                            {conflict['second']}<br><br>
                            ⏱️ Overlap: {overlap_text}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.success("🎉 No scheduling conflicts found!")

    # ================= FREE TIME VIEW =================
    elif section == "⏰ Free Time":
        st.markdown("### ⏰ Your Available Time")

        st.caption(
            "Free slots are calculated from your calendar "
            "using the existing 9 AM – 6 PM time window."
        )

        if free_slots:
            for start, end in free_slots:
                duration = int((end - start).total_seconds() / 60)

                st.markdown(
                    f"""
                    <div class="free-card">
                        <div class="event-title">🌿 Available Slot</div>
                        <div class="event-time">
                            🕒 {start.strftime('%I:%M %p')}
                            – {end.strftime('%I:%M %p')}<br>
                            ⏳ Duration: {duration // 60}h {duration % 60}m
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("No free slots of at least 15 minutes.")

    # ================= FOOTER =================
    st.divider()
    st.markdown(
        "<div style='text-align:center; color:#91a4c5; "
        "padding:12px;'>💜 Smart Calendar AI &nbsp; | &nbsp; "
        "Work Smarter, Not Harder</div>",
        unsafe_allow_html=True,
    )

except Exception as error:
    st.error("Could not load Google Calendar.")
    st.caption(
        "Check your internet connection and Google Calendar login."
    )
    st.exception(error)
