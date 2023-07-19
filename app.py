import pandas as pd
import streamlit as st
import yfinance as yf
from datetime import date
from io import BytesIO

st.title('Cotações de Fundos')

st.image('https://th.bing.com/th/id/R.592a9b01eb077958f53aa385dc40f1d5?rik=ESxDzIaUACogwg&pid=ImgRaw&r=0')

file = st.text_input(
    'Digite o Fundo desejado'
    
)

nome_fundo = f'{file}.SA'

start = st.date_input('Escolha a data inicial: ')

end = st.date_input('Escolha a data final: ')

if start == '' or end == '':
    st.write('Por favor, escolha as datas desejadas')
else:
    cotacao = yf.download(nome_fundo, start=start , end= end, interval='1mo')

cotacao = cotacao['Close']

if not cotacao.empty:
    buffer = BytesIO()

    with pd.ExcelWriter(buffer, mode='xlsx', engine='openpyxl') as writer:
            cotacao.to_excel(writer, index=True)

    buffer.seek(0)

    def download_arquivo(buffer, nome_arquivo):
        buffer.seek(0)
        st.download_button(label='Baixe seu arquivo em xlsx', data=buffer, file_name=nome_arquivo)

    download_arquivo(buffer, f'Cotações_{nome_fundo}.xlsx')

st.write('Suas cotações: ', cotacao)









