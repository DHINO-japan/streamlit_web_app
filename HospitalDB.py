import streamlit as st
import pandas as pd
import plotly.express as px

st.title('病院データベース')
st.caption('これは病院DB用の閲覧用アプリです。')
st.markdown('<style>h1{color: #191970;}</style>', unsafe_allow_html=True)
st.markdown('<style>h1{font-size: 21px;}</style>', unsafe_allow_html=True)

#チェックボックス
st.markdown('<style>div[data-baseweb="select"] > div {font-size: 14px;}</style>', unsafe_allow_html=True)
prefectures = ['北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県', '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県', '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県', '静岡県', '愛知県', '三重県', '滋賀県', '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県', '鳥取県', '島根県', '岡山県', '広島県', '山口県', '徳島県', '香川県', '愛媛県', '高知県', '福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県']
selected_prefectures = st.multiselect('都道府県を選択してください', prefectures)

# CSSスタイルの設定
st.markdown('<style>div[data-baseweb="select"] > div {font-size: 14px;}</style>', unsafe_allow_html=True)

# スライダーのスタイル設定
st.markdown(
    """
    <style>
        .css-1g6m5ra,
        .css-1t42vgg {
            background-color: #191970;  /* 紺に変更 */
        }
    </style>
    """, unsafe_allow_html=True
)

#スライダー
values = st.slider(
    '病床数の選択範囲※病院全体の病床数です。',
   20, 1000, (100, 300))
st.write('選択した病床数:', values)

#データ分析関連
df = pd.read_csv('projects/python/HosputalDB/hdbmaster2.csv')
df = df[(df['bed'] >= values[0]) & (df['bed'] <= values[1])]

# 都道府県で絞り込み
if selected_prefectures:
    df = df[df['都道府県'].isin(selected_prefectures)]
st.dataframe(df[[ '施設名称', '都道府県', 'bed', '1床当り面積', '設立主体', '工事種別', '竣工年', '構造']])

# ボタンを追加して色分けを選択
color_options = ['1床当り面積', '設立主体', '工事種別', '竣工年', '構造', '設計者']
selected_color = st.selectbox('色分けする項目を選択してください', color_options)

# ボタンがクリックされたときに実行されるコード
if st.button('表示'):
    # 散布図をプロット
    fig = px.scatter(df, x='bed', y='1床当り面積', color=selected_color, labels={'bed': '病床数', '1床当り面積': '1床当り面積'})
    
    # プロットの表示
    st.plotly_chart(fig)

#散布図
import altair as alt

df['color'] = df['bed'].apply(lambda x: 'red' if x >= 200 else 'blue')

fig = alt.Chart(df).mark_circle(size=60).encode(
    alt.X('bed:Q', title='病床数'),
    alt.Y('1床当り面積:Q', title='1床当り面積'),
    color=alt.Color('color:N', legend=None),
    tooltip=['施設名称', '都道府県', 'bed', '1床当り面積']
).properties(
    width=700,
    height=500
).interactive()

st.write(fig)