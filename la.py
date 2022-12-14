import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


druglist = ['Lidocaine 1%','Lidocaine 2% plain', 'Lidocaine 2% w/ epi', 'Bupivicaine 0.25%','Bupivicaine 0.5%','Ropivicaine 0.5%' ]
drugvarlist = ['lidocaine1','lidocaine2plain','lidocaine2epi','bupi25','bupi5','ropi5']
concentrationlist = [10,20,20,2.5,5,5]
drugtoxlist = [4.5,4.5,7.0,2.5,2.5,3.0]

def text_field(label, columns=None, **input_params):
    c1, c2 = st.columns(2)

    c1.markdown('##')
    c1.markdown(label)

    input_params.setdefault("key",label)

    return c2.number_input("", value=0, **input_params)

def toxic_field(label, columns=None, **input_params):
    c1, c2 = st.columns(2)

    c1.markdown('##')
    c1.markdown(label)

    input_params.setdefault("key",label+'tox')

    return c2.number_input("ml/kg", **input_params)

st.title('Local Anesthetic Remaining Calculator')

kgs = st.number_input('Patient weight',0,200, value=50, key='kgs')
with st.expander('Toxic doses'):
    for i,j,k in zip(druglist,drugvarlist,drugtoxlist):
        globals()[j+'tox'] = toxic_field(i,value=k)

st.subheader('Doses given')

# enter dose given fields
for i,j in zip(drugvarlist,druglist):
    globals()[i] = text_field(j)

givenlist = []
for i in drugvarlist:
    givenlist.append(globals()[i])

### calculate max dose
drugmaxlist = []
for i in drugvarlist:
    m = kgs*globals()[i+'tox']
    globals()[i+'max'] = m
    drugmaxlist.append(m)

#create table
df = pd.DataFrame(columns=['Drug','Dose given (ml)','Dose remaining (ml)','Fraction of total given','Max dose (mg)'])
df['Drug'] = druglist
df['Dose given (ml)'] = givenlist

fractionlist = []
for y,j,z in zip(df['Dose given (ml)'],concentrationlist,drugmaxlist):
    fractionlist.append((y*j)/z)
df['Fraction of total given'] = fractionlist
totalfraction = df['Fraction of total given'].sum()

df['Max dose (mg)'] = drugmaxlist

remaininglist = []
for maxdose,concentration in zip(drugmaxlist,concentrationlist):
    remaininglist.append(round(((maxdose - (maxdose * totalfraction )) / concentration),0))
df['Dose remaining (ml)'] = remaininglist

st.table(df)
