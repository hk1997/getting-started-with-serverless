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
        await generateAndSendOTP(event.email, event.phone);
        return "OTP successfully sent to your email and phone!";
      }
      return "You have already requested for an OTP!";
    }
    else{
      await generateAndSendOTP(event.email, event.phone);
      return "OTP successfully sent to your email and phone!";
    }
  } catch(err) {
    return "Some error occurred, please try again";
  }
};

const generateAndSendOTP = async (email,phone) => {
  const OTP = Math.floor(Math.random() * 1999) + 1000;
  const otpParams = {
    TableName: 'OTPs',
    Item: {
      "email" : email,
      "phone" : phone,
      "otp" : OTP,
      "expiry" : Math.floor(Date.now()/1000)+300,
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
  
  const snsParams = {
    Message: `Your OTP is ${OTP}`,
    PhoneNumber: phone,
  };
  await sns.publish(snsParams).promise();
  context.succeed("Done!");
  
  await db.put(otpParams).promise();
}
