#%%
import json



# %%
with open("test.json") as f:
    data = json.load(f)
print(data)
# %%
data.get("DIC-config").get("correl_wind_size")
# %%
