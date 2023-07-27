import { HttpClient, HttpHeaders } from '@angular/common/http'
import { Injectable } from '@angular/core';
import { HelperService } from './helper.service';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private http: HttpClient, private helper: HelperService) { }

  RegisterUser(username: string, password: string, email: string) {
    let postData = new FormData();

    postData.append("username", username)
    postData.append("password", password)
    postData.append("email", email)

    return this.http.post('http://127.0.0.1:5000/api/v1.0/account/register', postData)
  }

  LoginUser(username: string, password: string) {
    let auth = btoa(`${username}:${password}`);
    return this.http.get(
      'http://127.0.0.1:5000/api/v1.0/account/login', {
        headers: {
          'Authorization': `Basic ${auth}`
        }
    })
  }

  user_logout(token: any) {
    const httpOptions = {
      headers: new HttpHeaders({
        'x-access-token': token
      })
    }

    return this.http.get(
      'http://127.0.0.1:5000/api/v1.0/account/logout', httpOptions)
  }

  delete_account(user_id: string) {

    const httpOptions = {
      headers: new HttpHeaders({
        'x-access-token': this.helper.get_token()
      })
    }

    return this.http.delete(
      'http://127.0.0.1:5000/api/v1.0/account/remove/' + user_id, httpOptions)
  }

  get_user_accounts() {

    const httpOptions = {
      headers: new HttpHeaders({
        'x-access-token': this.helper.get_token()
      })
    }

    return this.http.get(
      'http://127.0.0.1:5000/api/v1.0/account', httpOptions)
  }

  set_user_role(user_id: string, admin: string) {

    let postData = new FormData();

    postData.append("user_id", user_id)
    postData.append("admin", admin)

    const httpOptions = {
      headers: new HttpHeaders({
        'x-access-token': this.helper.get_token()
      })
    }

    return this.http.post(
      'http://127.0.0.1:5000/api/v1.0/account/role', postData, httpOptions)
  }

  check_username(username: string) {
    return this.http.get(
      'http://127.0.0.1:5000/api/v1.0/checkUsername/' + username)
  }
}