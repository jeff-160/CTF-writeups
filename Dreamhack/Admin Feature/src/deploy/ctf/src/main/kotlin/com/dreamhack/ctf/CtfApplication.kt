package com.dreamhack.ctf

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication
import org.springframework.stereotype.Controller
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@SpringBootApplication
class CtfApplication

fun main(args: Array<String>) {
    runApplication<CtfApplication>(*args)
}

@RestController
@RequestMapping("/")
internal class IndexController {
    @GetMapping
    fun index(): String {
        return "Hi"
    }
}