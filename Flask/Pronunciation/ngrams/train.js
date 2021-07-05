#!/usr/bin/env node
var path = require('path');
var glob = require("glob")
var path = require('path'); 
var fs = require('fs');
var ngramUtils = require('./ngram-utils');

var ngrams = {}

console.log("Started Application");
// options is optional
glob("subset/*.txt", function (er, files) {
	var languageProfile = {};
	files.forEach(function(file){
		var lang = path.basename(file, '.txt'); 
		console.log("Training [Lanugage: ", lang, "] [File: ", file, "]");
		var text = fs.readFileSync(file,'utf8'); 
		languageProfile[lang] = ngramUtils.generateProfile(text, 300);
	}); 
	fs.writeFileSync('language-profile.json', JSON.stringify(languageProfile));
	console.log("Written Language Profile to File [language-profile.json]");
});
