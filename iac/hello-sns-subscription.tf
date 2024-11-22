resource "aws_sns_topic_subscription" "hello_active_http_subscription" {
  topic_arn = aws_sns_topic.hello_topic.arn
  protocol  = "https"
  endpoint  = "${var.service_url}/hello"

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.hello_topic_dlq.arn
  })

  delivery_policy = jsonencode({
    healthyRetryPolicy: {
      numRetries       : 2,       # Retry up to 2 times
      minDelayTarget   : 2,       # Minimum delay of 2 seconds
      maxDelayTarget   : 10,      # Maximum delay of 10 seconds
      numMaxDelayRetries : 1,     # Retry 1 time at max delay
      backoffFunction  : "linear" # Use linear backoff for predictable delays
    }
  })
}