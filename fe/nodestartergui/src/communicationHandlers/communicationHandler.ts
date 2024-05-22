import axios from "axios";

class CommunicationHandler {
  stopScan() {
    return axios
      .get("/api/stopScan")
      .then(function (response) {
        console.log(response);
        return response.data;
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  startScan() {
    axios
      .get("api/startScan")
      .then(function (response) {
        return response.data;
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  startNodes(startParams) {
    const data = {
      startParams: startParams,
    };

    axios
      .post("api/startNodes", data)
      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  stopNodes(stopParams) {
    const data = {
      stopParams: stopParams,
    };

    axios
      .post("/api/shutdownAgents", data)
      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  async postData(url, data) {
    try {
      const response = await axios.post(url, data);
      console.log("POST Response:", response.data);
      return response.data;
    } catch (error) {
      console.error("POST Error:", error);
      throw error;
    }
  }

  // GET Method
  async getData(url) {
    try {
      const response = await axios.get(url);
      console.log("GET Response:", response.data);
      return response.data;
    } catch (error) {
      console.error("GET Error:", error);
      throw error;
    }
  }

  // DELETE Method
  async deleteData(url) {
    try {
      const response = await axios.delete(url);
      console.log("DELETE Response:", response.data);
      return response.data;
    } catch (error) {
      console.error("DELETE Error:", error);
      throw error;
    }
  }

  // PUT Method
  async putData(url, data) {
    try {
      const response = await axios.put(url, data);
      console.log("PUT Response:", response.data);
      return response.data;
    } catch (error) {
      console.error("PUT Error:", error);
      throw error;
    }
  }
}

export default CommunicationHandler;
