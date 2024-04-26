import axios from "axios";

class CommunicationHandler {
  serverAddr: string;

  constructor() {
    var full = window.location.host;
    var parts = full.split(".");
    this.serverAddr = parts[0];
  }

  stopScan() {
    axios
      .get(`http://${this.serverAddr}/stopScan`)
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
      .get(`http://${this.serverAddr}/startScan`)
      .then(function (response) {
        return response;
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
      .post(`http://${this.serverAddr}/startNodes`, data)
      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
  }
}

export default CommunicationHandler;
