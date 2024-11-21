# IAM Role for EventBridge Scheduler to publish to SNS
resource "aws_iam_role" "scheduler_to_sns_role" {
  name = "scheduler-to-sns-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "scheduler.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# Policy for allowing EventBridge Scheduler to publish to the SNS topic
resource "aws_iam_role_policy" "scheduler_to_sns_policy" {
  name = "scheduler-to-sns-policy"
  role = aws_iam_role.scheduler_to_sns_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "sns:Publish"
        Resource = aws_sns_topic.scheduled_topic.arn
      }
    ]
  })
}