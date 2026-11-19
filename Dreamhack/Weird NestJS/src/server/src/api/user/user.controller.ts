import { Controller, Get, Query, UseGuards } from '@nestjs/common';
import { AdminRoleGuard } from 'src/common/guard';
import { UserDocument } from 'src/common/schemas';
import { UserService } from './user.service';

@Controller('user')
export class UserController {
  constructor(private readonly userService: UserService) {}

  @UseGuards(AdminRoleGuard)
  @Get()
  async getAllUser(): Promise<UserDocument[]> {
    return await this.userService.getAllUser();
  }

  @Get('get')
  async getUser(
    @Query('id') id: string,
    @Query('password') password: string,
  ): Promise<any> {
    const user = await this.userService.getUser(id, password);
    return await this.userService.getAccessToken(user);
  }
}
