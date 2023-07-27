import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../Services/auth.service';

@Component({
  selector: 'app-admin-panel',
  templateUrl: './admin-panel.component.html',
  styleUrls: ['./admin-panel.component.css']
})
export class AdminPanelComponent {

  users_list: any = [];

  constructor(private auth: AuthService, private router: Router) {}

  ngOnInit() {
    this.users_list = this.auth.get_user_accounts()
  }

  admin_updated(event: boolean, user_id: any) {
    console.log(event)
    console.log("HELLO")
    let role: any;
    if (event == false) {
      // Update admin to true
      role = 'True'
    } else {
      // Update admin to false
      role = 'False'
    }
    console.log(role)

    this.auth.set_user_role(user_id, role).subscribe(
      (response: any) => {
        console.log(response)
        this.users_list = this.auth.get_user_accounts()
      }
    )
  }

  remove_user(id: string) {
    this.auth.delete_account(id).subscribe(
      (response: any) => {
        window.alert(response.Complete)
        window.location.reload()
      }
    )
  }

  viewWatchlist(id: string) {
    this.router.navigate(['/watchlist/' + id,])

  }
}
