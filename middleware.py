from typing import Any, Awaitable, Callable

import requests
from fastapi import Request

from models import SNSMessage


def sns_message_parse(
    func: Callable[[SNSMessage], Awaitable[Any]],
) -> Callable[[Request], Awaitable[Any]]:
    async def wrapper(request: Request) -> Any:
        message = await request.json()
        print(message)
        sns_message = SNSMessage.model_validate(message)
        if sns_message.Subject == "fail":
            raise Exception("Failing due to subject")
        if sns_message.Type == "SubscriptionConfirmation":
            subscribe_url = sns_message.SubscribeURL
            if subscribe_url:
                response = requests.get(str(subscribe_url))
                return {
                    "message": "Subscription confirmed",
                    "status_code": response.status_code,
                }
        return await func(sns_message)

    return wrapper
