const express = require('express')
const bodyParser = require('body-parser')
const app = express()

var accounts={"BISC2023":"TeamH4C"}
var board={}
var now=""

app.set('view engine', 'pug')
app.use(bodyParser.urlencoded({ extended: false }))

app.get('/', function(req,resp){
    if(now===""){
        resp.render('alert',{contents:'login plz',red:'/login'})
    }else{
        resp.render('index', {name:now,board:board})
    }
})
app.get('/login',function(req,resp){
    resp.render('login')
})
app.post('/login',function(req,resp){
    var {id,pw}=req.body
    if(id.toLowerCase()==='bisc2023'){
        resp.render('alert',{contents:'u r not admin',red:'/login'})
    }else{
        id=id.toUpperCase()
        if(id in accounts & accounts[id]===pw){
            now=id
            resp.redirect('/')
        }else{
            resp.render('alert',{contents:'fail',red:'/login'})
        }
    }
})

app.get('/register',function(req,resp){
    resp.render('register')
})

app.post('/register',function(req,resp){
    var {id,pw}=req.body
    if(id in accounts){
        resp.render('alert',{contents:'already taken:<',red:'/login'})
    }else{
        accounts[id]=pw
        resp.redirect('/login')
    }
    
})
app.get('/logout',function(req,resp){
    now=""
    resp.redirect('/login')
})

app.get('/note',function(req,resp){
    var title=req.query.title
    if(now===""){
        resp.render('alert',{contents:'login plz',red:'/login'})
    }else{
        resp.render('note', {pretty:board[title][2],name:now,title:title,board:board})
    }
})
app.get('/write',function(req,resp){
    if(now===""){
        resp.render('alert',{contents:'login plz',red:'/login'})
    }else{
        resp.render('write', {name:now})
    }
})
app.post('/write',function(req,resp){
    if(now===""){
        resp.render('alert',{contents:'login plz',red:'/login'})
    }else{
        var {title, content}=req.body
        board[title]=[now,content,false]
        resp.render('alert', {contents:'good!',red:'/'})
    }
})
app.get('/edit',function(req,resp){
    if(now===""){
        resp.render('alert',{contents:'whoru?',red:'/login'})
    }else{
        var title=req.query.title
        resp.render('edit',{pretty:board[title][2],name:now,title:title,board:board})
    }
})
app.post('/edit',function(req,resp){
    if(now===""){
        resp.render('alert',{contents:'whoru?',red:'/login'})
    }else{
        var {title,b_title,content,pretty}=req.body
        if(now!=="BISC2023"){
            pretty=false
        }
        board[title]=[board[b_title][0],content,pretty?pretty:false]
        if(title!==b_title){
            delete board[b_title]
        }
        resp.render('alert',{contents:'Edit this note',red:'/'})
    }
})

app.listen(80)

