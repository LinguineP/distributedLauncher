import axios from "axios";
import DataVault from "./dataVault.ts";

class CommunicationHandler {
  private paramsUrl: string = "/api/cmdParams";
  private sessionUrl: string = "/api/sessions";
  private imagePngUrl: string = "/api/imagePng";

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
      const dataVault = DataVault.getInstance(); //cache, note available scripts do not change in runtime
      dataVault.setItem("paramsList", response.data.paramsList); //puts the intem in the shared Cache  and resets the dirty flag
      return response.data;
    } catch (error) {
      console.error("POST Error:", error);
      throw error;
    }
  }

  async getCmdParams() {
    try {
      const response = await axios.get(this.paramsUrl);
      const dataVault = DataVault.getInstance(); //cache
      if (dataVault.getItem("paramsList")) {
        dataVault.removeItem("paramsList");
      }
      dataVault.setItem("paramsList", response.data.paramsList); //puts the intem in the shared Cache  and resets the dirty flag
      if (!dataVault.getItem("availableScripts")) {
        dataVault.setItem("availableScripts", response.data.availableScripts); //here we need to write available scripts as well
      }
      return response.data;
    } catch (error) {
      console.error("GET Error:", error);
      throw error;
    }
  }

  async deleteCmdParam(id: number) {
    try {
      const response = await axios.delete(`${this.paramsUrl}/${id}`);
      const dataVault = DataVault.getInstance(); //cache
      dataVault.setDirty("paramsList");
      return response.data;
    } catch (error) {
      console.error("DELETE Error:", error);
      throw error;
    }
  }

  async putCmdParam(id: number, data: any) {
    try {
      const response = await axios.put(`${this.paramsUrl}/${id}`, data);
      const dataVault = DataVault.getInstance(); //cache
      dataVault.setDirty("paramsList");
      return response.data;
    } catch (error) {
      console.error("PUT Error:", error);
      throw error;
    }
  }
  //---------------------------------------sessionRelated-------------------------

  async postSession(data: any) {
    try {
      const response = await axios.post(this.sessionUrl, data);
      const dataVault = DataVault.getInstance(); //cache, note available scripts do not change in runtime
      dataVault.setItem("sessionList", response.data.sessionList); //puts the intem in the shared Cache  and resets the dirty flag
      return response.data;
    } catch (error) {
      console.error("POST Error:", error);
      throw error;
    }
  }

  async getSessions() {
    try {
      const response = await axios.get(this.sessionUrl);
      const dataVault = DataVault.getInstance(); //cache
      if (dataVault.getItem("sessionList")) {
        dataVault.removeItem("sessionList");
      }
      dataVault.setItem("sessionList", response.data.paramsList); //puts the intem in the shared Cache  and resets the dirty flag
      return response.data;
    } catch (error) {
      console.error("GET Error:", error);
      throw error;
    }
  }

  //-------------------------------- batch params -------------------
  async getBatchUsedParams() {
    try {
      const response = await axios.get(this.sessionUrl + "/batchParams");
      const dataVault = DataVault.getInstance(); //cache
      if (dataVault.getItem("sessionList")) {
        dataVault.removeItem("sessionList");
      }
      dataVault.setItem("sessionList", response.data.paramsList); //puts the intem in the shared Cache  and resets the dirty flag
      return response.data;
    } catch (error) {
      console.error("GET Error:", error);
      throw error;
    }
  }

  //-------- processing realted --------------------
  fetchDataMeasuringStatus = async () => {
    try {
      const response = await axios.get("/api/measuringStatus");
      return response.data;
    } catch (error) {
      console.error("Error fetching processing status:", error);
      throw error;
    }
  };

  startMeasuringTask = async (data) => {
    try {
      await axios.post("/api/startMeasuring", data);
    } catch (error) {
      console.error("Error starting data processing:", error);
      throw error;
    }
  };

  //--------analysis-----------------------
  exportCsv = async () => {
    try {
      await axios.post("/api/exportCSV");
    } catch (error) {
      console.error("Error starting data processing:", error);
      throw error;
    }
  };

  doAnalysis = async (data) => {
    try {
      await axios.post("/api/doAnalysis", data);
    } catch (error) {
      console.error("Error starting data processing:", error);
      throw error;
    }
  };
  //--------------------image fetch------------
  async fetchImage(imagePath: string) {
    const encodedPath = imagePath; // Encode the path for URL
    try {
      const response = await axios.get(`${this.imagePngUrl}/${encodedPath}`, {
        responseType: "blob",
      });
      return URL.createObjectURL(response.data);
    } catch (error) {
      console.error("Error fetching the image:", error);
      throw error;
    }
  }

  async getSessionResults(sessionId: string): Promise<any> {
    try {
      const response = await axios.get(`/api/sessions/sessionResults`, {
        params: { sessionId },
      });
      return response.data;
    } catch (error) {
      console.error("GET Session Results Error:", error);
      throw error;
    }
  }

  async getBatchResults(sessionId: string) {
    try {
      const response = await axios.get(`/api/sessions/batchResults`, {
        params: { sessionId },
      });
      return response.data;
    } catch (error) {
      console.error("GET Batch Results Error:", error);
      throw error;
    }
  }
}

export default CommunicationHandler;
