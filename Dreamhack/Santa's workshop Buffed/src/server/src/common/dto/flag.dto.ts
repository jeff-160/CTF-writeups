import { IsString } from "class-validator";

export class ListDto {
  @IsString()
  username: string;
}