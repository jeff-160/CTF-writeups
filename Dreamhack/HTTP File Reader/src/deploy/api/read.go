package api

import (
	"fmt"
	"io"
	"net"
	"net/http"
	"os/exec"
	"regexp"
	"strings"

	"github.com/gin-gonic/gin"
)

var banned = regexp.MustCompile(`(?i)(flag|[\@\$\*\{\!\?\.\%\;\|\"\'\#\^\&\(\)\+\=\<\>\\])`)

func CheckFileName(path string) error {
	if loc := banned.FindStringIndex(path); loc != nil {
		bad := path[loc[0]:loc[1]]
		return fmt.Errorf("disallowed char detected: %q", bad)
	}
	return nil
}

func RegisterReadRoutes(r *gin.Engine) {
	r.GET("/api/read", func(c *gin.Context) {
		ipPort :=c.Request.RemoteAddr
		host := ipPort
		if i := strings.LastIndex(ipPort, ":"); i != -1 {
			host = ipPort[:i]
		}
	
		clientIP := net.ParseIP(host)
		if clientIP == nil {
			c.String(http.StatusBadRequest, "invalid client ip")
			return
		}

		if !clientIP.Equal(net.ParseIP("127.0.0.1")) {
			c.String(http.StatusForbidden, "access denied")
			return
		}

		filename := c.Query("filename")
		if filename == "" {
			c.String(http.StatusBadRequest, "missing filename")
			return
		}

		if err := CheckFileName(filename); err != nil {
			c.String(http.StatusForbidden, err.Error())
			return
		}

		cmd := exec.Command("sh", "-c", "cat " + filename)
		stdout, err := cmd.StdoutPipe()
		if err != nil {
			c.String(http.StatusInternalServerError, "failed to create stdout pipe")
			return
		}

		if err := cmd.Start(); err != nil {
			c.String(http.StatusInternalServerError, fmt.Sprintf("failed to start command: %v", err))
			return
		}

		c.Header("Content-Type", "text/plain")
		if _, err := io.Copy(c.Writer, stdout); err != nil {
			c.String(http.StatusInternalServerError, fmt.Sprintf("error copying output: %v", err))
			return
		}

		cmd.Wait()
	})

}
