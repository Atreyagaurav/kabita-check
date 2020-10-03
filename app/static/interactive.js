function fill_sample() {
    document.getElementById('kabita-maintext').value = "# शार्दुलविक्रीडित-छन्द-कविता\n# SSSIISISIIISSSISSIS \n# यसरि '#' पछाडि लेखिएका लाईन जाच हुदैन।\n\nहोस् दीर्घायु सुस्वास्थ्य झै मधुरता वाणी मिठो नम्र होस्\nआफ्नो धर्म र कर्म मानमनिता भाषा कला चाख होस्\n\nइच्छा आँट खुशी सबै सफलहोस् तिम्रा सबै चाहना\nयो जन्मोत्सवले सधै खुश भरोस् हाम्रो छ यै कामना\n";
}

function check_kabita() {
    document.getElementById('kabita-response').innerHTML = " Analyzing...."
    data = {text : document.getElementById('kabita-maintext').value}
    return fetch("/check", {
	method: "POST",
	headers: {
	    'Content-Type': 'application/json;charset=utf-8'
	},
	body: JSON.stringify(data)
    }).then(res => {return res.json()}).then( data => {
	console.log("Request complete! response:", data);
	document.getElementById('lines-analysed').innerHTML = data["total"];
	document.getElementById('lines-correct').innerHTML = data["correct"];
	document.getElementById('lines-error').innerHTML = data["wrong"];
	document.getElementById('lines-ignored').innerHTML = data["ignored"];
	document.getElementById('chanda-name').innerHTML = data["chanda_name"];
	document.getElementById('chanda-rule').innerHTML = data["chanda_rule"];
	document.getElementById('kabita-response').innerHTML = data["html"];
    })
}
