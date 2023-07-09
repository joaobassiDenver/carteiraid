import streamlit as st
import pandas as pd
import tabula as tb
import openpyxl

st.title('Geradora Carteira em PDF')

st.image('https://th.bing.com/th/id/R.592a9b01eb077958f53aa385dc40f1d5?rik=ESxDzIaUACogwg&pid=ImgRaw&r=0')

file = st.file_uploader(
    'Importe a carteira em PDF',
    type = 'pdf'
)

pdf = st.file_uploader(
    'Selecione o arquivo csv',
    type = 'csv'
)

tb.convert_into(file, "extrato.csv", output_format="csv", pages= "all")

def download_excel(file):
    output = io.BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)
    return output

download_link = download_excel(file)
st.markdown(download_link, unsafe_allow_html=True)

st.download_button(f'Baixar carteira em CSV', data=download_link, file_name='Carteira.csv', 
mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

pdf = pd.read_csv('extrato.csv', encoding='latin1',decimal = ',')

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

download_link = download_excel(pdf)
st.markdown(download_link, unsafe_allow_html=True)

st.download_button(f'Baixar carteira em CSV', data=download_link, file_name=f'{file}.csv', 
mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')



