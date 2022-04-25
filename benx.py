import pandas as pd
import streamlit as st

# Ler base
url = 'https://github.com/soilmo/Indica/raw/main/servicos.csv?raw=true'
df = pd.read_csv(url, encoding='utf-8', sep = ";")

# Mudar título
st.set_page_config(page_title = "Indica Leopoldina", page_icon=":nerd_face:")

# Esconder menu canto superior direito
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Carregar Logo
st.title("Indica Leopoldina")

st.markdown("Encontre as melhores indicações da região :smile:")


def opcoes_resultado(aux, i):
    nome = aux['nome'].iloc[i]
    telefone = aux['telefone'].iloc[i]
    zap = str(aux['whatsapp'].iloc[i]).replace("-","").replace(".","").replace(" ","").replace("(","").replace(")","")
    descricao = aux['descricao'].iloc[i]
    insta = aux['instagram'].iloc[i]
    return nome, telefone, zap, descricao, insta


# Buscar categoria
categorias =list(df['categoria'].unique())
categorias.sort()

categoria = st.selectbox("Qual categoria?", options=categorias, index = categorias.index("Lanches e doces"))
filtro = df['categoria']==categoria

if df[filtro].shape[0] == 1:
    st.markdown("Temos " + str(df[filtro].shape[0]) + " indicação para você")
else:
    st.markdown("Temos " + str(df[filtro].shape[0]) + " indicações para você")

aux = df[filtro]
    
for i in range(aux.shape[0]):

    nome, telefone, zap, descricao, insta = opcoes_resultado(aux, i)
    
    if zap == zap:
        link_zap = 'https://api.whatsapp.com/send?phone=55'+str(zap)+'&text=Oi%20'+str(nome).replace(" ","%20")+'%2C%20te%20achei%20pelo%20Indica%20Leopoldina.%20Gostaria%20de%20saber%20mais%20sobre%20seu%20serviço%20de%20'+categoria.replace(" ","%20")
        t = '*Mensagem no Zap*'
        link_zap = f'[{t}]({link_zap})'
    if insta == insta:
        link_insta = 'https://www.instagram.com/'+str(insta)+'/'
        t = '*Instagram*'
        link_insta = f'[{t}]({link_insta})'

    with st.expander(label=nome, expanded=False):
    
        st.markdown("__Telefone:__ " + str(telefone))
        st.markdown("__Descrição:__ " + str(descricao))
        if zap == zap and insta == insta:
            st.markdown(link_zap + " | " +link_insta, unsafe_allow_html=True)
        elif zap != zap and insta == insta:
            st.markdown(link_insta, unsafe_allow_html=True)
        elif zap == zap and insta != insta:
            st.markdown(link_zap, unsafe_allow_html=True)
            
# Busca específica
st.session_state.busca = st.text_input("Não encontrou o que queria? Digite a palavra chave de sua busca", "").lower()

if st.session_state.busca != "":

    resultados = []
    for i in range(df.shape[0]):
        desc = df['descricao'].iloc[i]
        try:
            if st.session_state.busca in desc.lower():
                resultados.append(i)
        except:
            pass

    if len(resultados) == 1:
        st.markdown("Temos " + str(len(resultados)) + " resultado para você")
    else:
        st.markdown("Temos " + str(len(resultados)) + " resultados para você")

    filtro = df.index.isin(resultados)
    aux = df[filtro]

    for i in range(aux.shape[0]):

        nome, telefone, zap, descricao, insta = opcoes_resultado(aux, i)
        
        if zap == zap:
            link_zap = 'https://api.whatsapp.com/send?phone=55'+str(zap)+'&text=Oi%20'+str(nome).replace(" ","%20")+'%2C%20te%20achei%20pela%20Busca!%20Gostaria%20de%20saber%20mais%20sobre%20seu%20serviço%20de%20'+categoria.replace(" ","%20")
            t = '*Mensagem no Zap*'
            link_zap = f'[{t}]({link_zap})'
        if insta == insta:
            link_insta = 'https://www.instagram.com/'+str(insta)+'/'
            t = '*Instagram*'
            link_insta = f'[{t}]({link_insta})'

        with st.expander(label=nome, expanded=False):
        
            st.markdown("__Telefone:__ " + str(telefone))
            st.markdown("__Descrição:__ " + str(descricao))
            if zap == zap and insta == insta:
                st.markdown(link_zap + " | " +link_insta, unsafe_allow_html=True)
            elif zap != zap and insta == insta:
                st.markdown(link_insta, unsafe_allow_html=True)
            elif zap == zap and insta != insta:
                st.markdown(link_zap, unsafe_allow_html=True)

t = "*Indicações, dúvidas ou sugestões? Fale com a gente :)*"
link_duvidas = 'https://api.whatsapp.com/send?phone=5512982328955&text=Oi%20Indica%20Leopoldina!%20Pode%20me%20ajudar%3F'
st.markdown(f'[{t}]({link_duvidas})', unsafe_allow_html=True)
