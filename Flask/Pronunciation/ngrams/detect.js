#!/usr/bin/env node
var path = require('path');
var glob = require("glob")
var path = require('path'); 
var fs = require('fs');
var ngramUtils = require('../../app/ngram-utils');

// Generic Function to sort the scores. 
function sortScores(scores){
	return Object.keys(scores).map(function(language) {
    	return {'language': language, 'score':scores[language]};
	}).sort(function(first, second) {
		return first['score'] - second['score'];
	});
}

if (process.argv.length != 3){
	console.log("Usage npm run detect <phrase>");
	return;
}

var NOT_FOUND = 1000; 

// Loading our language profiles
console.log("Reading Language Profiles from [language-profile.json]");
var languageProfiles = JSON.parse(fs.readFileSync('language-profile.json', 'utf-8'));

// Reading the text the user wants to detect from the input.  
var text = process.argv[2]; 
console.log("Determining Language for [text: ", text, "]");

// Generate the ngrams from the document.  
var documentProfile = ngramUtils.generateProfile(text, 300);

// Create an empty scores array
var scores = Object.create(null);

// Initialise this with 0 for each language;
Object.keys(languageProfiles).forEach(function(language){
	scores[language] = 0;
})

// Compute the out of index for each language.  
documentProfile.forEach(function(documentNgram){
	var documentIndex = documentNgram.index; 
	var languages = Object.keys(languageProfiles);

	languages.forEach(function(language){
		var languageProfile = languageProfiles[language];
		var languageNgram = languageProfile.filter(function(languageNgram){
			return languageNgram.ngram == documentNgram.ngram;
		});

		if (languageNgram.length == 1){
			scores[language] +=  Math.abs(languageNgram[0].index - documentIndex);
		} else {
			scores[language] += NOT_FOUND;
		}
	});	
});

var sortedScores = sortScores(scores);
console.log("Results ===============");
console.log(JSON.stringify(sortedScores));



