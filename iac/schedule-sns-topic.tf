resource "aws_sns_topic" "scheduled_topic" {
  name = "${var.environment}_${var.service_name}_scheduled-topic"
}

resource "aws_sqs_queue" "scheduled_topic_dlq" {
    name = "${aws_sns_topic.scheduled_topic.name}_dlq"
}

resource "aws_sqs_queue_policy" "scheduled_topic_dlq_policy" {
  queue_url = aws_sqs_queue.scheduled_topic_dlq.url

  policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = "*"
        Action    = "sqs:SendMessage"
        Resource  = aws_sqs_queue.scheduled_topic_dlq.arn
        Condition = {
          ArnEquals = {
            "aws:SourceArn" = aws_sns_topic.scheduled_topic.arn
          }
        }
      }
    ]
  })
}