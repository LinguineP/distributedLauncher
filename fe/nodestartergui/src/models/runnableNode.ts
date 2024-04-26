class runnableNode {
  ip: string;
  id: string;
  hostName: string;

  constructor(ip: string, id: string, hostName: string) {
    this.ip = ip;
    this.id = id;
    this.hostName = hostName;
  }

  getIp() {
    return this.ip;
  }

  setIp(ip: string) {
    this.ip = ip;
  }

  getId() {
    return this.id;
  }

  setId(id: string) {
    this.id = id;
  }

  getHostname() {
    return this.hostName;
  }

  setHostname(hostname: string) {
    this.hostName = hostname;
  }
}

export default runnableNode;
