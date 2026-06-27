from prometheus_client import Counter, Gauge, Histogram
OTP_ERRORS=Counter("otp_errors", "OTP errors")
VERIF_OTP=Counter("verification_otps", "Verification otps")
