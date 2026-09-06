import streamlit as st
import pandas as pd
import textwrap
from resume_parser import extract_resume_text
from text_cleaner import clean_text
from skill_extractor import extract_skills, get_all_skills
from job_matcher import load_job_roles, match_resume_to_roles
from roadmap_generator import get_skill_gap, generate_roadmap


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CareerIQ | AI Resume Analyzer",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 15% 10%, rgba(99, 102, 241, 0.18), transparent 28%),
        radial-gradient(circle at 85% 15%, rgba(6, 182, 212, 0.14), transparent 25%),
        linear-gradient(135deg, #070b17 0%, #0d1224 50%, #080d19 100%);
    color: #f8fafc;
}


/* Hide default Streamlit elements */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}


/* Sidebar */

[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, #0b1020 0%, #090d19 100%);
    border-right: 1px solid rgba(148, 163, 184, 0.12);
}
/* ============================================================
   BRIGHTER TEXT & BETTER CONTRAST
   ============================================================ */

/* Sidebar headings */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4,
[data-testid="stSidebar"] h5,
[data-testid="stSidebar"] h6 {
    color: #f8fafc !important;
}

/* Sidebar normal text */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #cbd5e1 !important;
}

/* Sidebar captions */
[data-testid="stSidebar"] .stCaption {
    color: #cbd5e1 !important;
}

/* Streamlit metric numbers */
[data-testid="stMetricValue"] {
    color: #f8fafc !important;
    font-weight: 800 !important;
}

/* Streamlit metric labels */
[data-testid="stMetricLabel"] {
    color: #cbd5e1 !important;
    font-weight: 700 !important;
}

/* Streamlit metric descriptions */
[data-testid="stMetricDelta"] {
    color: #cbd5e1 !important;
}

/* Custom metric labels */
.metric-label {
    color: #cbd5e1 !important;
}

/* Custom metric subtitles */
.metric-sub {
    color: #cbd5e1 !important;
}

/* General small text */
.stCaption {
    color: #cbd5e1 !important;
}
[data-testid="stSidebar"] h2 {
    color: #f8fafc;
}


/* Main content */

.block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1250px;
}


/* Hero */

.hero {
    padding: 42px 45px;
    border-radius: 28px;
    background:
        linear-gradient(
            135deg,
            rgba(30, 41, 88, 0.92),
            rgba(13, 148, 136, 0.25)
        );
    border: 1px solid rgba(129, 140, 248, 0.25);
    box-shadow:
        0 25px 70px rgba(0, 0, 0, 0.35),
        inset 0 1px 0 rgba(255, 255, 255, 0.05);
    margin-bottom: 28px;
}

.hero-badge {
    display: inline-block;
    padding: 7px 14px;
    border-radius: 50px;
    background: rgba(99, 102, 241, 0.18);
    border: 1px solid rgba(129, 140, 248, 0.35);
    color: #c7d2fe;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.5px;
}

.hero h1 {
    font-size: 42px;
    line-height: 1.1;
    margin: 18px 0 12px 0;
    color: #ffffff;
    font-weight: 800;
}

.hero p {
    font-size: 16px;
    color: #cbd5e1;
    max-width: 750px;
    line-height: 1.7;
}


/* Upload card */

.upload-card {
    padding: 28px;
    border-radius: 22px;
    background: rgba(15, 23, 42, 0.72);
    border: 1px solid rgba(148, 163, 184, 0.14);
    box-shadow: 0 15px 45px rgba(0, 0, 0, 0.22);
    margin-bottom: 25px;
}


/* Metric cards */

.metric-card {
    padding: 23px;
    min-height: 125px;
    border-radius: 20px;
    background: rgba(15, 23, 42, 0.75);
    border: 1px solid rgba(148, 163, 184, 0.13);
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.2);
}

.metric-label {
    color: #94a3b8;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.metric-value {
    margin-top: 8px;
    font-size: 27px;
    font-weight: 800;
    color: #ffffff;
}

.metric-sub {
    color: #94a3b8;
    font-size: 12px;
    margin-top: 5px;
}


/* Section headings */

.section-title {
    font-size: 21px;
    font-weight: 700;
    color: #f8fafc;
    margin-top: 28px;
    margin-bottom: 16px;
}


/* Career cards */

.career-card {
    padding: 19px 22px;
    margin: 10px 0;
    border-radius: 16px;
    background: rgba(15, 23, 42, 0.72);
    border: 1px solid rgba(148, 163, 184, 0.12);
}

.career-name {
    font-size: 15px;
    font-weight: 600;
    color: #f8fafc;
}

.career-score {
    float: right;
    font-weight: 800;
    color: #a5b4fc;
}


/* Skill pills */

.skill-pill {
    display: inline-block;
    padding: 7px 12px;
    margin: 4px 4px 4px 0;
    border-radius: 50px;
    background: rgba(99, 102, 241, 0.13);
    border: 1px solid rgba(129, 140, 248, 0.22);
    color: #c7d2fe;
    font-size: 12px;
    font-weight: 600;
}

.missing-pill {
    display: inline-block;
    padding: 7px 12px;
    margin: 4px 4px 4px 0;
    border-radius: 50px;
    background: rgba(245, 158, 11, 0.10);
    border: 1px solid rgba(245, 158, 11, 0.25);
    color: #fcd34d;
    font-size: 12px;
    font-weight: 600;
}


/* Roadmap */

.roadmap-card {
    padding: 20px;
    border-radius: 18px;
    background: rgba(15, 23, 42, 0.75);
    border: 1px solid rgba(148, 163, 184, 0.12);
    margin-bottom: 12px;
}

.week-label {
    color: #a5b4fc;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.week-topic {
    color: #ffffff;
    font-size: 17px;
    font-weight: 700;
    margin-top: 6px;
}

.week-goal {
    color: #94a3b8;
    font-size: 13px;
    line-height: 1.6;
    margin-top: 7px;
}


/* Info box */

.info-box {
    padding: 17px 20px;
    border-radius: 15px;
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(96, 165, 250, 0.18);
    color: #cbd5e1;
    font-size: 13px;
    line-height: 1.6;
}


/* Buttons */

.stButton > button {
    border-radius: 12px;
    border: 1px solid rgba(129, 140, 248, 0.35);
    background: linear-gradient(
        135deg,
        #6366f1,
        #4f46e5
    );
    color: white;
    font-weight: 700;
    min-height: 48px;
    transition: 0.2s ease;
}

.stButton > button:hover {
    border-color: #a5b4fc;
    transform: translateY(-1px);
}


/* File uploader */

[data-testid="stFileUploader"] {
    background: rgba(15, 23, 42, 0.75);
    border: 1px dashed rgba(129, 140, 248, 0.45);
    border-radius: 18px;
    padding: 12px;
}

[data-testid="stFileUploader"] section {
    background: transparent;
}

[data-testid="stFileUploader"] small {
    color: #94a3b8 !important;
}

[data-testid="stFileUploader"] span {
    color: #cbd5e1;
}
/* Extracted Resume Text */
[data-testid="stTextArea"] textarea {
    background-color: #111827 !important;
    color: #f8fafc !important;
    border: 1px solid rgba(148, 163, 184, 0.20) !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
}

[data-testid="stTextArea"] label {
    color: #cbd5e1 !important;
    font-weight: 600 !important;
}

[data-testid="stTextArea"] textarea::selection {
    background-color: #4f46e5 !important;
    color: #ffffff !important;
}
/* Selectbox */

[data-baseweb="select"] > div {
    background-color: rgba(15, 23, 42, 0.8);
    border-color: rgba(148, 163, 184, 0.18);
}


/* Divider */

hr {
    border-color: rgba(148, 163, 184, 0.10);
}


/* Footer */

.custom-footer {
    text-align: center;
    color: #64748b;
    font-size: 12px;
    margin-top: 45px;
    padding-top: 20px;
    border-top: 1px solid rgba(148, 163, 184, 0.08);
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    """
<div style="
    padding: 42px;
    border-radius: 28px;
    background: linear-gradient(135deg, #1e2958, #0f766e);
    border: 1px solid rgba(129,140,248,0.35);
    box-shadow: 0 20px 60px rgba(0,0,0,0.35);
    margin-bottom: 30px;
">

<div style="
    display:inline-block;
    padding:7px 14px;
    border-radius:30px;
    background:rgba(99,102,241,0.25);
    color:#c7d2fe;
    font-size:13px;
    font-weight:700;
">
✦ AI CAREER INTELLIGENCE ENGINE
</div>

<h1 style="
    color:white;
    font-size:42px;
    font-weight:800;
    margin:18px 0 10px 0;
">
Turn Your Resume Into<br>
Your Career Roadmap.
</h1>

<p style="
    color:#dbeafe;
    font-size:16px;
    line-height:1.7;
    max-width:760px;
">
Analyze your resume, discover the roles that match your skills,
identify career gaps, and understand what to learn next —
all from one intelligent dashboard.
</p>

</div>
""",
    unsafe_allow_html=True
)

# ============================================================
# LOAD JOB ROLES
# ============================================================

job_roles = load_job_roles()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## ✦ CareerIQ")

    st.caption("AI Resume Analyzer")

    st.divider()

    st.markdown("### 🎯 Target Career")

    target_role = st.selectbox(
        "Choose a role to analyze",
        ["Auto Detect"] + job_roles["role"].tolist(),
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### How it works")

    st.markdown("""
    <div class="info-box">

    <b>01</b> Upload your resume<br><br>

    <b>02</b> AI extracts your skills<br><br>

    <b>03</b> Roles are matched using NLP<br><br>

    <b>04</b> Skill gaps are identified<br><br>

    <b>05</b> Your learning roadmap is generated

    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.caption(
        "Career guidance only • Not an automatic hiring decision"
    )


# ============================================================
# UPLOAD SECTION
# ============================================================

st.markdown(
    '<div class="section-title">📄 Resume Analysis</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Drop your resume here",
    type=["pdf", "docx"],
    help="Supported formats: PDF and DOCX"
)

st.markdown(
    """
    <div style="
        color:#64748b;
        font-size:12px;
        margin-top:8px;
        margin-bottom:20px;
    ">
    🔒 Your resume is processed for analysis and is not permanently stored.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ANALYSIS
# ============================================================

if uploaded_file is not None:

    st.success(f"✓ Ready to analyze: {uploaded_file.name}")

    if st.button(
        "✦  ANALYZE MY RESUME",
        use_container_width=True
    ):

        try:

            with st.spinner("Analyzing your resume..."):

                # Extract
                raw_text = extract_resume_text(uploaded_file)

                # Clean
                cleaned_text = clean_text(raw_text)

                # Skills
                categorized_skills = extract_skills(cleaned_text)
                all_skills = get_all_skills(cleaned_text)

                # Job matching
                results = match_resume_to_roles(
                    " ".join(all_skills),
                    job_roles
                )

            st.success("Analysis completed successfully!")

            # ==================================================
            # SUMMARY METRICS
            # ==================================================

            st.markdown(
                '<div class="section-title">📊 Career Snapshot</div>',
                unsafe_allow_html=True
            )

            top_role = results[0]

            col1, col2, col3 = st.columns(3)

            with col1:

                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Overall Match</div>
                    <div class="metric-value">
                        {top_role['match_score']}%
                    </div>
                    <div class="metric-sub">
                        Best matching career
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col2:

                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Top Career</div>
                    <div class="metric-value" style="font-size:21px;">
                        {top_role['role']}
                    </div>
                    <div class="metric-sub">
                        Highest compatibility
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col3:

                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Skills Detected</div>
                    <div class="metric-value">
                        {len(all_skills)}
                    </div>
                    <div class="metric-sub">
                        Across multiple categories
                    </div>
                </div>
                """, unsafe_allow_html=True)


            # ==================================================
            # CAREER RECOMMENDATIONS
            # ==================================================

            st.markdown(
                '<div class="section-title">🎯 Your Career Matches</div>',
                unsafe_allow_html=True
            )

            top_three = results[:3]

            # --------------------------------------------------
            # BEST MATCH
            # --------------------------------------------------

            best = top_three[0]
            best_score = float(best["match_score"])

            st.markdown("### 🏆 Best Career Match")

            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(
                    f"## 🥇 {best['role']}"
                )

                st.caption(
                    "Your strongest career match based on the skills "
                    "identified from your resume."
                )

            with col2:
                st.metric(
                    "Match Score",
                    f"{best_score:.2f}%"
                )

            st.progress(
                min(best_score / 100, 1.0)
            )


            # --------------------------------------------------
            # SECOND AND THIRD MATCH
            # --------------------------------------------------

            if len(top_three) > 1:

                columns = st.columns(2)

                for index, item in enumerate(top_three[1:3]):

                    score = float(item["match_score"])

                    medal = "🥈" if index == 0 else "🥉"

                    with columns[index]:

                        st.markdown(
                            f"### {medal} {item['role']}"
                        )

                        st.metric(
                            "Match Score",
                            f"{score:.2f}%"
                        )

                        st.progress(
                            min(score / 100, 1.0)
                        )


            # ==================================================
            # CAREER FIT — EASY VISUAL COMPARISON
            # ==================================================
            st.markdown("### 📊 Career Fit Comparison")

            max_score = max(
                float(item["match_score"])
                for item in top_three
            )

            for item in top_three:

                role = item["role"]
                score = float(item["match_score"])

                st.markdown(
                    f"**{role}** — {score:.2f}%"
                )

                visual_score = (
                    score / max_score
                    if max_score > 0
                    else 0
                )

                st.progress(
                    visual_score
                )


            st.info(
                f"💡 Your strongest current career match is "
                f"**{best['role']}** with a match score of "
                f"**{best_score:.2f}%**. "
                f"The comparison above shows how your recommended "
                f"roles rank relative to each other."
            )


            # ==================================================
            # SKILL INTELLIGENCE
            # ==================================================

            st.markdown(
                '<div class="section-title">🧠 Skill Intelligence</div>',
                unsafe_allow_html=True
            )

            total_skills = sum(
                len(skills)
                for skills in categorized_skills.values()
            )

            st.markdown("### ✨ Resume Skill Profile")

            st.metric(
                "Skills Detected",
                total_skills
            )

            st.caption(
                "Skills identified from your resume and grouped "
                "by category."
            )


            # --------------------------------------------------
            # SKILL CATEGORIES
            # --------------------------------------------------

            category_icons = {
                "Programming": "💻",
                "Data & Databases": "🗄️",
                "AI & Machine Learning": "🤖",
                "Web & APIs": "🌐",
                "Cloud & DevOps": "☁️",
                "Tools & Visualization": "📊"
            }

            skill_categories = [
                (category, skills)
                for category, skills
                in categorized_skills.items()
                if skills
            ]

            for row_start in range(
                0,
                len(skill_categories),
                2
            ):

                row = skill_categories[
                    row_start:row_start + 2
                ]

                columns = st.columns(2)

                for column, (category, skills) in zip(
                    columns,
                    row
                ):

                    icon = category_icons.get(
                        category,
                        "🔹"
                    )

                    with column:

                        st.markdown(
                            f"### {icon} {category}"
                        )

                        st.caption(
                            f"{len(skills)} skills detected"
                        )

                        for skill in skills:

                            st.markdown(
                                f"✓ **{skill.title()}**"
                            )


            # --------------------------------------------------
            # SKILL PROFILE INSIGHT
            # --------------------------------------------------

            if total_skills >= 15:

                profile_message = (
                    "Your resume shows a broad technical skill "
                    "profile across multiple areas."
                )

            elif total_skills >= 8:

                profile_message = (
                    "Your resume has a solid technical foundation "
                    "with several identifiable skill areas."
                )

            else:

                profile_message = (
                    "Your resume contains a few identifiable skills. "
                    "Adding more project-specific skills may improve "
                    "career matching."
                )

            st.info(
                f"💡 **Skill Profile Insight:** "
                f"{profile_message}"
            )


            # ==================================================
            # TARGET ROLE ANALYSIS
            # ==================================================

            if target_role != "Auto Detect":

                selected_role = job_roles[
                    job_roles["role"] == target_role
                ].iloc[0]

                required_skills = [
                    skill.strip().lower()
                    for skill in selected_role[
                        "required_skills"
                    ].split(",")
                ]

                matched_skills, missing_skills = get_skill_gap(
                    all_skills,
                    required_skills
                )

                target_score = next(
                    item["match_score"]
                    for item in results
                    if item["role"] == target_role
                )

                # ----------------------------------------------
                # TARGET ROLE HEADER
                # ----------------------------------------------

                st.markdown(
                    '<div class="section-title">'
                    f'🎯 Target Role: {target_role}'
                    '</div>',
                    unsafe_allow_html=True
                )

                # ----------------------------------------------
                # RESUME COMPATIBILITY
                # ----------------------------------------------

                st.metric(
                    "Resume Compatibility",
                    f"{target_score:.2f}%",
                    "Based on job-related resume information"
                )

                # ----------------------------------------------
                # MATCHED / MISSING SKILLS
                # ----------------------------------------------

                col1, col2 = st.columns(2)

                with col1:

                    st.markdown(
                        '<div class="section-title">'
                        '✅ Matched Skills'
                        '</div>',
                        unsafe_allow_html=True
                    )

                    if matched_skills:

                        pills = ""

                        for skill in matched_skills:

                            pills += (
                                f'<span class="skill-pill">'
                                f'✓ {skill.title()}'
                                f'</span>'
                            )

                        st.markdown(
                            pills,
                            unsafe_allow_html=True
                        )

                    else:

                        st.info(
                            "No matching skills detected."
                        )

                with col2:

                    st.markdown(
                        '<div class="section-title">'
                        '⚡ Skill Gaps'
                        '</div>',
                        unsafe_allow_html=True
                    )

                    if missing_skills:

                        pills = ""

                        for skill in missing_skills:

                            pills += (
                                f'<span class="missing-pill">'
                                f'! {skill.title()}'
                                f'</span>'
                            )

                        st.markdown(
                            pills,
                            unsafe_allow_html=True
                        )

                    else:

                        st.success(
                            "All required skills detected!"
                        )

                # ----------------------------------------------
                # ROADMAP
                # ----------------------------------------------

                st.markdown(
                    '<div class="section-title">'
                    '🗺️ Personalized Learning Roadmap'
                    '</div>',
                    unsafe_allow_html=True
                )

                roadmap = generate_roadmap(
                    missing_skills
                )

                for item in roadmap:

                    st.markdown(
                        f'<div class="roadmap-card">'
                        f'<div class="week-label">{item["week"]}</div>'
                        f'<div class="week-topic">{item["topic"]}</div>'
                        f'<div class="week-goal">{item["goal"]}</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
            else:

                st.markdown(
                    """
                    <div class="info-box">
                    🎯 <b>Choose a target role</b> from the sidebar
                    to unlock detailed skill-gap analysis and your
                    personalized learning roadmap.
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            # ==================================================
            # EXTRACTED TEXT
            # ==================================================

            with st.expander(
                "🔍 View Extracted Resume Text"
            ):

                st.text_area(
                    "Resume Text",
                    raw_text,
                    height=300
                )


        except Exception as e:

            st.error(
                f"Something went wrong during analysis: {e}"
            )


else:

    st.markdown(
        """
        <div class="info-box">
        📌 <b>Ready when you are.</b><br>
        Upload a PDF or DOCX resume above to start your
        career analysis.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div style="
        text-align:center;
        margin-top:40px;
        padding:20px;
        border-top:1px solid rgba(148,163,184,0.15);
    ">
        <div style="
            color:#a5b4fc;
            font-size:14px;
            font-weight:700;
        ">
            ✦ CareerIQ
        </div>

        <div style="
            color:#cbd5e1;
            font-size:12px;
            margin-top:6px;
        ">
            AI Resume Analyzer • Career guidance powered by resume insights
        </div>
    </div>
    """.replace("\n", ""),
    unsafe_allow_html=True
)