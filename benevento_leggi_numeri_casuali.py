import streamlit as st
import pandas as pd
import pickle as pkl
import numpy as np
import time
from datetime import datetime
from helpers import return_final_set_of_chosen_numbers, extract_error_and_str_params

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

st.warning(
    "Inserisci il codice identificativo e premi invio",
)
seed_str = st.text_input("Codice", "0")
st.write("Hai inserito il codice", seed_str)

final_seed = int(seed_str)
the_error_choice, allow_same_street = extract_error_and_str_params(entire_seed=final_seed)

# Sidebar

st.sidebar.write("\n\n")
st.sidebar.write("Livello di errore:", the_error_choice)
strada_str = str(np.where(allow_same_street, 'Si', 'No'))
st.sidebar.write("Piu' punti di raccolta nella stessa strada:", strada_str)
# st.sidebar.write("Permetti la selezione di piu' punti raccolta nella stessa strada. \n (Consigliamo di no)")
# allow_same_street = st.sidebar.toggle("Lo permetto")





st.write("\n\n")



if st.button("Genera tabella"):
    rng = np.random.default_rng(seed=final_seed)
    df_to_print = []
    for current_tipo in dict_with_the_number_of_things_to_sample[the_error_choice].keys():
        final_choice = return_final_set_of_chosen_numbers(current_tipo, the_error_choice, dict_with_the_number_of_things_to_sample, elenco_punti_prelievo, rng=rng, alllow_same_street=allow_same_street)
        final_choice = np.sort(final_choice)
        tmp_df = elenco_punti_prelievo.loc[(current_tipo,final_choice),:]
        df_to_print.append(tmp_df)
    df_to_print = pd.concat(df_to_print)[['Nome strada']]
    st.table(df_to_print)
else:
    st.write("Inserisci il codice identificativo nella barra all'inizio della pagina, premi invio e poi premi il bottone: 'Genera tabella'")





