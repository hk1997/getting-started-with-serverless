const AWS = require('aws-sdk');

exports.handler = async (event) => {
  AWS.config.update({region: 'ap-south-1'});
  let s3 = new AWS.S3();
  const params = {
    Bucket : 'guna-shekar-02',
  };
  const result = await s3.listObjects(params).promise();
  return result;
};
