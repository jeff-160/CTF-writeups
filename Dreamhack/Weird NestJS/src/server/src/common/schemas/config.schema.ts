import { Prop, Schema, SchemaFactory, SchemaOptions } from '@nestjs/mongoose';
import mongoose, { Document } from 'mongoose';

export type ConfigDocument = Config & Document;

const options: SchemaOptions = {
  timestamps: false,
  versionKey: false,
};

@Schema(options)
export class Config {
  @Prop({ type: Map, of: mongoose.Schema.Types.Mixed })
  data: Record<string, any>;
}

export const ConfigSchema = SchemaFactory.createForClass(Config);
