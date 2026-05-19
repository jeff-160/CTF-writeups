package com.dreamhack.ctf.admin.repository

import com.dreamhack.ctf.admin.model.ApiKey
import org.springframework.data.jpa.repository.JpaRepository

interface AdminRepository: JpaRepository<ApiKey, Long> {
    fun findByApiKey(apiKey: String): ApiKey?
    fun findByApiKeyEndingWith(apiKey: String): ApiKey?
}