# MY ENGINEERING DEGREE OS 🎓

A self-managed 1st-to-8th semester engineering degree command center built with **Python**, **Streamlit**, and **Pandas**, featuring syllabus tracking, assessments, scorecards, degree execution checklists, and **Degree AI** with Gemini API integration and grounded fallback.

---

## 🌟 Key Features

1. **Dashboard:** Central command center displaying current semester, degree completion %, completed credits, next assessment, next holiday, prototype score %, and 8-semester credit progress chart.
2. **Semesters 1-8:** Semester cards with course count, credits, completion status, progress bars, and filterable drill-down views.
3. **Courses & Syllabus:** Comprehensive course list filterable by semester, showing course codes, titles, credits, faculty allocation, status, and modular syllabi.
4. **University Syllabus:** Degree programme structure (B.Tech CSE, 175 Credits), category-wise credit distribution, and official syllabus reference citation field.
5. **Academic / Leave Calendar:** Coexisting institutional calendar tracking academic milestones and holidays, filterable by academic year, semester, and event type.
6. **Internal Assessments:** Date-based tracking for IA1, IA2, assignments, lab evaluations, project reviews, and end-semester exams.
7. **Status Tracker:** Course progression monitor tracking Not Started, In Progress, and Completed courses with visual progress bars.
8. **Scorecard:** Academic performance tracking calculating prototype score percentages and semester averages from score records.
9. **Plan & Checklist:** Degree execution control panel featuring This Week (next 7 days), Semester Milestones, and Degree Milestones with health indicators (Done, Due Soon, Overdue) and in-app CSV editing via `st.data_editor`.
10. **Ask Degree AI:** Grounded student chatbot answering strictly from degree data (Courses, Calendar, Assessments, Scores, Plan) with Gemini API support and deterministic local fallback adhering to safe-AI refusal rules.
11. **Data Admin:** Interactive data administration suite enabling students to inspect, edit, and persist changes to all underlying CSV tables without code modifications.

---

## 📁 Project Structure

```text
Engineering-degree-os/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Project dependencies
├── README.md                   # Project documentation
│
└── data/                       # CSV Data Store
    ├── semesters.csv           # 1st-to-8th semester metadata and credit totals
    ├── courses.csv             # Courses across all 8 semesters with syllabi & faculty
    ├── academic_calendar.csv   # Academic milestones and holidays
    ├── assessments.csv         # IA1, IA2, assignments, labs, project reviews, exams
    ├── scores.csv              # Course marks, maximum marks, and grades
    └── plan_checklist.csv      # Milestone checklist items, target dates, and statuses
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/deepak7-shadow/Engineering-degree-os.git
cd Engineering-degree-os
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 🤖 Ask Degree AI & Gemini API Setup

- For local AI generation, configure your Gemini API key in `.streamlit/secrets.toml`:
  ```toml
  GEMINI_API_KEY="your-gemini-api-key"
  ```
- If no API key is provided, the app operates in **Deterministic Grounded Mode**, accurately answering queries on incomplete courses, upcoming assessments, holidays, course topics, semester status, and checklist items, while safely refusing unverified university regulations.
