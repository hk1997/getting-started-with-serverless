// const AWS = require('aws-sdk');

// exports.handler = async (event) => {
//   AWS.config.update({region: 'ap-south-1'});
//   let s3 = new AWS.S3();
//   const params = {
//     Bucket : 'guna-shekar-02',
//   };
//   const result = await s3.listObjects(params).promise();
//   return result;
// };

//ABOVE CODE USES ASYNC/AWAIT PATTERN TO LIST OBJECTS. BELOW CODE USES PROMISES TO SEND EMAIL OF THE OBJECTS.

const AWS = require('aws-sdk');

exports.handler = (event) => {
  AWS.config.update({region: 'ap-south-1'});
  let s3 = new AWS.S3();
  const params = {
    Bucket : 'guna-shekar-02',
  };
  const result = s3.listObjects(params).promise();
  return result.then(data => {
    const email = new AWS.SES();
    
    let keys = [];
    data.Contents.forEach(item => keys.push(item.Key));

    let emailParams = {
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
    
    const emailResponse = email.sendEmail(emailParams).promise();
    return emailResponse.then(data => {
      const response = {
        statusCode: 200,
        body: data.MessageId,
      };
      return response;
    })
    .catch(err => {
      const response = {
        statusCode: 403,
        body: JSON.stringify(err),
      }
      return response;
    });
    
  })
  .catch(err => {
    const response = {
      statusCode: err.statusCode,
      body: JSON.stringify(err),
    };
    return response;
  });
};


