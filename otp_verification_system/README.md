## OTP Verification System
Your are required to build an OTP verfication System.

### Requirements:
- There should be four API's
1) To send otp to mobile number.
2) To send otp to email address.
3) To verify the received otp.
4) To resend otp allowing atmost 3 retries.
- There should be expiry of timeout of 5 minutes, after which the otp will expire.

### Suggested AWS services
API gateway( To expose API endpoints), DynamoDb(Please look into timeout feature of it to set expire timeout),
Lambdas, SNS.
PS: For sending messages to mobile number, ensure you are sending transactional message instead of promotional message.

### Contributions Guidelines
- Create folder with your name.
- Add your files(lambdas) in the folder.
