const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
require("dotenv").config();


// Create Express App
const app = express();


// Middleware
app.use(cors());
app.use(express.json());


// Serve uploaded images
app.use("/uploads", express.static("uploads"));



// MongoDB Connection
mongoose.connect(process.env.MONGO_URI)
.then(() => {

    console.log("MongoDB Connected");

})
.catch((error) => {

    console.log("MongoDB Connection Error:", error);

});



// Test Route
app.get("/", (req,res)=>{

    res.send("SignatureGuard Backend Running");

});




// Authentication Routes
const authRoutes = require("./routes/authRoutes");

app.use(
    "/api/auth",
    authRoutes
);




// Prediction Routes
const predictionRoutes = require("./routes/predictionRoutes");


app.use(
    "/api/prediction",
    predictionRoutes
);




// Server Port
const PORT = process.env.PORT || 5000;



app.listen(PORT,()=>{

    console.log(`Server running on port ${PORT}`);

});