const { getAllUser } = require("../services/CRUDService");

const getUsersAPI = async (req, res) => {
  let result = await getAllUser();
  return res.status(200).json({
    errorCode: 0,
    data: result,
  });
};
module.exports = {
    getUsersAPI
}