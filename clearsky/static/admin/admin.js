function openEditMenu(event, tabName) {
    var i, x, tablinks;

    x = document.getElementsByClassName("tabContent");

    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none"
    }

    tablinks = document.getElementsByClassName("tablink");

    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].style.backgroundColor = "darkslategray";
    }

    document.getElementById(tabName).style.display = "block";
    event.currentTarget.style.backgroundColor = "blue";
    event.currentTarget.style.color = "white"
}

function logout() {

}