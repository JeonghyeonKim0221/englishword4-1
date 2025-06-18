import streamlit as st
import random

# -------------------- 데이터 --------------------
# 각 단원별 단어와 뜻을 딕셔너리 형태로 저장합니다.
words = {
    1: {
        "afternoon": "오후", "bag": "가방", "evening": "저녁", "everyone": "모두",
        "friend": "친구", "meet": "만나다", "morning": "아침", "name": "이름",
        "new": "새로운", "night": "밤", "to": "~에게", "we": "우리"
    },
    2: {
        "again": "다시", "angry": "화난", "happy": "행복한", "sad": "슬픈",
        "sleepy": "졸린", "some": "약간의", "thirsty": "목마른", "tired": "피곤한",
        "try": "시도하다", "water": "물"
    },
    3: {
        "careful": "조심하는", "drink": "마시다", "eat": "먹다", "enter": "들어가다",
        "house": "집", "kick": "차다", "line": "줄", "love": "사랑하다",
        "over": "~너머로", "push": "밀다", "talk": "말하다", "welcome": "환영하다"
    },
    4: {
        "bad": "나쁜", "badminton": "배드민턴", "baseball": "야구", "basketball": "농구",
        "busy": "바쁜", "let": "~하게 하다", "pass": "통과하다, 건네주다", "play": "놀다, 경기하다",
        "sick": "아픈", "soccer": "축구", "sound": "소리", "tennis": "테니스"
    },
    5: {
        "bread": "빵", "cream": "크림", "help": "돕다", "hot": "더운, 뜨거운",
        "ice": "얼음", "milk": "우유", "much": "많이", "noodles": "국수",
        "salad": "샐러드", "soup": "수프", "want": "원하다"
    },
    6: {
        "bed": "침대", "box": "상자", "bus": "버스", "chair": "의자",
        "desk": "책상", "fan": "선풍기", "know": "알다", "table": "탁자",
        "under": "~아래에", "where": "어디에"
    }
}

# 모든 단어를 합친 리스트 (퀴즈 보기 생성용)
all_words = []
for lesson_words in words.values():
    all_words.extend(lesson_words.keys())

# -------------------- 페이지 상태 관리 --------------------
# session_state를 초기화합니다.
if 'page' not in st.session_state:
    st.session_state.page = 'main'
if 'lesson_number' not in st.session_state:
    st.session_state.lesson_number = 0
if 'quiz_questions' not in st.session_state:
    st.session_state.quiz_questions = []
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'score' not in st.session_state:
    st.session_state.score = 0

# -------------------- 페이지 이동 함수 --------------------
def go_to_main():
    """메인 페이지로 이동하고 퀴즈 상태를 초기화합니다."""
    st.session_state.page = 'main'
    st.session_state.quiz_questions = []
    st.session_state.current_question = 0
    st.session_state.score = 0

def go_to_word_list(lesson):
    """선택한 단원의 단어장 페이지로 이동합니다."""
    st.session_state.page = 'word_list'
    st.session_state.lesson_number = lesson

def go_to_quiz():
    """퀴즈 페이지로 이동하고 퀴즈를 설정합니다."""
    st.session_state.page = 'quiz'
    st.session_state.current_question = 0
    st.session_state.score = 0
    
    # 퀴즈 문제 10개 생성
    all_word_pairs = []
    for lesson in words.values():
        all_word_pairs.extend(lesson.items())
    
    # 중복되지 않게 10개의 단어 선택
    random_questions = random.sample(all_word_pairs, 10)
    
    quiz_set = []
    for eng, kor in random_questions:
        # 정답을 제외한 단어 리스트
        other_words = [w for w in all_words if w != eng]
        # 오답 2개 랜덤 선택
        wrong_answers = random.sample(other_words, 2)
        
        options = wrong_answers + [eng]
        random.shuffle(options)
        
        quiz_set.append({
            "question": kor,
            "answer": eng,
            "options": options
        })
    st.session_state.quiz_questions = quiz_set

# -------------------- 페이지 렌더링 함수 --------------------

def render_main_page():
    """메인 페이지를 화면에 표시합니다."""
    st.title("📚 4학년 영어 천재(함) 단어 학습")
    st.write("---")
    st.subheader("🌷 단원별 단어장")

    cols = st.columns(3)
    for i in range(1, 7):
        # 3열로 버튼 배치
        with cols[(i-1) % 3]:
            if st.button(f"{i}단원", use_container_width=True):
                go_to_word_list(i)

    st.write("---")
    st.subheader("🎓 도전! 단어 퀴즈")
    if st.button("퀴즈 시작하기", type="primary", use_container_width=True):
        go_to_quiz()

def render_word_list_page():
    """단어장 페이지를 화면에 표시합니다."""
    lesson = st.session_state.lesson_number
    st.title(f"📖 {lesson}단원 단어장")

    # 단어와 뜻을 표 형태로 표시
    word_data = words[lesson]
    st.table(word_data)

    if st.button("메인으로 돌아가기"):
        go_to_main()

def handle_answer(selected_option):
    """퀴즈 답변을 처리합니다."""
    question_data = st.session_state.quiz_questions[st.session_state.current_question]
    
    if selected_option == question_data['answer']:
        st.session_state.score += 1
        st.toast("정답이에요! 🎉", icon="✅")
    else:
        st.toast(f"아쉬워요! 정답은 '{question_data['answer']}'였어요.", icon="❌")

    # 다음 문제로 이동
    st.session_state.current_question += 1
    if st.session_state.current_question >= len(st.session_state.quiz_questions):
        st.session_state.page = 'results'


def render_quiz_page():
    """퀴즈 페이지를 화면에 표시합니다."""
    if not st.session_state.quiz_questions:
        st.warning("퀴즈를 시작하려면 메인 페이지로 돌아가세요.")
        if st.button("메인으로 돌아가기"):
            go_to_main()
        return

    q_idx = st.session_state.current_question
    
    st.title("🎓 도전! 단어 퀴즈")
    st.progress((q_idx + 1) / len(st.session_state.quiz_questions), text=f"문제 {q_idx + 1}/10")

    question_data = st.session_state.quiz_questions[q_idx]
    
    st.subheader(f"\"{question_data['question']}\"")
    st.write("위의 뜻에 해당하는 영어 단어를 고르세요.")
    
    options = question_data['options']
    cols = st.columns(len(options))
    
    for i, option in enumerate(options):
        with cols[i]:
            if st.button(option, key=f"q{q_idx}_opt{i}", use_container_width=True, on_click=handle_answer, args=(option,)):
                pass


def render_results_page():
    """퀴즈 결과 페이지를 화면에 표시합니다."""
    score = st.session_state.score
    total = len(st.session_state.quiz_questions)

    st.title("✨ 퀴즈 결과 ✨")
    st.header(f"총 {total}문제 중 {score}개를 맞혔어요!")

    # 격려 메시지
    if score == total:
        st.success("와, 대단해요! 모든 문제를 맞혔네요! 🥳")
        st.balloons()
    elif score >= total * 0.7:
        st.info("정말 잘했어요! 조금만 더 힘내요! 👍")
    else:
        st.warning("아쉬워요. 단어장을 다시 한번 보고 도전해볼까요? 💪")

    if st.button("메인으로 돌아가기", type="primary"):
        go_to_main()

# -------------------- 메인 로직 --------------------
# 현재 페이지 상태에 따라 적절한 함수를 호출합니다.
if st.session_state.page == 'main':
    render_main_page()
elif st.session_state.page == 'word_list':
    render_word_list_page()
elif st.session_state.page == 'quiz':
    render_quiz_page()
elif st.session_state.page == 'results':
    render_results_page()
