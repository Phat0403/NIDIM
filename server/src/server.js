require("dotenv").config();

const express = require("express");
const apiRoutes = require("./routes/api");
const connection = require("./config/database");

const app = express();
const port = process.env.PORT || 8080;
const hostname = process.env.HOST_NAME;
app.use("/api/v1", apiRoutes);


(async () => {
  try {
    await connection();
    app.listen(port, hostname, () => {
      console.log(`Example app listening on port ${port}`);
    });
  } catch (error) {
    console.log("Error connection to DB");
  }
})();
