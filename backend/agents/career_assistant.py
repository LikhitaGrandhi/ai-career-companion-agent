# =========================================================
# AI CAREER ASSISTANT
# =========================================================

def detect_intent(question):
    """
    Detect the main intent of the user's question.
    """

    question_lower = question.lower()

    # Skill gap
    if any(word in question_lower for word in [
        "skill gap",
        "missing skill",
        "missing skills",
        "skills am i missing",
        "what skills do i need",
        "skills should i learn",
        "improve my skills"
    ]):
        return "skill_gap"

    # Internship
    if any(word in question_lower for word in [
        "internship",
        "internships",
        "job",
        "jobs",
        "opportunities",
        "which role",
        "which roles"
    ]):
        return "internship"

    # Resume
    if any(word in question_lower for word in [
        "resume",
        "cv",
        "curriculum vitae"
    ]):
        return "resume"

    # Interview
    if any(word in question_lower for word in [
        "interview",
        "interviews",
        "interview preparation",
        "prepare for interview",
        "prepare me"
    ]):
        return "interview"

    # Cover letter
    if any(word in question_lower for word in [
        "cover letter",
        "coverletter"
    ]):
        return "cover_letter"

    # General career question
    return "general"


# =========================================================
# CONVERSATION CONTEXT
# =========================================================

def get_recent_context(conversation_history):
    """
    Convert previous conversation messages into
    a simple text context.
    """

    if not conversation_history:
        return ""

    recent_messages = conversation_history[-6:]

    context_lines = []

    for message in recent_messages:

        if hasattr(message, "role"):
            role = message.role
            text = message.message
        else:
            role = message.get("role", "")
            text = message.get("message", "")

        context_lines.append(
            f"{role}: {text}"
        )

    return "\n".join(context_lines)


def is_follow_up_question(question):
    """
    Detect questions that depend on previous conversation.
    """

    question_lower = question.lower().strip()

    follow_up_phrases = [
        "what about it",
        "what about that",
        "how about it",
        "how about that",
        "tell me more",
        "explain more",
        "what should i do",
        "what should i learn",
        "how can i improve",
        "how do i improve",
        "how should i prepare",
        "what about the first one",
        "what about the second one",
        "the first one",
        "the second one",
        "that internship",
        "that role",
        "that job",
        "this internship",
        "this role",
        "this job",
        "for it",
        "for that"
    ]

    return any(
        phrase in question_lower
        for phrase in follow_up_phrases
    )


# =========================================================
# INTERNSHIP RESPONSE
# =========================================================

def generate_internship_response(jobs):

    if not jobs:
        return (
            "I could not find suitable internship matches "
            "from your current profile."
        )

    response = "Based on your profile, here are some relevant internship matches:\n\n"

    for index, job in enumerate(jobs[:5], start=1):

        title = job.get(
            "job_title",
            job.get("title", "Unknown Role")
        )

        company = job.get(
            "company",
            "Unknown Company"
        )

        location = job.get(
            "location",
            "Location not specified"
        )

        score = job.get(
            "match_score",
            job.get("similarity_score", 0)
        )

        response += (
            f"{index}. {title} - {company}\n"
            f"   Location: {location}\n"
            f"   Match Score: {round(float(score), 2)}\n\n"
        )

    response += (
        "You can ask me about the skills required for any "
        "of these internships."
    )

    return response


# =========================================================
# SKILL GAP RESPONSE
# =========================================================

def generate_skill_gap_response(skill_gap_results):

    if not skill_gap_results:
        return (
            "I could not generate a skill-gap analysis "
            "for your current profile."
        )

    response = (
        "Here is the skill-gap analysis based on the "
        "available internship roles:\n\n"
    )

    for index, result in enumerate(
        skill_gap_results[:5],
        start=1
    ):

        job_title = result.get(
            "job_title",
            result.get("title", "Internship Role")
        )

        company = result.get(
            "company",
            ""
        )

        missing_skills = result.get(
            "missing_skills",
            []
        )

        critical_gaps = result.get(
            "critical_gaps",
            []
        )

        preferred_gaps = result.get(
            "preferred_gaps",
            []
        )

        response += (
            f"{index}. {job_title}"
        )

        if company:
            response += f" - {company}"

        response += "\n"

        if missing_skills:
            response += (
                f"   Missing skills: "
                f"{', '.join(map(str, missing_skills))}\n"
            )
        else:
            response += (
                "   Missing skills: No major missing skills identified.\n"
            )

        if critical_gaps:
            response += (
                f"   Critical gaps: "
                f"{', '.join(map(str, critical_gaps))}\n"
            )

        if preferred_gaps:
            response += (
                f"   Preferred gaps: "
                f"{', '.join(map(str, preferred_gaps))}\n"
            )

        response += "\n"

    response += (
        "Focus first on the critical skills, then work on "
        "preferred skills through projects and practice."
    )

    return response


# =========================================================
# RESUME RESPONSE
# =========================================================

def generate_resume_response(student):

    skills = student.get(
        "skills",
        []
    )

    projects = student.get(
        "projects",
        []
    )

    response = (
        "Your resume should clearly highlight your education, "
        "technical skills, projects, experience and certifications.\n\n"
    )

    if skills:
        response += (
            "Your current technical skills include: "
            f"{', '.join(map(str, skills))}\n\n"
        )

    if projects:
        response += (
            "Your projects should include measurable details "
            "such as technologies used, features implemented "
            "and your contribution.\n\n"
        )

    response += (
        "For an internship-focused resume, keep the content "
        "relevant to the role and avoid adding skills or "
        "achievements that are not actually present in your profile."
    )

    return response


# =========================================================
# INTERVIEW RESPONSE
# =========================================================

def generate_interview_response():

    return (
        "For internship interview preparation, focus on four areas:\n\n"
        "1. Technical fundamentals related to the role.\n"
        "2. Questions based on your projects.\n"
        "3. Problem-solving and coding practice.\n"
        "4. HR questions such as introduction, strengths, "
        "career goals and project experience.\n\n"
        "You should also be able to clearly explain every "
        "technology and project mentioned in your resume."
    )


# =========================================================
# COVER LETTER RESPONSE
# =========================================================

def generate_cover_letter_response(student):

    name = student.get(
        "name",
        "the candidate"
    )

    return (
        f"A cover letter for {name} should briefly explain "
        "your interest in the internship, relevant technical "
        "skills, projects or experience, and why your background "
        "matches the role.\n\n"
        "Keep it specific to the internship and avoid adding "
        "experiences or achievements that are not present in "
        "your profile."
    )


# =========================================================
# GENERAL RESPONSE
# =========================================================

def generate_general_response(
    question,
    student,
    conversation_history=None
):

    context = get_recent_context(
        conversation_history
    )

    # -----------------------------------------------------
    # Context-aware follow-up
    # -----------------------------------------------------

    if context and is_follow_up_question(question):

        return (
            "Based on our previous conversation, "
            "your question is related to the career "
            "information we discussed earlier.\n\n"
            f"Your current question is: {question}\n\n"
            "You can continue by asking me specifically "
            "about the internship, skills, resume, "
            "cover letter or interview preparation."
        )

    # -----------------------------------------------------
    # General career response
    # -----------------------------------------------------

    return (
        "I can help you with:\n\n"
        "• Internship matching\n"
        "• Skill-gap analysis\n"
        "• Resume improvement\n"
        "• Cover letters\n"
        "• Interview preparation\n"
        "• Career planning\n\n"
        "Ask me a specific question about your career "
        "or internship preparation."
    )


# =========================================================
# MAIN CAREER ASSISTANT
# =========================================================

def answer_career_question(
    question,
    student,
    jobs=None,
    skill_gap_results=None,
    conversation_history=None
):

    if jobs is None:
        jobs = []

    if skill_gap_results is None:
        skill_gap_results = []

    if conversation_history is None:
        conversation_history = []

    # -----------------------------------------------------
    # Detect intent
    # -----------------------------------------------------

    intent = detect_intent(question)

    # -----------------------------------------------------
    # Context-aware follow-up
    # -----------------------------------------------------

    if is_follow_up_question(question):

        previous_context = get_recent_context(
            conversation_history
        )

        if previous_context:

            question_lower = question.lower()

            # Follow-up about skills
            if any(word in question_lower for word in [
                "skill",
                "skills",
                "learn",
                "improve"
            ]):

                intent = "skill_gap"

            # Follow-up about interview
            elif any(word in question_lower for word in [
                "prepare",
                "preparation",
                "interview"
            ]):

                intent = "interview"

            # Follow-up about resume
            elif any(word in question_lower for word in [
                "resume",
                "cv"
            ]):

                intent = "resume"

            # Follow-up about internship/job
            elif any(word in question_lower for word in [
                "internship",
                "role",
                "job"
            ]):

                intent = "internship"

    # -----------------------------------------------------
    # Generate response
    # -----------------------------------------------------

    if intent == "internship":

        response = generate_internship_response(
            jobs
        )

    elif intent == "skill_gap":

        response = generate_skill_gap_response(
            skill_gap_results
        )

    elif intent == "resume":

        response = generate_resume_response(
            student
        )

    elif intent == "interview":

        response = generate_interview_response()

    elif intent == "cover_letter":

        response = generate_cover_letter_response(
            student
        )

    else:

        response = generate_general_response(
            question=question,
            student=student,
            conversation_history=conversation_history
        )

    # -----------------------------------------------------
    # Return result
    # -----------------------------------------------------

    return {
        "intent": intent,
        "response": response
    }