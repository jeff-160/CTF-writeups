import { IsString, IsEnum } from 'nestjs-swagger-dto';

export const deployment = ['prod', 'dev'] as const;
export type Deployment = (typeof deployment)[number];

export class ClusterDto {
  @IsString({
    description: 'Project Name',
    example: 'Backend',
  })
  name: string;

  @IsString({
    description: 'Project Version',
    example: '1.0.0',
  })
  version: string;

  @IsString({
    description: 'Project Desc',
    example: '',
  })
  description: string;

  @IsEnum({
    enum: { deployment } as any,
    description: 'Deploy Mode',
    example: deployment[0],
  })
  mode: Deployment;

  @IsString({
    description: 'Cluster Name',
    example: '',
  })
  hostname: string;

  @IsString({
    description: 'Author',
    example: 'whguswo',
  })
  author: string;
}
