const AWS = require('aws-sdk');
const db = new AWS.DynamoDB.DocumentClient({
  region: 'ap-south-1',
});

exports.handler = async (event) => {
  const params = {
    TableName: 'OTPs',
    Key: {
      "email" : event.email,
    },
  };
  try {
    const found = await db.get(params).promise();
    if(found.Item && found.Item.expiry > Date.now()/1000) {
      if(found.Item.otp == event.otp){
        await db.delete(params).promise();
        return "OTP successfully verified!";
      }
      else
        return "Given OTP is wrong, please provide correct OTP";
    } else {
      return "OTP not requested/expired";
    }
  } catch(err) {
    return "Some error occurred, please try again!";
  }
};
