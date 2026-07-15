import random
import streamlit as st

st.title("📚 중학생 영어 단어 게임")
st.write(
    "중학생 수준의 영어 단어 뜻 퀴즈입니다. 단어를 보고 알맞은 뜻을 골라보세요!"
)

WORDS = [
    {"word": "library", "meaning": "도서관"},
    {"word": "ticket", "meaning": "표"},
    {"word": "summer", "meaning": "여름"},
    {"word": "teacher", "meaning": "선생님"},
    {"word": "friend", "meaning": "친구"},
    {"word": "school", "meaning": "학교"},
    {"word": "travel", "meaning": "여행하다"},
    {"word": "music", "meaning": "음악"},
    {"word": "apple", "meaning": "사과"},
    {"word": "family", "meaning": "가족"},
    {"word": "computer", "meaning": "컴퓨터"},
    {"word": "market", "meaning": "시장"},
    {"word": "rainy", "meaning": "비 오는"},
    {"word": "picture", "meaning": "그림, 사진"},
    {"word": "breakfast", "meaning": "아침 식사"},
]

QUIZ_LENGTH = 8

if "quiz_words" not in st.session_state:
    st.session_state.quiz_words = []

if "question_index" not in st.session_state:
    st.session_state.question_index = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "selected" not in st.session_state:
    st.session_state.selected = None

if "show_result" not in st.session_state:
    st.session_state.show_result = False


def start_quiz():
    st.session_state.quiz_words = random.sample(WORDS, QUIZ_LENGTH)
    st.session_state.question_index = 0
    st.session_state.score = 0
    st.session_state.selected = None
    st.session_state.show_result = False


def next_question():
    st.session_state.show_result = False
    st.session_state.selected = None
    st.session_state.question_index += 1


def check_answer():
    st.session_state.show_result = True
    current = st.session_state.quiz_words[st.session_state.question_index]
    if st.session_state.selected == current["meaning"]:
        st.session_state.score += 1


start_button = st.button("게임 시작")
if start_button:
    start_quiz()

if not st.session_state.quiz_words:
    st.info("오른쪽 위의 '게임 시작' 버튼을 눌러 퀴즈를 시작하세요.")
else:
    current = st.session_state.quiz_words[st.session_state.question_index]
    st.write(f"### 문제 {st.session_state.question_index + 1} / {QUIZ_LENGTH}")
    st.write(f"**영어 단어:** {current['word']}")

    meanings = [word["meaning"] for word in WORDS if word["meaning"] != current["meaning"]]
    choices = random.sample(meanings, 3) + [current["meaning"]]
    random.shuffle(choices)

    st.session_state.selected = st.radio("뜻을 고르세요", choices, index=choices.index(st.session_state.selected) if st.session_state.selected in choices else 0)

    confirm_button = st.button("확인") if not st.session_state.show_result else False
    next_button = st.button("다음 문제") if st.session_state.show_result and st.session_state.question_index < QUIZ_LENGTH - 1 else False
    restart_button = st.button("다시 시작") if st.session_state.show_result and st.session_state.question_index == QUIZ_LENGTH - 1 else False

    if confirm_button:
        check_answer()

    if st.session_state.show_result:
        if st.session_state.selected == current["meaning"]:
            st.success("정답입니다! 🎉")
        else:
            st.error(f"틀렸습니다. 정답은 '{current['meaning']}' 입니다.")

        st.write(f"이번 문제 뜻: **{current['meaning']}**")
        st.write(f"현재 점수: **{st.session_state.score}점**")

        if next_button:
            next_question()
        elif restart_button:
            start_quiz()
