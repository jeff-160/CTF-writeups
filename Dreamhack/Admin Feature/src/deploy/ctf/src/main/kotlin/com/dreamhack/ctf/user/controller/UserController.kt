package com.dreamhack.ctf.user.controller

import com.dreamhack.ctf.user.model.User
import com.dreamhack.ctf.user.service.UserService
import com.dreamhack.ctf.user.service.UserServiceException
import jakarta.servlet.http.HttpSession
import org.springframework.http.ResponseEntity
import org.springframework.stereotype.Controller
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RequestMapping

@Controller
@RequestMapping("/user")
class UserController(
    private val userService: UserService
) {

    @PostMapping("/register")
    fun register(@RequestBody data: User, authUser: HttpSession): ResponseEntity<Map<String, Any>> {
        val response = mutableMapOf<String, Any>()
        return try {


            if(userService.doRegister(data.username, data.password)){
                response["result"] = 200
                response["message"] = "Successfully registered user."
                return ResponseEntity.status(200).body(response)

            } else {
                response["result"] = 400
                response["message"] = "Registration failed."
                ResponseEntity.status(400).body(response)
            }

        } catch (e: UserServiceException){
            response["result"] = e.statusCode.value()
            response["message"] = e.message
            return ResponseEntity.status(400).body(response)
        }
    }

    @PostMapping("/login")
    fun login(@RequestBody data: User, authUser: HttpSession): ResponseEntity<Map<String, Any>> {
        val response = mutableMapOf<String, Any>()
        try {
            val user = userService.doLogin(data.username, data.password)

            authUser.setAttribute("username", user.username)
            response["result"] = 200
            response["message"] = "Successfully logged in."
            return ResponseEntity.status(200).body(response)


        } catch (e: UserServiceException){
            response["result"] = e.statusCode.value()
            response["message"] = e.message
            return ResponseEntity.status(400).body(response)

        }
    }

}