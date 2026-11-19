import { Prop, Schema, SchemaFactory, SchemaOptions } from "@nestjs/mongoose";
import { Document, Types } from "mongoose";

export type FlagDocument = Flag & Document;

@Schema()
export class Flag {
  @Prop({
    required: true,
    type: Types.ObjectId,
    ref: "User",
  })
  user: Types.ObjectId;

  @Prop({
    required: true,
    type: String,
  })
  name: string;
}

export const FlagSchema = SchemaFactory.createForClass(Flag);