# Start by making sure the `assemblyai` package is installed.
# If not, you can install it by running the following command:
# pip install -U assemblyai
#
# Note: Some macOS users may need to use `pip3` instead of `pip`.

import assemblyai as aai

# Replace with your API key
aai.settings.api_key = "721e3b73e4d244b3a352a4811a2ed97a"

# URL of the file to transcribe
FILE_URL = "https://assembly.ai/wildfires.mp3"

# You can also transcribe a local file by passing in a file path
# FILE_URL = './path/to/file.mp3'

transcriber = aai.Transcriber()


mp3_filename=r'C:\Users\evert\VSCode Projects\meeting_summary_ai\meeting_summary_ai\meeting_mp3\307286f58c444bffad40e0885bf8a45f.mp3'

config = aai.TranscriptionConfig(speaker_labels=True, speakers_expected=2,language_code='pt')



transcript = transcriber.transcribe(mp3_filename,config=config)

if transcript.status == aai.TranscriptStatus.error:
    print(transcript.error)
#else:
    #print(transcript.text)


for sentenca in transcript.utterances:
    print('Pessoa {pessoa} - {frase}'.format(pessoa=sentenca.speaker,frase=sentenca.text))