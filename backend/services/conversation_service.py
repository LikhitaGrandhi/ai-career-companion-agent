from backend.models.conversation import ConversationMessage


# Temporary in-memory conversation storage
_conversations = {}


def get_conversation(student_id: str):
    """
    Get conversation history for a student.
    """
    return _conversations.get(student_id, [])


def add_message(student_id: str, role: str, message: str):
    """
    Add a user or assistant message to the conversation.
    """
    conversation = _conversations.setdefault(student_id, [])

    new_message = ConversationMessage(
        role=role,
        message=message
    )

    conversation.append(new_message)

    return conversation


def clear_conversation(student_id: str):
    """
    Clear conversation history for a student.
    """
    _conversations.pop(student_id, None)