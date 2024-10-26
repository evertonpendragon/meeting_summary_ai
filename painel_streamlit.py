import streamlit as st
from moviepy.editor import *
import uuid
import assemblyai as aai
from openai import OpenAI

client = OpenAI(api_key=st.secrets['openai']['api_key'])
aai.settings.api_key = st.secrets['assemblyai']['api_key']


def mp4_to_mp3(mp4_filename, mp3_filename):
    to_convert = AudioFileClip(mp4_filename)
    to_convert.write_audiofile(mp3_filename)
    to_convert.close()

def generate_response(promt_system, prompt_text):
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",  # Specify the model to use
        messages=[
            {"role":"system", "content":promt_system},
            {"role":"user","content":prompt_text}
            
            ],
		#max_tokens=4000,		# Limits how long the response can be
		temperature=0.7			# A value between 0-1 that controls randomness
	)  # Ensure this line ends with the closing parenthesis
    texto_retorno = response.choices[0].message.content.strip()
    return texto_retorno


st.title('automacao de atas')

st.write("Criando uma ferramenta cabulosa")


uploaded_file = st.file_uploader("Selecione seu arquivo:",accept_multiple_files=False,type=["mp4"])




if uploaded_file:
    with st.spinner('Convertendo de mp4 para mp3'):
        mp4_filename = f".\meeting_mp4\{uploaded_file.name}"
        mp3_filename = r".\meeting_mp3\{arq_mp3}.mp3".format(arq_mp3=uuid.uuid4().hex)

        tempfile = open(mp4_filename,'wb')
        tempfile.write(uploaded_file.read())

        mp4_to_mp3( mp4_filename,  mp3_filename)

    st.success(f"Arquivo convertido. {mp3_filename}")

    with st.spinner('Transcrevendo audio em texto'):
        transcriber = aai.Transcriber()
        config = aai.TranscriptionConfig(speaker_labels=True, speakers_expected=2,language_code='pt')

        transcript = transcriber.transcribe(mp3_filename,config=config)

        if transcript.status == aai.TranscriptStatus.error:
            print(transcript.error)
        #else:
            #print(transcript.text)

        texto_transcrito=''
        for sentenca in transcript.utterances:
            print('Pessoa {pessoa} - {frase}'.format(pessoa=sentenca.speaker,frase=sentenca.text))
            texto_transcrito += 'Pessoa {pessoa} - {frase}\r\n'.format(pessoa=sentenca.speaker,frase=sentenca.text) 
        st.text_area("Transcrição",texto_transcrito)
    st.success("Feito!")

    
    with st.spinner('Gerando ata de reunião'):
        promt_system="Você é um especialista em gerar atas de reunião. "
        prompt_text = "Em uma redação de nível especializado, remusa as notas de reunião em um único parágrafo. Em seguida, escreva uma lista de cada um de seus pontos-chaves tratados na reunião. Por fim, liste as próximas etapas ou itens de ação sugeridos pelos palestrantes, se houver."
        
        prompt_text+="\r\n---\r\n"
        prompt_text=texto_transcrito
        prompt_text+="\r\n---\r\n"
        gpt_response=generate_response(promt_system, prompt_text)

    st.text_area("Transcrição",gpt_response)
    st.success("Feito!")