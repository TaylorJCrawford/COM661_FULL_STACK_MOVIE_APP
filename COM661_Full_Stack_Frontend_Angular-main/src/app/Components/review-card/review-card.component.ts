import { Component, Input, ViewEncapsulation } from '@angular/core';
import { HelperService } from '../Services/helper.service';
import { WebService } from '../Services/web.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-review-card',
  templateUrl: './review-card.component.html',
  styleUrls: ['./review-card.component.css'],
  encapsulation: ViewEncapsulation.None,
})
export class ReviewCardComponent {

  @Input() review: any;
  @Input() title: any;
  user_id: string = "";
  is_admin: boolean = false;

  constructor(private helper: HelperService,
    private webService: WebService,
    private router: Router) { }

  ngOnInit() {
    this.user_id = this.helper.get_user_id()
    this.is_admin = this.helper.is_admin()
  }

  remove(title: string) {

    this.webService.removeReview(title)
      .subscribe((response: any) => {
        window.alert([response.Message]);
        window.location.reload()
      })
  }

  edit(review: any) {
    this.router.navigate(['/movie/edit/', this.title, review.user_id])
  }

  get_star_rating(popularity: number) {
    console.log(popularity)
    let html = ``
    if (popularity >= 5) {
      html = `
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star checked"></span>`
    } else if (popularity == 4) {
      html = `
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star"></span>`
    } else if (popularity == 3) {
      html = `
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span>`
    } else if (popularity == 2) {
      html = `
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span>`
    } else if (popularity == 1) {
      html = `
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span>`
    } else {
      html = `
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span>`
    }

    return html
  }
}
