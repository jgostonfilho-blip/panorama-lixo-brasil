import streamlit as st
import requests
import xml.etree.ElementTree as ET
import pandas as pd
import plotly.express as px

# Configuração da página do Streamlit
st.set_page_config(page_title="Panorama do Lixo no Brasil", page_icon="♻️", layout="wide")

# Título e cabeçalho principal
st.title("♻️ Panorama do Descarte de Resíduos no Brasil")
st.write("Acompanhe dados oficiais e pesquise em tempo real as últimas notícias sobre a gestão de resíduos sólidos, reciclagem e sustentabilidade no país.")

st.markdown("---")

# --- SEÇÃO 1: DADOS REAIS (Base ABRELPE) ---
st.header("📊 Dados Atuais (Panorama Nacional)")
st.write("Dados baseados nos levantamentos mais recentes da Associação Brasileira de Empresas de Limpeza Pública e Resíduos Especiais (ABRELPE).")

col1, col2, col3 = st.columns(3)
col1.metric(label="Geração Anual de Lixo", value="81.8 Milhões ton", delta="1.04 kg/hab/dia", delta_color="off")
col2.metric(label="Taxa de Reciclagem", value="~ 4%", delta="Abaixo da média global (19%)", delta_color="inverse")
col3.metric(label="Descarte Inadequado", value="39%", delta="Vão para lixões ou aterros controlados", delta_color="inverse")

# Gráfico interativo
st.subheader("Destinação Final dos Resíduos Coletados")
dados_destinacao = pd.DataFrame({
    "Destino": ["Aterros Sanitários (Adequado)", "Lixões e Aterros Controlados (Inadequado)"],
    "Porcentagem": [61, 39]
})

fig = px.pie(dados_destinacao, values="Porcentagem", names="Destino", hole=0.4, 
             color="Destino", color_discrete_map={"Aterros Sanitários (Adequado)": "#2e7d32", 
                                                  "Lixões e Aterros Controlados (Inadequado)": "#c62828"})
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# --- SEÇÃO 2: BUSCADOR DE NOTÍCIAS (EM TEMPO REAL) ---
st.header("📰 Pesquisa de Notícias em Tempo Real")
st.write("Utilize a lacuna abaixo para buscar as últimas reportagens sobre o descarte de lixo, lixões, coleta seletiva e leis ambientais no Brasil.")

# Lacuna de pesquisa
query = st.text_input("Digite o termo que deseja pesquisar:", value="descarte de lixo Brasil")

def buscar_noticias(termo, limite=10):
    """
    Busca notícias reais usando o feed RSS público do Google News focado no Brasil.
    """
    termo_formatado = termo.replace(" ", "%20")
    # URL do Google News RSS com filtros de idioma (pt-BR) e localidade (BR)
    url = f"https://news.google.com/rss/search?q={termo_formatado}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    
    try:
        resposta = requests.get(url)
        # Fazendo o parse do XML retornado pelo Google News
        root = ET.fromstring(resposta.content)
        noticias = []
        
        for item in root.findall('./channel/item')[:limite]:
            titulo = item.find('title').text
            link = item.find('link').text
            data = item.find('pubDate').text
            
            # Limpando a string do título (o Google News costuma colocar o nome do site no final)
            if " - " in titulo:
                titulo = titulo.rsplit(" - ", 1)[0]
                
            noticias.append({"titulo": titulo, "link": link, "data": data})
            
        return noticias
    except Exception as e:
        return None

# Botão de ação
if st.button("Buscar Notícias", type="primary"):
    with st.spinner("Buscando as notícias mais recentes na internet..."):
        resultados = buscar_noticias(query)
        
        if resultados:
            st.success(f"Foram encontradas {len(resultados)} notícias recentes sobre '{query}':")
            for noti in resultados:
                # Usando HTML básico e Markdown para exibir o card da notícia
                st.markdown(f"### 🔗 [{noti['titulo']}]({noti['link']})")
                st.caption(f"📅 **Publicado em:** {noti['data']}")
                st.write("---")
        else:
            st.warning("Não foi possível encontrar notícias no momento ou ocorreu um erro de conexão.")