import { Injectable, NestMiddleware } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';
import { JwtService } from '@nestjs/jwt';

@Injectable()
export class JwtExpireMiddleware implements NestMiddleware {
  constructor(private readonly jwtService: JwtService) {}

  async use(req: Request, res: Response, next: NextFunction) {
    const token = req.headers.authorization?.split(' ')[1];

    if (token) {
      try {
        const decoded = await this.jwtService.verifyAsync(token);
        req.user = decoded;

        next();
      } catch (err) {
        res
          .status(401)
          .json({ message: 'JWT token is invalid or has expired.' });
      }
    } else {
      res
        .status(401)
        .json({ message: 'Please provide the JWT token in the Bearer header.' });
    }
  }
}
