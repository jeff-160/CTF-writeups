import { HttpException, Injectable } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { ManageConfigDto } from 'src/common/dto/config.dto';
import { Config, ConfigDocument } from 'src/common/schemas';
import * as fs from 'fs';

@Injectable()
export class ConfigService {
  constructor(
    @InjectModel(Config.name)
    private configModel: Model<ConfigDocument>,
  ) {}

  async getAllConfig(): Promise<any> {
    const configs = await this.configModel.find();

    return configs;
  }

  async createConfig(obj: object): Promise<ConfigDocument> {
    const config = new this.configModel({
      data: obj,
    });

    await config.save();

    return config;
  }

  async manageConfig(data: ManageConfigDto): Promise<any> {
    const config = await this.configModel.findById(data.config);
    if (!config) throw new HttpException('configDB Not Found.', 404);

    const updateObject = {};
    data.field.forEach(([oldField, newField]) => {
      updateObject["$rename"] = updateObject["$rename"] || {};
      updateObject["$rename"][oldField] = newField;
    });
    console.log(updateObject);
    const result = await this.configModel.findByIdAndUpdate(data.config, updateObject);

    return result;
  }

}
