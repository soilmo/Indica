import pandas as pd
import streamlit as st
import email, smtplib, ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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

#@st.cache(persist=True, max_entries = 20, ttl = 1800, show_spinner=False)
def enviar_email(tipo, termo, pessoa):
    
    subject = "IL|"+str(tipo)+"|"+str(termo)+"|"+str(pessoa)
    body = "IL|"+str(tipo)+"|"+str(termo)+"|"+str(pessoa)
    sender_email = "pedrohs.t19@gmail.com"
    receiver_email = "pedrohs.t19@gmail.com"
    password = "291096santiago"

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

#@st.cache(persist=True, max_entries = 20, ttl = 1800, show_spinner=False)
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
    st.markdown("Temos " + str(df[filtro].shape[0]) + " indicação")
else:
    st.markdown("Temos " + str(df[filtro].shape[0]) + " indicações")

aux = df[filtro]
    
for i in range(aux.shape[0]):

    nome, telefone, zap, descricao, insta = opcoes_resultado(aux, i)
    if zap != "nan" and zap == zap:
        link_zap = 'https://api.whatsapp.com/send?phone=55'+str(zap)+'&text=Oi%20'+str(nome).replace(" ","%20")+'%2C%20te%20achei%20pelo%20Indica%20Leopoldina.%20Gostaria%20de%20saber%20mais%20sobre%20seu%20serviço%20de%20'+categoria.replace(" ","%20")
        t = '*Mensagem no Zap*'
        link_zap = f'[{t}]({link_zap})'
    if insta != "nan" and insta == insta:
        link_insta = 'https://www.instagram.com/'+str(insta)+'/'
        t = '*Instagram*'
        link_insta = f'[{t}]({link_insta})'
    
    
    #with st.expander(label=nome, expanded=False):
    if st.button(nome):
        
        st.markdown("__Descrição:__ " + str(descricao))
        
        if telefone == telefone:
                st.markdown("__Telefone:__ " + str(telefone))
            
        if zap != "nan" and zap == zap and insta != "nan" and insta == insta:
            st.markdown(link_zap + " | " +link_insta, unsafe_allow_html=True)
        elif (zap == "nan" or zap!=zap) and (insta != "nan" and insta == insta):
            st.markdown(link_insta, unsafe_allow_html=True)
        elif (zap != "nan" and zap == zap) and (insta == "nan" or insta != insta):
            st.markdown(link_zap, unsafe_allow_html=True)
        
        #enviar_email("categoria", categoria, nome)
        
            
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
        
        if zap != "nan" and zap == zap:
            link_zap = 'https://api.whatsapp.com/send?phone=55'+str(zap)+'&text=Oi%20'+str(nome).replace(" ","%20")+'%2C%20te%20achei%20pela%20Busca!%20Gostaria%20de%20saber%20mais%20sobre%20seu%20serviço%20de%20'+categoria.replace(" ","%20")
            t = '*Mensagem no Zap*'
            link_zap = f'[{t}]({link_zap})'
        if insta != "nan" and insta == insta:
            link_insta = 'https://www.instagram.com/'+str(insta)+'/'
            t = '*Instagram*'
            link_insta = f'[{t}]({link_insta})'

        if st.button(nome + " "):
            st.markdown("__Descrição:__ " + str(descricao))
            
            if telefone == telefone:
                st.markdown("__Telefone:__ " + str(telefone))

            if zap != "nan" and zap == zap and insta != "nan" and insta == insta:
                st.markdown(link_zap + " | " +link_insta, unsafe_allow_html=True)
            elif (zap == "nan" or zap!=zap) and (insta != "nan" and insta == insta):
                st.markdown(link_insta, unsafe_allow_html=True)
            elif (zap != "nan" and zap == zap) and (insta == "nan" or insta != insta):
                st.markdown(link_zap, unsafe_allow_html=True)
            #enviar_email("busca", categoria, nome)
        


t = "*Indicações, dúvidas ou sugestões? Fale com a gente :)*"
link_duvidas = 'https://api.whatsapp.com/send?phone=5512982328955&text=Oi%20Indica%20Leopoldina!%20Pode%20me%20ajudar%3F'
st.markdown(f'[{t}]({link_duvidas})', unsafe_allow_html=True)
