import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- CONFIGURAÇÕES ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EQUIPE_DIR = os.path.join(BASE_DIR, "Equipe")
LOGO_PATH = os.path.join(BASE_DIR, "dell_logo.png")

st.set_page_config(layout="wide", page_title="Dell QA Analytics Pro", page_icon="📊")

# --- LÓGICA DE LOGIN ---
if "logado" not in st.session_state:
    st.session_state.logado = False
if "usuario_identificado" not in st.session_state:
    st.session_state.usuario_identificado = ""

def realizar_login():
    if st.session_state.usuario_input and st.session_state.senha_input == "dellqa2026": 
        st.session_state.logado = True
        st.session_state.usuario_identificado = st.session_state.usuario_input
    elif not st.session_state.usuario_input:
        st.warning("Por favor, digite o nome de usuário.")
    else:
        st.error("Senha incorreta. Tente novamente.")

if not st.session_state.logado:
    st.markdown("""
        <style>
        .stButton > button {
            width: 100%;
            background-color: #0076CE !important;
            color: white !important;
            font-weight: 800 !important;
            height: 45px;
            border-radius: 8px;
            border: none;
            transition: 0.3s;
            margin-top: 10px;
        }
        div[data-testid="stVerticalBlock"] > div { text-align: center; }
        </style>
    """, unsafe_allow_html=True)

    st.write("<br><br><br>", unsafe_allow_html=True)
    _, col_central, _ = st.columns([1.2, 1, 1.2])
    
    with col_central:
        if os.path.exists(LOGO_PATH): 
            st.image(LOGO_PATH, use_container_width=True)
        st.markdown("<h2 style='text-align: center; color: #0076CE; margin-bottom: 20px;'>Dell QA Analytics Pro</h2>", unsafe_allow_html=True)
        st.text_input("Usuário:", key="usuario_input", placeholder="Seu nome")
        st.text_input("Senha:", type="password", key="senha_input", placeholder="Senha do Squad")
        st.button("Entrar", on_click=realizar_login)
    st.stop() 

# --- DASHBOARD (APÓS LOGIN) ---

DELL_BLUE = "#0076CE"
MESES_ORDEM = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    * {{ font-family: 'Inter', sans-serif; }}
    .stApp {{ background-color: #FDFDFD; }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 24px; }}
    .stTabs [data-baseweb="tab"] {{ height: 60px; font-weight: 800 !important; font-size: 22px !important; color: #64748B; }}
    .stTabs [aria-selected="true"] {{ color: {DELL_BLUE} !important; border-bottom: 4px solid {DELL_BLUE} !important; }}
    
    /* BARRA DE INSTRUÇÃO COM IDENTIFICAÇÃO */
    .header-instruction {{ 
        background: #F3F4F6; padding: 15px; border-radius: 12px; border-left: 5px solid {DELL_BLUE}; 
        margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;
    }}
    .user-tag {{ background: {DELL_BLUE}; color: white; padding: 5px 15px; border-radius: 20px; font-weight: 600; font-size: 14px; }}

    .welcome-card {{ background: white; border-radius: 15px; padding: 20px; border: 1px solid #E5E7EB; height: 340px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); overflow: hidden; }}
    .welcome-card-title {{ color: {DELL_BLUE}; font-weight: 800; font-size: 16px; margin-bottom: 12px; text-transform: uppercase; }}
    .welcome-card-value {{ font-size: 58px; font-weight: 800; color: #111827; margin: 15px 0; }}
    .list-item {{ font-size: 14px; padding: 6px 0; border-bottom: 1px solid #F3F4F6; display: flex; justify-content: space-between; align-items: center; }}

    .card-premium {{ background: white; border-radius: 12px; height: 180px; border: 1px solid #E5E7EB; display: flex; overflow: hidden; margin-bottom: 1rem; }}
    .status-bar {{ width: 12px; height: 100%; }}
    .card-content {{ padding: 25px; flex-grow: 1; display: flex; flex-direction: column; justify-content: center; }}
    .card-label {{ text-transform: uppercase; font-size: 14px; font-weight: 600; color: #6B7280; margin-bottom: 4px; }}
    .card-value {{ font-size: 34px; font-weight: 800; display: flex; align-items: center; gap: 10px; }}
    .trend-badge {{ font-size: 18px; font-weight: 800; padding: 2px 8px; border-radius: 6px; display: flex; align-items: center; gap: 4px; }}
    .trend-up {{ background: #DCFCE7 !important; color: #10B981 !important; }}
    .trend-down {{ background: #FEE2E2 !important; color: #EF4444 !important; }}

    .ranking-container {{ background: white; border-radius: 15px; padding: 20px; border: 1px solid #E2E8F0; height: 680px; overflow-y: auto; }}
    .colab-item {{ display: flex; align-items: center; justify-content: space-between; padding: 12px; border-bottom: 1px solid #F1F5F9; }}
    .pos-number {{ width: 38px; height: 38px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 14px; margin-right: 15px; flex-shrink: 0; }}
    .bolinha-verde {{ background: #10B981; color: white; }}
    .bolinha-vermelha {{ background: #EF4444; color: white; }}
    .bolinha-amarela {{ background: #F59E0B; color: white; }}
    .bolinha-cinza {{ background: #94A3B8; color: white; }}
    
    .info-tag {{ background: #E1EFFE; color: {DELL_BLUE}; font-size: 14px; font-weight: 600; padding: 5px 12px; border-radius: 6px; margin-right: 10px; }}
    .pill-box {{ background: white; border: 1px solid #E5E7EB; border-radius: 12px; padding: 12px; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between; font-size: 14px; }}
    </style>
""", unsafe_allow_html=True)

# --- FUNÇÕES DE DADOS ---

def carregar_dados_colaborador(nome_arquivo):
    caminho = os.path.join(EQUIPE_DIR, nome_arquivo)
    try:
        df_full = pd.read_excel(caminho, engine='openpyxl')
        df_full.columns = [str(c).strip() for c in df_full.columns]
        df_foc = pd.DataFrame()
        df_foc['Mês'] = df_full['Mês'].astype(str).str.strip().str.capitalize()
        
        def tratar_ferias(val, nota):
            if (pd.isna(val) or str(val).lower() == 'nan' or str(val).strip() == "") and nota == 0:
                return "FÉRIAS"
            return str(val).strip() if not pd.isna(val) else ""

        df_foc['Pontos'] = pd.to_numeric(df_full['Pontos_Mes'], errors='coerce').fillna(0)
        df_foc['Pos_Mes_Txt'] = [tratar_ferias(t, n) for t, n in zip(df_full['Posicao_Mensal'], df_foc['Pontos'])]
        df_foc['Pos_Geral_Txt'] = [tratar_ferias(t, n) for t, n in zip(df_full['Posicao_Geral'], df_foc['Pontos'])]
        df_foc['Obs'] = [tratar_ferias(t, n) for t, n in zip(df_full['Observacoes'], df_foc['Pontos'])]
        
        df_foc['Pos_Mes'] = pd.to_numeric(df_full['Posicao_Mensal'], errors='coerce').fillna(0)
        df_foc['Pos_Geral'] = pd.to_numeric(df_full['Posicao_Geral'], errors='coerce').fillna(0)
        df_foc['Dias'] = pd.to_numeric(df_full['Dias_Trabalhados'], errors='coerce').fillna(0)
        df_foc['Casos'] = pd.to_numeric(df_full['Casos_Mes'], errors='coerce').fillna(0)
        df_foc['Suporte'] = pd.to_numeric(df_full['Suporte_Solicitado'], errors='coerce').fillna(0)
        df_foc['Atestados'] = pd.to_numeric(df_full['Atestados'], errors='coerce').fillna(0)
        
        # NOVAS COLUNAS COM PROTEÇÃO (CASO NÃO EXISTAM NO EXCEL)
        for col in ['Retornos', 'Acoes_Sociais', 'Horas_Voluntariado']:
            if col in df_full.columns:
                df_foc[col] = pd.to_numeric(df_full[col], errors='coerce').fillna(0)
            else:
                df_foc[col] = 0

        df_meta = pd.read_excel(caminho, header=None, usecols=[17], nrows=4)
        t_res = str(df_meta.iloc[2, 0]).strip().upper()
        p_res = str(df_meta.iloc[3, 0]).strip().capitalize()
        if "Fisic" in p_res: p_res = "Físico"
        elif "Audit" in p_res: p_res = "Auditivo"
        elif "Visu" in p_res or "Ceg" in p_res: p_res = "Visual"
        
        return df_foc, str(df_meta.iloc[0, 0]), str(df_meta.iloc[1, 0]), t_res, p_res
    except: return None, None, None, None, None

def carregar_dados_equipe_completa():
    all_data = []
    if os.path.exists(EQUIPE_DIR):
        for arq in [f for f in os.listdir(EQUIPE_DIR) if f.endswith(".xlsx")]:
            df, n, b, t, p = carregar_dados_colaborador(arq)
            if df is not None:
                df['Nome_Exibicao'] = n; df['Turma_Exibicao'] = t; df['PCD_Tipo'] = p
                all_data.append(df)
    return pd.concat(all_data) if all_data else pd.DataFrame()

def get_status_color(pos, media, txt="", obs=""):
    comb = (str(txt) + str(obs)).lower()
    if any(x in comb for x in ["férias", "ferias", "atestado", "licença"]): return "#94A3B8"
    if pos == 0 or media == 0: return "#94A3B8"
    if 1 <= pos <= 8: return "#10B981"
    if pos >= 35: return "#EF4444"
    return "#F59E0B"

def render_premium_card(label, pos, media, trend_val="", delta=0, color="#94A3B8", txt="", obs=""):
    comb = (str(txt) + str(obs)).lower().strip()
    status_esp = ""
    for s in ["férias", "ferias", "atestado", "licença"]:
        if s in comb: status_esp = "FÉRIAS" if "feria" in s else s.upper(); break
    
    if status_esp: val_display, trend_html = status_esp, ""
    elif pos == 0 or media == 0: val_display, trend_html = " - ", ""
    else:
        val_display = f"{int(pos)}º"
        if trend_val == "up" and delta > 0: trend_html = f'<span class="trend-badge trend-up">↑ {int(delta)}</span>'
        elif trend_val == "down" and delta > 0: trend_html = f'<span class="trend-badge trend-down">↓ {int(delta)}</span>'
        else: trend_html = ""
    st.markdown(f"""<div class="card-premium"><div class="status-bar" style="background-color: {color};"></div><div class="card-content"><div class="card-label">{label}</div><div class="card-value">{val_display} {trend_html}</div><div class="card-footer">Média: {media:.2f}</div></div></div>""", unsafe_allow_html=True)

# --- INTERFACE ---

aba_individual, aba_equipe = st.tabs(["👤 Performance Individual", "👥 Panorama da Equipe"])

with aba_individual:
    c1, c2, c3 = st.columns([2.5, 2, 2])
    with c1:
        if os.path.exists(LOGO_PATH): st.image(LOGO_PATH, width=400)
    with c2:
        arquivos_ind = sorted([f for f in os.listdir(EQUIPE_DIR) if f.endswith(".xlsx")])
        mapa_arq = {f.replace(".xlsx", "").replace("_", " ").title(): f for f in arquivos_ind}
        colab_sel = st.selectbox("👤 Selecionar Colaborador", ["Selecione..."] + list(mapa_arq.keys()), key="f_colab")
    with c3:
        mes_sel_ind = st.selectbox("📅 Mês de Análise", MESES_ORDEM, index=0, key="f_mes_ind")

    # BARRA DE INSTRUÇÃO COM IDENTIFICAÇÃO DO USUÁRIO LOGADO
    st.markdown(f'''
        <div class="header-instruction">
            <span style="font-size: 20px; color: {DELL_BLUE}; font-weight: 800;">Dell QA Analytics Pro</span>
            <span class="user-tag">👤 Usuário: {st.session_state.usuario_identificado.title()}</span>
        </div>
    ''', unsafe_allow_html=True)

    df_master = carregar_dados_equipe_completa()

    if colab_sel == "Selecione...":
        if not df_master.empty:
            df_mes_atu = df_master[df_master['Mês'] == mes_sel_ind.capitalize()]
            w1, w2, w3, w4 = st.columns(4)
            with w1:
                turmas = df_mes_atu.drop_duplicates('Nome_Exibicao')['Turma_Exibicao'].value_counts().sort_index()
                html_t = "".join([f'<div class="list-item"><span>{t}</span><b>{v}</b></div>' for t,v in turmas.items()])
                st.markdown(f'<div class="welcome-card"><div class="welcome-card-title">👥 Equipe por Turma</div>{html_t}</div>', unsafe_allow_html=True)
            with w2:
                total_p = len(df_master.drop_duplicates('Nome_Exibicao'))
                afastados_no_mes = df_mes_atu[df_mes_atu.apply(lambda r: any(x in (str(r['Pos_Mes_Txt'])+str(r['Obs'])).lower() for x in ["férias","ferias","atestado","licença"]), axis=1)]
                num_a = len(afastados_no_mes.drop_duplicates('Nome_Exibicao'))
                st.markdown(f'<div class="welcome-card"><div class="welcome-card-title">🩺 Health Check ({mes_sel_ind})</div><div class="welcome-card-value">{ ((total_p-num_a)/total_p*100) if total_p>0 else 0:.0f}%</div>Ativos: {total_p-num_a}<br>Afastados: {num_a}</div>', unsafe_allow_html=True)
            with w3:
                pcds = df_mes_atu.drop_duplicates('Nome_Exibicao')['PCD_Tipo'].value_counts()
                html_p = "".join([f'<div class="list-item"><span>{p}</span><b>{v}</b></div>' for p,v in pcds.items() if p.upper() not in ["NÃO","NA","N/A","NO"]])
                st.markdown(f'<div class="welcome-card"><div class="welcome-card-title">♿ PCD por Categoria</div>{html_p if html_p else "Sem registros."}</div>', unsafe_allow_html=True)
            with w4:
                rank_d = df_master.groupby('Nome_Exibicao').apply(lambda x: x['Pontos'].sum()/x['Dias'].sum() if x['Dias'].sum()>0 else 0).sort_values().reset_index()
                ultimos = rank_d[rank_d[0]>0].head(4)
                html_r = "".join([f'<div class="list-item"><span style="color:#EF4444;">{n[:18]}</span><b>{v:.2f}</b></div>' for n,v in zip(ultimos['Nome_Exibicao'], ultimos[0])])
                st.markdown(f'<div class="welcome-card"><div class="welcome-card-title">⚠️ Últimos do Ranking Geral</div>{html_r}</div>', unsafe_allow_html=True)
    else:
        # INDIVIDUAL
        df_ind, nome_f, badge, turma, pcd = carregar_dados_colaborador(mapa_arq[colab_sel])
        if df_ind is not None:
            l_atu = df_ind[df_ind['Mês'] == mes_sel_ind.capitalize()]
            if not l_atu.empty:
                row = l_atu.iloc[0]; idx = MESES_ORDEM.index(mes_sel_ind)
                df_ac = df_ind[df_ind['Mês'].isin([m.capitalize() for m in MESES_ORDEM[:idx+1]])]
                m_g = df_ac['Pontos'].sum() / df_ac['Dias'].sum() if df_ac['Dias'].sum() > 0 else 0
                m_m = row['Pontos'] / row['Dias'] if row['Dias'] > 0 else 0
                
                # Tendências
                t_m, d_m, t_g, d_g = "", 0, "", 0
                if idx > 0:
                    l_ant = df_ind[df_ind['Mês'] == MESES_ORDEM[idx-1].capitalize()]
                    if not l_ant.empty:
                        ant = l_ant.iloc[0]
                        if ant['Pos_Mes']>0 and row['Pos_Mes']>0:
                            d_m = abs(row['Pos_Mes']-ant['Pos_Mes']); t_m = "up" if row['Pos_Mes'] < ant['Pos_Mes'] else "down" if row['Pos_Mes'] > ant['Pos_Mes'] else ""
                        if ant['Pos_Geral']>0 and row['Pos_Geral']>0:
                            d_g = abs(row['Pos_Geral']-ant['Pos_Geral']); t_g = "up" if row['Pos_Geral'] < ant['Pos_Geral'] else "down" if row['Pos_Geral'] > ant['Pos_Geral'] else ""

                st.markdown(f"<h1 style='color:{DELL_BLUE}; font-weight:800;'>{nome_f}</h1>", unsafe_allow_html=True)
                st.markdown(f'<div><span class="info-tag">🆔 {badge}</span><span class="info-tag">👥 {turma}</span></div>', unsafe_allow_html=True)
                st.divider()

                ca1, ca2, ca3 = st.columns([2, 2, 1.3])
                with ca1: render_premium_card("Ranking Mensal", row['Pos_Mes'], m_m, t_m, d_m, get_status_color(row['Pos_Mes'], m_m, row['Pos_Mes_Txt'], row['Obs']), row['Pos_Mes_Txt'], row['Obs'])
                with ca2: render_premium_card("Ranking Geral (Acumulado)", row['Pos_Geral'], m_g, t_g, d_g, get_status_color(row['Pos_Geral'], m_g, row['Pos_Geral_Txt'], row['Obs']), row['Pos_Geral_Txt'], row['Obs'])
                with ca3:
                    st.markdown(f'<div class="pill-box"><span>📅 Dias (Mês / Ano)</span><b>{int(row["Dias"])} / {int(df_ind["Dias"].sum())}</b></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="pill-box"><span>🔄 Casos Retornos</span><b>{int(row["Retornos"])}</b></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="pill-box"><span>🤝 Ações Sociais</span><b>{int(row["Acoes_Sociais"])}</b></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="pill-box"><span>⏳ Voluntariado (h)</span><b>{int(row["Horas_Voluntariado"])}h</b></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="pill-box"><span>🛠️ Suporte Solicitado</span><b>{int(row["Suporte"])}</b></div>', unsafe_allow_html=True)

                st.divider()
                # 4 GRÁFICOS
                df_graf = df_ind[df_ind['Pontos']>0].copy()
                df_graf['Mês'] = pd.Categorical(df_graf['Mês'], categories=MESES_ORDEM, ordered=True)
                df_graf = df_graf.sort_values('Mês')
                
                f_s = dict(size=15, color="black", family="Arial Black")
                r1, r2 = st.columns(2)
                with r1:
                    fig1 = go.Figure()
                    clrs1 = [get_status_color(p, m, r, o) for p, m, r, o in zip(df_graf['Pos_Mes'], df_graf['Pontos'], df_graf['Pos_Mes_Txt'], df_graf['Obs'])]
                    fig1.add_trace(go.Scatter(x=df_graf['Mês'], y=df_graf['Pos_Mes'], mode='markers+lines+text', text=df_graf['Pos_Mes'].astype(int), textposition="top right", textfont=f_s, marker=dict(size=12, color=clrs1, line=dict(width=2, color="white")), cliponaxis=False))
                    fig1.update_yaxes(autorange="reversed", range=[df_graf['Pos_Mes'].max()+3, 1]); fig1.update_xaxes(categoryorder='array', categoryarray=MESES_ORDEM, range=[-0.5, 11.5])
                    fig1.update_layout(plot_bgcolor='white', title="Evolução Ranking Mensal", height=380); st.plotly_chart(fig1, use_container_width=True)
                with r2:
                    fig2 = go.Figure()
                    clrs2 = [get_status_color(p, m, r, o) for p, m, r, o in zip(df_graf['Pos_Geral'], df_graf['Pontos'], df_graf['Pos_Geral_Txt'], df_graf['Obs'])]
                    fig2.add_trace(go.Scatter(x=df_graf['Mês'], y=df_graf['Pos_Geral'], mode='markers+lines+text', text=df_graf['Pos_Geral'].astype(int), textposition="top right", textfont=f_s, marker=dict(size=12, color=clrs2, line=dict(width=2, color="white")), cliponaxis=False))
                    fig2.update_yaxes(autorange="reversed", range=[df_graf['Pos_Geral'].max()+3, 1]); fig2.update_xaxes(categoryorder='array', categoryarray=MESES_ORDEM, range=[-0.5, 11.5])
                    fig2.update_layout(plot_bgcolor='white', title="Evolução Ranking Geral", height=380); st.plotly_chart(fig2, use_container_width=True)
                
                g1, g2 = st.columns(2)
                with g1:
                    fig3 = px.line(df_graf, x='Mês', y='Pontos', markers=True, text='Pontos', title="Evolução de Pontos")
                    fig3.update_traces(textposition="top right", textfont=f_s, line_color=DELL_BLUE, cliponaxis=False); fig3.update_xaxes(categoryorder='array', categoryarray=MESES_ORDEM, range=[-0.5, 11.5])
                    fig3.update_layout(plot_bgcolor='white', height=380); st.plotly_chart(fig3, use_container_width=True)
                with g2:
                    fig4 = px.bar(df_graf, x='Mês', y='Casos', text='Casos', title="Volume de Casos")
                    fig4.update_traces(marker_color=DELL_BLUE, textfont=f_s, textposition="outside", cliponaxis=False); fig4.update_xaxes(categoryorder='array', categoryarray=MESES_ORDEM, range=[-0.5, 11.5])
                    fig4.update_layout(plot_bgcolor='white', height=380); st.plotly_chart(fig4, use_container_width=True)

# --- ABA 2 ---
with aba_equipe:
    ce1, ce2, ce3 = st.columns([1.5, 2.2, 2.2])
    with ce1:
        if os.path.exists(LOGO_PATH): st.image(LOGO_PATH, width=350)
    with ce2: mes_eq_g = st.selectbox("🏆 Mês Ranking Geral", MESES_ORDEM, index=0, key="f_mes_eq_g")
    with ce3: mes_eq_m = st.selectbox("📅 Mês Ranking Mensal", MESES_ORDEM, index=0, key="f_mes_eq_m")
    st.divider()
    if not df_master.empty:
        col_g, col_m = st.columns(2)
        with col_g:
            st.subheader(f"🏆 Ranking Geral (Até {mes_eq_g})")
            ms_r = [m.capitalize() for m in MESES_ORDEM[:MESES_ORDEM.index(mes_eq_g)+1]]
            res = df_master[df_master['Mês'].isin(ms_r)].groupby(['Nome_Exibicao', 'Turma_Exibicao']).apply(lambda x: x['Pontos'].sum() / x['Dias'].sum() if x['Dias'].sum() > 0 else 0).sort_values(ascending=False).reset_index()
            res.columns = ['Nome', 'Turma', 'Media']
            html_g = "".join([f'<div class="colab-item"><div class="pos-number {"bolinha-verde" if i<8 else "bolinha-vermelha" if i>=len(res)-4 else "bolinha-amarela"}">{i+1}º</div><div style="flex-grow:1;"><b>{r["Nome"]}</b><br><small>{r["Turma"]}</small></div><div style="font-weight:800;">{f"{r["Media"]:.2f}" if r["Media"]>0 else "FÉRIAS"}</div></div>' for i,r in res.iterrows()])
            st.markdown(f'<div class="ranking-container">{html_g}</div>', unsafe_allow_html=True)
            
        with col_m:
            st.subheader(f"📅 Ranking Mensal: {mes_eq_m}")
            df_m = df_master[df_master['Mês'] == mes_eq_m.capitalize()].copy()
            df_m['Media'] = df_m['Pontos'] / df_m['Dias']; df_m = df_m.sort_values(by="Media", ascending=False).reset_index(drop=True)
            df_m['is_cinza'] = df_m.apply(lambda r: any(x in (str(r['Pos_Mes_Txt'])+str(r['Obs'])).lower() for x in ["férias","ferias","atestado","licença"]), axis=1)
            at_idx = df_m[~df_m['is_cinza']].index
            v_idx, r_idx = at_idx[:8], at_idx[-4:]
            html_m = "".join([f'<div class="colab-item"><div class="pos-number {"bolinha-cinza" if r["is_cinza"] else "bolinha-verde" if i in v_idx else "bolinha-vermelha" if i in r_idx else "bolinha-amarela"}">{i+1}º</div><div style="flex-grow:1;"><b>{r["Nome_Exibicao"]}</b><br><small>{r["Turma_Exibicao"]}</small></div><div style="font-weight:800;">{f"{r["Media"]:.2f}" if not r["is_cinza"] else "FÉRIAS"}</div></div>' for i,r in df_m.iterrows()])
            st.markdown(f'<div class="ranking-container">{html_m}</div>', unsafe_allow_html=True)