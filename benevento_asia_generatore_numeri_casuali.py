import streamlit as st
import pandas as pd
import pickle as pkl
import numpy as np
import time
from datetime import datetime
from helpers import return_final_set_of_chosen_numbers, put_together_seed_and_params

#############################################
####### Load stuff
#############################################

with open('dict_with_the_number_of_things_to_sample.pkl', 'rb') as handle:
    dict_with_the_number_of_things_to_sample = pkl.load(handle)

elenco_punti_prelievo = pd.read_pickle('final_list_of_street_for_streamlit.pkl')

#############################################
####### Streamlit
#############################################

# Titoli

'''
# Piano di campionamento valutazione pulizia strada

'''

# st.header("Generatore di strade da campionare (cambia test)")
# st.success(
#     "Testo che gabriella vuole metta",
# )

st.sidebar.image('logo_asia.png', caption=None, width=None, clamp=False, channels="RGB", output_format="auto", use_container_width=True)

# Sidebar

st.sidebar.write("\n\n")
the_error_choice = st.sidebar.selectbox(
    "Seleziona il livello di errore desiderato",
    ("1%", "5%"),
    index=1,
    placeholder="Scegli un livello di errore",
)
st.sidebar.write("Hai selezionato:", the_error_choice)
if(the_error_choice =='1%'):
    confidence_interval = '99%'
elif(the_error_choice =='5%'):
    confidence_interval = '95%'
else:
    confidence_interval = ''
st.sidebar.write("La tua scelta corrisponde ad un livello di confidenza del ", confidence_interval)

st.sidebar.write("\n\n")
# st.sidebar.write("Permetti la selezione di piu' punti raccolta nella stessa strada. \n (Consigliamo di no)")
# allow_same_street = st.sidebar.toggle("Lo permetto")

string_allow_same_street = st.sidebar.radio(
    "Permetti la selezione di piu' punti raccolta nella stessa strada. \n (Consigliamo di no)",
    ["Si", "No"],
    index=1,
)
if(string_allow_same_street=='Si'):
    allow_same_street = True
else:
    allow_same_street = False





st.write("\n\n")
st.button("Rigenera le strade da campionare", type="primary")

current_time = int(time.time())
final_seed = put_together_seed_and_params(seed_int=current_time, the_error_choice=the_error_choice, allow_same_street=allow_same_street)
rng = np.random.default_rng(seed=final_seed)

df_to_print = []
for current_tipo in dict_with_the_number_of_things_to_sample[the_error_choice].keys():
    final_choice = return_final_set_of_chosen_numbers(current_tipo, the_error_choice, dict_with_the_number_of_things_to_sample, elenco_punti_prelievo, rng=rng, alllow_same_street=allow_same_street)
    final_choice = np.sort(final_choice)
    tmp_df = elenco_punti_prelievo.loc[(current_tipo,final_choice),:]
    df_to_print.append(tmp_df)
df_to_print = pd.concat(df_to_print)[['Nome strada']]




st.table(df_to_print)

current_date = datetime.now().date()
formatted_date = current_date.strftime("%Y_%m_%d")
name_to_save = formatted_date+'_piano_campionamento.csv'
st.download_button('Scarica la tabella in CSV', df_to_print.to_csv(), name_to_save)

st.write('Condividi il codice identificativo dei risultati:')

st.success(
    final_seed
)