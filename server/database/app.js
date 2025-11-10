"use strict";

const express = require("express");
const mongoose = require("mongoose");
const fs = require("fs");
const cors = require("cors");
const bodyParser = require("body-parser");

const app = express();
const port = process.env.PORT || 3030;

app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

// Load JSON seed data
const reviewsData = JSON.parse(fs.readFileSync("reviews.json", "utf8"));
const dealershipsData = JSON.parse(fs.readFileSync("dealerships.json", "utf8"));

// DB Connection
mongoose.connect("mongodb://mongo_db:27017/", { dbName: "dealershipsDB" });

const Reviews = require("./review");
const Dealerships = require("./dealership");

// Seed DB only once
(async () => {
  try {
    await Reviews.deleteMany({});
    await Reviews.insertMany(reviewsData.reviews);

    await Dealerships.deleteMany({});
    await Dealerships.insertMany(dealershipsData.dealerships);
  } catch (error) {
    console.error("Error seeding database:", error);
  }
})();

// Routes
app.get("/", (req, res) => {
  res.send("Welcome to the Mongoose API");
});

// Fetch ALL reviews
app.get("/fetchReviews", async (req, res) => {
  try {
    const docs = await Reviews.find();
    res.json(docs);
  } catch (error) {
    res.status(500).json({ error: "Error fetching reviews" });
  }
});

// Fetch reviews for one dealer
app.get("/fetchReviews/dealer/:id", async (req, res) => {
  try {
    const docs = await Reviews.find({ dealership: req.params.id });
    res.json(docs);
  } catch (error) {
    res.status(500).json({ error: "Error fetching dealer reviews" });
  }
});

// Fetch ALL dealerships
app.get("/fetchDealers", async (req, res) => {
  try {
    const dealers = await Dealerships.find();
    res.json(dealers);
  } catch (error) {
    res.status(500).json({ error: "Error fetching dealers" });
  }
});

// Fetch dealer by state
app.get("/fetchDealers/:state", async (req, res) => {
  try {
    const dealers = await Dealerships.find({ state: req.params.state });
    res.json(dealers);
  } catch (error) {
    res.status(500).json({ error: "Error fetching dealers by state" });
  }
});

// Fetch dealer by ID
app.get("/fetchDealer/:id", async (req, res) => {
  try {
    const dealer = await Dealerships.findOne({ id: req.params.id });
    res.json(dealer);
  } catch (error) {
    res.status(500).json({ error: "Error fetching dealer" });
  }
});

// Insert review
app.post("/insert_review", async (req, res) => {
  try {
    const data = req.body;

    const lastReview = await Reviews.find().sort({ id: -1 }).limit(1);
    const newId = lastReview.length > 0 ? lastReview[0].id + 1 : 1;

    const review = new Reviews({
      id: newId,
      name: data.name,
      dealership: data.dealership,
      review: data.review,
      purchase: data.purchase,
      purchase_date: data.purchase_date,
      car_make: data.car_make,
      car_model: data.car_model,
      car_year: data.car_year
    });

    const saved = await review.save();
    res.json(saved);
  } catch (error) {
    res.status(500).json({ error: "Error inserting review" });
  }
});

// Start server
app.listen(port, "0.0.0.0", () => {
  console.log(`✅ Server is running on port ${port}`);
});
