import { HttpException, HttpStatus } from '@nestjs/common';

export type OpcodeNames =
  | 'Success'
  | 'InvalidError'
  | 'NoPermission'
  | 'ValidateFailed'
  | 'NotFound';

export type OpcodeItem = (details?: { [key: string]: any }) => HttpException;
export const globalOpcode: { [key in OpcodeNames]: OpcodeItem } = {
  Success: $(
    0,
    HttpStatus.OK,
    'Request was successful.',
  ),
  InvalidError: $(
    -999,
    HttpStatus.INTERNAL_SERVER_ERROR,
    'An unknown internal error occurred.',
  ),
  NoPermission: $(
    -401,
    HttpStatus.UNAUTHORIZED,
    'Unauthorized. Please provide a JWT token.',
  ),
  ValidateFailed: $(
    -1,
    HttpStatus.BAD_REQUEST,
    'Invalid format. Please ensure all information is entered correctly.',
  ),
  NotFound: $(
    -404,
    HttpStatus.NOT_FOUND,
    'Invalid request. Please check if the route exists.',
  ),
};

export function $(
  opcode: number,
  statusCode: number,
  message?: string,
): OpcodeItem {
  return (details: { [key: string]: any } = {}) =>
    new HttpException({ opcode, message, ...details }, statusCode);
}
