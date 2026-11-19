import { ApiProperty } from '@nestjs/swagger';
import { IsArray, IsMongoId } from 'class-validator';

export class ManageConfigDto {
  @ApiProperty()
  @IsMongoId()
  config: string;

  @ApiProperty()
  @IsArray()
  field: [[string, string]];
}
