import streamlit as st
import pandas as pd
import pymouser
import numpy as np

st.set_page_config(layout="wide",page_title="Component Lifecycle Management")




df1 = ""
#df1 = pd.read_csv("bom.csv")





uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df1 = pd.read_csv(uploaded_file)

#df1

user = st.secrets["mouserCredential"]

mouser = pymouser.MouserAPI(user)

data ={}

dataTable = pd.DataFrame.from_dict({'PCBA':[""],'PN':[""],'LifecycleStatus':[""],'AvailabilityInStock':[""],'SuggestedReplacement':[""],'LeadTime':[""],'MouserPartNumber': [""],'Description':[""] })
                                
                                
i =0


while i<len(df1):    
    PCBA = df1.iloc[i,1]
    component = df1.iloc[i,0]
    #PCBA
    #component
    err, res = mouser.search_by_PN(component)
    #res
    i = i+1
    if err:
        print("Error during request:")
    else:
        if res['NumberOfResult'] == 0:
            data = {'PCBA':[PCBA],
                                'PN':[component],
                                'MouserPartNumber': "PN not found",
                                'Manufacturer': "",
                                'Description': "",
                                'LeadTime':"",
                                'LifecycleStatus': "PN not found",
                                'SuggestedReplacement' : "",
                                'AvailabilityInStock':"",
                                #'RefDate':[date.today()],
                                }

            dataTable = pd.concat([dataTable,pd.DataFrame.from_dict(data)])
        else:
            for match in res['Parts']:
                try:
                    compAvailability = res["Parts"][0]["Availability"]
                except:
                    compAvailability  =0
                
                compDatasheet =res["Parts"][0]["DataSheetUrl"]
                compDescription = res["Parts"][0]["Description"]
                compLifecycle = res["Parts"][0]["LifecycleStatus"]
                compLeadTime = res["Parts"][0]["LeadTime"]
                compReplacement = res["Parts"][0]["SuggestedReplacement"]

                if not compLifecycle:
                    compLc = "Vigente"
                else:
                    compLc =res["Parts"][0]["LifecycleStatus"]
                
                
                data = {'PCBA':[PCBA],
                                'PN':[component],
                                'MouserPartNumber': [match['MouserPartNumber']],
                                'Manufacturer': [match['Manufacturer']],
                                'Description': [match['Description']],
                                'LeadTime':[match['LeadTime']],
                                'LifecycleStatus': compLc,
                                'SuggestedReplacement' : [match['SuggestedReplacement']],
                                'AvailabilityInStock':[match['AvailabilityInStock']],
                                }

                dataTable = pd.concat([dataTable,pd.DataFrame.from_dict(data)])

            
        

def fontColor_conditional(val):
    color = 'black'

    if val=="Vigente":
        color = 'black'
    if val == 'PN not found':
        color = '#FF0000'       #vermelho
    if val == 'Obsolete':
        color = '#FFFF00'        #amarelo

    return 'color: %s' % color

def bgcolor_condtional(val):
    bgcolor = 'white'
    if val == 'PN not found':
        bgcolor = 'yellow'
    if val == 'Obsolete':
        bgcolor = 'red'
    if val == 'Vigente':
        bgcolor = '#B8E7A7'                 #verde claro  
    
    return 'background-color: %s' % bgcolor



dataTable.reset_index(inplace=True)

s = dataTable.style\
    .map(fontColor_conditional)\
    .map(bgcolor_condtional)\

s

