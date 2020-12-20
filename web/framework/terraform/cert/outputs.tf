# we output the validation cert arn here so that stuff
# waits for the cert to be valid before using it
output "arn" {
  value = aws_acm_certificate_validation.validation.certificate_arn
}
