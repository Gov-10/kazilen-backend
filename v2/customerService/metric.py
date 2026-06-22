from prometheus_client import Counter, Gauge, Histogram
VERIF_OTP=Counter("verification_otp", "Number of verification otp sent")
OTP_SMS=Counter("otp_sms_sent", "verification sms sent")
OTP_ERRORS=Counter("otp_errors", "otp errors")
