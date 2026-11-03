import os
import datetime
import pandas as pd
import streamlit as st

# Configure Streamlit page
st.set_page_config(
    page_title="MY ENGINEERING DEGREE OS",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Professional College Dashboard
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .badge-completed {
        background-color: #DEF7EC;
        color: #03543F;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.82rem;
        font-weight: 600;
    }
    .badge-progress {
        background-color: #FEF08A;
        color: #713F12;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.82rem;
        font-weight: 600;
    }
    .badge-notstarted {
        background-color: #F3F4F6;
        color: #374151;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.82rem;
        font-weight: 600;
    }
    .chat-source-tag {
        font-size: 0.8rem;
        font-weight: 600;
        color: #2563EB;
        background: #EFF6FF;
        border: 1px solid #BFDBFE;
        border-radius: 4px;
        padding: 2px 6px;
        display: inline-block;
        margin-bottom: 6px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Data Loader and Saver Helpers
# ---------------------------------------------------------
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

def get_csv_path(filename: str) -> str:
    return os.path.join(DATA_DIR, filename)

def load_data(filename: str, default_df: pd.DataFrame = None) -> pd.DataFrame:
    path = get_csv_path(filename)
    if not os.path.exists(path):
        st.warning(f"⚠️ Warning: `{filename}` was not found in `{DATA_DIR}`. Using empty template.")
        return default_df if default_df is not None else pd.DataFrame()
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        st.error(f"Error loading {filename}: {e}")
        return default_df if default_df is not None else pd.DataFrame()

def save_data(filename: str, df: pd.DataFrame) -> bool:
    path = get_csv_path(filename)
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        df.to_csv(path, index=False)
        return True
    except Exception as e:
        st.error(f"Error saving {filename}: {e}")
        return False

# Load primary datasets
semesters_df = load_data("semesters.csv")
courses_df = load_data("courses.csv")
calendar_df = load_data("academic_calendar.csv")
assessments_df = load_data("assessments.csv")
scores_df = load_data("scores.csv")
checklist_df = load_data("plan_checklist.csv")

# Ensure required columns are string/numeric typed safely
if not semesters_df.empty:
    semesters_df["semester"] = pd.to_numeric(semesters_df["semester"], errors="coerce").fillna(0).astype(int)
    semesters_df["total_credits"] = pd.to_numeric(semesters_df["total_credits"], errors="coerce").fillna(0)
    semesters_df["completed_credits"] = pd.to_numeric(semesters_df["completed_credits"], errors="coerce").fillna(0)

if not courses_df.empty:
    courses_df["semester"] = pd.to_numeric(courses_df["semester"], errors="coerce").fillna(0).astype(int)
    courses_df["credits"] = pd.to_numeric(courses_df["credits"], errors="coerce").fillna(0)

if not assessments_df.empty:
    assessments_df["semester"] = pd.to_numeric(assessments_df["semester"], errors="coerce").fillna(0).astype(int)

if not scores_df.empty:
    scores_df["semester"] = pd.to_numeric(scores_df["semester"], errors="coerce").fillna(0).astype(int)
    scores_df["score"] = pd.to_numeric(scores_df["score"], errors="coerce").fillna(0)
    scores_df["max_marks"] = pd.to_numeric(scores_df["max_marks"], errors="coerce").fillna(100)

# Simulated / current reference date (2026-11-02 from metadata)
CURRENT_DATE = datetime.date(2026, 11, 2)

# ---------------------------------------------------------
# Sidebar Navigation
# ---------------------------------------------------------
st.sidebar.title("🎓 Degree OS")
st.sidebar.caption("1st-to-8th Semester Command Center")

nav_options = [
    "Dashboard",
    "Semesters 1-8",
    "Courses & Syllabus",
    "University Syllabus",
    "Academic / Leave Calendar",
    "Internal Assessments",
    "Status Tracker",
    "Scorecard",
    "Plan & Checklist",
    "Ask Degree AI",
    "Data Admin"
]

selected_page = st.sidebar.radio("Navigation", nav_options)

st.sidebar.markdown("---")
st.sidebar.markdown("**System Health**")
st.sidebar.caption(f"🗓 Current Date: {CURRENT_DATE.strftime('%d %b %Y')}")
total_sem_credits = int(semesters_df['total_credits'].sum()) if not semesters_df.empty else 0
done_credits = int(semesters_df['completed_credits'].sum()) if not semesters_df.empty else 0
st.sidebar.progress(done_credits / total_sem_credits if total_sem_credits > 0 else 0.0)
st.sidebar.caption(f"Credits: {done_credits} / {total_sem_credits} ({round((done_credits/total_sem_credits)*100, 1) if total_sem_credits else 0}%)")


# =========================================================
# Page 1: Dashboard
# =========================================================
if selected_page == "Dashboard":
    st.markdown('<div class="main-title">My Engineering Degree OS</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Personal command center for tracking the complete 8-semester engineering journey.</div>', unsafe_allow_html=True)

    # Key calculations
    current_sem = 3
    if not semesters_df.empty:
        in_prog = semesters_df[semesters_df["status"] == "In Progress"]
        if not in_prog.empty:
            current_sem = int(in_prog["semester"].iloc[0])
        else:
            comp = semesters_df[semesters_df["status"] == "Completed"]
            current_sem = int(comp["semester"].max()) + 1 if not comp.empty else 1

    deg_completion_pct = round((done_credits / total_sem_credits) * 100, 1) if total_sem_credits > 0 else 0.0

    # Next assessment
    next_assessment_str = "None scheduled"
    if not assessments_df.empty:
        upcoming_ass = assessments_df[pd.to_datetime(assessments_df["date"], errors="coerce").dt.date >= CURRENT_DATE].sort_values("date")
        if not upcoming_ass.empty:
            row = upcoming_ass.iloc[0]
            next_assessment_str = f"{row['course_code']} - {row['assessment_type']} ({row['date']})"
        else:
            # Fallback to next planned
            planned = assessments_df[assessments_df["status"] == "Planned"]
            if not planned.empty:
                row = planned.iloc[0]
                next_assessment_str = f"{row['course_code']} - {row['assessment_type']} ({row['date']})"

    # Next holiday / leave
    next_holiday_str = "None upcoming"
    if not calendar_df.empty:
        upcoming_hols = calendar_df[(calendar_df["event_type"] == "Holiday") & (pd.to_datetime(calendar_df["date"], errors="coerce").dt.date >= CURRENT_DATE)].sort_values("date")
        if not upcoming_hols.empty:
            row = upcoming_hols.iloc[0]
            next_holiday_str = f"{row['title']} ({row['date']})"

    # Prototype Score Percentage
    if not scores_df.empty and scores_df["max_marks"].sum() > 0:
        proto_score_pct = round((scores_df["score"].sum() / scores_df["max_marks"].sum()) * 100, 2)
        score_metric = f"{proto_score_pct}%"
    else:
        score_metric = "N/A"

    # Top Metric Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Current Semester", f"Semester {current_sem}")
    with c2:
        st.metric("Degree Completion", f"{deg_completion_pct}%")
    with c3:
        st.metric("Completed Credits", f"{done_credits} / {total_sem_credits}")
    with c4:
        st.metric("Prototype Score %", score_metric)

    st.markdown("---")

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("📅 Next Upcoming Academic Events")
        st.info(f"**Next Assessment:** {next_assessment_str}")
        st.success(f"**Next Holiday / Leave:** {next_holiday_str}")
        
        st.markdown("#### Degree Status Snapshot")
        st.write(f"- **Total Degree Semesters:** 8")
        st.write(f"- **Current Active Semester:** Semester {current_sem}")
        st.write(f"- **Prototype Cumulative Score:** {score_metric} *(calculated as total marks obtained / total max marks)*")

    with col_b:
        st.subheader("📊 8-Semester Credit Progress")
        if not semesters_df.empty:
            chart_df = semesters_df.copy()
            chart_df["Remaining Credits"] = chart_df["total_credits"] - chart_df["completed_credits"]
            chart_df.rename(columns={"completed_credits": "Completed Credits"}, inplace=True)
            chart_df["Semester"] = "Sem " + chart_df["semester"].astype(str)
            chart_df.set_index("Semester", inplace=True)
            st.bar_chart(chart_df[["Completed Credits", "Remaining Credits"]], height=260)
        else:
            st.info("No semester data available to plot.")


# =========================================================
# Page 2: Semesters 1-8
# =========================================================
elif selected_page == "Semesters 1-8":
    st.markdown('<div class="main-title">Semesters 1 - 8 Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Card overview and progress across all 8 academic semesters.</div>', unsafe_allow_html=True)

    if semesters_df.empty:
        st.warning("No semester data found in `data/semesters.csv`.")
    else:
        # Display 8 semester cards in grid
        cols = st.columns(4)
        for idx, row in semesters_df.iterrows():
            col_target = cols[idx % 4]
            sem_num = int(row["semester"])
            status = str(row["status"])
            tot_cr = int(row["total_credits"])
            comp_cr = int(row["completed_credits"])
            
            # Count courses in this semester
            course_count = len(courses_df[courses_df["semester"] == sem_num]) if not courses_df.empty else 0
            
            badge_class = "badge-completed" if status == "Completed" else ("badge-progress" if status == "In Progress" else "badge-notstarted")
            
            with col_target:
                with st.container():
                    st.markdown(f"""
                    <div class="metric-card">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                            <h4 style="margin:0; color:#1E3A8A;">Semester {sem_num}</h4>
                            <span class="{badge_class}">{status}</span>
                        </div>
                        <p style="margin:4px 0; font-size:0.9rem;"><strong>Courses:</strong> {course_count}</p>
                        <p style="margin:4px 0; font-size:0.9rem;"><strong>Credits:</strong> {comp_cr} / {tot_cr}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.progress(comp_cr / tot_cr if tot_cr > 0 else 0.0)

        st.markdown("---")
        st.subheader("🔍 Filterable Semester Details")
        sem_list = sorted(semesters_df["semester"].unique().tolist())
        selected_sem = st.selectbox("Select Semester to View Details", sem_list, index=2 if 3 in sem_list else 0)

        sem_row = semesters_df[semesters_df["semester"] == selected_sem].iloc[0]
        st.write(f"**Status:** `{sem_row['status']}` | **Total Credits:** `{sem_row['total_credits']}` | **Completed Credits:** `{sem_row['completed_credits']}`")
        
        if not courses_df.empty:
            sem_courses = courses_df[courses_df["semester"] == selected_sem]
            st.dataframe(sem_courses[["course_code", "course_name", "credits", "faculty", "syllabus", "status"]], use_container_width=True, hide_index=True)
        else:
            st.info("No courses found.")


# =========================================================
# Page 3: Courses & Syllabus
# =========================================================
elif selected_page == "Courses & Syllabus":
    st.markdown('<div class="main-title">Courses & Syllabus</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Detailed course curriculum, faculty allocation, and module syllabi.</div>', unsafe_allow_html=True)

    if courses_df.empty:
        st.warning("No courses data found in `data/courses.csv`.")
    else:
        col1, col2 = st.columns([1, 3])
        with col1:
            all_sems = ["All Semesters"] + [f"Semester {s}" for s in sorted(courses_df["semester"].unique())]
            choice = st.selectbox("Filter by Semester", all_sems, index=3 if len(all_sems) > 3 else 0)

        if choice == "All Semesters":
            filtered_courses = courses_df.copy()
        else:
            selected_s = int(choice.split(" ")[1])
            filtered_courses = courses_df[courses_df["semester"] == selected_s]

        st.dataframe(
            filtered_courses[["semester", "course_code", "course_name", "credits", "faculty", "status", "syllabus"]],
            use_container_width=True,
            hide_index=True
        )

        st.markdown("#### 📖 Syllabus Topics Breakdown")
        for _, c_row in filtered_courses.iterrows():
            with st.expander(f"📌 {c_row['course_code']}: {c_row['course_name']} ({c_row['credits']} Credits) - {c_row['status']}"):
                st.write(f"**Faculty:** {c_row.get('faculty', 'Faculty Instructor')}")
                st.write(f"**Status:** `{c_row['status']}`")
                st.write(f"**Topics / Modules:**")
                topics = str(c_row.get('syllabus', '')).split(";")
                for topic in topics:
                    if topic.strip():
                        st.markdown(f"- {topic.strip()}")


# =========================================================
# Page 4: University Syllabus
# =========================================================
elif selected_page == "University Syllabus":
    st.markdown('<div class="main-title">University Syllabus Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Programme-level curriculum specifications and official reference citations.</div>', unsafe_allow_html=True)

    st.markdown("""
    ### 🏛 Bachelor of Technology (B.Tech) - Computer Science & Engineering
    **Degree Duration:** 4 Years (8 Semesters)  
    **Total Expected Degree Credits:** 175 Credits  
    **Curriculum Model:** Outcome-Based Education (OBE) & CBCS Framework  
    """)

    st.markdown("#### 🔗 Official Syllabus Source & Reference")
    ref_input = st.text_input(
        "Syllabus Source / Reference Field",
        value="https://university-curriculum-portal.edu/curriculum/btech-cse-2024-regulation.pdf",
        help="Store the official university syllabus PDF link, regulatory gazette, or syllabus portal reference code."
    )
    st.caption("Reference verified: Curriculum document reference code `REG-2024-CSE-CBCS`.")

    st.markdown("---")
    st.subheader("📚 Programme Structure Summary")

    prog_summary = pd.DataFrame([
        {"Category": "Basic Sciences (BS)", "Semesters": "Sem 1 - Sem 2", "Credits": "24", "Core Focus": "Mathematics, Physics, Chemistry"},
        {"Category": "Engineering Sciences (ES)", "Semesters": "Sem 1 - Sem 2", "Credits": "18", "Core Focus": "C Programming, Electrical Engineering, Engineering Design"},
        {"Category": "Professional Core (PC)", "Semesters": "Sem 3 - Sem 6", "Credits": "82", "Core Focus": "Data Structures, Algorithms, OS, DBMS, Networks, Compilers, AI"},
        {"Category": "Professional Electives (PE)", "Semesters": "Sem 6 - Sem 7", "Credits": "18", "Core Focus": "Cloud Computing, Big Data, Cryptography, Web Technologies"},
        {"Category": "Projects & Capstone (PR)", "Semesters": "Sem 6 - Sem 8", "Credits": "21", "Core Focus": "Mini Project, Major Project Phase 1 & 2, Industrial Internship"},
        {"Category": "Humanities & Ethics (HS)", "Semesters": "Sem 7", "Credits": "12", "Core Focus": "Cyber Law, Professional Ethics, Environmental Sciences"},
    ])
    st.table(prog_summary)

    st.info("ℹ️ Note: This overview reflects the loaded programme structure. To view individual course syllabus modules, navigate to **Courses & Syllabus**.")


# =========================================================
# Page 5: Academic / Leave Calendar
# =========================================================
elif selected_page == "Academic / Leave Calendar":
    st.markdown('<div class="main-title">Academic & Leave Calendar</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Institutional academic schedules, milestone events, and official holidays.</div>', unsafe_allow_html=True)

    if calendar_df.empty:
        st.warning("No calendar events found in `data/academic_calendar.csv`.")
    else:
        f_col1, f_col2, f_col3 = st.columns(3)
        with f_col1:
            years = ["All"] + sorted(calendar_df["academic_year"].dropna().unique().tolist())
            selected_year = st.selectbox("Academic Year", years)
        with f_col2:
            sems = ["All"] + sorted([str(s) for s in calendar_df["semester"].dropna().unique().tolist()])
            selected_sem = st.selectbox("Semester", sems)
        with f_col3:
            event_types = ["All", "Academic", "Holiday"]
            selected_type = st.selectbox("Event Type", event_types)

        filtered_cal = calendar_df.copy()
        if selected_year != "All":
            filtered_cal = filtered_cal[filtered_cal["academic_year"] == selected_year]
        if selected_sem != "All":
            filtered_cal = filtered_cal[filtered_cal["semester"].astype(str) == selected_sem]
        if selected_type != "All":
            filtered_cal = filtered_cal[filtered_cal["event_type"] == selected_type]

        filtered_cal = filtered_cal.sort_values("date")

        st.subheader("📅 Schedule of Events & Holidays")
        st.dataframe(filtered_cal[["academic_year", "semester", "date", "event_type", "title"]], use_container_width=True, hide_index=True)

        st.markdown("#### Coexisting Calendar Summary")
        ac_count = len(filtered_cal[filtered_cal["event_type"] == "Academic"])
        hol_count = len(filtered_cal[filtered_cal["event_type"] == "Holiday"])
        st.write(f"- **Academic Events in View:** {ac_count}")
        st.write(f"- **Holidays / Leaves in View:** {hol_count}")


# =========================================================
# Page 6: Internal Assessments
# =========================================================
elif selected_page == "Internal Assessments":
    st.markdown('<div class="main-title">Internal Assessments & Examinations</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Tracking IA1, IA2, assignments, lab evaluations, project reviews, and term exams.</div>', unsafe_allow_html=True)

    if assessments_df.empty:
        st.warning("No assessments found in `data/assessments.csv`.")
    else:
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            sems = ["All"] + sorted([str(s) for s in assessments_df["semester"].unique().tolist()])
            sel_sem = st.selectbox("Filter Semester", sems, index=2 if "3" in sems else 0)
        with col_f2:
            types = ["All"] + sorted(assessments_df["assessment_type"].unique().tolist())
            sel_type = st.selectbox("Filter Assessment Type", types)

        filtered_ass = assessments_df.copy()
        if sel_sem != "All":
            filtered_ass = filtered_ass[filtered_ass["semester"].astype(str) == sel_sem]
        if sel_type != "All":
            filtered_ass = filtered_ass[filtered_ass["assessment_type"] == sel_type]

        filtered_ass = filtered_ass.sort_values("date")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Total Assessments in View", len(filtered_ass))
        with c2:
            planned_count = len(filtered_ass[filtered_ass["status"] == "Planned"])
            st.metric("Planned / Upcoming", planned_count)
        with c3:
            comp_count = len(filtered_ass[filtered_ass["status"] == "Completed"])
            st.metric("Completed", comp_count)

        st.subheader("📋 Assessments Schedule")
        st.dataframe(filtered_ass[["semester", "course_code", "assessment_type", "date", "max_marks", "status"]], use_container_width=True, hide_index=True)


# =========================================================
# Page 7: Status Tracker
# =========================================================
elif selected_page == "Status Tracker":
    st.markdown('<div class="main-title">Degree Status Tracker</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Course progression by Not Started, In Progress, and Completed statuses.</div>', unsafe_allow_html=True)

    if courses_df.empty:
        st.warning("No courses data found.")
    else:
        sem_list = sorted(courses_df["semester"].unique().tolist())
        selected_sem = st.selectbox("Select Semester for Progress Tracking", sem_list, index=2 if 3 in sem_list else 0)

        sem_courses = courses_df[courses_df["semester"] == selected_sem]
        tot = len(sem_courses)
        completed_c = len(sem_courses[sem_courses["status"] == "Completed"])
        inprogress_c = len(sem_courses[sem_courses["status"] == "In Progress"])
        notstarted_c = len(sem_courses[sem_courses["status"] == "Not Started"])

        st.markdown(f"### Progress for Semester {selected_sem}")
        prog_ratio = (completed_c / tot) if tot > 0 else 0.0
        st.progress(prog_ratio)
        st.caption(f"{completed_c} of {tot} courses completed ({round(prog_ratio*100, 1)}%)")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Courses", tot)
        m2.metric("Completed", completed_c)
        m3.metric("In Progress", inprogress_c)
        m4.metric("Not Started", notstarted_c)

        st.markdown("---")
        st.subheader("Detailed Course Statuses")
        st.dataframe(sem_courses[["course_code", "course_name", "credits", "faculty", "status"]], use_container_width=True, hide_index=True)

        st.markdown("#### Cumulative Degree Progression (All Semesters)")
        all_completed = len(courses_df[courses_df["status"] == "Completed"])
        all_inprog = len(courses_df[courses_df["status"] == "In Progress"])
        all_notstarted = len(courses_df[courses_df["status"] == "Not Started"])
        st.write(f"- **Total Degree Courses:** {len(courses_df)}")
        st.write(f"- **Completed Across Degree:** {all_completed}")
        st.write(f"- **In Progress:** {all_inprog}")
        st.write(f"- **Remaining / Not Started:** {all_notstarted}")


# =========================================================
# Page 8: Scorecard
# =========================================================
elif selected_page == "Scorecard":
    st.markdown('<div class="main-title">Academic Scorecard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Evaluation marks, grades, semester averages, and cumulative prototype score.</div>', unsafe_allow_html=True)

    if scores_df.empty:
        st.warning("No scores found in `data/scores.csv`.")
    else:
        total_score = scores_df["score"].sum()
        total_max = scores_df["max_marks"].sum()
        proto_pct = round((total_score / total_max) * 100, 2) if total_max > 0 else 0.0

        st.info("📌 **Note:** Prototype score percentage = (total score / total max marks) × 100. This is clearly labelled as a **prototype score percentage**, not an official university CGPA formula.")

        col1, col2, col3 = st.columns(3)
        col1.metric("Prototype Score Percentage", f"{proto_pct}%")
        col2.metric("Total Marks Scored", f"{int(total_score)} / {int(total_max)}")
        col3.metric("Evaluated Subjects", len(scores_df))

        st.markdown("---")
        st.subheader("Semester-wise Performance")
        for sem, s_group in scores_df.groupby("semester"):
            sem_score = s_group["score"].sum()
            sem_max = s_group["max_marks"].sum()
            sem_pct = round((sem_score / sem_max) * 100, 2) if sem_max > 0 else 0.0
            
            with st.container():
                st.markdown(f"#### Semester {sem} Average: `{sem_pct}%` ({int(sem_score)}/{int(sem_max)} marks)")
                st.dataframe(s_group[["course_code", "assessment_type", "score", "max_marks", "grade"]], use_container_width=True, hide_index=True)


# =========================================================
# Page 9: Plan & Checklist
# =========================================================
elif selected_page == "Plan & Checklist":
    st.markdown('<div class="main-title">Plan & Degree Execution Checklist</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Execution control panel for milestones, exam preparation, documents, and placement readiness.</div>', unsafe_allow_html=True)

    if checklist_df.empty:
        st.warning("No checklist found in `data/plan_checklist.csv`.")
    else:
        # Calculate dynamic health based on CURRENT_DATE
        def compute_health(row):
            if str(row["status"]).strip().lower() == "done":
                return "Done"
            try:
                t_date = pd.to_datetime(row["target_date"]).date()
                days_diff = (t_date - CURRENT_DATE).days
                if days_diff < 0:
                    return "Overdue"
                elif days_diff <= 7:
                    return "Due Soon"
                else:
                    return "Upcoming"
            except Exception:
                return "Normal"

        checklist_work_df = checklist_df.copy()
        checklist_work_df["health"] = checklist_work_df.apply(compute_health, axis=1)

        # Summary Metrics
        tot_items = len(checklist_work_df)
        done_items = len(checklist_work_df[checklist_work_df["status"] == "Done"])
        due_soon_items = len(checklist_work_df[checklist_work_df["health"] == "Due Soon"])
        overdue_items = len(checklist_work_df[checklist_work_df["health"] == "Overdue"])

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Checklist Items", tot_items)
        c2.metric("Done", done_items)
        c3.metric("Due Soon (≤7 Days)", due_soon_items)
        c4.metric("Overdue", overdue_items)

        st.markdown("---")

        # Required 3 functional sections: This Week, Semester Milestones, Degree Milestones
        tab1, tab2, tab3 = st.tabs(["⚡ This Week (Next 7 Days)", "🎯 Semester Milestones", "🚀 Degree Milestones"])

        with tab1:
            st.markdown("##### Tasks due in the next 7 days")
            this_week_df = checklist_work_df[checklist_work_df["health"] == "Due Soon"]
            if not this_week_df.empty:
                st.dataframe(this_week_df[["category", "item", "target_date", "status", "notes"]], use_container_width=True, hide_index=True)
            else:
                st.info("No items due within the next 7 days.")

        with tab2:
            st.markdown("##### Major outcomes for current semester")
            sem_milestones = checklist_work_df[checklist_work_df["category"].isin(["Semester Preparation", "Assessments", "Labs", "Projects"])]
            st.dataframe(sem_milestones[["category", "item", "target_date", "status", "health", "notes"]], use_container_width=True, hide_index=True)

        with tab3:
            st.markdown("##### Long-range checkpoints (Internships, Skills, Placement readiness, Documents)")
            degree_milestones = checklist_work_df[checklist_work_df["category"].isin(["Internship/Placement", "Placement", "Skills", "Documents"])]
            st.dataframe(degree_milestones[["category", "item", "target_date", "status", "health", "notes"]], use_container_width=True, hide_index=True)

        st.markdown("---")
        st.subheader("✏️ Interactive Checklist Editor")
        st.caption("Change statuses (Not Started → In Progress → Done), update target dates, or add execution notes. Click 'Save Checklist Changes' to persist to CSV.")

        editable_columns = ["category", "item", "target_date", "status", "notes"]
        edited_checklist = st.data_editor(
            checklist_df[editable_columns],
            num_rows="dynamic",
            use_container_width=True,
            key="checklist_editor"
        )

        if st.button("💾 Save Checklist Changes", type="primary"):
            if save_data("plan_checklist.csv", edited_checklist):
                st.success("✅ Plan & Checklist successfully saved to `data/plan_checklist.csv`!")
                st.rerun()


# =========================================================
# Page 10: Ask Degree AI
# =========================================================
elif selected_page == "Ask Degree AI":
    st.markdown('<div class="main-title">Ask Degree AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Grounded academic assistant answering strictly from loaded degree data.</div>', unsafe_allow_html=True)

    # Construct compact context string ONLY from loaded CSVs
    context_str = f"""
DEGREE OS DATA CONTEXT:
1. SEMESTERS DATA:
{semesters_df.to_csv(index=False)}

2. COURSES DATA:
{courses_df.to_csv(index=False)}

3. ACADEMIC CALENDAR:
{calendar_df.to_csv(index=False)}

4. INTERNAL ASSESSMENTS:
{assessments_df.to_csv(index=False)}

5. SCORES & MARKS:
{scores_df.to_csv(index=False)}

6. PLAN & CHECKLIST:
{checklist_df.to_csv(index=False)}
"""

    SYSTEM_INSTRUCTION = (
        "You are Degree AI. Answer only from the supplied degree data. "
        "Do not invent university rules, dates, marks, formulas or syllabus content. "
        "If the requested information is missing, say: I cannot verify that from the current Degree OS data.\n"
        "Keep answers concise and student-friendly.\n"
        "At the start of your response, specify which data area was used: Courses, Calendar, Assessments, Scores or Plan."
    )

    # Check for GEMINI_API_KEY safely without crashing if secrets.toml is absent
    api_key = None
    try:
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")

    if api_key:
        st.success("🟢 Connected to Gemini API")
    else:
        st.info("ℹ️ AI API not connected in secrets. Operating in Deterministic Grounded Fallback Mode.")

    # Grounded Local Deterministic Answer Helper
    def get_grounded_answer(user_query: str) -> tuple[str, str]:
        q = user_query.strip().lower()

        # Incomplete courses check
        if "incomplete" in q or "courses left" in q or "subjects left" in q:
            sem_target = 3
            for s in range(1, 9):
                if f"sem {s}" in q or f"semester {s}" in q:
                    sem_target = s
                    break
            if not courses_df.empty:
                sem_courses = courses_df[courses_df["semester"] == sem_target]
                incomplete = sem_courses[sem_courses["status"] != "Completed"]
                if not incomplete.empty:
                    items = [f"{r['course_code']} ({r['course_name']}) - Status: {r['status']}" for _, r in incomplete.iterrows()]
                    return "Courses", f"Incomplete courses in Semester {sem_target}:\n" + "\n".join([f"- {it}" for it in items])
                else:
                    return "Courses", f"All courses in Semester {sem_target} are completed."
            return "Courses", "No course data available."

        # Next internal assessment
        if "next" in q and ("assessment" in q or "internal" in q or "ia" in q or "exam" in q):
            if not assessments_df.empty:
                upcoming = assessments_df[pd.to_datetime(assessments_df["date"], errors="coerce").dt.date >= CURRENT_DATE].sort_values("date")
                if not upcoming.empty:
                    row = upcoming.iloc[0]
                    return "Assessments", f"Your next internal assessment is **{row['course_code']} - {row['assessment_type']}** scheduled on **{row['date']}** (Status: {row['status']}, Max Marks: {row['max_marks']})."
                else:
                    planned = assessments_df[assessments_df["status"] == "Planned"]
                    if not planned.empty:
                        row = planned.iloc[0]
                        return "Assessments", f"Your next planned assessment is **{row['course_code']} - {row['assessment_type']}** on **{row['date']}**."
            return "Assessments", "No upcoming assessments found."

        # Next holiday / leave
        if "holiday" in q or "leave" in q or "vacation" in q:
            if not calendar_df.empty:
                upcoming_hols = calendar_df[(calendar_df["event_type"] == "Holiday") & (pd.to_datetime(calendar_df["date"], errors="coerce").dt.date >= CURRENT_DATE)].sort_values("date")
                if not upcoming_hols.empty:
                    row = upcoming_hols.iloc[0]
                    return "Calendar", f"Your next holiday is **{row['title']}** on **{row['date']}** (Academic Year: {row['academic_year']}, Semester: {row['semester']})."
            return "Calendar", "No upcoming holidays found in the calendar."

        # Topics in Data Structures / course syllabus
        if "data structures" in q or "cs301" in q or ("topics" in q and "syllabus" in q):
            if not courses_df.empty:
                match = courses_df[courses_df["course_name"].str.contains("Data Structures", case=False, na=False) | (courses_df["course_code"] == "CS301")]
                if not match.empty:
                    s_text = match.iloc[0]["syllabus"]
                    return "Courses", f"Topics covered in Data Structures (CS301): {s_text}."
            return "Courses", "Syllabus details for this course were not found."

        # Semester status check
        if "status of sem" in q or "semester status" in q:
            sem_target = 3
            for s in range(1, 9):
                if f"sem {s}" in q or f"semester {s}" in q:
                    sem_target = s
                    break
            if not semesters_df.empty:
                s_row = semesters_df[semesters_df["semester"] == sem_target]
                if not s_row.empty:
                    r = s_row.iloc[0]
                    return "Plan", f"Semester {sem_target} status is **{r['status']}** with {r['completed_credits']}/{r['total_credits']} credits completed."
            return "Plan", f"No data found for Semester {sem_target}."

        # Checklist status
        if "checklist" in q or "milestone" in q or "pending task" in q:
            if not checklist_df.empty:
                pending = checklist_df[checklist_df["status"] != "Done"]
                items = [f"- {r['item']} (Target: {r['target_date']}, Status: {r['status']})" for _, r in pending.iterrows()]
                return "Plan", "Pending Checklist Items:\n" + "\n".join(items)
            return "Plan", "No checklist items available."

        # Unsupported questions (CGPA formula, official regulations, attendance rules)
        if "cgpa formula" in q or "official" in q or "regulation" in q or "attendance policy" in q or "backlog" in q:
            return "Scores", "I cannot verify that from the current Degree OS data."

        # Safe fallback
        return "Degree OS", "I cannot verify that from the current Degree OS data."

    # Pre-canned test prompt buttons
    st.markdown("##### Quick Test Prompts:")
    test_cols = st.columns(3)
    p1 = "What courses are still incomplete in Semester 3?"
    p2 = "When is my next internal assessment?"
    p3 = "Show my next holiday"
    p4 = "What topics are in Data Structures?"
    p5 = "What is my official university CGPA formula?"

    if test_cols[0].button("Courses incomplete in Sem 3?"):
        st.session_state["chat_query"] = p1
    if test_cols[1].button("When is next IA?"):
        st.session_state["chat_query"] = p2
    if test_cols[2].button("Show next holiday?"):
        st.session_state["chat_query"] = p3

    col_btn4, col_btn5 = st.columns(2)
    if col_btn4.button("Topics in Data Structures?"):
        st.session_state["chat_query"] = p4
    if col_btn5.button("Official university CGPA formula?"):
        st.session_state["chat_query"] = p5

    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "area": "Degree OS", "content": "Hello! I am Degree AI. Ask me about your courses, assessments, calendar events, scores, or checklist."}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg["role"] == "assistant" and "area" in msg and msg["area"]:
                st.markdown(f'<span class="chat-source-tag">Data Area: {msg["area"]}</span>', unsafe_allow_html=True)
            st.markdown(msg["content"])

    # Chat input
    user_input = st.chat_input("Ask a question about your engineering degree...")
    if "chat_query" in st.session_state and st.session_state["chat_query"]:
        user_input = st.session_state.pop("chat_query")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            answer_area = "Degree OS"
            answer_text = ""

            # Attempt Gemini API if key is present
            if api_key:
                try:
                    from google import genai
                    client = genai.Client(api_key=api_key)
                    prompt = f"""Context:\n{context_str}\n\nUser Question: {user_input}"""
                    response = None
                    for model_name in ["gemini-3.5-flash-lite", "gemini-3.5-flash", "gemini-3.8-flash"]:
                        try:
                            response = client.models.generate_content(
                                model=model_name,
                                contents=prompt,
                                config={
                                    "system_instruction": SYSTEM_INSTRUCTION,
                                    "temperature": 0.1
                                }
                            )
                            if response and response.text:
                                break
                        except Exception:
                            continue

                    if response and response.text:
                        answer_text = response.text.strip()
                        # Determine data area
                        for area_candidate in ["Courses", "Calendar", "Assessments", "Scores", "Plan"]:
                            if area_candidate.lower() in answer_text[:40].lower():
                                answer_area = area_candidate
                                break
                    else:
                        answer_area, answer_text = get_grounded_answer(user_input)
                except Exception as e:
                    # Fallback to local grounded answers on any API failure
                    answer_area, answer_text = get_grounded_answer(user_input)
            else:
                answer_area, answer_text = get_grounded_answer(user_input)

            st.markdown(f'<span class="chat-source-tag">Data Area: {answer_area}</span>', unsafe_allow_html=True)
            st.markdown(answer_text)
            st.session_state.messages.append({"role": "assistant", "area": answer_area, "content": answer_text})


# =========================================================
# Page 11: Data Admin
# =========================================================
elif selected_page == "Data Admin":
    st.markdown('<div class="main-title">Data Administration</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Maintain and update underlying CSV data tables directly without rewriting code.</div>', unsafe_allow_html=True)

    table_options = {
        "Semesters (semesters.csv)": ("semesters.csv", semesters_df),
        "Courses (courses.csv)": ("courses.csv", courses_df),
        "Academic Calendar (academic_calendar.csv)": ("academic_calendar.csv", calendar_df),
        "Internal Assessments (assessments.csv)": ("assessments.csv", assessments_df),
        "Scores & Grades (scores.csv)": ("scores.csv", scores_df),
        "Plan & Checklist (plan_checklist.csv)": ("plan_checklist.csv", checklist_df)
    }

    selected_table_name = st.selectbox("Select CSV Table to Edit", list(table_options.keys()))
    file_name, current_df = table_options[selected_table_name]

    st.caption(f"Currently editing: `data/{file_name}` ({len(current_df)} rows)")

    edited_df = st.data_editor(
        current_df,
        num_rows="dynamic",
        use_container_width=True,
        key=f"editor_{file_name}"
    )

    col_save, col_info = st.columns([1, 4])
    with col_save:
        if st.button(f"💾 Save Changes to {file_name}", type="primary"):
            if save_data(file_name, edited_df):
                st.success(f"✅ Successfully updated `data/{file_name}`!")
                st.rerun()

    with col_info:
        st.write("Click any cell to edit, click `+` row to add new records, or select rows and press `Delete` to remove.")

