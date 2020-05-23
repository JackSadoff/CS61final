/* 	Node API demo
	Author: Tim Pierson, Dartmouth CS61, Spring 2020

	Add config.js file to root directory
	To run: nodemon api.js <local|sunapee>
	App will use the database credentials and port stored in config.js for local or sunapee server
	Recommend Postman app for testing verbs other than GET, find Postman at https://www.postman.com/
*/

var express=require('express');
let mysql = require('mysql');
const bodyParser = require('body-parser'); //allows us to get passed in api calls easily
var app=express();

// get config
var env = process.argv[2] || 'local'; //use localhost if enviroment not specified
var config = require('./config')[env]; //read credentials from config.js


//Database connection
app.use(function(req, res, next){
	global.connection = mysql.createConnection({
		host     : config.database.host, 
		user     : config.database.user, 
		password : config.database.password, 
		database : config.database.schema 
	});
	connection.connect();
	next();
});

app.use(bodyParser.urlencoded({extended:true}));
app.use(bodyParser.json());
const bcrypt = require('bcrypt-nodejs');
const saltRounds = 10;

// set up router
var router = express.Router();

// log request types to server console
router.use(function (req,res,next) {
	console.log("/" + req.method);
	next();
});



// set up routing
// calls should be made to /api/employees/:user/:password with GET/PUT/POST/DELETE verbs
// you can test GETs with a browser using URL http://localhost:3000/api/employees/:user/:password or http://localhost:3000/api/employees/30075445
// recommend Postman app for testing other verbs, find it at https://www.postman.com/
router.get("/",function(req,res){
	res.send("Yo!  This my API.  Call it right, or don't call it at all!");
});

// GET - read data from database, return status code 200 if successful
router.get("/api/employees/:user/:password",function(req,res){
	const username=req.params.user;
	const password=req.params.password;
	global.connection.query('SELECT Password, Admin, idEmployees FROM nyc_inspections.Employees WHERE Username = ?', [username],function (error, results, fields) {
		if (error) throw error;
		if (results[0]==undefined){
		res.send(JSON.stringify({"status": 401, "error": "invalid credentials"}));
		return;
		}
		const hash = results[0].Password;const admin=results[0].Admin;const empid=results[0].idEmployees;
	  bcrypt.compare(password, hash, function(err, success) {
		if (err) throw err;
       if (success && (admin == 1)){ 
	// get all employees (limited to first 10 here), return status code 200
	global.connection.query('SELECT * FROM nyc_inspections.Employees', function (error, results, fields) {
		if (error) throw error;
		res.send(JSON.stringify({"status": 200, "error": null, "response": results}));
	});
} else {

res.send(JSON.stringify({"status": 401, "error": "invalid credentials"}));
console.log("invalid credentials")
}
});
});});
router.get("/api/employees/:user/:password/:id",function(req,res){
	console.log(req.params.id);
		const username=req.params.user;
	const password=req.params.password;
	global.connection.query('SELECT Password, Admin, idEmployees FROM nyc_inspections.Employees WHERE Username = ?', [username],function (error, results, fields) {
		if (error) throw error;
		if (results[0]==undefined){
		res.send(JSON.stringify({"status": 401, "error": "invalid credentials"}));
		return;
		}
		const hash = results[0].Password;const admin=results[0].Admin;const empid=results[0].idEmployees;
	  bcrypt.compare(password, hash, function(err, success) {
		if (err) throw err;
	  if (success && (admin == 1 || (admin == 0 && req.params.id == empid))){
	// get all employees (limited to first 10 here), return status code 200
	//read a single employee with RestauantID = req.params.id (the :id in the url above), return status code 200 if successful, 404 if not
	global.connection.query('SELECT * FROM nyc_inspections.Employees WHERE idEmployees = ?', [req.params.id],function (error, results, fields) {
		if (error) throw error;
		res.send(JSON.stringify({"status": 200, "error": null, "response": results}));
	});
} else {

res.send(JSON.stringify({"status": 401, "error": "invalid credentials"}));
console.log("invalid credentials")
}
});
});});
// PUT - UPDATE data in database, make sure to get the ID of the row to update from URL route, return status code 200 if successful
router.put("/api/employees/:user/:password/:id",function(req,res){
	console.log(req.query);
			const username=req.params.user;
	const password=req.params.password;
	global.connection.query('SELECT Password, Admin, idEmployees FROM nyc_inspections.Employees WHERE Username = ?', [username],function (error, results, fields) {
		if (error) throw error;
if (results[0]==undefined){
		res.send(JSON.stringify({"status": 401, "error": "invalid credentials"}));
		return;
		}
		const hash = results[0].Password;const admin=results[0].Admin;const empid=results[0].idEmployees;
	  bcrypt.compare(password, hash, function(err, success) {
		if (err) throw err;
if (success && (admin == 1 || (admin == 0 && req.params.id == empid))){
	var quer=req.query
	bcrypt.genSalt(saltRounds,function (err,salt){
	if (err) throw error;

	bcrypt.hash(req.query.Password, salt,null, function(err, hash) {
	if (err) throw error;
	console.log(hash);
	if (typeof quer.Password !== 'undefined'){
	quer.Password=hash;}
	console.log(quer);
	//read a single employee with RestauantID = req.params.id (the :id in the url above), return status code 200 if successful, 404 if not
	global.connection.query('UPDATE  nyc_inspections.Employees SET ? WHERE idEmployees=? ', [quer, req.params.id],function (error, results, fields) {
		if (error) throw error;
		res.send(JSON.stringify({"status": 200, "error": null, "response": results}));
	});
	});
	});} else {

res.send(JSON.stringify({"status": 401, "error": "invalid credentials"}));
console.log("invalid credentials")
}
});
});
});

// POST -- create new employee, return location of new restaurant in location header, return status code 200 if successful
router.post("/api/employees/:user/:password",function(req,res){
	console.log(req.query);
	const username=req.params.user;
	const password=req.params.password;
	global.connection.query('SELECT Password, Admin, idEmployees FROM nyc_inspections.Employees WHERE Username = ?', [username],function (error, results, fields) {
		if (error) throw error;
		if (results[0]==undefined){
		res.send(JSON.stringify({"status": 401, "error": "invalid credentials"}));
		return;
		}
		const hash = results[0].Password;const admin=results[0].Admin;const empid=results[0].idEmployees;
	  bcrypt.compare(password, hash, function(err, success) {
		if (err) throw err;
		if (success && admin == 1){
	var quer=req.query
	bcrypt.genSalt(saltRounds,function (err,salt){
	if (err) throw error;

	bcrypt.hash(req.query.Password, salt,null, function(err, hash) {
	if (err) throw error;
	console.log(hash);
	quer.Password=hash;
	console.log(quer);
	//read a single employee with RestauantID = req.params.id (the :id in the url above), return status code 200 if successful, 404 if not
	global.connection.query('INSERT INTO nyc_inspections.Employees SET ?', [quer],function (error, results, fields) {
		if (error) throw error;
		res.send(JSON.stringify({"status": 200, "error": null, "response": results}));
	});
	});
	});} else {

res.send(JSON.stringify({"status": 401, "error": "invalid credentials"}));
console.log("invalid credentials")
}
});
});
	
});

// DELETE -- delete employee with idEmployees of :id, return status code 200 if successful
router.delete("/api/employees/:user/:password/:id",function(req,res){
	console.log(req.params);
	const username=req.params.user;
	const password=req.params.password;
	global.connection.query('SELECT Password, Admin, idEmployees FROM nyc_inspections.Employees WHERE Username = ?', [username],function (error, results, fields) {
		if (error) throw error;
		if (results[0]==undefined){
		res.send(JSON.stringify({"status": 401, "error": "invalid credentials"}));
		return;
		}
		const hash = results[0].Password;const admin=results[0].Admin;const empid=results[0].idEmployees;
	  bcrypt.compare(password, hash, function(err, success) {
		if (err) throw err;
		if (success && admin == 1){
	//read a single employee with RestauantID = req.params.id (the :id in the url above), return status code 200 if successful, 404 if not
	global.connection.query('DELETE  FROM nyc_inspections.Employees WHERE idEmployees = ?', [req.params.id],function (error, results, fields) {
		if (error) throw error;
		res.send(JSON.stringify({"status": 200, "error": null, "response": results}));
	});} else {

res.send(JSON.stringify({"status": 401, "error": "invalid credentials"}));
console.log("invalid credentials")
}
});
});
});




// start server running on port 3000 (or whatever is set in env)
app.use(express.static(__dirname + '/'));
app.use("/",router);
app.set( 'port', ( process.env.PORT || config.port || 3000 ));

app.listen(app.get( 'port' ), function() {
	console.log( 'Node server is running on port ' + app.get( 'port' ));
	console.log( 'Environment is ' + env);
});
