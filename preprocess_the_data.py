import pandas as pd
import pickle as pkl

elenco_punti_prelievo = pd.read_csv('Elenco punti prelievo.csv')
elenco_punti_prelievo.dropna(inplace=True)
elenco_punti_prelievo = elenco_punti_prelievo[elenco_punti_prelievo['Tipologia']!='Tipologia']
# elenco_punti_prelievo.rename(columns={'Nome strada':'Nome_strada'}, inplace=True)
elenco_punti_prelievo.reset_index(drop=True, inplace=True)
elenco_punti_prelievo['Numero'] = elenco_punti_prelievo['Numero'].astype(int)
elenco_punti_prelievo


def _strip_punti_from_same_streets(the_name):
    if(not ' - ' in the_name):
        return the_name
    else:
        return  the_name.split(' - ')[0]
    


elenco_punti_prelievo['nome_strada_senza_punti']=elenco_punti_prelievo['Nome strada'].apply(lambda x: _strip_punti_from_same_streets(x))
elenco_punti_prelievo.set_index(['Tipologia','Numero']).to_pickle('final_list_of_street_for_streamlit.pkl')


dict_with_the_number_of_things_to_sample = {}
dict_with_the_number_of_things_to_sample['1%'] = {}
dict_with_the_number_of_things_to_sample['5%'] = {}

dict_with_the_number_of_things_to_sample['1%']['A'] = 12
dict_with_the_number_of_things_to_sample['1%']['B'] = 7
dict_with_the_number_of_things_to_sample['1%']['C'] = 94
dict_with_the_number_of_things_to_sample['1%']['D'] = 26
dict_with_the_number_of_things_to_sample['1%']['E'] = 2
dict_with_the_number_of_things_to_sample['1%']['F'] = 1

dict_with_the_number_of_things_to_sample['5%']['A'] = 2
dict_with_the_number_of_things_to_sample['5%']['B'] = 1
dict_with_the_number_of_things_to_sample['5%']['C'] = 13
dict_with_the_number_of_things_to_sample['5%']['D'] = 3
dict_with_the_number_of_things_to_sample['5%']['E'] = 1
dict_with_the_number_of_things_to_sample['5%']['F'] = 1

with open('dict_with_the_number_of_things_to_sample.pkl', 'wb') as handle:
    pkl.dump(dict_with_the_number_of_things_to_sample, handle)