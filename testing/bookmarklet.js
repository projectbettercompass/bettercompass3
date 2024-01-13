javascript: (() => {
    function getCookie(cname) {
        let name = cname + '=';
        let decodedCookie = decodeURIComponent(document.cookie);
        let ca = decodedCookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) == ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
                return c.substring(name.length, c.length);
            }
        }
        return '';
    }
    const url = window.location.href;
    const regex = /https:\/\/([^\/]+)\.compass\.education\//;
    const match = url.match(regex);
    if (match) {
        const end = match[1];
        alert(document.cookie);
        alert('Session_id: \n' + getCookie('cspid') + '\n \n \n' + 'School Prefix: \n' + end);
    } else {
        alert('Not a compass page');
    }
})();