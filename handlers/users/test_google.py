import pyotp
totp = pyotp.TOTP('6R2FXEVVYXBYERDA')
jopa = totp.now()
print("Current OTP:", jopa, type(jopa))
print(totp.verify(jopa))
