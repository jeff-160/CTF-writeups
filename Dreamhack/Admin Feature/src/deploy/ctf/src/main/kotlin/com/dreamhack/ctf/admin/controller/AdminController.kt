package com.dreamhack.ctf.admin.controller

import com.dreamhack.ctf.admin.dto.ApiKeySearchDto
import com.dreamhack.ctf.admin.service.AdminService
import com.dreamhack.ctf.admin.service.AdminServiceException
import jakarta.servlet.http.HttpSession
import org.springframework.http.ResponseEntity
import org.springframework.stereotype.Controller
import org.springframework.web.bind.annotation.*

@Controller
@RequestMapping("/admin")
class AdminController(
    private val adminService: AdminService,
) {

    @PostMapping("/search")
    fun searchKey(@RequestBody data: ApiKeySearchDto, authUser: HttpSession): ResponseEntity<Map<String, Any>> {
        val response = mutableMapOf<String, Any>()
        try {

            val apiKey = adminService.doSearchKeyWithLimit(
                sessionUsername = authUser.getAttribute("username") as? String,
                password = data.password,
                apiKey = data.apiKey
            )

            response["result"] = 200
            response["message"] = apiKey.role
            return ResponseEntity.ok(response)


        } catch (e: AdminServiceException) {
            val statusCode = e.statusCode.value()
            response["result"] = statusCode
            response["message"] = e.message
            return ResponseEntity.status(statusCode).body(response)
        }
    }

    @PostMapping("/run")
    fun runCmd(@RequestParam cmd: String?, @RequestHeader("X-Api-Key") apiKey: String = "", authUser: HttpSession): ResponseEntity<Map<String, Any>> {
        val response = mutableMapOf<String, Any>()
        try {

            val result = adminService.testCommand(
                sessionUsername = authUser.getAttribute("username") as? String,
                cmd = cmd,
                apiKey = apiKey
            )

            response["result"] = 200
            response["message"] = result
            return ResponseEntity.ok(response)


        } catch (e: AdminServiceException){
            val statusCode = e.statusCode.value()
            response["result"] = statusCode
            response["message"] = e.message
            return ResponseEntity.status(statusCode).body(response)
        }
    }
}