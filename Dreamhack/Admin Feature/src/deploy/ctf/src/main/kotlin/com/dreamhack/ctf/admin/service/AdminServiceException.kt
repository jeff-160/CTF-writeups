package com.dreamhack.ctf.admin.service

import org.springframework.http.HttpStatus
import org.springframework.web.server.ResponseStatusException


class AdminServiceException(
    status: HttpStatus,
    message: String
) : ResponseStatusException(status, message)