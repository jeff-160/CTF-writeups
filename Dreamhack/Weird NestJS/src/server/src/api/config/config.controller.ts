import { Body, Controller, Get, Patch, Post } from '@nestjs/common';
import { ManageConfigDto } from 'src/common/dto/config.dto';
import { ConfigDocument } from 'src/common/schemas';
import { ConfigService } from './config.service';

@Controller('config')
export class ConfigController {
  constructor(private readonly configService: ConfigService) {}

  @Get()
  async getAllConfig(): Promise<ConfigDocument[]> {
    return await this.configService.getAllConfig();
  }

  @Post()
  async createConfig(@Body() data: object): Promise<ConfigDocument> {
    return await this.configService.createConfig(data);
  }

  @Patch()
  async manageConfig(@Body() data: ManageConfigDto): Promise<ConfigDocument> {
    return await this.configService.manageConfig(data);
  }
}
