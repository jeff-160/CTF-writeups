import { HttpException, Injectable } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model, Types } from 'mongoose';
import { ListDto } from 'src/common/dto';
import { Flag, FlagDocument, UserDocument } from 'src/common/schemas';
import { ValidationService } from 'src/common/validation/validation.service';

@Injectable()
export class AdminService {
  constructor(
    @InjectModel(Flag.name)
    private flagModel: Model<FlagDocument>,

    private readonly validationService: ValidationService,
  ) {}

  async getAllFlag(): Promise<FlagDocument[]> {
    const flags = await this.flagModel.find();

    return flags;
  }

  async getFlagList(username: string): Promise<FlagDocument[]> {
    const validation = await this.validationService.validateData(ListDto, JSON.parse(`{"username":"${username}"}`));
    if (!validation) throw new HttpException('Bad Request.', 401);

    const list = await this.flagModel.find(validation).lean();
    if (list.length == 0) { throw new HttpException(`No Flag, account: ${username}`, 404) };

    return list;
  }

  async addFlag(user: UserDocument): Promise<FlagDocument> {
    const existingFlag = await this.flagModel.findOne({ user: new Types.ObjectId(user._id) });
    if (existingFlag) throw new HttpException('This Account already have flag.', 403);

    const flag = new this.flagModel({
      name: "Taegeukgi",
      user: new Types.ObjectId(user._id),
    });

    await flag.save();
    return flag;
  }

  async removeFlag(user: UserDocument): Promise<boolean> {
    const existingFlag = await this.flagModel.deleteMany({ user: new Types.ObjectId(user._id) });
    return true;
  }

  async getFlag(user: UserDocument): Promise<string> {
    const existingFlag = await this.flagModel.find({ user: new Types.ObjectId(user._id) });
    if (existingFlag.length > 3) return process.env.FLAG;
    else throw new HttpException('You don\'t have enough flags.', 404);
  }
}
