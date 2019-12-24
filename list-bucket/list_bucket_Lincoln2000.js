var AWS  = require("aws-sdk");
const s3 = new AWS.S3();
const ses = new AWS.SES();

exports.handler = async (event)=>{
    var listjson;
    var buck = event["Records"][0]["s3"]["bucket"]["name"];
    var params = {
        "Bucket": buck
    };
    try{
        listjson =  await s3.listObjectsV2(params).promise();
    }
    catch(err){
        return err;
    }

    var listofContents = [];
    for(let i=0;i<listjson.Contents.length;i++){
        listofContents.push(listjson.Contents[i].Key);
    }
    var myEmail = "sarvagya60@gmail.com";
    var charset = "UTF-8";

    params = {
        Destination: {
         ToAddresses: [myEmail]
        }, 
        Message: {
         Body: {
          Html: {
          Charset: charset, 
          Data: JSON.stringify(listofContents)
          }, 
         }, 
         Subject: {
          Charset: charset, 
          Data: "Contents of Bucket- " + buck
         }
        },
        Source: myEmail
       };

    var emailed;
    try{
        emailed = await ses.sendEmail(params).promise();
    }
    catch(err){
        emailed = err;
    }
    return emailed;
};