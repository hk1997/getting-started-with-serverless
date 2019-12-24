var AWS  = require("aws-sdk");
const s3 = new AWS.S3();

exports.handler = async (event)=>{
    var listjson;
    var params = {
        "Bucket": event.bucket
    }
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
    return listofContents;
};