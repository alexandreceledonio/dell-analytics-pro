import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import time

# --- CONFIGURAÇÕES DE CAMINHO BLINDADAS (SINCRO COM GITHUB) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if os.path.exists(os.path.join(BASE_DIR, "equipe")):
    EQUIPE_DIR = os.path.join(BASE_DIR, "equipe")
else:
    EQUIPE_DIR = os.path.join(os.getcwd(), "equipe")

LOGO_PATH = os.path.join(BASE_DIR, "dell_logo.png")

st.set_page_config(layout="wide", page_title="Dell QA Analytics Pro", page_icon="📊")  

# --- LÓGICA DE LOGIN ---
if "logado" not in st.session_state:
    st.session_state.logado = False
if "usuario_identificado" not in st.session_state:
    st.session_state.usuario_identificado = ""

def realizar_login(usuario, senha):
    if usuario and senha == "dellqa2026": 
        st.session_state.logado = True
        st.session_state.usuario_identificado = usuario
        st.rerun()
    elif not usuario:
        st.warning("Por favor, digite o nome de usuário.")
    else:
        st.error("Senha incorreta. Tente novamente.")

if not st.session_state.logado:
    st.markdown("""
        <style>
        [data-testid="stForm"] { border: none !important; padding: 0 !important; }
        div[data-testid="stFormSubmitButton"], div[data-testid="stFormSubmitButton"] > button {
            width: 100% !important; display: block;
        }
        div[data-testid="stFormSubmitButton"] > button {
            background-color: #0076CE !important; color: white !important;
            font-weight: 800 !important; height: 45px; border-radius: 8px;
            border: none; transition: 0.3s; margin-top: 10px;
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
        with st.form("login_form"):
            usuario_input = st.text_input("Usuário:", placeholder="Seu nome")
            senha_input = st.text_input("Senha:", type="password", placeholder="Senha do Squad")
            botao_entrar = st.form_submit_button("Entrar")
            if botao_entrar:
                realizar_login(usuario_input, senha_input)
    st.stop() 

# --- CONSTANTES ---
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
    
    .header-instruction {{ 
        background: #F3F4F6; padding: 15px; border-radius: 12px; border-left: 5px solid {DELL_BLUE}; 
        margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;
    }}
    .user-tag {{ background: {DELL_BLUE}; color: white; padding: 5px 15px; border-radius: 20px; font-weight: 600; font-size: 14px; }}

    .welcome-card {{ background: white; border-radius: 15px; padding: 20px; border: 1px solid #E5E7EB; height: 340px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); overflow: hidden; }}
    .welcome-card-title {{ color: {DELL_BLUE}; font-weight: 800; font-size: 16px; margin-bottom: 12px; text-transform: uppercase; }}
    .welcome-card-value {{ font-size: 58px; font-weight: 800; color: #111827; margin: 15px 0; }}
    .list-item {{ font-size: 14px; padding: 6px 0; border-bottom: 1px solid #F3F4F6; display: flex; justify-content: space-between; align-items: center; }}

    .card-premium {{ background: white; border-radius: 12px; height: 180px; border: 1px solid #E5E7EB; display: flex; overflow: hidden; margin-bottom: 1rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }}
    .status-bar {{ width: 12px; height: 100%; }}
    .card-content {{ padding: 25px; flex-grow: 1; display: flex; flex-direction: column; justify-content: center; }}
    .card-label {{ text-transform: uppercase; font-size: 14px; font-weight: 600; color: #6B7280; margin-bottom: 4px; }}
    .card-value {{ font-size: 34px; font-weight: 800; display: flex; align-items: center; gap: 10px; }}
    .trend-badge {{ font-size: 18px; font-weight: 800; padding: 2px 8px; border-radius: 6px; }}
    .trend-up {{ background: #DCFCE7 !important; color: #10B981 !important; }}
    .trend-down {{ background: #FEE2E2 !important; color: #EF4444 !important; }}
    
    .mini-card {{
        background: white; border: 1px solid #E5E7EB; border-radius: 10px; padding: 15px;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.02); height: 110px;
    }}
    .mini-card-label {{ font-size: 11px; font-weight: 600; color: #6B7280; text-transform: uppercase; margin-bottom: 5px; }}
    .mini-card-value {{ font-size: 18px; font-weight: 800; color: #111827; }}
    
    .ranking-container {{ background: white; border-radius: 15px; padding: 20px; border: 1px solid #E2E8F0; height: 680px; overflow-y: auto; }}
    .colab-item {{ display: flex; align-items: center; justify-content: space-between; padding: 12px; border-bottom: 1px solid #F1F5F9; }}
    .pos-number {{ width: 38px; height: 38px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 14px; margin-right: 15px; flex-shrink: 0; }}
    .bolinha-verde {{ background: #10B981; color: white; }}
    .bolinha-vermelha {{ background: #EF4444; color: white; }}
    .bolinha-amarela {{ background: #F59E0B; color: white; }}
    .bolinha-cinza {{ background: #94A3B8; color: white; }}
    
    .info-tag {{ background: #E1EFFE; color: {DELL_BLUE}; font-size: 14px; font-weight: 600; padding: 5px 12px; border-radius: 6px; margin-right: 10px; }}

    /* ESTILO DO PAINEL DE ALERTA ESCALONADO */
    .alert-container {{ background: white; border-radius: 15px; padding: 20px; border: 1px solid #FEE2E2; height: 340px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); }}
    .alert-header {{ color: #EF4444; font-weight: 800; font-size: 16px; margin-bottom: 10px; text-transform: uppercase; }}
    .alert-row {{ padding: 10px 0; border-bottom: 1px solid #FEE2E2; }}
    .alert-name {{ font-weight: 700; color: #111827; font-size: 13px; display: block; margin-bottom: 5px; }}
    .alert-status {{ font-size: 10px; font-weight: 800; padding: 2px 6px; border-radius: 4px; margin-bottom: 5px; display: inline-block; }}
    .status-atencao {{ background: #FEF3C7; color: #92400E; }}
    .status-chamada {{ background: #FEE2E2; color: #B91C1C; border: 1px solid #EF4444; }}
    .alert-pills {{ display: flex; gap: 4px; }}
    .alert-pill {{ background: #EF4444; color: white; padding: 2px 8px; border-radius: 10px; font-size: 10px; font-weight: 700; }}
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

# Lógica mestre de cores das bolinhas (Centralizada para gráficos e alertas)
def get_status_color(pos, media, txt="", obs="", total_ativos=38):
    comb = (str(txt) + str(obs)).lower()
    if any(x in comb for x in ["férias", "ferias", "atestado", "licença"]): return "#94A3B8" # CINZA
    if pos == 0 or media == 0: return "#94A3B8"
    if 1 <= pos <= 8: return "#10B981" # VERDE
    if pos > (total_ativos - 4): return "#EF4444" # VERMELHO
    return "#F59E0B" # AMARELO

def render_premium_card(label, pos, media, trend_val="", delta=0, color="#94A3B8", txt="", obs=""):
    comb = (str(txt) + str(obs)).lower().strip()
    status_esp = ""
    for s in ["férias", "ferias", "atestado", "licença"]:
        if s in comb: status_esp = "FÉRIAS" if "feria" in s else s.upper(); break
    
    if status_esp: val_display, trend_html = status_esp, ""
    elif pos == 0 or media == 0: val_display, trend_html = " - ", ""
    else:
        val_display = f"{int(pos)}º"
        if trend_val == "up" and delta > 0: 
            trend_html = f'<span class="trend-badge trend-up">↑ {int(delta)}</span>'
        elif trend_val == "down" and delta > 0: 
            trend_html = f'<span class="trend-badge trend-down">↓ {int(delta)}</span>'
        elif trend_val == "stable": 
            bg_color = color + "22"
            trend_html = f'<span class="trend-badge" style="background: {bg_color} !important; color: {color} !important; border: 1px solid {color};">=</span>'
        else: trend_html = ""
            
    st.markdown(f"""<div class="card-premium"><div class="status-bar" style="background-color: {color};"></div><div class="card-content"><div class="card-label">{label}</div><div class="card-value">{val_display} {trend_html}</div><div class="card-footer">Média: {media:.2f}</div></div></div>""", unsafe_allow_html=True)

# --- INTERFACE ---

aba_individual, aba_equipe = st.tabs(["👤 Performance Individual", "👥 Panorama da Equipe"])
df_master = carregar_dados_equipe_completa()

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

    st.markdown(f'''
        <div class="header-instruction">
            <span style="font-size: 20px; color: {DELL_BLUE}; font-weight: 800;">Dell QA Analytics Pro</span>
            <span class="user-tag">👤 Usuário: {st.session_state.usuario_identificado.title()}</span>
        </div>
    ''', unsafe_allow_html=True)

    if colab_sel == "Selecione...":
        if not df_master.empty:
            df_mes_atu = df_master[df_master['Mês'] == mes_sel_ind.capitalize()]
            w1, w2, w3, w4 = st.columns(4)
            with w1:
                turmas = df_mes_atu.drop_duplicates('Nome_Exibicao')['Turma_Exibicao'].value_counts().sort_index()
                html_t = "".join([f'<div class="list-item"><span>{t}</span><b>{v}</b></div>' for t,v in turmas.items()])
                st.markdown(f'<div class="welcome-card"><div class="welcome-card-title">👥 Equipe por Turma</div>{html_t}</div>', unsafe_allow_html=True)
            
            # --- ESPAÇO CENTRAL: ALERTA DE PRODUTIVIDADE COM LÓGICA DAS BOLINHAS ---
            with w2:
                alertas_html = ""
                nomes_unicos = df_master['Nome_Exibicao'].unique()
                idx_mes_sel = MESES_ORDEM.index(mes_sel_ind)
                meses_hist = [m.capitalize() for m in MESES_ORDEM[:idx_mes_sel+1]]

                for nome in nomes_unicos:
                    dados_n = df_master[df_master['Nome_Exibicao'] == nome].copy()
                    meses_vermelhos_nome = []
                    
                    for m_check in meses_hist:
                        linha = dados_n[dados_n['Mês'] == m_check]
                        if not linha.empty:
                            r = linha.iloc[0]
                            # Calcula a cor exata da bolinha para este mês
                            df_ref_mes = df_master[df_master['Mês'] == m_check].copy()
                            df_ref_mes['is_cinza'] = df_ref_mes.apply(lambda row: any(x in (str(row['Pos_Mes_Txt'])+str(row['Obs'])).lower() for x in ["férias","ferias","atestado","licença"]), axis=1)
                            atv = len(df_ref_mes[~df_ref_mes['is_cinza']])
                            
                            media_m = r['Pontos']/r['Dias'] if r['Dias']>0 else 0
                            cor_bolinha = get_status_color(r['Pos_Geral'], media_m, r['Pos_Geral_Txt'], r['Obs'], 38) # Regra do Geral
                            
                            if cor_bolinha == "#EF4444":
                                meses_vermelhos_nome.append(m_check[:3])

                    if len(meses_vermelhos_nome) >= 3:
                        status = '<span class="alert-status status-chamada">🚨 CHAMAR PARA CONVERSA</span>'
                        pills = "".join([f'<span class="alert-pill">{m}</span>' for m in meses_vermelhos_nome[-3:]])
                        alertas_html += f'<div class="alert-row"><span class="alert-name">{nome[:18]}</span>{status}<div class="alert-pills">{pills}</div></div>'
                    elif len(meses_vermelhos_nome) == 2:
                        status = '<span class="alert-status status-atencao">⚠️ ATENÇÃO: Possível Conversa</span>'
                        pills = "".join([f'<span class="alert-pill">{m}</span>' for m in meses_vermelhos_nome[-2:]])
                        alertas_html += f'<div class="alert-row"><span class="alert-name">{nome[:18]}</span>{status}<div class="alert-pills">{pills}</div></div>'

                if not alertas_html:
                    alertas_html = "<div style='color:#10B981; font-size:14px; margin-top:20px;'>✅ Produtividade em dia.</div>"
                
                st.markdown(f'''
                    <div class="alert-container">
                        <div class="alert-header">⚠️ ALERTA DE PRODUTIVIDADE</div>
                        <div style="overflow-y: auto; height: 260px;">{alertas_html}</div>
                    </div>
                ''', unsafe_allow_html=True)

            with w3:
                pcds = df_mes_atu.drop_duplicates('Nome_Exibicao')['PCD_Tipo'].value_counts()
                html_p = "".join([f'<div class="list-item"><span>{p}</span><b>{v}</b></div>' for p,v in pcds.items() if p.upper() not in ["NÃO","NA","N/A","NO"]])
                st.markdown(f'<div class="welcome-card"><div class="welcome-card-title">♿ PCD por Categoria</div>{html_p if html_p else "Sem registros."}</div>', unsafe_allow_html=True)
            with w4:
                rank_d = df_master.groupby('Nome_Exibicao').apply(lambda x: x['Pontos'].sum()/x['Dias'].sum() if x['Dias'].sum()>0 else 0).sort_values().reset_index()
                rank_d.columns = ['Nome_Exibicao', 'Media']
                ultimos = rank_d[rank_d['Media']>0].head(4).copy()
                ultimos = ultimos.sort_values(by='Media', ascending=False)
                html_r = "".join([f'<div class="list-item"><span style="color:#EF4444;">{n[:18]}</span><b>{v:.2f}</b></div>' for n,v in zip(ultimos['Nome_Exibicao'], ultimos['Media'])])
                st.markdown(f'<div class="welcome-card"><div class="welcome-card-title">⚠️ Últimos do Ranking Geral</div>{html_r}</div>', unsafe_allow_html=True)
    else:
        # PERMANECE IGUAL (BASE MASTER INDIVIDUAL)
        df_ind, nome_f, badge, turma, pcd = carregar_dados_colaborador(mapa_arq[colab_sel])
        if df_ind is not None:
            df_mes_total = df_master[df_master['Mês'] == mes_sel_ind.capitalize()].copy()
            df_mes_total['is_cinza'] = df_mes_total.apply(lambda r: any(x in (str(r['Pos_Mes_Txt'])+str(r['Obs'])).lower() for x in ["férias","ferias","atestado","licença"]), axis=1)
            total_ativos_mes = len(df_mes_total[~df_mes_total['is_cinza']])
            total_time_completo = 38

            l_atu = df_ind[df_ind['Mês'] == mes_sel_ind.capitalize()]
            if not l_atu.empty:
                row = l_atu.iloc[0]; idx = MESES_ORDEM.index(mes_sel_ind)
                df_ac = df_ind[df_ind['Mês'].isin([m.capitalize() for m in MESES_ORDEM[:idx+1]])]
                m_g = df_ac['Pontos'].sum() / df_ac['Dias'].sum() if df_ac['Dias'].sum() > 0 else 0
                m_m = row['Pontos'] / row['Dias'] if row['Dias'] > 0 else 0
                
                t_m, d_m, t_g, d_g = "", 0, "", 0
                if idx > 0:
                    l_ant = df_ind[df_ind['Mês'] == MESES_ORDEM[idx-1].capitalize()]
                    if not l_ant.empty:
                        ant = l_ant.iloc[0]
                        if ant['Pos_Mes']>0 and row['Pos_Mes']>0:
                            if row['Pos_Mes'] < ant['Pos_Mes']: d_m, t_m = abs(row['Pos_Mes']-ant['Pos_Mes']), "up"
                            elif row['Pos_Mes'] > ant['Pos_Mes']: d_m, t_m = abs(row['Pos_Mes']-ant['Pos_Mes']), "down"
                            else: d_m, t_m = 0, "stable"
                        if ant['Pos_Geral']>0 and row['Pos_Geral']>0:
                            if row['Pos_Geral'] < ant['Pos_Geral']: d_g, t_g = abs(row['Pos_Geral']-ant['Pos_Geral']), "up"
                            elif row['Pos_Geral'] > ant['Pos_Geral']: d_g, t_g = abs(row['Pos_Geral']-ant['Pos_Geral']), "down"
                            else: d_g, t_g = 0, "stable"

                st.markdown(f"<h1 style='color:{DELL_BLUE}; font-weight:800;'>{nome_f}</h1>", unsafe_allow_html=True)
                st.markdown(f'<div><span class="info-tag">🆔 {badge}</span><span class="info-tag">👥 {turma}</span></div>', unsafe_allow_html=True)
                st.divider()

                col_c1, col_c2 = st.columns(2)
                with col_c1: render_premium_card("Ranking Mensal", row['Pos_Mes'], m_m, t_m, d_m, get_status_color(row['Pos_Mes'], m_m, row['Pos_Mes_Txt'], row['Obs'], total_ativos_mes), row['Pos_Mes_Txt'], row['Obs'])
                with col_c2: render_premium_card("Ranking Geral (Acumulado)", row['Pos_Geral'], m_g, t_g, d_g, get_status_color(row['Pos_Geral'], m_g, row['Pos_Geral_Txt'], row['Obs'], total_time_completo), row['Pos_Geral_Txt'], row['Obs'])
                
                st.write("") 
                m1, m2, m3, m4 = st.columns(4)
                with m1:
                    st.markdown(f'<div class="mini-card"><div class="mini-card-label">📅 Dias (Mês / Ano)</div><div class="mini-card-value">{int(row["Dias"])} / {int(df_ind["Dias"].sum())}</div></div>', unsafe_allow_html=True)
                with m2:
                    st.markdown(f'<div class="mini-card"><div class="mini-card-label">🤝 Ações Sociais (Mês / Ano)</div><div class="mini-card-value">{int(row["Acoes_Sociais"])} / {int(df_ind["Acoes_Sociais"].sum())}</div></div>', unsafe_allow_html=True)
                with m3:
                    st.markdown(f'<div class="mini-card"><div class="mini-card-label">⏳ Voluntariado (Mês / Ano)</div><div class="mini-card-value">{int(df_ind["Horas_Voluntariado"].sum())}h</div></div>', unsafe_allow_html=True)
                with m4:
                    st.markdown(f'<div class="mini-card"><div class="mini-card-label">🛠️ Suporte (Mês / Ano)</div><div class="mini-card-value">{int(df_ind["Suporte"].sum())}</div></div>', unsafe_allow_html=True)

                st.divider()
                
                df_graf = df_ind[df_ind['Pontos']>0].copy()
                df_graf['Mês'] = pd.Categorical(df_graf['Mês'], categories=MESES_ORDEM, ordered=True)
                df_graf = df_graf.sort_values('Mês')
                
                def config_fig(fig, title, col=None, is_geral=False, is_rank=True):
                    fig.update_xaxes(categoryorder='array', categoryarray=MESES_ORDEM, range=[-0.5, 11.5], showgrid=True)
                    fig.update_layout(title=title, height=400, plot_bgcolor='white', margin=dict(t=80, b=40, l=40, r=40))
                    if is_rank:
                        y_max = df_graf[col].max() if not df_graf.empty else 38
                        fig.update_yaxes(autorange="reversed", range=[y_max + 2, -1.5])
                        def obter_clrs():
                            lista = []
                            for _, lin in df_graf.iterrows():
                                m_ref = lin['Mês']; df_ref = df_master[df_master['Mês'] == m_ref].copy()
                                df_ref['is_cinza'] = df_ref.apply(lambda r: any(x in (str(r['Pos_Mes_Txt'])+str(r['Obs'])).lower() for x in ["férias","ferias","atestado","licença"]), axis=1)
                                atv = total_time_completo if is_geral else len(df_ref[~df_ref['is_cinza']])
                                lista.append(get_status_color(lin[col], 1, lin['Pos_Mes_Txt'], lin['Obs'], atv))
                            return lista
                        fig.update_traces(marker=dict(size=12, color=obter_clrs()), line=dict(color=DELL_BLUE, width=3))
                    else:
                        y_val_max = df_graf[col].max() if not df_graf.empty else 100
                        fig.update_yaxes(range=[-5, y_val_max * 1.3])
                        fig.update_traces(line_color=DELL_BLUE, marker=dict(size=10, color=DELL_BLUE))
                    return fig

                f_s = dict(size=15, color="black", family="Arial Black")
                r1, r2 = st.columns(2)
                with r1:
                    fig1 = go.Figure(go.Scatter(x=df_graf['Mês'], y=df_graf['Pos_Mes'], mode='markers+lines+text', text=df_graf['Pos_Mes'].astype(int), textposition="bottom center", textfont=f_s))
                    st.plotly_chart(config_fig(fig1, "Ranking Mensal (Jan-Dez)", 'Pos_Mes'), use_container_width=True)
                with r2:
                    fig2 = go.Figure(go.Scatter(x=df_graf['Mês'], y=df_graf['Pos_Geral'], mode='markers+lines+text', text=df_graf['Pos_Geral'].astype(int), textposition="bottom center", textfont=f_s))
                    st.plotly_chart(config_fig(fig2, "Ranking Geral (Jan-Dez)", 'Pos_Geral', is_geral=True), use_container_width=True)
                
                g1, g2 = st.columns(2)
                with g1:
                    fig3 = px.line(df_graf, x='Mês', y='Pontos', markers=True, text='Pontos', title="Evolução de Pontos")
                    fig3.update_traces(textposition="bottom center", textfont=f_s)
                    st.plotly_chart(config_fig(fig3, "Evolução de Pontos", col='Pontos', is_rank=False), use_container_width=True)
                with g2:
                    fig4 = px.line(df_graf, x='Mês', y='Casos', markers=True, text='Casos', title="Volume de Casos")
                    fig4.update_traces(textposition="bottom center", textfont=f_s)
                    st.plotly_chart(config_fig(fig4, "Volume de Casos", col='Casos', is_rank=False), use_container_width=True)

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
            st.markdown(f"<h3 style='color:{DELL_BLUE}; font-weight:800;'>🏆 Ranking Geral até {mes_eq_g}</h3>", unsafe_allow_html=True)
            ms_r = [m.capitalize() for m in MESES_ORDEM[:MESES_ORDEM.index(mes_eq_g)+1]]
            res = df_master[df_master['Mês'].isin(ms_r)].groupby(['Nome_Exibicao', 'Turma_Exibicao']).apply(lambda x: x['Pontos'].sum() / x['Dias'].sum() if x['Dias'].sum() > 0 else 0).sort_values(ascending=False).reset_index()
            res.columns = ['Nome', 'Turma', 'Media']
            html_g = "".join([f'<div class="colab-item"><div class="pos-number {"bolinha-verde" if i<8 else "bolinha-vermelha" if i>=len(res)-4 else "bolinha-amarela"}">{i+1}º</div><div style="flex-grow:1;"><b>{r["Nome"]}</b><br><small>{r["Turma"]}</small></div><div style="font-weight:800;">{f"{r["Media"]:.2f}" if r["Media"]>0 else "FÉRIAS"}</div></div>' for i,r in res.iterrows()])
            st.markdown(f'<div class="ranking-container">{html_g}</div>', unsafe_allow_html=True)
            
        with col_m:
            st.markdown(f"<h3 style='color:{DELL_BLUE}; font-weight:800;'>📅 Ranking Mensal: {mes_eq_m}</h3>", unsafe_allow_html=True)
            df_m = df_master[df_master['Mês'] == mes_eq_m.capitalize()].copy()
            df_m['Media'] = df_m['Pontos'] / df_m['Dias']; df_m = df_m.sort_values(by="Media", ascending=False).reset_index(drop=True)
            df_m['is_cinza'] = df_m.apply(lambda r: any(x in (str(r['Pos_Mes_Txt'])+str(r['Obs'])).lower() for x in ["férias","ferias","atestado","licença"]), axis=1)
            at_idx = df_m[~df_m['is_cinza']].index
            v_idx, r_idx = at_idx[:8], at_idx[-4:]
            html_m = "".join([f'<div class="colab-item"><div class="pos-number {"bolinha-cinza" if r["is_cinza"] else "bolinha-verde" if i in v_idx else "bolinha-vermelha" if i in r_idx else "bolinha-amarela"}">{i+1}º</div><div style="flex-grow:1;"><b>{r["Nome_Exibicao"]}</b><br><small>{r["Turma_Exibicao"]}</small></div><div style="font-weight:800;">{f"{r["Media"]:.2f}" if not r["is_cinza"] else "FÉRIAS"}</div></div>' for i,r in df_m.iterrows()])
            st.markdown(f'<div class="ranking-container">{html_m}</div>', unsafe_allow_html=True)