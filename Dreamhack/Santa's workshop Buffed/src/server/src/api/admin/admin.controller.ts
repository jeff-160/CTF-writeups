import { Controller, Body, Get, Post, Delete, Req } from '@nestjs/common';
import { Request } from 'express';
import { ListDto } from 'src/common/dto';
import { FlagDocument } from 'src/common/schemas';
import { AdminService } from './admin.service';

@Controller('admin')
export class AdminController {
  constructor(private readonly adminService: AdminService) {}

  // 받은 표식 목록
  @Get()
  async getAllFlag(): Promise<FlagDocument[]> {
    return await this.adminService.getAllFlag();
  }

  @Post('list')
  async getFlagList(@Body() listDto: ListDto): Promise<FlagDocument[]> {
    return await this.adminService.getFlagList(listDto.username);
  }

  // 착한아이에게 표식 선물하기
  @Get('flag')
  async addFlag(@Req() request: Request): Promise<FlagDocument> {
    return await this.adminService.addFlag(request.user);
  }

  // 나쁜아이의 표식 박탈하기
  @Delete('flag')
  async removeFlag(@Req() request: Request): Promise<boolean> {
    return await this.adminService.removeFlag(request.user);
  }

  @Get('check')
  async getRealFlag(@Req() request: Request): Promise<string> {
    return await this.adminService.getFlag(request.user);
  }
}
