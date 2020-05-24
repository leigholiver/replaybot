
resource "aws_dynamodb_table" "db_table" {
  count        = length(var.tables)
  name         = "${var.project_name}_${var.name}_${var.tables[count.index].name}"
  billing_mode = "PAY_PER_REQUEST"

  # id
  hash_key = "id"
  attribute {
    name = "id"
    type = "S"
  }

  # expiries  
  dynamic "ttl" {
    for_each = var.tables[count.index].expires != "" ? [true] : []
    content {
      attribute_name = "expires"
      enabled        = ttl.value
    }
  }

  # sort key
  dynamic "attribute" {
    for_each = var.tables[count.index].sort_key != "" ? [var.tables[count.index].sort_key] : []
    content {
      name = attribute.value
      type = "S"
    }
  }
  dynamic "attribute" {
    for_each = var.tables[count.index].sort_key != "" ? [var.tables[count.index].sort_key] : []
    content {
      name = "${attribute.value}_index"
      type = "S"
    }
  }
  dynamic "global_secondary_index" {
    for_each = var.tables[count.index].sort_key != "" ? [var.tables[count.index].sort_key] : []
    content {
      name            = "${global_secondary_index.value}_sort"
      hash_key        = "${global_secondary_index.value}_index"
      range_key       = global_secondary_index.value
      projection_type = "ALL"
    }
  }

  # indexes
  dynamic "attribute" {
    for_each = var.tables[count.index].indexes
    content {
      name = attribute.value
      type = "S"
    }
  }
  dynamic "global_secondary_index" {
    for_each = var.tables[count.index].indexes
    content {
      name            = "${global_secondary_index.value}_index"
      hash_key        = global_secondary_index.value
      projection_type = "ALL"
    }
  }
}

resource "aws_iam_policy" "db_policy" {
  count  = length(aws_dynamodb_table.db_table)
  name   = "${aws_dynamodb_table.db_table[count.index].name}_db_policy"
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
        "Sid": "AllAPIActionsOnTable",
        "Effect": "Allow",
        "Action": "dynamodb:*",
        "Resource": "${aws_dynamodb_table.db_table[count.index].arn}"
    }
    %{for i, index in var.tables[count.index].indexes}
      ,
      {
          "Sid": "AllQueryOnIndex${i}",
          "Effect": "Allow",
          "Action": "dynamodb:Query",
          "Resource": "${aws_dynamodb_table.db_table[count.index].arn}/index/${index}_index"
      }
    %{endfor}
    %{if var.tables[count.index].sort_key != ""}
      ,
      {
          "Sid": "AllQueryOnSortKey",
          "Effect": "Allow",
          "Action": "dynamodb:Query",
          "Resource": "${aws_dynamodb_table.db_table[count.index].arn}/index/${var.tables[count.index].sort_key}_sort"
      }
    %{endif}
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "db_attachment" {
  count      = length(aws_dynamodb_table.db_table)
  name       = "${aws_dynamodb_table.db_table[count.index].name}_attachment"
  roles      = ["${var.role.name}"]
  policy_arn = aws_iam_policy.db_policy[count.index].arn
}