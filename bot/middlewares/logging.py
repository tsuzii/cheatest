from __future__ import annotations
from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware
from loguru import logger

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from aiogram.types import CallbackQuery, ChatMemberUpdated, InlineQuery, Message, PreCheckoutQuery, TelegramObject


class LoggingMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.logger = logger
        super().__init__()

    def process_message(self, message: Message) -> dict[str, Any]:
        print_attrs: dict[str, Any] = {"chat_type": message.chat.type}

        if message.from_user:
            print_attrs["user_id"] = message.from_user.id
        if message.text:
            print_attrs["text"] = message.text
        if message.video:
            print_attrs["caption"] = message.caption
            print_attrs["caption_entities"] = message.caption_entities
            print_attrs["video_id"] = message.video.file_id
            print_attrs["video_unique_id"] = message.video.file_unique_id
        if message.audio:
            print_attrs["duration"] = message.audio.duration
            print_attrs["file_size"] = message.audio.file_size
        if message.photo:
            print_attrs["caption"] = message.caption
            print_attrs["caption_entities"] = message.caption_entities
            print_attrs["photo_id"] = message.photo[-1].file_id
            print_attrs["photo_unique_id"] = message.photo[-1].file_unique_id

        return print_attrs

    def process_callback_query(self, callback_query: CallbackQuery) -> dict[str, Any]:
        print_attrs: dict[str, Any] = {
            "query_id": callback_query.id,
            "data": callback_query.data,
            "user_id": callback_query.from_user.id,
            "inline_message_id": callback_query.inline_message_id,
        }

        if callback_query.message:
            print_attrs["message_id"] = callback_query.message.message_id
            print_attrs["chat_type"] = callback_query.message.chat.type
            print_attrs["chat_id"] = callback_query.message.chat.id

        return print_attrs

    def process_inline_query(self, inline_query: InlineQuery) -> dict[str, Any]:
        print_attrs: dict[str, Any] = {
            "query_id": inline_query.id,
            "user_id": inline_query.from_user.id,
            "query": inline_query.query,
            "offset": inline_query.offset,
            "chat_type": inline_query.chat_type,
            "location": inline_query.location,
        }

        return print_attrs

    def process_pre_checkout_query(self, pre_checkout_query: PreCheckoutQuery) -> dict[str, Any]:
        print_attrs: dict[str, Any] = {
            "query_id": pre_checkout_query.id,
            "user_id": pre_checkout_query.from_user.id,
            "currency": pre_checkout_query.currency,
            "amount": pre_checkout_query.total_amount,
            "payload": pre_checkout_query.invoice_payload,
            "option": pre_checkout_query.shipping_option_id,
        }

        return print_attrs

    def process_my_chat_member(self, my_chat_member: ChatMemberUpdated) -> dict[str, Any]:
        print_attrs: dict[str, Any] = {
            "user_id": my_chat_member.from_user.id,
            "chat_id": my_chat_member.chat.id,
        }

        return print_attrs

    def process_chat_member(self, chat_member: ChatMemberUpdated) -> dict[str, Any]:
        print_attrs: dict[str, Any] = {
            "user_id": chat_member.from_user.id,
            "chat_id": chat_member.chat.id,
            "old_state": chat_member.old_chat_member,
            "new_state": chat_member.new_chat_member,
        }

        return print_attrs

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        print_attrs: dict[str, Any] = {}
        message: Message | None = getattr(event, "message", None)
        callback_query: CallbackQuery | None = getattr(event, "callback_query", None)
        inline_query: InlineQuery | None = getattr(event, "inline_query", None)
        pre_checkout_query: PreCheckoutQuery | None = getattr(event, "pre_checkout_query", None)
        my_chat_member: ChatMemberUpdated | None = getattr(event, "my_chat_member", None)
        chat_member: ChatMemberUpdated | None = getattr(event, "chat_member", None)

        if message:
            print_attrs = self.process_message(message)

            logger_msg = (
                "received message | "
                + " | ".join(f"{key}: {value}" for key, value in print_attrs.items() if value is not None),
            )
            self.logger.info(*logger_msg)
        elif callback_query:
            print_attrs = self.process_callback_query(callback_query)

            logger_msg = (
                "received callback query | "
                + " | ".join(f"{key}: {value}" for key, value in print_attrs.items() if value is not None),
            )
            self.logger.info(*logger_msg)
        elif inline_query:
            print_attrs = self.process_inline_query(inline_query)

            logger_msg = (
                "received inline query | "
                + " | ".join(f"{key}: {value}" for key, value in print_attrs.items() if value is not None),
            )
            self.logger.info(*logger_msg)
        elif pre_checkout_query:
            print_attrs = self.process_pre_checkout_query(pre_checkout_query)

            logger_msg = (
                "received pre-checkout query | "
                + " | ".join(f"{key}: {value}" for key, value in print_attrs.items() if value is not None),
            )
            self.logger.info(*logger_msg)
        elif my_chat_member:
            print_attrs = self.process_my_chat_member(my_chat_member)

            logger_msg = (
                "received my chat member update | "
                + " | ".join(f"{key}: {value}" for key, value in print_attrs.items() if value is not None),
            )
            self.logger.info(*logger_msg)
        elif chat_member:
            print_attrs = self.process_chat_member(chat_member)

            logger_msg = (
                "received chat member update | "
                + " | ".join(f"{key}: {value}" for key, value in print_attrs.items() if value is not None),
            )
            self.logger.info(*logger_msg)

        return await handler(event, data)
