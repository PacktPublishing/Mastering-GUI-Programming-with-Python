function highlight_selection(){
    let tag = document.createElement('found');
    tag.style.backgroundColor = 'lightgreen';
    window.getSelection().getRangeAt(0).surroundContents(tag);}

function highlight_term(term){
    //cleanup
    let found_tags = document.getElementsByTagName("found");
    while (found_tags.length > 0){
	found_tags[0].outerHTML = found_tags[0].innerHTML;}
    let matches = 0
    //search forward and backward
    while (window.find(term)){
	highlight_selection();
	matches++;
    }
    while (window.find(term, false, true)){
	highlight_selection();
	matches++;
    }
    return matches;
}
