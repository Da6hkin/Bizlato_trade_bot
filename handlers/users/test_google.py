import pyotp
totp = pyotp.TOTP('PMLYJHRMPLYF4AHR')
jopa = totp.now()
print("Current OTP:", jopa, type(jopa))
print(totp.verify(jopa))
