import { Component, Input } from '@angular/core';
import { WebService } from '../Services/web.service';
import { ActivatedRoute } from '@angular/router';
@Component({
  selector: 'app-feed',
  templateUrl: './feed.component.html',
  styleUrls: ['./feed.component.css']
})
export class FeedComponent {

  p: any;
  page: number = 1;
  page_size: number = 6;
  pagination_active: boolean = true;
  totalRecords: any = 100;
  data: any = [];

  constructor(public webService: WebService, private route: ActivatedRoute) { }

  ngOnInit() {

    this.webService.getDataSetSize().subscribe(
      (response: any) => {
        this.totalRecords = response.result;
      }
    );

    let search_term = this.route.snapshot.params['search_term']

    if (search_term != undefined) {
      // Search Feed By Title
      this.pagination_active = false;
      if (search_term.includes('actor=') != false || search_term.includes('keywords=') != false) {
        this.webService.get_movie_by_searh_term(search_term).subscribe(
          (data) => {
            this.data = data;
          }
        );
      } else {
        this.webService.get_movie_by_title(search_term).subscribe(
          (data) => {
            this.data = data;
          }
        );
      }
    } else {
      // Standard Feed
      if (sessionStorage['page']) {
        this.page = Number(sessionStorage['page']);
      }
      if (sessionStorage['page_size']) {
        this.page = Number(sessionStorage['page_size']);
      }
      this.webService.get_movies(this.page, this.page_size).subscribe(
        (data) => {
          this.data = data;
        }
      );
    }
  }

  pagination(event: any) {
    console.log(event)
    this.getData(event, 6)
    this.page = event
    sessionStorage['page'] = this.page;
  }

  getData(page: number, page_size: number) {
    this.webService.get_movies(page, page_size).subscribe(
      (data) => {
        this.data = data;
        console.log(this.data)
      }
    );
  }
}
