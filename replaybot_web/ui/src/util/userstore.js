/*
we use both session and localstorage as firefox in 
private browsing seems to be funny about localstorage
and it logs me out all the time
*/
export function login(accessToken, user) {
    set('accessToken', accessToken);
    set('user', JSON.stringify(user));
}

export function getUser() {
    return JSON.parse(get('user'));
}

export function getToken() {
    return get('accessToken');
}

export function logout() {
    localStorage.clear();
    sessionStorage.clear();
}

function get(key) {
    let tmp = localStorage.getItem(key);
    if(!tmp) {
        tmp = sessionStorage.getItem(key);
    }
    return tmp;
}

function set(key, data) {
    localStorage.setItem(key, data);
    sessionStorage.setItem(key, data);
}