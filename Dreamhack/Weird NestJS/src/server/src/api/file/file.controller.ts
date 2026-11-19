import { Body, Controller, Get, UseGuards } from '@nestjs/common';
import { AdminRoleGuard } from 'src/common/guard';
import { FileService } from './file.service';

@Controller('file')
export class FileController {
  constructor(private readonly fileService: FileService) {}

  @UseGuards(AdminRoleGuard)
  @Get()
  async getFile(): Promise<any> {
    return await this.fileService.getFile();
  }
}
