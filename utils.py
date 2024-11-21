import uuid
from datetime import datetime, timezone

import boto3  # type: ignore
from fastapi import HTTPException

from settings import HELLO_TOPIC_NAME, ROLE_NAME, SCHEDULED_TOPIC_NAME

iam = boto3.client("iam")  # type: ignore


def get_role_arn(role_name: str) -> str:
    try:
        response = iam.get_role(RoleName=role_name)  # type: ignore
        return response["Role"]["Arn"]  # type: ignore
    except Exception as e:
        raise RuntimeError(f"Unable to retrieve RoleArn: {str(e)}")


def get_topic_arn(topic_name: str) -> str:
    sns = boto3.client("sns")  # type: ignore
    try:
        response = sns.list_topics()  # type: ignore
        for topic in response.get("Topics", []):  # type: ignore
            if topic_name in topic["TopicArn"]:
                return topic["TopicArn"]  # type: ignore
        raise ValueError(f"Topic with name '{topic_name}' not found.")
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve topic ARN: {e}")


def create_scheduled_event(schedule_time: datetime, message: str) -> dict[str, str]:
    scheduler = boto3.client("scheduler")  # type: ignore
    # Generate a unique event ID
    event_id = str(uuid.uuid4())

    # Convert the scheduled time to ISO 8601 format
    schedule_time_iso = schedule_time.astimezone(timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%S"
    )

    try:
        # Create a one-time schedule using EventBridge Scheduler
        scheduler.create_schedule(  # type: ignore
            Name=f"schedule-message-{event_id}",
            ScheduleExpression=f"at({schedule_time_iso})",
            FlexibleTimeWindow={
                "Mode": "OFF",  # Disable time flexibility for one-time schedules
            },
            Target={
                "Arn": get_topic_arn(SCHEDULED_TOPIC_NAME),
                "RoleArn": get_role_arn(ROLE_NAME),
                "Input": f'{{"message": "{message}"}}',
            },
            State="ENABLED",
        )
        return {"status": "success", "message": "Message scheduled successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def publish_message(message: str, subject: str | None) -> dict[str, str]:
    sns = boto3.client("sns")  # type: ignore
    try:
        # Get the topic ARN from its name
        topic_arn = get_topic_arn(HELLO_TOPIC_NAME)

        # Prepare the publish parameters
        publish_params = {
            "TopicArn": topic_arn,
            "Message": message,
        }
        if subject:
            publish_params["Subject"] = subject

        # Publish the message
        response = sns.publish(**publish_params)  # type: ignore
        return response  # type: ignore
    except Exception as e:
        print(f"Failed to publish message: {e}")
        return {"Error": str(e)}
