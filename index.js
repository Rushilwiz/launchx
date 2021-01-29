#!/usr/bin/nodejs

// -------------- load packages -------------- //
var express = require('express');
var app = express();
var hbs = require('hbs');
var path = require('path');

// -------------- express initialization -------------- //
app.set('port', process.env.PORT || 8080);
// tell express that the view engine is hbs
app.set('view engine', 'hbs');
app.use(express.static('static'));

// -------------- express endpoints -------------- //
app.get('/', function(req, res){
    res.render('index');
});

app.get('/calendar', function(req, res){
    res.render('calendar');
});

app.get('/officers', function(req, res){
    res.render('officers');
});

app.get('/innovatetj', function(req, res){
    res.render('innovatetj');
});

app.get('/favicon.ico', function(req, res){
    res.sendFile(path.join(__dirname, 'favicon.ico'));
});

// -------------- listener -------------- //
var listener = app.listen(app.get('port'), function(){
    console.log('--------------------------------------------');
    console.log(Date());
    console.log('Express server started on port: ' + listener.address().port);
});
