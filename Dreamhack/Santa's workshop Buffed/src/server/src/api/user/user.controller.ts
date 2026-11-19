import { Controller, Post, Body } from '@nestjs/common';
import { LoginDto } from 'src/common/dto';
import { UserService } from './user.service';

@Controller('user')
export class UserController {
  constructor(private readonly userService: UserService) {}

  @Post('login')
  async login(@Body() loginDto: LoginDto): Promise<any> {
    console.log(loginDto.username, loginDto.password);
    const user = await this.userService.getUser(loginDto.username, loginDto.password);
    return await this.userService.getAccessToken(user);
  }
}
