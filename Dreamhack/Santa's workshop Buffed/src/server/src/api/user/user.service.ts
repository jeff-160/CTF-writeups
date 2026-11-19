import { HttpException, Injectable } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { LoginDto } from 'src/common/dto';
import { User, UserDocument } from 'src/common/schemas';
import { ValidationService } from 'src/common/validation/validation.service';

@Injectable()
export class UserService {
  constructor(
    @InjectModel(User.name)
    private userModel: Model<UserDocument>,

    private readonly jwtService: JwtService,
    private readonly validationService: ValidationService,
  ) {}

  async getUser(username: string, password: string): Promise<UserDocument> {
    const validation = await this.validationService.validateData(LoginDto, JSON.parse(`{"username":"${username}", "password":"${password}"}`));
    console.log(validation);
    if (validation.hasOwnProperty("$where")) throw new HttpException('Do not try Injection.', 401);
    if (!validation) throw new HttpException('username or password is Not String.', 401);

    const user = await this.userModel.findOne({ username: validation.username, password: validation.password }).lean();
    if (!user) throw new HttpException('User Not Found.', 404);
    if (user.password != validation.password) throw new HttpException('User Not Found.', 403); // code status로 구분?

    return user;
  }

  async getAccessToken(user: UserDocument): Promise<any> {
    delete user['password'];

    const accessToken = this.jwtService.sign(user, { expiresIn: '1y' });

    return { token: accessToken };
  }

}
