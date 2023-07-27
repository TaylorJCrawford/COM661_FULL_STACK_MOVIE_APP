import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class HelperService {

  constructor() { }

  is_admin(): boolean {
    let value: any = localStorage.getItem('role');
    if (value == 'admin') return true
    return false
  }

  is_token_present(): boolean {
    let value: any = localStorage.getItem('token');
    if (value != undefined) return true
    return false
  }

  get_user_id(): string {
    let user_id: any = localStorage.getItem('user_id');
    return user_id;
  }

  readLocalStorageValue(key: string): string {

    let value: any = localStorage.getItem(key);
    console.log("User Role Is: " + value)
    if (value != null){
      return value
    } else
    return ""
  }

  get_token(): string{
    let value: any = localStorage.getItem('token');
    return value
  }

}