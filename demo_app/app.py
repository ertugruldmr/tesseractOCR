import os
import numpy as np
import tensorflow as tf
import pytesseract
import gradio as gr
import requests
from tensorflow.keras.layers import StringLookup


# installing
os.system("pip install pytesseract")
os.system("sudo apt install tesseract-ocr")

# configurations
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
os.environ['TESSDATA_PREFIX'] = TESSDATA_PREFIX = "/usr/share/tesseract-ocr/4.00/tessdata/"

# defining params
base_dir = "https://github.com/tesseract-ocr/tessdata/raw/main/"
valid_langs = ['eng', 'ara', 'ces', 'chi_sim', 'chi_tra', 'deu', 'fra', 'ita', 'jpn', 'kor', 'nld', 'por', 'rus', 'spa', 'tur', 'rus']

# Util Functions
def prepare_path(lang, base=base_dir, valid_langs=valid_langs):
  
  # Checking the params
  if lang not in valid_langs: raise "It is not valid language"
  
  # preparing the requeits
  url = f"{base_dir}{lang}.traineddata"
  req_url = f"{url}?raw=true"
  return url, req_url

def download_required_language(lang, TESSDATA_PREFIX=TESSDATA_PREFIX):
  
  required_file = f"{lang}.traineddata"
  
  # if it is not alread installed, download it.
  if required_file not in os.listdir(TESSDATA_PREFIX):
      try:
        # Prepare the corresponding configuration downloading path
        url, req_url = prepare_path(lang)
        
        # add the new language into local
        dst = os.path.join(TESSDATA_PREFIX, required_file)
        with open(dst, "wb") as f:
          f.write(requests.get(url).content)
        
        return f"{lang} package has installed successfully"
      except Exception as e:
        return f"Be sure lang param is valid,\nerror:{e}"
    
  else:
    return f"{lang} package has already installed"

def ocr_implement(img, lang):
  
  try:
    # pre-process to easy read
    processed_img = img.convert('L')
    test = pytesseract.image_to_string(processed_img, lang=lang )
  except Exception as e:
        return f"Be sure lang param is valid,\nerror:{e}"

  return test

# Defining GUI Components
with gr.Blocks() as demo:
    img = gr.Image(type="pil", source="upload")
    lang  = gr.Dropdown(choices=valid_langs, value="eng", label="Language")
    with gr.Row():
        extract_btn = gr.Button("Extract text form image")
        install_lang = gr.Button("install language")
    output = gr.Textbox()

    # connecting the button functions
    extract_btn.click(ocr_implement, inputs=[img, lang], outputs=output)
    install_lang.click(download_required_language, inputs=lang, outputs=output)

    # setting the exmples
    gr.Examples("Examples", img)

# Launching the demo
if __name__ == "__main__":
    demo.launch()
