const mongoose = require("mongoose");


const predictionSchema = new mongoose.Schema({

userId:{
    type:mongoose.Schema.Types.ObjectId,
    ref:"User",
    required:true
},


image:{
    type:String,
    required:true
},


result:{
    type:String,
    default:"Pending"
},


confidence:{
    type:Number,
    default:0
},


createdAt:{
    type:Date,
    default:Date.now
}


});


module.exports = mongoose.model(
"Prediction",
predictionSchema
);