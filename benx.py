import pandas as pd
import streamlit as st
from datetime import datetime

import telebot

# iniciar bot telegram
api = '2033329178:AAFAzrTtJE3uYqAoyEBdMlns_GcLjpk2big'
bot = telebot.TeleBot(api)

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

t = "*Indicações ou dúvidas? Fale com a gente :)*"
#link_duvidas = 'https://api.whatsapp.com/send?phone=5512982328955&text=Oi%20Indica%20Leopoldina!%20Pode%20me%20ajudar%3F'
link_duvidas = 'https://instagram.com/indicaleopoldina?igshid=YmMyMTA2M2Y='
st.markdown(f'[{t}]({link_duvidas})', unsafe_allow_html=True)

# Ler base
@st.cache(persist=True, max_entries = 20, ttl = 1800, show_spinner=False, suppress_st_warning=True)
def ler_base():
    url = 'https://github.com/soilmo/Indica/raw/main/servicos.csv?raw=true'
    df = pd.read_csv(url, encoding='utf-8', sep = ";")
    print("Leu")
    return df

def enviar_msg_telegram(bot, tipo, termo, pessoa):
    #texto = "IL|"+str(tipo)+"|"+str(termo)+"|"+str(pessoa)+"|"+datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    texto = "IL|"+str(tipo)+"|"+str(termo)+"|"+str(pessoa)
    bot.send_message("1333490728", texto)


@st.cache(persist=True, max_entries = 20, ttl = 1800, show_spinner=False, suppress_st_warning=True)
def opcoes_resultado(aux, i):
    nome = aux['nome'].iloc[i]
    telefone = aux['telefone'].iloc[i]
    endereco = aux['endereco'].iloc[i]
    categoria = aux['categoria'].iloc[i]
    
    zap = str(aux['whatsapp'].iloc[i]).replace("-","").replace(".","").replace(" ","").replace("(","").replace(")","")
    descricao = aux['descricao'].iloc[i]
    insta = aux['instagram'].iloc[i]
    return nome, categoria, endereco, telefone, zap, descricao, insta


# Carregar base
df = ler_base()

# Nova visita
# enviar_msg_telegram(bot, "VISITA", "", "")


# Buscar categoria
categorias =list(df['categoria'].unique())
categorias.sort()

categoria = st.selectbox("Qual categoria?", options=categorias, index = categorias.index("Lanches e doces"))
filtro = df['categoria']==categoria

if df[filtro].shape[0] == 1:
    st.markdown("Temos " + str(df[filtro].shape[0]) + " indicação")
else:
    st.markdown("Temos " + str(df[filtro].shape[0]) + " indicações")

aux = df[filtro]
    
for i in range(aux.shape[0]):

    nome, categoria_res, endereco, telefone, zap, descricao, insta = opcoes_resultado(aux, i)
    if zap != "nan" and zap == zap:
        link_zap = 'https://api.whatsapp.com/send?phone=55'+str(zap)+'&text=Oi%20'+str(nome).replace(" ","%20")+'%2C%20te%20achei%20pelo%20Indica%20Leopoldina%20(https://bit.ly/indicaleopoldina).%20Gostaria%20de%20saber%20mais%20sobre%20seu%20serviço%20de%20'+categoria.replace(" ","%20")
        
        t = '*Mensagem no Zap*'
        link_zap = f'[{t}]({link_zap})'
    if insta != "nan" and insta == insta:
        link_insta = 'https://www.instagram.com/'+str(insta)+'/'
        t = '*Instagram*'
        link_insta = f'[{t}]({link_insta})'
    
    if st.button(nome):
        
        st.markdown("__Descrição:__ " + str(descricao))
        
        if telefone == telefone:
                st.markdown("__Telefone:__ " + str(telefone))
        if endereco == endereco:
                st.markdown("__Endereço:__ " + str(endereco))
        

        if zap != "nan" and zap == zap and insta != "nan" and insta == insta:
            st.markdown(link_zap + " | " +link_insta, unsafe_allow_html=True)
        elif (zap == "nan" or zap!=zap) and (insta != "nan" and insta == insta):
            st.markdown(link_insta, unsafe_allow_html=True)
        elif (zap != "nan" and zap == zap) and (insta == "nan" or insta != insta):
            st.markdown(link_zap, unsafe_allow_html=True)
        
        enviar_msg_telegram(bot, "categoria", categoria, nome)
        
            
# Busca específica


st.session_state.busca = st.text_input("Não encontrou o que queria? Digite a palavra chave de sua busca", "").lower().replace(" ","")

if st.session_state.busca != "":

    resultados = []
    for i in range(df.shape[0]):
        desc = df['descricao'].iloc[i]
        cat = df['categoria'].iloc[i]
        try:
            if st.session_state.busca in desc.lower() or st.session_state.busca in cat.lower():
                resultados.append(i)
        except:
            pass

    if len(resultados) == 1:
        st.markdown("Temos " + str(len(resultados)) + " resultado")
    else:
        st.markdown("Temos " + str(len(resultados)) + " resultados")

    filtro = df.index.isin(resultados)
    aux = df[filtro]

    for i in range(aux.shape[0]):

        nome, categoria_res, endereco, telefone, zap, descricao, insta = opcoes_resultado(aux, i)
    
        
        if zap != "nan" and zap == zap:
            link_zap = 'https://api.whatsapp.com/send?phone=55'+str(zap)+'&text=Oi%20'+str(nome).replace(" ","%20")+'%2C%20te%20achei%20pelo%20Indica%20Leopoldina%20(https://bit.ly/indicaleopoldina).%20Gostaria%20de%20saber%20mais%20sobre%20seu%20serviço%20de%20'+categoria_res.replace(" ","%20")
            t = '*Mensagem no Zap*'
            link_zap = f'[{t}]({link_zap})'
        if insta != "nan" and insta == insta:
            link_insta = 'https://www.instagram.com/'+str(insta)+'/'
            t = '*Instagram*'
            link_insta = f'[{t}]({link_insta})'

        if st.button(nome + " | " + categoria_res):
            st.markdown("__Descrição:__ " + str(descricao))
            
            if telefone == telefone:
                st.markdown("__Telefone:__ " + str(telefone))
            if endereco == endereco:
                st.markdown("__Endereço:__ " + str(endereco))
        
            if zap != "nan" and zap == zap and insta != "nan" and insta == insta:
                st.markdown(link_zap + " | " +link_insta, unsafe_allow_html=True)
            elif (zap == "nan" or zap!=zap) and (insta != "nan" and insta == insta):
                st.markdown(link_insta, unsafe_allow_html=True)
            elif (zap != "nan" and zap == zap) and (insta == "nan" or insta != insta):
                st.markdown(link_zap, unsafe_allow_html=True)
            
            enviar_msg_telegram(bot, "busca", categoria_res, nome)
        
