const Prediction = require("../models/Prediction");
const axios = require("axios");

exports.uploadSignature = async (req, res) => {
  try {
    console.log("========== REQUEST RECEIVED ==========");
    console.log("BODY:", req.body);
    console.log("FILE:", req.file);

    if (!req.file) {
      return res.status(400).json({
        message: "No file received",
      });
    }

    console.log("Calling Flask API...");

    const aiResponse = await axios.post(
      "http://127.0.0.1:5001/predict"
    );

    console.log("Flask Response:", aiResponse.data);

    const prediction = await Prediction.create({
      userId: req.body.userId,
      image: req.file.filename,
      result: aiResponse.data.result,
      confidence: aiResponse.data.confidence,
    });

    console.log("Saved To MongoDB");

    res.status(201).json({
      message: "Signature analyzed successfully",
      prediction,
    });

  } catch (error) {
    console.error("FULL ERROR:");
    console.error(error);

    res.status(500).json({
      message: error.message,
    });
  }
};