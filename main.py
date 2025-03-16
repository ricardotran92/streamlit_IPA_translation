import pandas as pd
import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from gtts import gTTS
import io
import time
import re
# import urllib.parse

# """
# 1. TypeError: Tuple[t0, t1, ...]: each t must be a type. Got ~ResponseType. 
#     Content: "...grpc..."
#     Solution: pip install --upgrade google-generativeai grpcio
# """

load_dotenv()

## NAVIGATION for personal API key
st.set_page_config(page_title='IPA and Translation Generator', page_icon='🔊', layout='wide', initial_sidebar_state='expanded')
st.sidebar.title('Navigation')
st.sidebar.write('This app is powered by Google API.')
st.sidebar.write('Please provide your GEMINI API key.')
personal_key = st.sidebar.text_input('API Key', type='password')
if personal_key:
    api_key = personal_key
else:
    api_key = os.getenv('GOOGLE_API_KEY')
# print(api_key)


# Initialize llm model
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')


# Load prompt
with open('llm_guideline.md', 'r', encoding='utf-8-sig') as f:
    prompt_text = f.read()
    # print(prompt_text)
    prompts = [prompt_text]


# Functions
@st.cache_resource
def processing_text(text):
    text = text.replace('BrE IPA', '').replace('NAmE IPA', '').replace('Synonyms', '').replace('Antonyms', '').replace('Translation', '')
    text = re.sub(r'- \*+:', '', text)
    text = re.sub(r'\*+:', '', text)
    text = text.strip()
    return text

def processing_response(response):
    parts = response.split('\n')
    parts = [re.sub(r'\s+', ' ', part) for part in parts]

    bre_ipa = [part for part in parts if 'BrE IPA' in part][0]
    name_ipa = [part for part in parts if 'NAmE IPA' in part][0]
    symnoyms = [part for part in parts if 'Synonyms' in part][0]
    antonyms = [part for part in parts if 'Antonyms' in part][0]
    translation = [part for part in parts if 'Translation' in part][0]
    
    bre_ipa = processing_text(bre_ipa)
    name_ipa = processing_text(name_ipa)
    symnoyms = processing_text(symnoyms)
    antonyms = processing_text(antonyms)
    translation = processing_text(translation)

    return bre_ipa, name_ipa, symnoyms, antonyms, translation

def convert_df_to_excel(df):
    output = io.BytesIO() # create a BytesIO buffer
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False) # write the DataFrame to the BytesIO buffer
    processed_data = output.getvalue() # get the value of the BytesIO buffer
    return processed_data
    

# Page content
st.title('IPA and Translation Generator (English to Vietnamese)')

option = st.selectbox('Select an option', ['a word or sentence(s)', 'multi-inputs from file [txt, csv, xls, xlsx]'])
if option == 'a word or sentence(s)':
    text = st.text_area('Enter text')
    # print(text)
    prompt = f"""
    Please give the following English text: {text}
    - BrE IPA
    - NAmE IPA
    - synonym if available
    - antonym if available
    - Vietnamese translation
    """
    if st.button('Generate'):
        response = model.generate_content(contents=prompt).text
        # print(response)
        st.write(response)
        tts = gTTS(text=text, lang='en')
        # tts = gTTS('Add text-to-speech to your app', lang='en')
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        st.audio(audio_fp)

elif option == 'multi-inputs from file [txt, csv, xls, xlsx]':
    uploaded_file = st.file_uploader("Choose a file", type=['txt', 'csv', 'xls', 'xlsx'])
    if uploaded_file is not None:
        print(uploaded_file.type)
        if uploaded_file.type == 'text/plain':
            df = pd.read_csv(uploaded_file, encoding='utf-8-sig', sep='\t', header=None)

        elif uploaded_file.type == 'text/csv':
            df = pd.read_csv(uploaded_file, encoding='utf-8-sig', header=None)

        elif 'spreadsheet' in uploaded_file.type:
            df = pd.read_excel(uploaded_file, header=None)
        
        df.columns = ['text']
        responses = {}
        placeholder = st.empty() # create a placeholder to show the progress bar
        for i in range(df.shape[0]):
            placeholder.write(f'Processing {i+1}/{df.shape[0]}')
            prompt = prompts[0] + f"\n\n{df.loc[i, 'text']}"
            response = model.generate_content(contents=prompt).text
            responses.update({i: response})
            time.sleep(4) # rate limit: 15rpm
        
        placeholder.write('Done!')
        


        for index, response in responses.items():
            bre_ipa, name_ipa, symnoyms, antonyms, translation = processing_response(response)
            df.loc[index, 'bre_ipa'] = bre_ipa
            df.loc[index, 'name_ipa'] = name_ipa
            df.loc[index, 'synonyms'] = symnoyms
            df.loc[index, 'antonyms'] = antonyms
            df.loc[index, 'translation'] = translation

        
        st.write(df)
        st.write('Download the result')
        if not df.empty:
            excel_data = convert_df_to_excel(df)
            st.download_button(
                label="📥 Download Excel file",
                data=excel_data,
                file_name='IPA_translation.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' # mime type for excel
            )





    

