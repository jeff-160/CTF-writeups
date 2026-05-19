package com.dreamhack.ctf.user.service

import org.springframework.http.HttpStatus
import org.springframework.web.server.ResponseStatusException

class UserServiceException(
    status: HttpStatus,
    message: String
) : ResponseStatusException(status, message)