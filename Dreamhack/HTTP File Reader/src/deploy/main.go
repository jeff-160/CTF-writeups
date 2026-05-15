package main

import (
	"fmt"
	"html/template"
	"io"
	"log"
	"net"
	"net/http"
	"net/netip"
	"strconv"
	"strings"

	"gin-http-file-reader/api"

	"github.com/gin-gonic/gin"
)

type RequestInput struct {
	Host string `form:"host" binding:"required"`
	Port string `form:"port" binding:"required"`
	Path string `form:"path" binding:"required"`
}

func main() {
	r := gin.Default()
	r.SetHTMLTemplate(template.Must(template.ParseGlob("templates/*.html")))

	r.GET("/", func(c *gin.Context) {
		c.HTML(http.StatusOK, "index.html", nil)
	})

	r.POST("/request", func(c *gin.Context) {
		var input RequestInput
		if err := c.ShouldBind(&input); err != nil {
			c.HTML(http.StatusBadRequest, "index.html", gin.H{"error": err.Error()})
			return
		}

		host := strings.TrimPrefix(strings.TrimPrefix(input.Host, "http://"), "https://")

		portNum, err := strconv.Atoi(input.Port)
		if err != nil || portNum < 1 || portNum > 65535 {
			c.HTML(http.StatusBadRequest, "index.html", gin.H{"error": "invalid port"})
			return
		}

		var addr netip.Addr

		if parsed, err := netip.ParseAddr(host); err == nil {
			addr = parsed
		} else {
			ips, err := net.LookupIP(host)
			if err != nil || len(ips) == 0 {
				c.HTML(http.StatusInternalServerError, "index.html", gin.H{"error": "cannot resolve host"})
				return
			}
			ipStr := ips[0].String()
			parsed, err := netip.ParseAddr(ipStr)
			if err != nil {
				c.HTML(http.StatusInternalServerError, "index.html", gin.H{"error": "resolved address is invalid"})
				return
			}
			addr = parsed
		}
		unspecified, _ := netip.ParseAddr("0.0.0.0")
		if addr.IsLoopback() || addr == unspecified {
			c.HTML(http.StatusForbidden, "index.html", gin.H{"error": "localhost is not allowed"})
			return
		}


		url := fmt.Sprintf("http://%s:%d/%s", host, portNum, strings.TrimLeft(input.Path, "/"))

		resp, err := http.Get(url)
		if err != nil {
			c.HTML(http.StatusInternalServerError, "index.html", gin.H{"error": err.Error()})
			return
		}
		defer resp.Body.Close()

		body, _ := io.ReadAll(resp.Body)

		c.HTML(http.StatusOK, "index.html", gin.H{
			"url":        url,
			"resolvedIP": addr.String(),
			"statusCode": resp.StatusCode,
			"body":       string(body),
		})
	})

	api.RegisterReadRoutes(r)

	log.Println("Server running on :8080")
	_ = r.Run(":8080")
}
