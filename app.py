# 以下を「app.py」に書き込み
import streamlit as st
import pandas as pd
import openai
import secret_keys  # 外部ファイルにAPI keyを保存

from PIL import Image

openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去

# ユーザーインターフェイスの構築
st.title("Travel Assistant")

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは優秀な旅行アシスタントAIです。"}
        ]

#サンプルデータの作成
data = {
  '地方':['北海道','東北','東北','東北','東北','東北','東北'],
  '都道府県':['北海道','青森','秋田','岩手','山形','宮城','福島'],
  '名産品':['ラーメン','リンゴ','きりたんぽ','冷麺','さくらんぼ','牛タン','もも'],
  '画像': ['ramen.jpg','リンゴ.jpg','きりたんぽ.jpg','冷麺.jpg','さくらんぼ.jpg','牛タン.jpg','もも.jpg',],
}
df=pd.DataFrame(data)

# 地域選択のためのプルダウン
selected_region=st.selectbox('地域を選んでね！',df['地方'].unique())

# 選択された地域に基づく都道府県情報の表示
prefecturesr = df[df['地方']==selected_region]['都道府県']
selected_prefecture = st.selectbox("都道府県を選んでね！", prefecturesr)

# 選択された都道府県に対応する画像を取得
selected_product_data = df[df['都道府県'] == selected_prefecture]

# 画像を表示
for i, row in selected_product_data.iterrows():
    st.image(row['画像'], width=300)


# ユーザーが選択した都道府県と、関連する画像を表示
user_input = st.text_input("あなたは"+"「"+str(selected_prefecture)+ "」" + "を選んだよ！", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🚅"

        st.write(speaker + ": " + message["content"])
