package com.dreamhack.ctf.admin.model

import jakarta.persistence.*

@Entity
@Table(name = "api_key")
data class ApiKey (

    @Id
    val apiKey: String,

    @Enumerated(EnumType.STRING)
    val role: AuthRole
)