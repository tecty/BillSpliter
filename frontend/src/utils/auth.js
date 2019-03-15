export function getToken() {
  return localStorage.getItem("token");
}
export function getUsername() {
  return localStorage.getItem("username");
}
export function isLogin() {
  // return the bool value of whether there is a token
  return getToken() != null && getToken() != "";
}

export function getFirstname() {
  return localStorage.getItem("first_name")
    ? localStorage.getItem("first_name")
    : "";
}
export function getLastname() {
  return localStorage.getItem("last_name")
    ? localStorage.getItem("last_name")
    : "";
}
export function getPassword() {
  return localStorage.getItem("password");
}
