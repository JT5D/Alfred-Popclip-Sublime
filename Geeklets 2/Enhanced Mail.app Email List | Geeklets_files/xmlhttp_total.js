
var my_base_url='http://www.macosxtips.co.uk';
var my_pligg_base='/geeklets';


dochref = document.location.href.substr(document.location.href.search('/')+2, 1000);
if(dochref.search('/') == -1){
	$thisurl = document.location.href.substr(0,document.location.href.search('/')+2) + dochref;
} else {
	$thisurl = document.location.href.substr(0,document.location.href.search('/')+2) + dochref.substr(0, dochref.search('/'));
}
$thisurl = $thisurl + '/geeklets';

var xvotesString = Array ();

function vote(user, id, htmlid, md5, value) {
	var	postData = "id=" + id + "&user=" + user + "&md5=" + md5 + "&value=" + value;
	executevote(user, id, htmlid, md5, value, postData, 'vote')
}

function unvote (user, id, htmlid, md5, value) {
	var postData = "unvote=true&id=" + id + "&user=" + user + "&md5=" + md5 + "&value=" + value;
	executevote(user, id, htmlid, md5, value, postData, 'unvote')
}

function executevote(user, id, htmlid, md5, value, postData, isun) {
	var url = $thisurl + "/vote_total.php";
	if (user == '0') { window.location="http://www.macosxtips.co.uk/geeklets/login.php?return="+location.href; }
	$.post(url, postData, function(data) {
		xvotesString[htmlid] = data;
		if (xvotesString[htmlid].substr(0, 6) == "ERROR:") {
			alert(xvotesString[htmlid]);
		} else {
			changemnmvalues(user, id, htmlid, md5, value, isun);
		}
	});
}

function changemnmvalues(user, id, htmlid, md5, value, isun) {
	var uparrow = $('#xarrowup-'+htmlid),
		downarrow = $('#xarrowdown-'+htmlid),
		numberbox = $('#xvotes-'+htmlid);
	
	numberbox.text(xvotesString[htmlid].split('~--~')[0]);

	uparrow.removeAttr('onclick').unbind('click');
	downarrow.removeAttr('onclick').unbind('click');

	if (isun == 'vote') {
		if(value == 10) {
			uparrow.addClass('voted');
			uparrow.bind('click', function() { unvote(user, id, htmlid, md5, 10);});
			downarrow.bind('click', function() { unvote(user, id, htmlid, md5, 10);});
		} else {
			downarrow.addClass('voted');
			uparrow.bind('click', function() { unvote(user, id, htmlid, md5, -10);});
			downarrow.bind('click', function() { unvote(user, id, htmlid, md5, -10);});
		}
	} else {
		if(value == 10) {
			uparrow.removeClass('voted');
		} else {
			downarrow.removeClass('voted');
		}
		uparrow.bind('click', function() { vote(user, id, htmlid, md5, 10);});
		downarrow.bind('click', function() { vote(user, id, htmlid, md5, -10);});
	}
	return false;
}

