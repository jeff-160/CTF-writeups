package com.dreamhack.ctf.admin.service

import com.dreamhack.ctf.admin.model.ApiKey
import com.dreamhack.ctf.admin.model.AuthRole
import com.dreamhack.ctf.admin.repository.AdminRepository
import com.dreamhack.ctf.user.repository.UserRepository
import org.springframework.data.redis.core.StringRedisTemplate
import org.springframework.http.HttpStatus
import org.springframework.security.crypto.password.PasswordEncoder
import org.springframework.stereotype.Service
import java.security.MessageDigest
import java.time.Duration

@Service
class AdminService(
    private val adminRepository: AdminRepository,
    private val userRepository: UserRepository,
    private val passwordEncoder: PasswordEncoder,
    private val redisTemplate: StringRedisTemplate
) {

    fun doSearchKeyWithLimit(
        sessionUsername: String?,
        password: String,
        apiKey: String
    ): ApiKey {
        if (sessionUsername == null) {
            throw AdminServiceException(HttpStatus.UNAUTHORIZED, "Login first.")
        }
        val user = userRepository.findByUsername(sessionUsername) ?: throw AdminServiceException(HttpStatus.NOT_FOUND, "username not exist.")

        if (!passwordEncoder.matches(password, user.password)) {
            throw AdminServiceException(HttpStatus.UNAUTHORIZED, "Password does not match.")
        }

        val redisKey = "searchLimit:$sessionUsername:${sha256(password)}"
        val count = redisTemplate.opsForValue().get(redisKey)?.toIntOrNull() ?: 0
        if (count == 0){
            redisTemplate.expire(redisKey, Duration.ofHours(1))
        }
        if (count >= 5){
            throw AdminServiceException(HttpStatus.TOO_MANY_REQUESTS, "Rate limit exceeded.")
        }
        redisTemplate.opsForValue().increment(redisKey)

        return searchKey(apiKey)


    }

    fun testCommand(sessionUsername: String?, cmd: String?, apiKey: String): String {

        if (sessionUsername == null) {
            throw AdminServiceException(HttpStatus.UNAUTHORIZED, "Login first.")
        }

        val command = cmd ?: "ls"

        if (apiKey.isEmpty()){
            throw AdminServiceException(HttpStatus.FORBIDDEN, "API key required.")
        }

        if (sessionUsername != "admin") {
            getKey(apiKey).run {
                if (this.role != AuthRole.ADMIN) {
                    throw AdminServiceException(HttpStatus.FORBIDDEN, "Admin Role required.")
                }
            }
        }

        return runCommand(command)
    }

    private fun searchKey(key: String): ApiKey {
        return adminRepository.findByApiKeyEndingWith(key) ?: throw AdminServiceException(HttpStatus.NOT_FOUND, "API key not found.")
    }

    private fun getKey(key: String): ApiKey {
        return adminRepository.findByApiKey(key) ?: throw AdminServiceException(HttpStatus.NOT_FOUND, "API key not found.")
    }

    private fun runCommand(cmd: String): String{
        val p = Runtime.getRuntime().exec(cmd)
        val output = p.inputStream.bufferedReader().readText()
        val err = p.errorStream.bufferedReader().readText()
        p.waitFor()
        return if (err.isNotBlank()) err else output
    }

    private fun sha256(input: String): String {
        val bytes = MessageDigest.getInstance("SHA-256").digest(input.toByteArray())
        return bytes.joinToString("") { "%02x".format(it) }
    }

}