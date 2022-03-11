import streamlit as st
import pandas as pd
import numpy as np
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components
from PIL import Image

st.set_page_config(layout="wide",page_title='Lahmacun Endeksi', page_icon=':face:')

st.subheader('Lahmacun Endeksi')

@st.cache
def get_data():
    df = pd.read_excel('ys_istanbul2.xlsx')

    return df

data = get_data()

data = data.fillna('')

data = data.astype(str)
data = data.replace(r'^\s*$', np.nan, regex=True)
data['hiz'] = data['hiz'].apply(lambda x: float(x))
data['servis'] = data['servis'].apply(lambda x: float(x))
data['lezzet'] = data['lezzet'].apply(lambda x: float(x))
data['indirimsiz'] = data['indirimsiz'].apply(lambda x: float(x))
data['indirimli'] = data['indirimli'].apply(lambda x: float(x))
data['fiyat'] = data['fiyat'].apply(lambda x: float(x))
#data['sehir_agirlik'] = data['sehir_agirlik'].apply(lambda x: float(x))
#data['sehir_agirlik_d'] = data['sehir_agirlik_d'].apply(lambda x: float(x))
data[['ilce_genel', 'mahalle']] = data['ilce'].str.split('(', expand=True)
data['mahalle'] = data['mahalle'].str.replace(")", "")



# components.html("""<iframe title="Bölgelere Göre Ortalama Lahmacun Fiyatı" aria-label="Map" id="datawrapper-chart-LtjAS" src="https://datawrapper.dwcdn.net/LtjAS/7/" scrolling="no" frameborder="0" style="width: 0; min-width: 100% !important; border: none;" height="433"></iframe><script type="text/javascript">!function(){"use strict";window.addEventListener("message",(function(e){if(void 0!==e.data["datawrapper-height"]){var t=document.querySelectorAll("iframe");for(var a in e.data["datawrapper-height"])for(var r=0;r<t.length;r++){if(t[r].contentWindow===e.source)t[r].style.height=e.data["datawrapper-height"][a]+"px"}}}))}();
# </script>
#               """, height=850,)


#Veri seti sehirlere gore toplam rakam

sehir_data = data["ilce_genel"].value_counts()
sehirler=pd.DataFrame(sehir_data)
sehirler.reset_index(inplace=True)
sehirler.columns=["ilceler", "Toplam Lahmacun"]


options_total = {
  "title": {
    "text": "Veri Seti - Toplam Çekilen Lahmacun Fiyatı Sayısı",
    "subtext": f"{(sehirler['ilceler'][0])}ilçesinde toplamda {sehirler['Toplam Lahmacun'][0]} fiyat bilgisi mevcut"
  },
  "xAxis": {
    "data": sehirler['ilceler'].values.tolist(),
    "axisLabel": {
      "inside": 'true',
      "color": "#fff",
      "rotate" : 90
    },
    "axisTick": {
      "show": 'false'
    },
    "axisLine": {
      "show": 'false'

    },
    "z": 10
  },
  "yAxis": {
    "axisLine": {
      "show": 'false'
    },
    "axisTick": {
      "show": 'false'
    },
    "axisLabel": {
      "color": "#999"
    }
  },
  "dataZoom": [
    {
      "type": "inside"
    }
  ],
  "series": [
    {
      "type": "bar",
      "showBackground": 'true',
      "itemStyle": {"color": '#610007'},
      "data": sehirler["Toplam Lahmacun"].values.tolist()
    }
  ]
}

st_echarts(options=options_total, height='500px')



#Lahmacun Fiyatları Ortalama

lah_fiyat = data.groupby("ilce_genel").mean()
lah_fiyat.reset_index(inplace=True)
ort_fiyat = lah_fiyat.drop(columns=['hiz','lezzet','servis','indirimsiz','indirimli'])
ort_fiyat = ort_fiyat[['fiyat', 'ilce_genel']]

options_fiyat = {
  "title": {
    "text": "Ortalama Lahmacun Fiyatı",
    "subtext": f"En yüksek lahmacun fiyatına sahip ilçe: {round(ort_fiyat['fiyat'].max(),1)} TL ile Beşiktaş oldu"
  },
  "xAxis": {
    "data": ort_fiyat['ilce_genel'].values.tolist(),
    "axisLabel": {
      "inside": 'true',
      "color": "#fff",
      "rotate" : 90
    },
    "axisTick": {
      "show": 'false'
    },
    "axisLine": {
      "show": 'false'

    },
    "z": 10
  },
  "yAxis": {
    "axisLine": {
      "show": 'false'
    },
    "axisTick": {
      "show": 'false'
    },
    "axisLabel": {
      "color": "#999"
    }
  },
  "dataZoom": [
    {
      "type": "inside"
    }
  ],
  "series": [
    {
      "type": "bar",
      "showBackground": 'true',
      "itemStyle": {"color": '#610007'},
      "data": ort_fiyat["fiyat"].values.tolist()
    }
  ]
}

st_echarts(options=options_fiyat, height='500px')

sehirler_list = data['sehir'].unique()
sehir_selector = st.selectbox("Şehir seçiniz", options=sehirler_list)
    
if sehir_selector is None:

    st.warning("""Veriyi görmek için şehir seçiniz""") 

else:

    il_datasi = data[data["sehir"] == (sehir_selector)]
    ilceler = il_datasi.groupby(['sehir', 'ilce_genel', 'mahalle']).size().reset_index(name='Toplam')
    tum_ilce = ilceler['ilce_genel'].values.tolist()
    tum_total = ilceler['Toplam'].values.tolist()




    
    col1, col2, col3, col4 = st.columns([1,1,.2,2])

    with col1:
          d = pd.DataFrame(ilceler['ilce_genel'].unique())
          d = d.set_axis(['Tüm İlçeler'], axis=1, inplace=False)
          st.dataframe(d)

    with col2:
          m = pd.DataFrame(ilceler['mahalle'].unique())
          m = m.set_axis(['Tüm Mahalleler'], axis=1, inplace=False)
          st.dataframe(m)

    with col4:
        st.dataframe(ilceler)
        st.markdown(f"""<b>{sehir_selector}</b> iline ait toplam <b>{il_datasi['ilce_genel'].nunique()}</b> ilçe ve <b>{il_datasi['mahalle'].nunique()}</b> mahalle bilgisi mevcuttur.""", unsafe_allow_html=True)
    gauge_option1={
                    "tooltip": {
                        "formatter": "{a} <br/>{b} : {c}"
                    },
                    "series": [
                        {
                        "name": "Lahmacun Fiyati",
                        "type": "gauge",
                        "itemStyle": {"color": '#A6373F'},
                        "detail": {
                            "formatter": "{value} TL"
                        },
                        "data": [
                            {
                            "value": round(il_datasi['fiyat'].max(),0),
                            "name": "Maksimum"
                            }
                        ]
                        }
                    ]
                    }

    gauge_option2={
                    "tooltip": {
                        "formatter": "{a} <br/>{b} : {c}"
                    },
                    "series": [
                        {
                        "name": "Lahmacun Fiyati",
                        "itemStyle": {"color": '#3C8D2F'},
                        "type": "gauge",
                        "detail": {
                            "formatter": "{value} TL"
                        },
                        "data": [
                            {
                            "value": round(il_datasi['fiyat'].min(),0),
                            "name": "Minimum"
                            }
                        ]
                        }
                    ]
                    }

    gauge_option3={
                    "tooltip": {
                        "formatter": "{a} <br/>{b} : {c}"
                    },
                    "series": [
                        {
                        "name": "Lahmacun Fiyati",
                        "itemStyle": {"color": '#236A62'},
                        "type": "gauge",
                        "detail": {
                            "formatter": "{value} TL"
                        },
                        "data": [
                            {
                            "value": round(il_datasi['fiyat'].mean(),0),
                            "name": "Ortalama"
                            }
                        ]
                        }
                    ]
                    }
    

    col1, col2, col3= st.columns([1,1,1])
    with col1:
        st_echarts(options=gauge_option2, height='500px')

    with col2:
        st_echarts(options=gauge_option3, height='500px')

    with col3:
        st_echarts(options=gauge_option1, height='500px')



sehir_datasi = data[['sehir','ilce_genel','mahalle']]
sehir_datasi['sehirler'] = 'sehirler'
sehir_datasi = sehir_datasi[['sehirler', 'sehir', 'ilce_genel', 'mahalle']]
#sehir_datasi = sehir_datasi.to_json()

st.markdown("""<a href='https://github.com/dogudogru/ys_endeks/blob/main/ys_istanbul2.xlsx'>Veriyi bu linke tıklayarak indirebilirsiniz (View raw) </a>""", unsafe_allow_html=True)


st.markdown('***')


###### SIDEBAR

image = Image.open('logo_yeni.png')
st.sidebar.image(image=image)

st.sidebar.subheader("Lahmacun Endeksi Nedir?")