import { Injectable } from '@nestjs/common';
import * as fs from 'fs';

@Injectable()
export class FileService {
  constructor() {}

  async getFile(): Promise<any> {
    // TODO: Handling Requests by Receiving File Path
    // @ts-ignore
    return fs.readFileSync({ message: "This feature will be announced in 2050. (TBA)" }, { encoding: "utf-8" });
  }

}
