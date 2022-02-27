import streamlit as st
import pandas as pd
import numpy as np
from streamlit_echarts import st_echarts

st.set_page_config(layout="wide",page_title='Lahmacun Endeksi', page_icon=':face:')

st.title('Lahmacun Endeksi')

# @st.cache
# def get_data():
#     df = pd.read_excel('yemeksepeti_nuts2.xlsx')

#     return df

data = pd.read_excel('yemeksepeti_nuts2.xlsx')

data = data.fillna('')

data = data.astype(str)
data = data.replace(r'^\s*$', np.nan, regex=True)
data['hiz'] = data['hiz'].apply(lambda x: float(x))
data['servis'] = data['servis'].apply(lambda x: float(x))
data['lezzet'] = data['lezzet'].apply(lambda x: float(x))
data['indirimsiz'] = data['indirimsiz'].apply(lambda x: float(x))
data['indirimli'] = data['indirimli'].apply(lambda x: float(x))
data['fiyat'] = data['fiyat'].apply(lambda x: float(x))
data['sehir_agirlik'] = data['sehir_agirlik'].apply(lambda x: float(x))
data['sehir_agirlik_d'] = data['sehir_agirlik_d'].apply(lambda x: float(x))


with st.expander('Ağırlıklandırılmış ana veriyi görmek için tıklayınız.'):
    st.write(data)


st.markdown("""<a href='www.google.com'>Ağırlıklandırılmış veriyi bu linke tıklayarak indirebilirsiniz</a>""", unsafe_allow_html=True)



st.markdown('***')

#Veri seti sehirlere gore toplam rakam

sehir_data = data["sehir"].value_counts()
sehirler=pd.DataFrame(sehir_data)
sehirler.reset_index(inplace=True)
sehirler.columns=["Sehir", "Toplam Lahmacun"]


options_total = {
  "title": {
    "text": "Veri Seti - Toplam Çekilen Lahmacun Fiyatı Sayısı",
    "subtext": f"{(sehirler['Sehir'][0])} şehrinde toplamda {sehirler['Toplam Lahmacun'][0]} fiyat bilgisi mevcut"
  },
  "xAxis": {
    "data": sehirler['Sehir'].values.tolist(),
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
      "data": sehirler["Toplam Lahmacun"].values.tolist()
    }
  ]
}

st_echarts(options=options_total, height='500px')



#Lahmacun Fiyatları Ortalama

lah_fiyat = data.groupby("sehir").mean()
lah_fiyat.reset_index(inplace=True)
ort_fiyat = lah_fiyat.drop(columns=['hiz','lezzet','servis','indirimsiz','indirimli'])
ort_fiyat = ort_fiyat[['fiyat', 'sehir']]

options_fiyat = {
  "title": {
    "text": "Ortalama Lahmacun Fiyatı",
    "subtext": f"En yüksek lahmacun fiyatına sahip şehir: {round(ort_fiyat['fiyat'].max(),1)} TL ile {ort_fiyat['sehir'].max()} oldu"
  },
  "xAxis": {
    "data": ort_fiyat['sehir'].values.tolist(),
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
      "data": ort_fiyat["fiyat"].values.tolist()
    }
  ]
}

st_echarts(options=options_fiyat, height='500px')

sehirler = data['sehir'].unique()
sehirler = np.append(sehirler, 'Hiçbiri')
sehir_selector = st.multiselect("Şehir seçiniz", options=sehirler, default='İstanbul')
    
if 'Hiçbiri' in sehir_selector:

    st.warning("""Veriyi görmek için şehir ekleyin ya da "Hiçbiri" seçeneğini çıkarın""") 

else:

    il_datasi = data[data["sehir"].isin(sehir_selector)]
    st.write(il_datasi)

    gauge_option1={
                    "tooltip": {
                        "formatter": "{a} <br/>{b} : {c}"
                    },
                    "series": [
                        {
                        "name": "Lahmacun Fiyati",
                        "type": "gauge",
                        "detail": {
                            "formatter": "{value}"
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
                        "type": "gauge",
                        "detail": {
                            "formatter": "{value}"
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
                        "type": "gauge",
                        "detail": {
                            "formatter": "{value}"
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
        st_echarts(options=gauge_option1, height='500px')
    with col2:
        st_echarts(options=gauge_option2, height='500px')
    with col3:
        st_echarts(options=gauge_option3, height='500px')


