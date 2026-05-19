package com.dreamhack.ctf.user.service

import com.dreamhack.ctf.user.model.User
import com.dreamhack.ctf.user.repository.UserRepository
import org.springframework.http.HttpStatus
import org.springframework.security.crypto.password.PasswordEncoder
import org.springframework.stereotype.Service

@Service
class UserService (
    private val userRepository: UserRepository,
    private val passwordEncoder: PasswordEncoder
){

    fun doRegister(username: String, password: String): Boolean {
        if (userRepository.count() >=3) {
            throw UserServiceException(HttpStatus.FORBIDDEN, "Only 3 users are allowed.")
        }
        if (userRepository.existsByUsername(username)) {
            throw UserServiceException(HttpStatus.BAD_REQUEST, "User already exists.")
        }
        val encodedPassword = passwordEncoder.encode(password)
        val user = User(username = username, password = encodedPassword)
        userRepository.save(user)
        return true
    }

    fun doLogin(username: String, password: String): User {
        val user: User? = userRepository.findByUsername(username)
        if (user == null || !passwordEncoder.matches(password, user.password)) {
            throw UserServiceException(HttpStatus.UNAUTHORIZED, "The user or password is incorrect.")
        }

        return user
    }

}