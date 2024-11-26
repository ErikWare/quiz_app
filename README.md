# SAFe Product Owner/Product Manager Certification Test Application

Welcome to the **SAFe Product Owner/Product Manager Certification Test Application**! This tool is designed to help you prepare effectively for the SAFe (Scaled Agile Framework) Product Owner/Product Manager certification (version 6.0) by providing comprehensive and challenging practice questions based on key lessons of the curriculum.

## Table of Contents
1. [Overview of SAFe Lessons 1-5](#overview-of-safe-lessons-15)
    - [Lesson 1: Introduction to SAFe](#lesson-1-introduction-to-safe)
    - [Lesson 2: [Lesson 2 Title]](#lesson-2-lesson-2-title)
    - [Lesson 3: Leadership for PI Planning](#lesson-3-leadership-for-pi-planning)
    - [Lesson 4: Iteration Execution](#lesson-4-iteration-execution)
    - [Lesson 5: PI Execution](#lesson-5-pi-execution)
2. [Question Sets Created](#question-sets-created)
    - [Lesson 2: [Lesson 2 Topics]](#lesson-2-lesson-2-topics)
    - [Lesson 3: Leadership for PI Planning](#lesson-3-leadership-for-pi-planning)
    - [Lesson 4: Iteration Execution](#lesson-4-iteration-execution)
    - [Lesson 5: PI Execution](#lesson-5-pi-execution)
3. [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Steps](#steps)
4. [How to Use the Application](#how-to-use-the-application)
5. [JSON Structure](#json-structure)
6. [Study Tips](#study-tips)
7. [Next Steps](#next-steps)
8. [Conclusion](#conclusion)
9. [License](#license)
10. [Contact](#contact)
11. [Acknowledgments](#acknowledgments)

---

## Overview of SAFe Lessons 1-5

### Lesson 1: Introduction to SAFe

*Note: This lesson provides foundational knowledge of the SAFe framework, including its principles, values, roles, and the structure of Agile Release Trains (ARTs).*

- **Key Topics:**
  - Overview of the SAFe framework
  - SAFe principles and values
  - Roles and responsibilities within SAFe
  - Introduction to Agile Release Trains (ARTs)

### Lesson 2: [Lesson 2 Title]

*Note: Replace `[Lesson 2 Title]` with the actual title of Lesson 2.*

- **Key Topics:**
  - [Topic 1]
  - [Topic 2]
  - [Topic 3]
  - ...

### Lesson 3: Leadership for PI Planning

- **Key Topics:**
  1. **The Vision and PI Planning**
     - Establishing and communicating the program vision
     - Aligning team objectives with the vision
  2. **PI Objectives**
     - Defining measurable PI Objectives
     - Aligning objectives with business goals
  3. **Agile Release Train (ART) Planning Board and Dependencies**
     - Visualizing work and managing dependencies
     - Utilizing Kanban boards for backlog management
  4. **Risks and the End of PI Planning**
     - Identifying and mitigating risks
     - Finalizing plans and ensuring alignment

### Lesson 4: Iteration Execution

- **Key Topics:**
  1. **Stories and Story Maps**
     - Creating and organizing user stories
     - Utilizing story maps for visualizing user journeys
  2. **Iteration Planning**
     - Selecting and committing to user stories
     - Defining iteration goals and objectives
  3. **The Team Kanban**
     - Managing workflow and Work in Progress (WIP)
     - Identifying and addressing bottlenecks
  4. **Backlog Refinement**
     - Prioritizing and clarifying backlog items
     - Estimating effort and defining acceptance criteria
  5. **Iteration Review and Iteration Retrospective**
     - Demonstrating completed work
     - Reflecting on the iteration and identifying improvements
  6. **DevOps and Release on Demand**
     - Implementing DevOps practices
     - Enabling flexible and continuous releases

### Lesson 5: PI Execution

- **Key Topics:**
  1. **PO Sync**
     - Synchronizing Product Owners and aligning backlogs
     - Managing dependencies and progress towards PI Objectives
  2. **System Demo**
     - Demonstrating integrated work across teams
     - Gathering stakeholder feedback
  3. **The Innovation and Planning Iteration**
     - Allocating time for innovation, learning, and planning
     - Addressing technical debt and conducting team training
  4. **Inspect and Adapt (I&A)**
     - Reviewing PI performance
     - Conducting Problem-Solving Workshops
     - Developing and implementing improvement plans

## Question Sets Created

### Lesson 2: [Lesson 2 Topics]

*Note: Replace `[Lesson 2 Topics]` with the specific topics covered in Lesson 2.*

- **Topics Covered:**
  1. [Topic 1]
  2. [Topic 2]
  3. [Topic 3]
  4. ...

- **Question Set:**
  - **File:** `lesson_2.json`
  - **Number of Questions:** 50
  - **Format:** JSON
  - **Description:** Comprehensive questions covering the key topics of Lesson 2 to test your understanding and application of SAFe principles.

### Lesson 3: Leadership for PI Planning

- **Topics Covered:**
  1. The Vision and PI Planning
  2. PI Objectives
  3. Agile Release Train Planning Board and Dependencies
  4. Risks and the End of PI Planning

- **Question Set:**
  - **File:** `lesson_3.json`
  - **Number of Questions:** 50
  - **Format:** JSON
  - **Description:** Challenging questions focused on leadership roles, vision alignment, PI Objectives definition, managing dependencies, and risk mitigation during PI Planning.

### Lesson 4: Iteration Execution

- **Topics Covered:**
  1. Stories and Story Maps
  2. Iteration Planning
  3. The Team Kanban
  4. Backlog Refinement
  5. Iteration Review and Iteration Retrospective
  6. DevOps and Release on Demand

- **Question Set:**
  - **File:** `lesson_4.json`
  - **Number of Questions:** 50
  - **Format:** JSON
  - **Description:** In-depth questions on creating and managing user stories, effective iteration planning, utilizing Kanban boards, refining backlogs, conducting reviews and retrospectives, and implementing DevOps practices for release management.

### Lesson 5: PI Execution

- **Topics Covered:**
  1. PO Sync
  2. System Demo
  3. The Innovation and Planning Iteration
  4. Inspect and Adapt

- **Question Set:**
  - **File:** `lesson_5.json`
  - **Number of Questions:** 50
  - **Format:** JSON
  - **Description:** Comprehensive questions on synchronizing Product Owners, conducting system demos, managing innovation and planning iterations, and performing inspect and adapt sessions to drive continuous improvement.

## Installation

### Prerequisites

- **Python 3.x**: Ensure you have Python installed. You can download it from the [official website](https://www.python.org/downloads/).
- **Tkinter Library**: Tkinter usually comes pre-installed with Python. To verify, you can run the following command:

    ```bash
    python -m tkinter
    ```

    If Tkinter is not installed, you can install it via your package manager. For example, on Debian-based systems:

    ```bash
    sudo apt-get install python3-tk
    ```

### Steps

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/quiz_app.git
    cd quiz_app
    ```

2. **Install Dependencies**

    The application requires certain Python packages. Install them using pip:

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Application**

    Launch the application by executing:

    ```bash
    python quiz_app.py
    ```

## How to Use the Application

1. **Importing Question Sets:**
   - Save the provided JSON files (`lesson_2.json`, `lesson_3.json`, `lesson_4.json`, `lesson_5.json`) into your `/tests` directory within the application.

2. **Selecting a Quiz:**
   - Launch the application and navigate to the quiz selection menu.
   - Choose the desired lesson (e.g., Lesson 3: Leadership for PI Planning) from the dropdown menu.

3. **Starting the Quiz:**
   - Select between "Start Test" for a timed assessment or "Practice Test" for an untimed, self-paced study session.
   - Answer the questions presented, select your answers, and submit the quiz upon completion.

4. **Reviewing Results:**
   - After submission, review your performance summary to identify areas of strength and those needing improvement.
   - Read the provided rationales for each question to deepen your understanding of the concepts.

5. **Retaking Quizzes:**
   - Return to the home screen to retake quizzes or select other lesson quizzes to continue your study.

## JSON Structure

Each question in the JSON files follows a standardized structure to ensure compatibility with the quiz application. Below is an overview of the JSON schema:

- **`id`**: A unique identifier for the question (e.g., "Q1").
- **`type`**: Indicates whether the question is single-choice (`"single"`) or multiple-choice (`"multiple"`).
- **`question`**: The text of the question.
- **`options`**: An array of possible answer choices.
- **`answer`**: An array containing the correct answer(s). For single-choice questions, this array contains one element.
- **`rationale`**: An explanation of why the answer is correct, providing educational value.

### Sample Question Breakdown

```json
{
    "id": "Q1",
    "type": "single",
    "question": "What is the primary purpose of the PO Sync meeting in SAFe?",
    "options": [
        "To assign individual tasks to team members",
        "To synchronize and align Product Owners with the Product Manager and ensure backlog alignment",
        "To conduct performance reviews for team members",
        "To finalize the project budget"
    ],
    "answer": ["To synchronize and align Product Owners with the Product Manager and ensure backlog alignment"],
    "rationale": "The PO Sync meeting is designed to synchronize and align Product Owners with the Product Manager, ensuring that the backlogs are aligned with the program vision and objectives."
}
