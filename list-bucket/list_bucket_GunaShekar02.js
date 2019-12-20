const AWS = require('aws-sdk');
const s3 = new AWS.S3();

exports.handler = async (event, context) => {
  const bucket = event.Records[0].s3.bucket.name;
  const params = {
    Bucket: bucket,
  };
  try {
    const data = await s3.listObjects(params).promise();
    const ses = new AWS.SES();
    
    let keys = [];
    data.Contents.forEach(item => keys.push(item.Key));
    
    const emailParams = {
      Destination: { 
        ToAddresses: [
          'gunashekherproddatoori@gmail.com',
        ]
      },
      Message: {
        Body: { 
          Text: {
           Charset: "UTF-8",
           Data: JSON.stringify(keys),
          }
         },
         Subject: {
          Charset: 'UTF-8',
          Data: 'Objects in Bucket'
         }
        },
      Source: 'gunashekherproddatoori@gmail.com',
    };
    
    try {
      const emailResponse = await ses.sendEmail(emailParams).promise();
    } catch (err) {
      throw new Error(err);
    }
    return data;
  } catch (err) {
    throw new Error(err);
  }
};
