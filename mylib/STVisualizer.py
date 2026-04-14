import os
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import font_manager
import mylib.TextMining as tm

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_FILE = os.path.join(BASE_DIR, 'myFonts', 'NanumGothic.ttf')

# 1. 한글 폰트 등록하기
def regist_korean_font():
    font_manager.fontManager.addfont(FONT_FILE)
    plt.rc('font', family='NanumGothic')

# 2. 막대 그래프 그리기
def visualize_barhgraph(counter, num_words):
    top_words = counter.most_common(num_words)
    
    words = []
    counts = []
    for word, count in top_words:
        words.append(word)
        counts.append(count)

    fig, ax = plt.subplots()
    ax.barh(words[::-1], counts[::-1])
    st.pyplot(fig)

# 3. 워드클라우드 출력하기
def visualize_wordcloud(counter, num_words):
    if os.path.exists(FONT_FILE):
        wc_img = tm.generate_wordcloud(counter, num_words, FONT_FILE)
        
        fig, ax = plt.subplots()
        ax.imshow(wc_img)
        ax.axis('off')
        st.pyplot(fig)
    else:
        st.error("워드클라우드용 폰트가 없습니다.")

# 4. 데이터 확인용 팝업 창
@st.dialog("데이터 미리보기")
def view_raw_data_dialog(df):
    num = st.number_input("보여줄 줄 수", value=10)
    st.dataframe(df.head(num))