package com.dreamhack.ctf.user.model
import jakarta.persistence.Column
import jakarta.persistence.Entity
import jakarta.persistence.Id
import jakarta.persistence.Table

@Entity
@Table(name = "users")
data class User (
    @Id
    @Column(nullable = false, length = 100)
    val username: String,
    @Column(nullable = false, length = 100)
    val password: String

)