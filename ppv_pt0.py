# ====== ページ設定 ======
import streamlit as st
import random, time

st.set_page_config(layout="wide")

# ====== 初期化 ======
if "round" not in st.session_state:
    st.session_state.round = 1
    st.session_state.total_rounds = 6
    st.session_state.v = []
    st.session_state.scores = []
    st.session_state.max_scores = []
    st.session_state.input_vec = []
    st.session_state.round_active = False
    st.session_state.start_time = None

# ====== 新しいラウンド開始 ======
def new_round():
    st.session_state.v = [random.randint(1, 9) for _ in range(3)]
    st.session_state.input_vec = []
    st.session_state.round_active = True
    st.session_state.start_time = time.time()

# ====== レイアウト分割 ======
col_left, col_center, col_right = st.columns([1, 2, 1])

# --- 左（ルール表示） ---
with col_left:
    st.markdown("## 🎮 遊び方")
    st.markdown("""
    - お題ベクトル **v** が表示されます  
    - 100秒以内に3つの整数を選んで **x** を作ろう  
    - スコアは  
      \n|v|² - |v·x|  
    - 6ラウンド勝負！
    """)

# --- 中央（お題・テンキー） ---
with col_center:
    st.markdown(f"## Round {st.session_state.round} / {st.session_state.total_rounds}")

    if st.session_state.round <= st.session_state.total_rounds:
        if not st.session_state.round_active:
            new_round()

        v = st.session_state.v
        st.markdown(f"### v = {v}に垂直なベクトル探してな")

        # タイマー
        elapsed = int(time.time() - st.session_state.start_time)
        remaining = max(0, 100 - elapsed)
        st.markdown(f"⏱️ 残り時間: **{remaining}秒**")
        if remaining == 0 and st.session_state.round_active:
            # タイムアウトで次へ
            st.warning("時間切れ！")
            st.session_state.scores.append(0)
            st.session_state.max_scores.append(sum(v_i**2 for v_i in v))
            st.session_state.input_vec = []
            st.session_state.round_active = False
            st.session_state.round += 1

        # 入力中のベクトル
        st.markdown(f"入力中: {st.session_state.input_vec}")

        # テンキー
        digits = [[1,2,3],[4,5,6],[7,8,9]]
        for row in digits:
            cols = st.columns(3, gap="small")
            for i, num in enumerate(row):
                with cols[i]:
                    if st.button(str(num), use_container_width=True, key=f"btn_{num}"):
                        if len(st.session_state.input_vec) < 3:
                            st.session_state.input_vec.append(num)

        cols = st.columns(4, gap="small")
        with cols[0]:
            if st.button("±", use_container_width=True):
                if st.session_state.input_vec:
                    st.session_state.input_vec[-1] *= -1
        with cols[1]:
            if st.button("BS", use_container_width=True):
                if st.session_state.input_vec:
                    st.session_state.input_vec.pop()
        with cols[2]:
            if st.button("GO", use_container_width=True) and len(st.session_state.input_vec) == 3:
                x = st.session_state.input_vec
                score = sum(v_i**2 for v_i in v) - abs(sum(v_i * x_i for v_i, x_i in zip(v, x)))
                st.success(f"確定: {x}  得点: {score}")
                st.session_state.scores.append(score)
                st.session_state.max_scores.append(sum(v_i**2 for v_i in v))
                st.session_state.input_vec = []
                st.session_state.round_active = False
                st.session_state.round += 1

# --- 右（得点履歴） ---
with col_right:
    st.markdown("## 📊 得点履歴")
    for i, (s, m) in enumerate(zip(st.session_state.scores, st.session_state.max_scores), start=1):
        st.write(f"R{i}: {s} / {m}")

    total_score = sum(st.session_state.scores)
    max_total = sum(st.session_state.max_scores)
    st.markdown(f"### 合計: {total_score} / {max_total}")
    if max_total > 0:
        st.markdown(f"打率: {100*total_score/max_total:.1f}%")

# ====== 総合判定 ======
if st.session_state.round > st.session_state.total_rounds:
    total_score = sum(st.session_state.scores)
    max_total = sum(st.session_state.max_scores)
    rate = 100 * total_score / max_total if max_total else 0

    st.markdown("---")
    st.markdown(f"## 🎯 総合得点: {total_score} / {max_total} ({rate:.1f}%)")

    if rate >= 50:
        st.success("おめっとさん！ 打率5割以上！")
        st.balloons()
    else:
        st.info("残念！また挑戦してね！")


