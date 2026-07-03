conversation_context = {}


def store_message(phone, role, content):

    if phone not in conversation_context:
        conversation_context[phone] = []

    conversation_context[phone].append({
        "role": role,
        "content": content
    })

    conversation_context[phone] = conversation_context[phone][-6:]
    print(conversation_context)
def get_history(phone):

    return conversation_context.get(phone, [])

