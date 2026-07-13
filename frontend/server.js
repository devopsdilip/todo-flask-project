const express = require("express");
const axios = require("axios");

const app = express();

app.set("view engine", "ejs");
app.use(express.urlencoded({ extended: true }));

const BACKEND_URL =
  process.env.BACKEND_URL ||
  "http://backend:5000";

// Home
app.get("/", async (req, res) => {
    try {
        const response = await axios.get(`${BACKEND_URL}/students`);
        res.render("index", {
            students: response.data.students
        });
    } catch (err) {
        console.error(err.message);
        res.status(500).send("Backend unavailable");
    }
});

// Register page
app.get("/register", (req, res) => {
    res.render("register");
});

// Register
app.post("/register", async (req, res) => {
    try {
        await axios.post(`${BACKEND_URL}/students`, req.body);
        res.redirect("/success");
    } catch (err) {
        console.error(err.message);
        res.status(500).send("Registration failed.");
    }
});

// Success
app.get("/success", (req, res) => {
    res.render("success");
});

// Students
app.get("/students", async (req, res) => {
    try {
        const response = await axios.get(`${BACKEND_URL}/students`);
        res.render("students", {
            students: response.data.students
        });
    } catch (err) {
        console.error(err.message);
        res.status(500).send("Unable to fetch students.");
    }
});

app.listen(3000, () => {
    console.log("Frontend running on port 3000");
});
