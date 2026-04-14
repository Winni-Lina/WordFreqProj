import streamlit as st
import pandas as pd
import mylib.STVisualizer as sv
import mylib.TextMining as tm

# 웹페이지 제목 설정
st.set_page_config(page_title="단어 빈도 분석기", page_icon="📊")

# 시작하자마자 폰트 설정 실행
sv.regist_korean_font()

# 사이드바 (설정창)
with st.sidebar:
    st.header("1. 파일 올리기")
    data_file = st.file_uploader("CSV 파일을 선택하세요", type=['csv'])
    column_name = st.text_input('리뷰 컬럼 이름', value='review')
    
    if st.button("데이터 확인하기"):
        if data_file is not None:
            df = pd.read_csv(data_file)
            sv.view_raw_data_dialog(df)
        else:
            st.warning("파일을 먼저 올려주세요!")

    st.write("---")
    st.header("2. 시각화 옵션")
    with st.form('my_setting'):
        do_bar = st.checkbox('빈도수 막대 그래프', value=True)
        n_bar = st.slider('그래프 단어 개수', 10, 50, 20)
        
        do_wc = st.checkbox('워드클라우드', value=False)
        n_wc = st.slider('클라우드 단어 개수', 20, 500, 50)
        
        # 폼 제출 버튼
        btn_start = st.form_submit_button('분석 시작')

# 메인 화면 구성
st.title('📊 단어 빈도 시각화 대시보드')

# 분석 전 초기 메시지
info_box = st.empty()
info_box.info('파일을 업로드하고 [분석 시작] 버튼을 눌러주세요.')

if btn_start:
    if data_file is None:
        st.error('분석할 파일이 없습니다!')
    else:
        info_box.info('데이터를 분석하는 중입니다. 잠시만 기다려주세요...')
        
        # 1. 데이터 로드
        corpus = tm.load_corpus_from_csv(data_file, column_name)
        
        if corpus is None:
            st.error(f"'{column_name}' 컬럼을 찾을 수 없습니다. 이름을 확인해주세요.")
        else:
            # 2. 단어 빈도 계산
            counter = tm.analyze_word_freq(corpus)
            info_box.success(f"분석 완료! (총 {len(corpus)}개의 리뷰 분석됨)")

            # 3. 그래프 출력
            if do_bar:
                st.subheader("많이 나온 단어 순위")
                sv.visualize_barhgraph(counter, n_bar)
            
            if do_wc:
                st.subheader("워드클라우드")
                sv.visualize_wordcloud(counter, n_wc)
                
            if not do_bar and not do_wc:
                st.warning("그래프나 워드클라우드 중 하나를 선택해야 결과가 보입니다.")