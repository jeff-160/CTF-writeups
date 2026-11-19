import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { setupSwagger } from './common/modules';
import { NestExpressApplication } from '@nestjs/platform-express';
import { NotFoundFilter, UnauthorizedFilter } from './common/filters';
import helmet from 'helmet';

async function bootstrap() {
  const app = await NestFactory.create<NestExpressApplication>(AppModule);

  app.enableCors();
  app.use(helmet({ contentSecurityPolicy: false }));

  app.useGlobalFilters(new NotFoundFilter());
  app.useGlobalFilters(new UnauthorizedFilter());

  await setupSwagger(app);

  await app.listen(3000);
}
bootstrap();
