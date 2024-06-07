class DataVault {
  private static instance: DataVault;
  private storage: Map<string, any[]>;
  private dirty: Map<string, boolean>;

  private constructor() {
    this.storage = new Map<string, any[]>();
    this.dirty = new Map<string, boolean>();
  }

  public static getInstance(): DataVault {
    if (!DataVault.instance) {
      DataVault.instance = new DataVault();
    }
    return DataVault.instance;
  }

  public setItem(key: string, value: any): void {
    if (!this.storage.has(key)) {
      this.storage.set(key, []);
    }
    this.storage.get(key)!.push(value);
    this.dirty.set(key, false);
  }

  public setDirty(key: string) {
    this.dirty.set(key, false);
  }

  public getItem(key: string): any[] | undefined {
    return this.storage.get(key);
  }

  public getDirty(key: string): any {
    let ret = this.dirty.get(key);
    if (ret === undefined) {
      ret = true; //if dirty doesnt exist that means that the item doesnt exist =>should make a request
    }
    return ret;
  }

  public removeItem(key: string): void {
    this.storage.delete(key);
    this.dirty.delete(key);
  }

  public clear(): void {
    this.storage.clear();
    this.dirty.clear();
  }
}

//simple caching, components should only

export default DataVault;
