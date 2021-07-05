function getNgrams(text, n){
	var ngrams = {};
	var content = text
					// Make sure that there is letter before punctuation	
					.replace(/\.\s*/g, '_') 					
					// Discard all digits 
					.replace(/[0-9]/g, "")
					//Discard all punctuation except for apostrophe
					.replace(/[&\/\\#,+()$~%.":*?<>{}]/g,'')
					// Remove duplicate spaces	
					.replace(/\s*/g, '')
					.toLowerCase(); 
	for(var i = 0; i < content.length - (n-1); i++){
		var token = content.substring(i, i + n); 
		if (token in ngrams)
			ngrams[token] += 1; 
		else
			ngrams[token] = 1; 
	}
	return ngrams; 
}

function sortNgrams(ngrams){
	return Object.keys(ngrams).map(function(key) {
    	return {'ngram': key, 'freq':ngrams[key]};
	}).sort(function(first, second) {
		// If the frequency is the same favour larger ngrams
		return second['freq'] - first['freq'];
	}).map(function(ngram, index){
		ngram['index'] = index;
		return ngram;
	});
}


function merge(obj1,obj2){
    var obj3 = {};
    for (var attrname in obj1) { obj3[attrname] = obj1[attrname]; }
    for (var attrname in obj2) { obj3[attrname] = obj2[attrname]; }
    return obj3;
}

exports.generateProfile = function(text, topN){
	var biGrams = getNgrams(text, 2);
	var triGrams = getNgrams(text, 3);
	var ngrams = merge(biGrams, triGrams);
	var sortedNgrams = sortNgrams(ngrams);
	return sortedNgrams.slice(0, topN);
}