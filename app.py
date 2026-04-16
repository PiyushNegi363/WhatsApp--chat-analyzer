import streamlit as st
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, message="coroutine 'expire_cache' was never awaited")
import plotly.express as px
import plotly.graph_objects as go
from modules import preprocessor, helper
import requests
try:
    from streamlit_lottie import st_lottie
    LOTTIE_AVAILABLE = True
except ImportError:
    LOTTIE_AVAILABLE = False
import pandas as pd
import html
import time

# Page Configuration
st.set_page_config(page_title="WhatsApp Pro Analyzer", page_icon="📈", layout="wide")

# SaaS Design System & CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --primary: #22c55e;
        --primary-hover: #16a34a;
        --primary-glow: rgba(34, 197, 94, 0.4);
        --bg: #020617;
        --card-bg: rgba(15, 23, 42, 0.6);
        --text-high: #ffffff;
        --text-medium: #e2e8f0;
        --text-muted: #94a3b8;
        --spacing-xs: 8px;
        --spacing-sm: 16px;
        --spacing-md: 24px;
        --spacing-lg: 32px;
    }

    * { font-family: 'Inter', sans-serif; }

    .stApp {
        background-color: var(--bg);
        color: var(--text-medium);
    }

    /* --- Typography Hierarchy --- */
    h1 {
        font-size: clamp(28px, 5vw, 40px) !important;
        font-weight: 800 !important;
        line-height: 1.1 !important;
        color: var(--text-high) !important;
        letter-spacing: -1px !important;
        margin-bottom: var(--spacing-md) !important;
        background: linear-gradient(135deg, #fff 0%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    h2 {
        font-size: clamp(22px, 4vw, 30px) !important;
        font-weight: 700 !important;
        color: var(--text-high) !important;
        margin-top: var(--spacing-lg) !important;
        border-left: 4px solid var(--primary);
        padding-left: 15px;
    }

    /* --- Animations --- */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .animate-in {
        animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    /* --- UI Components --- */
    .hero-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 70vh;
        text-align: center;
        padding: 40px 20px;
    }

    .saas-card {
        background: var(--card-bg);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: var(--spacing-md);
        margin-bottom: var(--spacing-md);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .saas-card:hover {
        border-color: var(--primary);
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
    }

    .metric-container {
        padding: var(--spacing-md);
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    
    .metric-label {
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        color: var(--text-muted);
        letter-spacing: 1px;
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: var(--primary);
        text-shadow: 0 0 20px var(--primary-glow);
    }

    /* --- Sidebar Enhancements --- */
    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    .sidebar-logo {
        font-size: 24px;
        font-weight: 800;
        background: linear-gradient(90deg, #22c55e, #4ade80);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }

    /* --- Mobile Fixes --- */
    @media (max-width: 768px) {
        .metric-value { font-size: 24px; }
        .stColumns > div { margin-bottom: 20px; }
    }

    /* Better Tabs */
    .stTabs [data-baseweb="tab-list"] { 
        background-color: rgba(255, 255, 255, 0.03);
        padding: 5px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px !important;
    }
</style>
""", unsafe_allow_html=True)

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except: return None

lottie_chat = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_7wwmupbm.json") if LOTTIE_AVAILABLE else None

def styled_metric(label, value):
    safe_label = html.escape(str(label))
    safe_value = html.escape(str(value))
    st.markdown(f"""
    <div class="metric-container animate-in" aria-label="{safe_label}: {safe_value}">
        <div class="metric-label">{safe_label}</div>
        <div class="metric-value">{safe_value}</div>
    </div>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown('<div class="sidebar-logo">ChatPulse Pro</div>', unsafe_allow_html=True)
st.sidebar.markdown("---")

app_mode = st.sidebar.radio("Analysis Mode", ["Upload Chat", "Try Sample Chat"])

df = pd.DataFrame()
selected_user = "Overall"

if app_mode == "Upload Chat":
    uploaded_file = st.sidebar.file_uploader("Upload chat export (.txt)", type=["txt"])
    if uploaded_file is not None:
        try:
            bytes_data = uploaded_file.getvalue()
            data = bytes_data.decode("utf-8")
            with st.status("Preprocessing Data...", expanded=False) as status:
                df = preprocessor.preprocess(data)
                if df.empty:
                    status.update(label="Parsing Failed", state="error")
                    st.error("## 🔍 Parsing Failed")
                    st.warning("We couldn't detect a valid WhatsApp chat format. Please ensure you exported 'Without Media'.")
                else:
                    status.update(label="Ready for Analysis", state="complete")
        except Exception as e:
            st.sidebar.error(f"Error loading file: {str(e)}")
else:
    try:
        with open('data/sample_chat.txt', 'r') as f:
            data = f.read()
            df = preprocessor.preprocess(data)
            st.sidebar.success("Sample chat loaded!")
    except FileNotFoundError:
        st.sidebar.error("Sample chat file not found.")

if not df.empty:
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Analysis Perspective", user_list)
    
    # Automatic Generation Logic
    if 'prev_user' not in st.session_state:
        st.session_state.prev_user = None
    
    # We always analyze if we have data, but we use a status block just for the "heavy" lifting
    try:
        # Fetch stats once
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        
        # --- Dashboard Rendering (OUTSIDE status block) ---
        st.title(f"Dashboard: {selected_user}")
        
        # Action Bar
        col_act1, col_act2 = st.columns([3, 1])
        with col_act2:
            report_df = helper.generate_report_data(selected_user, df)
            st.download_button(
                label="📥 Download CSV Report",
                data=report_df.to_csv(index=False).encode('utf-8'),
                file_name=f"ChatPulse_{selected_user}_Report.csv",
                mime="text/csv",
                use_container_width=True
            )

        # 1. Performance Overview
        st.markdown("## 🏆 Performance Overview")
        m1, m2, m3, m4 = st.columns(4)
        with m1: styled_metric("Messages", f"{num_messages:,}")
        with m2: styled_metric("Total Words", f"{words:,}")
        with m3: styled_metric("Media Shared", f"{num_media_messages:,}")
        with m4: styled_metric("Links Shared", f"{num_links:,}")

        # 2. Activity Trends
        st.markdown("## 📈 Engagement Timelines")
        tab1, tab2 = st.tabs(["Monthly Velocity", "Daily Frequency"])
        
        with tab1:
            timeline = helper.monthly_timeline(selected_user, df)
            fig = px.line(timeline, x='time', y='message', 
                         hover_name='time', markers=True,
                         template="plotly_dark", color_discrete_sequence=['#22c55e'])
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                              margin=dict(l=0, r=0, t=20, b=0))
            st.plotly_chart(fig, use_container_width=True)
            
        with tab2:
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig = px.area(daily_timeline, x='only_date', y='message', 
                         template="plotly_dark", color_discrete_sequence=['#22c55e'])
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                              margin=dict(l=0, r=0, t=20, b=0))
            st.plotly_chart(fig, use_container_width=True)

        # 3. Distribution Maps
        st.markdown("## 🗓️ Activity Distribution")
        colA, colB = st.columns(2)
        
        with colA:
            st.markdown('<div class="saas-card"><h4>Weekly Intensity</h4>', unsafe_allow_html=True)
            busy_day = helper.week_activity_map(selected_user, df)
            fig = px.bar(busy_day, x='Day', y='Count', 
                        template="plotly_dark", color_discrete_sequence=['#22c55e'])
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                              xaxis_title="", yaxis_title="")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with colB:
            st.markdown('<div class="saas-card"><h4>Monthly Volume</h4>', unsafe_allow_html=True)
            busy_month = helper.month_activity_map(selected_user, df)
            fig = px.bar(busy_month, x='Month', y='Count', 
                        template="plotly_dark", color_discrete_sequence=['#22c55e'])
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                              xaxis_title="", yaxis_title="")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("#### 🕒 Weekly Pulse (Hourly)")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        if not user_heatmap.empty:
            fig = px.imshow(user_heatmap, 
                            color_continuous_scale='Greens',
                            template="plotly_dark", aspect="auto")
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                              xaxis_type='category')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Insufficient data for activity pulse heatmap.")

        # 4. Community Insights
        if selected_user == 'Overall':
            st.markdown("## 👥 Community Dynamics")
            x, new_df = helper.most_busy_users(df)
            colX, colY = st.columns([2, 1])
            
            with colX:
                st.markdown('<div class="saas-card">', unsafe_allow_html=True)
                fig = px.bar(x, x=x.index, y=x.values, 
                            title="Primary Contributors",
                            labels={'index': 'User', 'y': 'Messages'},
                            template="plotly_dark", color_discrete_sequence=['#22c55e'])
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with colY:
                st.markdown('<div class="saas-card"><h4>Share of Voice (%)</h4>', unsafe_allow_html=True)
                st.dataframe(new_df, use_container_width=True, hide_index=True)
                st.markdown('</div>', unsafe_allow_html=True)

        # 5. Semantic Analysis
        st.markdown("## 🔤 Semantic Analysis")
        colW1, colW2 = st.columns(2)
        
        with colW1:
            st.markdown('<div class="saas-card"><h4>Word Sentiment Cloud</h4>', unsafe_allow_html=True)
            df_wc = helper.create_wordcloud(selected_user, df)
            if df_wc:
                import matplotlib.pyplot as plt
                fig, ax = plt.subplots(facecolor='none', figsize=(10, 10))
                ax.imshow(df_wc, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig)
            else:
                st.info("No lexical content available for wordcloud.")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with colW2:
            st.markdown('<div class="saas-card"><h4>Lexical Trends</h4>', unsafe_allow_html=True)
            most_common_df = helper.most_common_words(selected_user, df)
            if not most_common_df.empty:
                fig = px.bar(most_common_df, x=1, y=0, orientation='h',
                            labels={'0': 'Term', '1': 'Count'},
                            template="plotly_dark", color_discrete_sequence=['#22c55e'])
                fig.update_layout(yaxis={'categoryorder':'total ascending'},
                                  plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                  xaxis_title="", yaxis_title="")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No common words detected.")
            st.markdown('</div>', unsafe_allow_html=True)

        # 6. Emoji Analysis
        st.markdown("## 😂 Emotional Pulse")
        emoji_df = helper.emoji_helper(selected_user, df)
        
        if not emoji_df.empty:
            colE1, colE2 = st.columns([1, 2])
            with colE1:
                st.markdown('<div class="saas-card">', unsafe_allow_html=True)
                st.dataframe(emoji_df.rename(columns={0: 'Emoji', 1: 'Freq'}), 
                             use_container_width=True, hide_index=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with colE2:
                st.markdown('<div class="saas-card">', unsafe_allow_html=True)
                fig = px.pie(emoji_df.head(10), values=1, names=0, 
                            title="Top Emotional Triggers",
                            template="plotly_dark", hole=0.6,
                            color_discrete_sequence=px.colors.sequential.Greens_r)
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No lexical emotions (emojis) detected.")

    except Exception as e:
        st.error(f"### ⚠️ Analysis Interrupted: {str(e)}")
        if st.button("Retry Analysis"): st.rerun()

else:
    # Landing Page - Visual Hero
    st.markdown("""
    <div class="hero-section animate-in">
        <div style='font-size: 100px; margin-bottom: 20px; filter: drop-shadow(0 0 20px var(--primary-glow));'>📊</div>
        <h1>Analyze Your Conversations</h1>
        <p style='font-size: 18px; color: var(--text-medium); max-width: 600px; margin: 0 auto;'>
            Unlock deep insights from your WhatsApp chats with professional-grade analytics and visual trends.
        </p>
        <div style='margin-top: 40px; padding: 20px; border-radius: 20px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05);'>
            <p style='color: var(--primary); font-weight: 600;'>🚀 Quick Start</p>
            <p style='color: var(--text-muted); font-size: 14px;'>Use the sidebar to upload a chat (.txt) or try the sample data.</p>
        </div>
        <p style='margin-top: 60px; color: grey; font-size: 12px;'>Privacy Secured: Data is processed entirely in your local browser session.</p>
    </div>
    """, unsafe_allow_html=True)
