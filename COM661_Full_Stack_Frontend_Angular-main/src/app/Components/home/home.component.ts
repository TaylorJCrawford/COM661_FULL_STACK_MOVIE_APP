import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../Services/auth.service';
import { HelperService } from '../Services/helper.service';
import { WebService } from '../Services/web.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {

  dataset_size = 0;

  constructor(private helper: HelperService,
    private webService: WebService,
    private auth: AuthService,
    private router: Router) {}

  ngOnInit() {
    this.webService.getDataSetSize().subscribe(
      (response: any) =>
        {
          this.dataset_size = response.result
        }
    );
  }

  isLogin() {
    return this.helper.is_token_present()
  }

  isAdmin() {
    return this.helper.is_admin()
  }

  deleteAccount() {

    let user_id = this.helper.get_user_id()
    console.log("Deleting Account")
    this.auth.delete_account(user_id).subscribe(
      (response: any) => {
        localStorage.removeItem('role')
        localStorage.removeItem('token')
        localStorage.removeItem('user_id')
        window.alert(response['Complete'])
        window.location.reload()
      }
    )
  }

  adminOpen() {
    this.router.navigate(['/admin',])
  }
}
