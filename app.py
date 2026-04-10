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

# Page Configuration
st.set_page_config(page_title="WhatsApp Pro Analyzer", page_icon="📈", layout="wide")

# SaaS Design System & CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --primary: #22c55e;
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
        font-size: 32px !important;
        font-weight: 700 !important;
        line-height: 1.25 !important;
        color: var(--text-high) !important;
        letter-spacing: -0.5px !important;
        margin-bottom: var(--spacing-lg) !important;
        margin-top: var(--spacing-lg) !important;
    }

    h2 {
        font-size: 26px !important;
        font-weight: 600 !important;
        line-height: 1.35 !important;
        color: var(--text-high) !important;
        letter-spacing: -0.3px !important;
        margin-bottom: var(--spacing-md) !important;
        margin-top: var(--spacing-lg) !important;
    }

    h3 {
        font-size: 20px !important;
        font-weight: 600 !important;
        line-height: 1.4 !important;
        color: var(--text-high) !important;
        margin-bottom: var(--spacing-sm) !important;
        margin-top: var(--spacing-md) !important;
    }

    h4 {
        font-size: 17px !important;
        font-weight: 500 !important;
        line-height: 1.5 !important;
        color: var(--text-medium) !important;
        margin-bottom: var(--spacing-xs) !important;
    }

    p, .stText, .stMarkdown {
        font-size: 15px !important;
        font-weight: 400 !important;
        line-height: 1.6 !important;
        color: var(--text-medium) !important;
        max-width: 80ch;
    }

    .caption {
        font-size: 12px !important;
        font-weight: 300 !important;
        color: var(--text-muted) !important;
        letter-spacing: 0.2px;
    }

    /* --- UI Components --- */
    .saas-card {
        background: var(--card-bg);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: var(--spacing-md);
        margin-bottom: var(--spacing-md);
        transition: all 0.2s ease-in-out;
    }
    
    .saas-card:hover {
        border-color: rgba(37, 211, 102, 0.3);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }

    .metric-container {
        padding: var(--spacing-sm);
        text-align: center;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.02);
    }
    
    .metric-label {
        font-size: 13px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: var(--text-muted);
        margin-bottom: 4px;
    }
    
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: var(--primary);
    }

    /* --- Sidebar --- */
    [data-testid="stSidebar"] {
        background-color: #020617;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        padding: 2rem 1rem;
    }

    /* --- Plotly --- */
    .js-plotly-plot { background: transparent !important; }

    /* --- Buttons & Inputs --- */
    .stButton>button {
        border-radius: 8px !important;
        font-weight: 500 !important;
        padding: 8px 24px !important;
        background-color: transparent !important;
        border: 1px solid var(--primary) !important;
        color: var(--primary) !important;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        background-color: var(--primary) !important;
        color: #fff !important;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        color: var(--text-muted);
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(37, 211, 102, 0.1) !important;
        color: var(--primary) !important;
    }

    /* Remove default red underline and replace with green */
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: var(--primary) !important;
        height: 2px !important;
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
    <div class="metric-container">
        <div class="metric-label">{safe_label}</div>
        <div class="metric-value">{safe_value}</div>
    </div>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("# ChatPulse Pro")
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
            with st.status("Preprocessing Chat Data...", expanded=False) as status:
                df = preprocessor.preprocess(data)
                if df.empty:
                    status.update(label="Preprocessing Failed", state="error")
                    st.error("## 🔍 Parsing Failed")
                    st.warning("We couldn't detect a valid WhatsApp chat format. Please ensure you exported 'Without Media'.")
                    
                    with st.expander("Show Diagnostic Info (Technical)"):
                        st.info("This snippet helps identify your specific device's export format:")
                        st.code(data[:500] if data else "Empty File", language="text")
                        st.markdown("""
                        **Common issues:**
                        - Exporting *with* media (unsupported).
                        - Using a very rare system language.
                        - File encoding issues (ChatPulse expected UTF-8).
                        """)
                else:
                    status.update(label="Preprocessing Complete!", state="complete")
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
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
    
    if st.sidebar.button("Generate Dashboard"):
        try:
            with st.status("Analyzing Chat Trends...", expanded=False) as status:
                st.write("Fetching Statistics...")
                num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
                
                # --- Dashboard Rendering ---
                st.title(f"Dashboard: {selected_user}")
                
                # Report Download
                report_df = helper.generate_report_data(selected_user, df)
                st.download_button(
                    label="📥 Download Professional Report (CSV)",
                    data=report_df.to_csv(index=False).encode('utf-8'),
                    file_name=f"ChatPulse_{selected_user}_Report.csv",
                    mime="text/csv",
                    key="download-report"
                )

                # Stats Area
                st.markdown("## 🏆 Performance Overview")
                c1, c2, c3, c4 = st.columns(4)
                with c1: styled_metric("Messages", f"{num_messages:,}")
                with c2: styled_metric("Total Words", f"{words:,}")
                with c3: styled_metric("Media Shared", f"{num_media_messages:,}")
                with c4: styled_metric("Links Shared", f"{num_links:,}")
                

                st.write("Processing Timelines...")
                # Timelines
                st.markdown("## 📈 Engagement Timelines")
                tab1, tab2 = st.tabs(["Monthly Velocity", "Daily Frequency"])
                
                with tab1:
                    timeline = helper.monthly_timeline(selected_user, df)
                    fig = px.line(timeline, x='time', y='message', 
                                 hover_name='time', markers=True,
                                 template="plotly_dark", color_discrete_sequence=['#25D366'])
                    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                      xaxis_title="Timeline", yaxis_title="Messages")
                    st.plotly_chart(fig, use_container_width=True)
                    
                with tab2:
                    daily_timeline = helper.daily_timeline(selected_user, df)
                    fig = px.area(daily_timeline, x='only_date', y='message', 
                                 template="plotly_dark", color_discrete_sequence=['#25D366'])
                    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                      xaxis_title="Date", yaxis_title="Messages")
                    st.plotly_chart(fig, use_container_width=True)
                

                # Activity Maps
                st.write("Mapping Activity...")
                st.markdown("## 🗓️ Activity Distribution")
                colA, colB = st.columns(2)
                
                with colA:
                    st.markdown("#### Weekly Intensity")
                    busy_day = helper.week_activity_map(selected_user, df)
                    fig = px.bar(busy_day, x='Day', y='Count', 
                                template="plotly_dark", color_discrete_sequence=['#25D366'])
                    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig, use_container_width=True)
                    
                    
                with colB:
                    st.markdown("#### Monthly Volume")
                    busy_month = helper.month_activity_map(selected_user, df)
                    fig = px.bar(busy_month, x='Month', y='Count', 
                                template="plotly_dark", color_discrete_sequence=['#25D366'])
                    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig, use_container_width=True)
                    

                st.markdown("#### 🕒 Weekly Pulse (Hourly)")
                user_heatmap = helper.activity_heatmap(selected_user, df)
                if not user_heatmap.empty:
                    fig = px.imshow(user_heatmap, 
                                    color_continuous_scale='Greens',
                                    template="plotly_dark", aspect="auto")
                    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                      xaxis_type='category') # Force categorical to fix 11:59:59 issue
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Insufficient data for activity pulse heatmap.")
                

                # Community Insights
                if selected_user == 'Overall':
                    st.write("Analyzing Community...")
                    st.markdown("## 👥 Community Dynamics")
                    x, new_df = helper.most_busy_users(df)
                    colX, colY = st.columns([2, 1])
                    
                    with colX:
                        fig = px.bar(x, x=x.index, y=x.values, 
                                    title="Primary Contributors",
                                    labels={'index': 'User', 'y': 'Total Messages'},
                                    template="plotly_dark", color_discrete_sequence=['#25D366'])
                        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                        st.plotly_chart(fig, use_container_width=True)
                    with colY:
                        st.markdown("#### Share of Voice (%)")
                        st.dataframe(new_df, use_container_width=True, hide_index=True)
                    

                # Content Analysis
                st.write("Extracting Semantic Insights...")
                st.markdown("## 🔤 Semantic Analysis")
                colW1, colW2 = st.columns(2)
                
                with colW1:
                    st.markdown("#### Word Sentiment Cloud")
                    df_wc = helper.create_wordcloud(selected_user, df)
                    if df_wc:
                        import matplotlib.pyplot as plt
                        fig, ax = plt.subplots(facecolor='none')
                        ax.imshow(df_wc)
                        ax.axis('off')
                        st.pyplot(fig)
                    else:
                        st.info("No lexical content available for wordcloud.")
                    
                with colW2:
                    st.markdown("#### Lexical Trends")
                    most_common_df = helper.most_common_words(selected_user, df)
                    if not most_common_df.empty:
                        fig = px.bar(most_common_df, x=1, y=0, orientation='h',
                                    labels={'0': 'Term', '1': 'Count'},
                                    template="plotly_dark", color_discrete_sequence=['#25D366'])
                        fig.update_layout(yaxis={'categoryorder':'total ascending'},
                                          plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No common words detected.")
                

                # Emoji Analysis
                st.write("Capturing Emotional Pulse...")
                st.markdown("## 😂 Emotional Pulse")
                emoji_df = helper.emoji_helper(selected_user, df)
                
                if not emoji_df.empty:
                    colE1, colE2 = st.columns([1, 2])
                    with colE1:
                        st.dataframe(emoji_df.rename(columns={0: 'Emoji', 1: 'Frequency'}), 
                                     use_container_width=True, hide_index=True)
                    with colE2:
                        fig = px.pie(emoji_df.head(10), values=1, names=0, 
                                    title="Top 10 Emotional Triggers",
                                    template="plotly_dark", hole=0.5,
                                    color_discrete_sequence=px.colors.sequential.Greens_r)
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No lexical emotions (emojis) detected.")
                
                
                status.update(label="Dashboard Generated Successfully!", state="complete")

        except Exception as e:
            st.error("### ⚠️ Unexpected Error")
            st.info("The application encountered a problem while analyzing this specific chat segment.")
            st.markdown(f"**Error Details:** `{str(e)}`")
            if st.button("Retry Analysis"):
                st.rerun()

else:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if LOTTIE_AVAILABLE and lottie_chat:
            try:
                st_lottie(lottie_chat, height=300, key="chat_anim")
            except:
                st.markdown("""
                <div style='text-align:center; padding: 2rem; border-radius: 20px; background: rgba(34, 197, 94, 0.05); margin-bottom: 2rem;'>
                    <div style='font-size: 80px; filter: drop-shadow(0 0 15px var(--primary));'>💬</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='text-align:center; padding: 2rem; border-radius: 20px; background: rgba(34, 197, 94, 0.1); margin-bottom: 2rem;'>
                <div style='font-size: 80px;'>📊</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center;'>Ready to Pulse?</h1>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center;">
            <p>Export your WhatsApp chat (without media) and upload to begin professional analysis.</p>
            <p style="color: grey; font-size: 14px;">Privacy first: Data is processed locally in your session.</p>
        </div>
        """, unsafe_allow_html=True)
