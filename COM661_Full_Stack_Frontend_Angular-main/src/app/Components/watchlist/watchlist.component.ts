import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CellClickedEvent } from 'ag-grid-community';
import { WebService } from '../Services/web.service';

@Component({
  selector: 'app-watchlist',
  templateUrl: './watchlist.component.html',
  styleUrls: ['./watchlist.component.css']
})
export class WatchlistComponent {

  is_select: boolean = false;
  watchlist: any;
  user_id: string = "";
  complete_watchlist: any = [];
  complete_list: any = [];
  render: boolean = false;
  movie: any = {
    'title': 'placeholder',
    'overview': 'placeholder',
    'release_date': 'placeholder',
    'popularity': 0,
    'language': 'placeholder',
    'poster': 'placeholder'
  }

  colDefs: any[] = [
    {field: 'title', sortable: true, filter: true},
    {field: 'overview', sortable: true, filter: true},
    {field: 'popularity', sortable: true, filter: true},
    {field: 'release_date', sortable: true, filter: true}
  ];

  constructor(private webService: WebService, private route: ActivatedRoute, private router:Router) {}

  ngOnInit() {
    // Get List of watchlist
    this.user_id = this.route.snapshot.params['user_id']
    this.watchlist = this.webService.getUserWatchlist(this.user_id).subscribe(
      (response: any) => {
      this.watchlist = response[0]
      for (let x = 0; x < response[0].length; x++) {

        this.webService.get_movie_by_title(response[0][x].title).subscribe(
          (response: any) => {
            this.complete_list.push(response[0])
            if (this.watchlist.length == this.complete_list.length)
            {
              this.complete_watchlist = this.complete_list;
              let arr: any = []
              if (this.complete_watchlist != arr){
                this.render = true;
              }
            }
          }
        );
      }
      },
      error => {
        console.log(error)
        window.alert(error.statusText)
      })
  }

  removeMovieFromWatchList(title: string) {
    this.webService.removeItemFromWatchlist(this.user_id, title).subscribe(
      (response: any) => {
        window.alert("Movie has been remove from watchlist.")
        window.location.reload()
      },
      error => window.alert(error.statusText))
  }

  onCellClick( event: CellClickedEvent )
  {
    this.movie = event.data
    this.is_select = true
  }

  sendTo(url: string) {
    this.router.navigate([url])
  }
}
