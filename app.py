import pandas as pd
import streamlit as st
import requests
import datetime
from io import BytesIO

st.title('Cotações de Fundos')

st.image('https://th.bing.com/th/id/R.592a9b01eb077958f53aa385dc40f1d5?rik=ESxDzIaUACogwg&pid=ImgRaw&r=0')

file = st.text_input(
    'Digite o Fundo desejado'
    )

start = st.text_input('Digite a data inicial no formato (YYYY-MM-DD): ')
end = st.text_input('Digite a data final no formato (YYYY-MM-DD): ')

api_key = 'KBTYPUBRYOA4XJQI'

nome_fundo = f'{file}'

if nome_fundo == '':
    print('Digite o ticker')
else:
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={nome_fundo}.SAO&apikey={api_key}'
    r = requests.get(url)
    data = r.json()

    cotacoes = data['Monthly Time Series']

    cotacoes = pd.DataFrame(cotacoes)

    cotacoes = cotacoes.transpose()

    cotacoes = cotacoes['4. close']

    cotacoes = pd.DataFrame(cotacoes)

    cotacoes = cotacoes.reset_index()

    df = []
    for data in range(len(cotacoes)):     
        
        if cotacoes['index'][data] <= end and cotacoes['index'][data] >= start:
            resultado = cotacoes['index'][data]
            df.append(resultado)

    df = pd.DataFrame(df)

    df = df.rename(columns = {0: 'index'})

    df_merged = pd.merge(df, cotacoes, on='index', how='left')

    df_merged['4. close'] = pd.to_numeric(df_merged['4. close'])

if not df_merged.empty:
    buffer = BytesIO()

    with pd.ExcelWriter(buffer, mode='xlsx', engine='openpyxl') as writer:
            df_merged.to_excel(writer, index=False)

    buffer.seek(0)

    def download_arquivo(buffer, nome_arquivo):
        buffer.seek(0)
        st.download_button(label='Baixe seu arquivo em xlsx', data=buffer, file_name=nome_arquivo)

    download_arquivo(buffer, f'Cotações_{nome_fundo}.xlsx')

st.write('Suas cotações: ', df_merged)
