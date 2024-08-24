const express = require("express");
const routerAPI = express.Router();
// const { getUsersAPI } = require("../controllers/apiController");
routerAPI.get("/", (req, res) => {
  res.json({ fruits: ["apple", "orange", "banana"] });
});

module.exports = routerAPI;
