import streamlit as st
import pandas as pd
import pymouser
import numpy as np
import requests
import matplotlib.pyplot as plt


st.set_page_config(layout="wide",page_title="Component Lifecycle Management")


defBgColorVigente = '#B8E7A7'
defBgColorObsoleto = 'red'
defBgColorPnNotFound = 'yellow'

df1 = ""

stsObsoleto = 0
stsVigente = 0
stsNaoEncontrado = 0
stsRestrictedAvailability = 0


with st.sidebar:
    uploaded_file = st.file_uploader("Choose a BoM file to evaluate the component availability")
    if uploaded_file is not None:
        df1 = pd.read_csv(uploaded_file)

user = st.secrets["mouserCredential"]

mouser = pymouser.MouserAPI(user)

data ={}

dataTable = pd.DataFrame.from_dict({'PCBA':[""],'PN':[""],'LifecycleStatus':[""],'AvailabilityInStock':[""],'SuggestedReplacement':[""],'LeadTime':[""],'MouserPartNumber': [""],'Description':[""] })
                                
                                
i =0


while i<len(df1):    
    PCBA = df1.iloc[i,1]
    component = df1.iloc[i,0]

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
        
            compLc = "PN not found"
            stsNaoEncontrado = stsNaoEncontrado +1
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
                    stsVigente = stsVigente+1
                    compLc = "Vigente"
                else:
                    compLc =res["Parts"][0]["LifecycleStatus"]
                    if compLc == "Obsolete":
                        compLc = "Obsoleto"
                        stsObsoleto = stsObsoleto+1
                    if compLc == "Restricted Availability":
                        compLc = "Restricted Availability"
                        stsRestrictedAvailability = stsRestrictedAvailability+1
                    
                        
                #component
                #compLifecycle
                #compLc
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
        color = '#FF0000'
    if val == 'Obsoleto':
        color = '#FFFF00'
    if val == 'Restricted Availability':
        color = '#FFFF00'
    return 'color: %s' % color

def bgcolor_condtional(val):
    bgcolor = 'white'
    if val == 'PN not found':
        bgcolor = defBgColorPnNotFound
    if val == 'Obsoleto':
        bgcolor = defBgColorObsoleto

    if val == 'Restricted Availability':
        bgcolor = defBgColorObsoleto

    if val == 'Vigente':
        bgcolor = defBgColorVigente
    
    return 'background-color: %s' % bgcolor



dataTable.reset_index(inplace=True)

s = dataTable.style\
    .map(fontColor_conditional)\
    .map(bgcolor_condtional)\


col1, col2, col3,col4 = st.columns(4)
with col1:
 
 

    #st.subheader("Vigente", divider="green")
#    st.subheader("Vigente")
    st.html("""<p style="font-size:1.5em; ">Vigente</p>""")
    st.markdown("""<hr style="height:8px;border:none;color:#4EA72E;background-color:#4EA72E;" /> """, unsafe_allow_html=True) 

    st.title(stsVigente )

with col2:
    #st.subheader("Obsoleto", divider="red")
    #st.subheader("Obsoleto")
    st.html("""<p style="font-size:1.5em; ">Obsoleto</p>""")
    st.markdown("""<hr style="height:8px;border:none;color:#FF0000;background-color:#FF0000;" /> """, unsafe_allow_html=True) 

    st.title(stsObsoleto)

with col3:
    #st.subheader("Restrito", divider="red")
    #st.subheader("Restrito")
    st.html("""<p style="font-size:1.5em; ">Restrito</p>""")
    st.markdown("""<hr style="height:8px;border:none;color:#7030A0;background-color:#7030A0;" /> """, unsafe_allow_html=True) 

    st.title(stsRestrictedAvailability)

with col4:
#    st.html("""<h5 style="font-size:3vw;">Não Encotr.</h5>
#                <p style="font-size:2vw;">Resize the browser window to see how the font size scales.</p>""")
    
    #st.html("""<h6 style="font-size:2vw;">Não Encotr.</h6>""")
    st.html("""<p style="font-size:1.5em; ">Não Encotr.</p>""")
    
    #st.subheader("Não Encont.", divider="orange")
    #st.subheader("Não Encont.")


    st.markdown("""<hr style="height:8px;border:none;color:#FFC000;background-color:#FFC000;" /> """, unsafe_allow_html=True) 
    
    st.title(stsNaoEncontrado)

s

with st.sidebar:   
 
    arr = np.random.normal(1, 1, size=100)
    fig, ax = plt.subplots()

    labels = 'Vigente', 'Obsoleto', 'Não Encontrado','Restricted Availability'
    sizes = [stsVigente,  stsObsoleto, stsNaoEncontrado,stsRestrictedAvailability]


    fig.patch.set_facecolor('none')
    ax.patch.set_facecolor('none')
    
    if stsNaoEncontrado+stsVigente+stsObsoleto!=0:
        ax.pie(sizes, labels=labels,autopct='%1.1f%%',colors=[defBgColorVigente, defBgColorObsoleto,defBgColorPnNotFound],textprops={'fontsize': 'large'})

        st.pyplot(fig)

