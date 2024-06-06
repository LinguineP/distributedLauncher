import axios from "axios";

class CommunicationHandler {
  private paramsUrl: string = "/api/cmdParams";
  private sessionUrl: string = "/api/sessions";

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

  async postCmdParam(data: any) {
    try {
      const response = await axios.post(this.paramsUrl, data);
      console.log("POST Response:", response.data);
      return response.data;
    } catch (error) {
      console.error("POST Error:", error);
      throw error;
    }
  }

  async getCmdParams() {
    try {
      const response = await axios.get(this.paramsUrl);
      console.log("GET Response:", response.data);
      return response.data;
    } catch (error) {
      console.error("GET Error:", error);
      throw error;
    }
  }

  async deleteCmdParam(id: number) {
    try {
      const response = await axios.delete(`${this.paramsUrl}/${id}`);
      console.log("DELETE Response:", response.data);
      return response.data;
    } catch (error) {
      console.error("DELETE Error:", error);
      throw error;
    }
  }

  async putCmdParam(id: number, data: any) {
    try {
      const response = await axios.put(`${this.paramsUrl}/${id}`, data);
      console.log("PUT Response:", response.data);
      return response.data;
    } catch (error) {
      console.error("PUT Error:", error);
      throw error;
    }
  }

  async postSession(data: any) {
    try {
      const response = await axios.post(this.sessionUrl, data);
      console.log("POST Response:", response.data);
      return response.data;
    } catch (error) {
      console.error("POST Error:", error);
      throw error;
    }
  }

  async getSessions() {
    try {
      const response = await axios.get(this.sessionUrl);
      console.log("GET Response:", response.data);
      return response.data;
    } catch (error) {
      console.error("GET Error:", error);
      throw error;
    }
  }
}

export default CommunicationHandler;
