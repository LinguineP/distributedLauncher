class DataVault {
  private static instance: DataVault;
  private storage: Map<string, any>;

  private constructor() {
    this.storage = new Map<string, any>();
  }

  public static getInstance(): DataVault {
    if (!DataVault.instance) {
      DataVault.instance = new DataVault();
    }
    return DataVault.instance;
  }

  public setItem(key: string, value: any): void {
    this.storage.set(key, value);
  }

  public getItem(key: string): any {
    return this.storage.get(key);
  }

  public removeItem(key: string): void {
    this.storage.delete(key);
  }

  public clear(): void {
    this.storage.clear();
  }
}

export default DataVault;
