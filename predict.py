import streamlit as st
import pandas as pd

# 1. SETUP PAGE
st.set_page_config(page_title="IPL 2026 Playoff Tracker", layout="wide")

# 2. INITIAL DATA (Current standings as of April 30, 2026)
if 'df' not in st.session_state:
    data = {
        'Team': ['SRH', 'PBKS', 'RCB', 'RR', 'GT', 'CSK', 'DC', 'KKR', 'MI', 'LSG'],
        'P': [11, 10, 9, 10, 10, 10, 10, 9, 10, 9],
        'W': [7, 6, 6, 6, 6, 5, 4, 3, 3, 2],
        'L': [4, 3, 3, 4, 4, 5, 6, 5, 7, 7],
        'NR': [0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
        'Pts': [14, 13, 12, 12, 12, 10, 8, 7, 6, 4],
        'NRR': [0.737, 0.571, 1.420, 0.510, -0.147, 0.151, -0.949, -0.539, -0.649, -1.076]
    }
    st.session_state.df = pd.DataFrame(data).set_index('Team')
    st.session_state.match_index = 0

# 3. FIXTURES LIST
fixtures = [
    ("May 07", "LSG", "RCB"), ("May 08", "DC", "KKR"),
    ("May 09", "RR", "GT"), ("May 10", "CSK", "LSG"), ("May 10", "RCB", "MI"),
    ("May 11", "PBKS", "DC"), ("May 12", "GT", "SRH"), ("May 13", "RCB", "KKR"),
    ("May 14", "PBKS", "MI"), ("May 15", "LSG", "CSK"), ("May 16", "KKR", "GT"),
    ("May 17", "PBKS", "RCB"), ("May 17", "DC", "RR"), ("May 18", "CSK", "SRH"),
    ("May 19", "RR", "LSG"), ("May 20", "KKR", "MI"), ("May 21", "GT", "CSK"),
    ("May 22", "SRH", "RCB"), ("May 23", "LSG", "PBKS"), ("May 24", "MI", "RR"),
    ("May 24", "KKR", "DC")
]

st.title("🏏 IPL 2026: Playoff Scenarios")

# 4. PREDICTION WIDGET
if st.session_state.match_index < len(fixtures):
    date, t1, t2 = fixtures[st.session_state.match_index]
    st.info(f"📅 **Next Match:** {date} — {t1} vs {t2}")

    winner = st.radio("Winner:", [t1, t2, "NR"], horizontal=True)

    if st.button("Confirm Result"):
        if winner == "NR":
            st.session_state.df.loc[t1, ['P', 'NR', 'Pts']] += [1, 1, 1]
            st.session_state.df.loc[t2, ['P', 'NR', 'Pts']] += [1, 1, 1]
        else:
            loser = t2 if winner == t1 else t1
            st.session_state.df.loc[winner, ['P', 'W', 'Pts']] += [1, 1, 2]
            st.session_state.df.loc[loser, ['P', 'L']] += [1, 1]
        st.session_state.match_index += 1
        st.rerun()
else:
    st.success("Season Predictions Complete!")
    if st.button("Reset Tournament"):
        st.session_state.clear()
        st.rerun()

# 5. QUALIFICATION & ELIMINATION LOGIC
df = st.session_state.df.copy()
df_sorted = df.sort_values(by=['Pts', 'NRR'], ascending=False)
sorted_index = df_sorted.index.tolist()

def get_status_name(team_name):
    row = df.loc[team_name]
    # Total games in IPL league stage is 14
    matches_remaining = 14 - row['P']
    max_pts = row['Pts'] + (matches_remaining * 2)

    # Thresholds
    fourth_place_pts = df_sorted.iloc[3]['Pts']
    fifth_place_team = df_sorted.iloc[4]
    fifth_place_max = fifth_place_team['Pts'] + (14 - fifth_place_team['P']) * 2

    # --- NEW LOGIC FOR FINAL STANDINGS ---
    # 1. If season is complete (Match 14), Top 4 are (Q), others are (E)
    if row['P'] == 14:
        if team_name in sorted_index[:4]:
            return f"{team_name} (Q)"
        else:
            return f"{team_name} (E)"

    # 2. During the season:
    # QUALIFIED if 5th place cannot catch your CURRENT points
    if team_name in sorted_index[:4] and row['Pts'] > fifth_place_max:
        return f"{team_name} (Q)"

    # ELIMINATED if your MAX points cannot reach current 4th place
    if max_pts < fourth_place_pts:
        return f"{team_name} (E)"

    return team_name

# Formatting Table
df_display = df_sorted.copy()
# Bold the names and apply (Q)/(E)
df_display.index = [f"**{get_status_name(name)}**" for name in df_display.index]

def highlight_rows(row):
    # Center align everything
    base_style = 'text-align: center;'
    if "(Q)" in row.name:
        return [base_style + 'background-color: #d4edda; color: #155724; font-weight: bold'] * len(row)
    elif "(E)" in row.name:
        return [base_style + 'background-color: #f8d7da; color: #721c24'] * len(row)
    return [base_style] * len(row)

st.divider()
st.subheader("Live Points Table")

# CSS for Bold Centered Headers
st.markdown("""
    <style>
        th { text-align: center !important; font-weight: bold !important; }
        td { text-align: center !important; }
    </style>
""", unsafe_allow_html=True)

st.table(df_display.style.apply(highlight_rows, axis=1).format(subset=['NRR'], formatter="{:.3f}"))
st.caption("**(Q)** = Qualified | **(E)** = Mathematically Eliminated")