from functools import wraps


def send_action(action):
    def decorator(func):
        @wraps(func)
        def decorated_function(update, context, *args, **kwargs):
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(update, context, *args, **kwargs)
        return decorated_function
    return decorator
