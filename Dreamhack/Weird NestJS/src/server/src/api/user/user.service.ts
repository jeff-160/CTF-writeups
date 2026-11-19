import { HttpException, Injectable } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { User, UserDocument } from 'src/common/schemas';

@Injectable()
export class UserService {
  constructor(
    @InjectModel(User.name)
    private userModel: Model<UserDocument>,

    private readonly jwtService: JwtService,
  ) {}

  async getAllUser(): Promise<UserDocument[]> {
    const users = await this.userModel.find({});

    return users;
  }

  async getUser(id: string, password: string): Promise<UserDocument> {
    const user = await this.userModel.findOne({ id: id, password: password }).lean();
    if (!user) throw new HttpException('User Not Found.', 404);

    return user;
  }

  async getAccessToken(user: UserDocument): Promise<any> {
    delete user['password'];

    const accessToken = this.jwtService.sign(user, { expiresIn: '1y' });

    return { token: accessToken };
  }

}
