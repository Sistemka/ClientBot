from telegram.bot import Bot
from telegram.ext import messagequeue as mq


class MQBot(Bot):
    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or mq.MessageQueue()

    def __del__(self):
        try:
            self._msg_queue.stop()
        except BaseException:
            pass

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        return super(MQBot, self).send_message(*args, **kwargs)

    @mq.queuedmessage
    def send_photo(self, *args, **kwargs):
        return super(MQBot, self).send_photo(*args, **kwargs)

    @mq.queuedmessage
    def delete_message(self, *args, **kwargs):
        return super(MQBot, self).delete_message(*args, **kwargs)

    @mq.queuedmessage
    def forward_message(self, *args, **kwargs):
        return super(MQBot, self).forward_message(*args, **kwargs)

    @mq.queuedmessage
    def answer_callback_query(self, *args, **kwargs):
        return super(MQBot, self).answer_callback_query(*args, **kwargs)

    @mq.queuedmessage
    def send_chat_action(self, *args, **kwargs):
        return super(MQBot, self).send_chat_action(*args, **kwargs)
