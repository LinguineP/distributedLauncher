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

}

export default CommunicationHandler;
