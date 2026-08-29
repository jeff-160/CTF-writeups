const checkLogin = (req, res, next) => {
    if (!req.session.isLogin) {
        return res.redirect("/user/login")
    } else {
        next()
    }
}

const getBodyToList = (body) => {
    const key_list = Object.keys(body)
    const return_data = []

    for (let key of key_list) {
        if(body[key].length > 200){
            return -1
        }
        return_data.push(body[key])
    }

    return return_data
}

// Reference https://github.com/nodejs/node/blob/main/lib/internal/util/inspect.js#L2141
const format = (...args) => {
    const first = args[0]
    let return_data = ''

    if (args.length == 1) {
        return first
    }

    let param_index = 0
    const params = args[1]

    for (let i = 0; i < first.length; i++) {
        if (first.charCodeAt(i) == 37) { // '%'
            const nextChar = first.charCodeAt(i + 1)
            let tmp_arg = ''

            if (param_index + 1 <= params.length) {
                switch (nextChar) {
                    case 115: // 's'
                        {
                            tmp_arg = String(params[param_index++].replace(/["\\]/g, ''))
                            break
                        }

                    case 100: // 'd'
                        {
                            tmp_arg = Number(params[param_index++])
                            break
                        }

                    case 37: // '%'
                        {
                            tmp_arg = "%"
                            break
                        }
                    default:
                        continue
                }

                return_data += tmp_arg
                i++
            }
        } 
        else {
            return_data += first[i]
        }
    }

    while (param_index < params.length) {
        return_data += " "
        return_data += params[param_index++].replace(/["'\\]/g, '')
    }
    
    return return_data
}


module.exports = {
    checkLogin,
    getBodyToList,
    format
}