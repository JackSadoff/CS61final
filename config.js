var config = {
sunapee: {
	database: {
		host     : 'sunapee.cs.dartmouth.edu', 
		user     : 'HealthQdb_sp20', //'your localhost username here'
		password : 'R8jJa2JRE', //your localhost password here'
		schema : 'HealthQdb_sp20' //'your localhost default schema here'
	},
	port: 3000
},
local: {
	database: {
		host     : 'sunapee.cs.dartmouth.edu', 
		user     : 'HealthQdb_sp20', //'your localhost username here'
		password : 'R8jJa2JRE', //your localhost password here'
		schema : 'HealthQdb_sp20' //'your localhost default schema here'
	},
	port: 3000
}
};
module.exports = config;
