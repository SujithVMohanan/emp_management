

def get_error_message(error):
    if hasattr(error, "messages"):
        return " ".join(error.messages)
    return str(error)