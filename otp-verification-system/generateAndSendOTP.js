const AWS = require('aws-sdk');
const db = new AWS.DynamoDB.DocumentClient({
  region: 'ap-south-1',
});
const ses = new AWS.SES();
const sns = new AWS.SNS({
  region: 'us-east-1',
});

exports.handler = async (event, context) => {
  const params = {
    TableName: 'OTPs',
    Key: {
      "email" : event.email,
    },
  };
  try {
    const found = await db.get(params).promise();
    if(found.Item){
      if(found.Item.expiry < Math.floor(Date.now()/1000)) {
        await generateAndSendOTP(event.email, event.phone, 0);
        context.succeed("Done!");
        return "OTP successfully sent to your email and phone!";
      } else if(found.Item.tries < 3) {
        await generateAndSendOTP(event.email, event.phone, found.Item.tries+1);
        context.succeed("Done!");
        return "OTP successfully sent to your email and phone!";
      } else {
        return "You have reached the maximum limit of requesting OTPs";
      }
    }
    else{
      await generateAndSendOTP(event.email, event.phone, 0);
      context.succeed("Done!");
      return "OTP successfully sent to your email and phone!";
    }
  } catch(err) {
    console.log(err);
    return "Some error occurred, please try again";
  }
};

const generateAndSendOTP = async (email,phone, currentTries) => {
  const OTP = Math.floor(Math.random() * 8999) + 1000;
  const otpParams = {
    TableName: 'OTPs',
    Item: {
      "email" : email,
      "phone" : phone,
      "otp" : OTP,
      "expiry" : Math.floor(Date.now()/1000)+300,
      "tries" : currentTries,
    },
  };
  const emailParams = {
    Destination: { 
      ToAddresses: [
        email,
      ]
    },
    Message: {
      Body: { 
        Text: {
         Charset: "UTF-8",
         Data: `Your OTP is : ${OTP}`,
        },
       },
       Subject: {
        Charset: 'UTF-8',
        Data: 'Your OTP'
       }
      },
    Source: 'gunashekherproddatoori@gmail.com',
  };
  await ses.sendEmail(emailParams).promise();
  await sns.setSMSAttributes({"DefaultSMSType" : "Transactional"}).promise();
  const snsParams = {
    Message: `Your OTP is ${OTP}`,
    PhoneNumber: phone,
  };
  await sns.publish(snsParams).promise();
  
  await db.put(otpParams).promise();
}
