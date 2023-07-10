import streamlit as st
import pandas as pd
import tabula
import io
import tempfile
import re
import base64
import os

st.title('Geradora Extrato em CSV')

st.image('https://th.bing.com/th/id/R.592a9b01eb077958f53aa385dc40f1d5?rik=ESxDzIaUACogwg&pid=ImgRaw&r=0')

file = st.file_uploader(
    'Importe o extrato em PDF',
    type='pdf'
)


if file is not None:
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp_file:
        temp_file_path = temp_file.name
        tabula.convert_into(file, temp_file_path, output_format='csv', pages='all')

    pdf = pd.read_csv(temp_file_path, encoding='latin1', decimal=',')

    conta = pdf.iloc[1][1]

    conta = re.findall(r'\d+', conta)
    n_conta = f'{conta[1]}-{conta[2]}'

    pdf.iloc[:, 2] = pdf.iloc[:, 2].fillna(' ')

    pdf.iloc[:, 1] = pdf.iloc[:, 1] + ' ' + pdf.iloc[:, 2]

    pdf = pdf.drop(pdf.columns[2], axis=1)
    pdf = pdf.drop(pdf.columns[4], axis=1)

    pdf = pdf.drop(range(0, 8))

    pdf = pdf.dropna(axis = 0)

    def formatar_valor(valor):
        valor = str(valor)
        valor = valor.replace('(', '').replace(')', '').replace(' ', '').replace('+', '')
        if valor.endswith('-'):
            return '-' + valor[:-1]
        else:
            return valor
        

    pdf.iloc[:, 2] = pdf.iloc[:, 2].apply(formatar_valor)
    pdf['Numero Conta'] = n_conta
    pdf = pdf.rename(columns={pdf.columns[0]: 'Data', pdf.columns[1]: 'Histórico', pdf.columns[2]: 'Valor', pdf.columns[3]: 'Saldo'})

    csv_file_path = 'Extrato.csv'
    pdf.to_csv(csv_file_path, sep=';', decimal=',', index=False)

    # Função auxiliar para fazer o download do arquivo CSV
    def download_csv():
        with open(csv_file_path, 'rb') as file:
            csv_content = file.read()
        b64 = base64.b64encode(csv_content).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="Extrato.csv">Baixar arquivo CSV</a>'
        return href

    # Adicione o botão para download do arquivo CSV
    st.markdown(download_csv(), unsafe_allow_html=True)

    st.button('Copiar informações', on_click=pdf.to_clipboard, args=(None,))

    st.dataframe(pdf)








