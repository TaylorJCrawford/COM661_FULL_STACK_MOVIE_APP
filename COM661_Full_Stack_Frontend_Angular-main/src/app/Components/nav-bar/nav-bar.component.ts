import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../Services/auth.service';
import { HelperService } from '../Services/helper.service';
import { WebService } from '../Services/web.service';

@Component({
  selector: 'app-nav-bar',
  templateUrl: './nav-bar.component.html',
  styleUrls: ['./nav-bar.component.css']
})
export class NavBarComponent {

  constructor(public webService: WebService, private router: Router, private helper: HelperService, private auth: AuthService) { }

  role: string = "";
  search_active: boolean = false;
  user_id: string = "";

  ngOnInit() {

    let href = String(window.location.href)
    if (href.includes('search')) {
      this.search_active = true
    } else {
      this.search_active = false
    }

    this.role = this.helper.readLocalStorageValue('role');
    this.user_id = this.helper.get_user_id();
  }

  is_admin() {
    return this.helper.is_admin()
  }

  is_token_present() {
    return this.helper.is_token_present()
  }

  display_register = "none";
  display_login = "none";
  display_links = "block";
  openModal_login() {
    this.display_login = "block";
  }
  onCloseHandled_login() {
    this.display_login = "none";
  }
  openModal_register() {
    this.display_register = "block";
    this.display_login = "none";
  }
  onCloseHandled_register() {
    this.display_register = "none";
  }
  openModal_back_to_login() {
    this.display_register = "none";
    this.display_login = "block";
  }

  display_search='none';
  openModal_search() {
    this.display_search = "block";
  }

  closeModal_search() {
    this.display_search = "none";
  }

  onSetRadios(elements: any) {

    for (let x = 0; x < elements.length; x++) {
      (<HTMLInputElement>document.getElementById(elements[x])).checked = false
    }

  }

  is_username_present = false

  checkUsername() {
    console.log("Checking Username");
    let username = (<HTMLInputElement>document.getElementById('username_register')).value
    this.auth.check_username(username).subscribe(
      (response: any) => {
        console.log(response.Present);

        if (response.Present == 'true') {
          this.is_username_present = true
        } else {
          this.is_username_present = false
        }
      }
    )
  }

  search_change(event: any) {
    let elements = ['search_actor', 'search_keyword_all', 'search_keyword_in', 'search_title']

    const index = elements.indexOf(event);

    if (index !== -1) {
      elements.splice(index, 1);
    }

    this.onSetRadios(elements)
  }

  get_active_search() {
    let elements = ['search_actor', 'search_keyword_all', 'search_keyword_in', 'search_title']
    for (let x = 0; x < elements.length; x++) {
      let checked = (<HTMLInputElement>document.getElementById(elements[x])).checked
      if (checked == true) {
        return elements[x]
      }
    }
    // Should never get to here.
    return ""
  }

  no_search_return() {
    this.search_active = false
    this.display_links = "block";
    this.router.navigate(['/'])
  }

  onSearch() {

    const input = document.getElementById('search_box') as HTMLInputElement;
    let input_value = input.value

    let active_search = this.get_active_search()

    if (active_search == 'search_keyword_all') {
      input_value = 'keywords=' + input_value + '&operator=all'
    } else if (active_search == 'search_keyword_in') {
      input_value = 'keywords=' + input_value + '&operator=in'
    } else if (active_search == 'search_actor') {
      input_value = 'actor=' + input_value
    }

    input.value = ""
    this.search_active = true
    this.display_links = "none";
    this.router.navigate(['/movie/search/', input_value])
  }

  // When User Clicks Login Button - On Modal:
  login(username: string = "", password: string = "") {

    if (username == "" || password == "") {
      username = (<HTMLInputElement>document.getElementById('username_login')).value;
      password = (<HTMLInputElement>document.getElementById('password_login')).value;
    }

    let token = this.auth.LoginUser(username, password);

    token.subscribe((response: any) => {

      let role: string;
      if (response.Admin == true) {
        role = 'admin'
      } else {
        role = 'user'
      }

      localStorage.setItem('token', response.Token)
      localStorage.setItem('role', role)
      localStorage.setItem('user_id', response['User ID'])
      window.location.reload()
    },
      error => {
        window.alert("Invalid Login!")
        this.clear_textboxes()
      }
    )
    this.onCloseHandled_login()
  }

  clear_textboxes() {
    (<HTMLInputElement>document.getElementById('username_register')).value = "";
    (<HTMLInputElement>document.getElementById('password_register')).value = "";
    (<HTMLInputElement>document.getElementById('email_register')).value = "";
    (<HTMLInputElement>document.getElementById('password_login')).value = "";
    (<HTMLInputElement>document.getElementById('username_login')).value = "";
  }

  click_logout() {

    let token = localStorage.getItem('token')
    this.auth.user_logout(token).subscribe((response: any) => {
      console.log(response.message)
    })

    localStorage.removeItem('role')
    localStorage.removeItem('token')
    localStorage.removeItem('user_id')
    this.search_active = false;
    this.display_links = "block";
    this.router.navigate(['/'])
  }

  register() {

    let username = (<HTMLInputElement>document.getElementById('username_register')).value;
    let password = (<HTMLInputElement>document.getElementById('password_register')).value;
    let email = (<HTMLInputElement>document.getElementById('email_register')).value;

    this.auth.RegisterUser(username, password, email).subscribe((response: any) => {
      window.alert(response.message)
      this.login(username, password)
    },
      error => window.alert("Invalid, Unable To Register."));
  }
}
