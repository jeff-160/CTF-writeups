import { Injectable, CanActivate, ExecutionContext, Inject } from '@nestjs/common';
import { UserService } from 'src/api/user/user.service';

@Injectable()
export class AdminRoleGuard implements CanActivate {
  constructor(
    @Inject(UserService)
    private readonly userService: UserService) {}

  async canActivate(
    context: ExecutionContext,
  ): Promise<boolean> {
    const req = context.switchToHttp().getRequest();

    const user = await this.userService.getUser('admin', req.query.password);
    if (req.user.role !== 'ADMIN' || req.user.id !== 'admin' || user.password !== req.query.password) return false;

    return true;
  }
}
