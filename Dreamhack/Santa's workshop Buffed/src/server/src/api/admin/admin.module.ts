import { Global, Module } from '@nestjs/common';
import { MongooseModule } from '@nestjs/mongoose';
import { Flag, FlagSchema } from 'src/common/schemas';
import { ValidationModule } from 'src/common/validation/validation.module';
import { AdminController } from './admin.controller';
import { AdminService } from './admin.service';

@Global()
@Module({
  imports: [
    ValidationModule,
    MongooseModule.forFeature([
      { name: Flag.name, schema: FlagSchema, }
    ]),
  ],
  controllers: [AdminController],
  providers: [AdminService],
  exports: [AdminService],
})
export class AdminModule {}
