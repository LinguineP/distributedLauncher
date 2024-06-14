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
    if (!Array.isArray(value)) {
      value = [value];
    }

    // Filter out undefined values
    value = value.filter((item) => item !== undefined);

    if (value.length === 0) {
      return;
    }

    const newValue = this.storage.has(key)
      ? this.storage
          .get(key)!
          .concat(value)
          .filter((item) => item !== undefined) // Ensure no undefined values in concatenated result
      : value;

    this.storage.set(key, newValue);
    this.dirty.set(key, false);
  }

  public setDirty(key: string): void {
    this.dirty.set(key, true); // Mark as dirty by setting to true
  }

  public getItem(key: string): any[] | undefined {
    return this.storage.get(key);
  }

  public getDirty(key: string): boolean {
    let ret = this.dirty.get(key);
    if (ret === undefined) {
      ret = true; // If dirty doesn't exist, the item doesn't exist => should make a request
    }
    return ret; //returns true if item is dirty(outdated or doesnt exits)
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

export default DataVault;
