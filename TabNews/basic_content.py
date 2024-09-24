#%%
import datetime
import json
import time
import pandas as pd
import requests

def get_response(**kwargs):
    ## kwargs -> todos os parametros nao obrigatorios
    ## artigo no medium -> https://medium.com/rafaeltardivo/python-entendendo-o-uso-de-args-e-kwargs-em-fun%C3%A7%C3%B5es-e-m%C3%A9todos-c8c2810e9dc8
    ## Utilizar o kwards facilita na hora de inserir os parametros dentro da URL, podendo trazer dentro da funçao

    url = "https://www.tabnews.com.br/api/v1/contents/"
    resp = requests.get(url, params=kwargs)
    return resp

def save_data(data, option="json"):
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S.%f")

    if option == "json":
        with open(f"data/contents/json/{now}.json", "w") as open_file:
            json.dump(data, open_file, indent=4)
    elif option == "parquet":
        df = pd.DataFrame(data)
        df.to_parquet(f"data/contents/parquet/{now}.parquet", index=False)
#%%
page = 1
date_stop = pd.to_datetime('2024-09-01').date()
while True:
    # parametros do site
    print(page)
    resp = get_response(page=1, per_page=100, strategy="new") 
    if resp.status_code == 200:
        data = resp.json()
        save_data(data)

        date = pd.to_datetime(data[-1]["updated_at"]).date()
        if len(data) < 100 or date < date_stop:
            break

        page += 1
        time.sleep(2)
        
    else:
        print(resp.status_code)
        print(resp.json())
        time.sleep(30)

# %%
