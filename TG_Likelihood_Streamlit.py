import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title('TG Likelihoods: shallow and deep temperatures')

# LOCATION OF THIS FILE
# /Users/whitneytrainor-guitton/Library/Application Support/JetBrains/PyCharmCE2021.3/scratches/streamlit_scratch.py


#@st.cache
def load_data():
    ## on colab
    # df = pd.read_csv('/content/gdrive/MyDrive/Colab Notebooks/TGH_Likelihood/ShallowReservoirDF1_wellDF2.csv')
    ## on PyCharm
    #data = pd.read_csv('/Users/whitneytrainor-guitton/My Drive (whitney@zanskar.us)/Colab Notebooks/TGH_Likelihood/ShallowReservoirDF1_wellDF2.csv')

    return data

# # Create a text element and let the reader know the data is loading.
# data_load_state = st.text('Loading data...')
# # Load 10,000 rows of data into the dataframe.
# df = load_data()
# # Notify the reader that the data was successfully loaded.
# data_load_state.text('Loading data...done!')

uploaded_file = st.file_uploader("Choose a file",type=['csv'])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df.head())

    st.subheader('TG Shallow-Deep Pairs')
    # st.write(df)

    st.subheader('Calculate & Display Likelihoods')
    myybins = np.arange(0., 1960, 10) #depth 1950.7
    myxbins = np.arange(0,110,3)   # temperature

    ## TEST: replace with widgets!!
    dep_shallow_meters = st.slider('shallow depth (meters)', 10, int(np.max(myybins)-10), 20, step=10) # min, max, default
    dep_reservoir_meters =  st.slider('deep depth (meters)', dep_shallow_meters+10, int(np.max(myybins)-10), 100, step=10)

    st.write("Shallow depth: ", round(dep_shallow_meters,-1), ' meters')
    st.write("Reservoir/deep depth: ", round(dep_reservoir_meters,-1), ' meters')

    fig, axes = plt.subplots(figsize=(10,8),ncols=1,nrows=1)
    suptitletxt='Shallow Depth {dep_shallow}, Reservoir Depth {dep_reservoir}'.format(dep_shallow=dep_shallow_meters,dep_reservoir=dep_reservoir_meters)
    plt.suptitle(suptitletxt,fontsize=15)

    # round to make sure it rounds to nearest 10
    dfpair = df[(df['depthbin_S'] ==round(dep_shallow_meters,-1)) & (df['depthbin_R'] == round(dep_reservoir_meters,-1))] # df[df['depthbin_S'] ==20] #

    ph=sns.kdeplot(data=dfpair,x='tempbin_R',y='tempbin_S',fill=True,cmap='rainbow',alpha=0.4,cbar=True,ax=axes)
    axes.set_ylim(0,myxbins[-1])
    axes.set_xlim(0,myxbins[-1])
    axes.set_ylabel('Shallow Temperatures (C)')
    axes.set_xlabel('Reservoir Temperatures (C)')
    x = np.linspace(*axes.get_xlim())
    plt.plot(x, x,'r',alpha=0.5)
    st.pyplot(fig)

    st.write(dfpair.describe())

